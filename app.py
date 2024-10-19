from flask import Flask, request, render_template
from transformers import pipeline
import PyPDF2
import re
from spellchecker import SpellChecker  

app = Flask(__name__)

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
spell_checker = SpellChecker()


def summarize_detailed_text(text):
    max_length = 300  
    min_length = 100 
    return summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)


def summarize_short_text(text):
    max_length = 150  
    min_length = 30   
    return summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)


def clean_and_correct_text(text):
    corrected_words = []
    for word in text.split():
        correction = spell_checker.correction(word)
        corrected_words.append(correction if correction else word)  

    corrected_text = ' '.join(corrected_words).strip()  
    corrected_text = re.sub(r'(?<!\w)(?=\w)', '', corrected_text) 
    corrected_text = '. '.join(sentence.strip().capitalize() for sentence in corrected_text.split('. '))    
    corrected_text = re.sub(r'\s+', ' ', corrected_text).strip()  

    return corrected_text


def process_large_document(text):
    max_chunk_size = 1000  
    overlap_size = 200
    chunks = []

    for i in range(0, len(text), max_chunk_size - overlap_size):
        chunk = text[i:i + max_chunk_size]
        chunks.append(chunk)

    detailed_summaries = []
    short_summaries = []
    
    for chunk in chunks:
        
        detailed_summary = summarize_detailed_text(chunk)[0]['summary_text']
        short_summary = summarize_short_text(chunk)[0]['summary_text']
        
        detailed_summaries.append(detailed_summary)
        short_summaries.append(short_summary)

   
    final_detailed_summary = ' '.join(detailed_summaries)
    final_short_summary = ' '.join(short_summaries)

    
    formatted_detailed_summary = clean_and_correct_text(final_detailed_summary)
    formatted_short_summary = clean_and_correct_text(final_short_summary)

    return formatted_detailed_summary, formatted_short_summary


@app.route('/', methods=['GET', 'POST'])
def home():
    detailed_summary = ""
    short_summary = ""
    if request.method == 'POST':
        text = request.form.get('text', '')  
        file = request.files.get('file')  

    
        if text.strip():
            detailed_summary, short_summary = process_large_document(text)
        
        elif file and file.filename.endswith('.pdf'):
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() if page.extract_text() else ""  
            if text:
                detailed_summary, short_summary = process_large_document(text)

    return render_template('summary_app.html', detailed_summary=detailed_summary, short_summary=short_summary)

if __name__ == '__main__':
    app.run(debug=True)
