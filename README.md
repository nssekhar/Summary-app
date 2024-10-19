# Text Summarization App

## Overview
The Text Summarization App is a Flask-based web application that allows users to generate both short and detailed summaries of text documents. It utilizes the BART model from Hugging Face Transformers for state-of-the-art natural language processing capabilities, making it an ideal tool for quickly digesting large amounts of information.

## Features
- **Text Input**: Users can paste text directly into a text area or upload files in various formats (.txt, .pdf, .docx, .pptx).
- **Content Type Selection**: Options for general text, scientific papers, or business reports to tailor the summarization process.
- **Summary Type Selection**: Users can choose between short and detailed summaries to suit their needs.
- **Background and Design**: A visually appealing interface with a custom background and styling for an engaging user experience.

## Requirements
- Python 3.x
- Flask
- Transformers (Hugging Face)
- PyPDF2
- SpellChecker

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd text-summarization-app
