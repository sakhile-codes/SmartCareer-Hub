import openai
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from PyPDF2 import PdfReader
from django.shortcuts import render
import requests

from .forms import CVUploadForm

import os

# Set the path to tesseract if needed
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update to your Tesseract installation path

openai.api_key = os.getenv('OPENAI_API_KEY')
OPENAI_ENDPOINT = 'https://api.openai.com/v1/chat/completions'
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def extract_text_from_image(image):
    text = pytesseract.image_to_string(image)
    return text

def extract_text_from_pdf(pdf):
    text = ""
    # Attempt to extract text using PyPDF2
    reader = PdfReader(pdf)
    for page in reader.pages:
        text += page.extract_text() or ""
    
    if not text.strip():  # If no text is extracted, use OCR
        pages = convert_from_path(pdf)
        for page in pages:
            text += pytesseract.image_to_string(page)
    
    return text

def get_openai_recommendations(cv_text, job_description):
    prompt = f"""
    Here is a CV text:\n\n{cv_text}\n\n
    Here is a job description:\n\n{job_description}\n\n
    Please provide the following:
    1. List of recommended skills and improvements to make the CV stronger and tailored to the job.
    2. An improved version of the CV that is better suited for this job.
    """

    
    print(f"Using API Key: {OPENAI_API_KEY}")
    try:
        
        headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json'
        }
        payload = {
            'model': 'gpt-4o-mini-2024-07-18',
            'messages': [
                {'role': 'user', 'content': prompt}
            ],
            'max_tokens': 300,
            'temperature': 0.5
        }

        response = requests.post(OPENAI_ENDPOINT, json=payload, headers=headers)
        response_data = response.json()

        # Log the response to check the structure
        print("Full API Response:", response_data) 
        
        return response_data['choices'][0]['message']['content'].strip() 
    except Exception as e:
        return f"Error in OpenAI API request: {str(e)}"

def upload_cv(request):
    if request.method == 'POST':
        form = CVUploadForm(request.POST, request.FILES)
        if form.is_valid():

            file = request.FILES['file']
            job_description = form.cleaned_data['job_description']
            file_type = file.content_type
            extracted_text = ""

            # Check file type based on extension
            if file.name.lower().endswith('.pdf'):
                extracted_text = extract_text_from_pdf(file)
            elif file.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                extracted_text = extract_text_from_image(file)
            else:
                extracted_text = "Unsupported file type."

             # Get recommendations and new CV from OpenAI
            openai_response = get_openai_recommendations(extracted_text, job_description)

            return render(request, 'upload_results.html', {
                'text': extracted_text,
                'openai_response': openai_response
            })
    else:
        form = CVUploadForm()
        return render(request, 'upload_cv.html', {'form': form})