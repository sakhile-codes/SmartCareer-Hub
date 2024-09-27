
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
import openai
import requests
import os
from twilio.rest import Client

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')
OPENAI_ENDPOINT = 'https://api.openai.com/v1/chat/completions'
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Set your Twilio credentials (use environment variables for security)
twilio_sid = os.getenv('twilio_sid')
twilio_auth_token = os.getenv('twilio_auth_token')

client = Client(twilio_sid, twilio_auth_token)

def generate_response(user_input):
    persona = """
    My name is Persona and I am the admin at SmartCareer Hub"""

    instructions = "Do your best to respond to customer inquiries in a clear and concise manner and help people with upskilling and job search"

    example_conversations = [
        {
            "user": "I'm having trouble logging in.",
            "assistant": "I am sorry to hear that you are having trouble logging in name?"
        },
    ]

    prompt = f"{persona}\n\n{instructions}\n\nExample Conversations:\n" + "\n".join([
        f"User: {conv['user']}\nAssistant: {conv['assistant']}" for conv in example_conversations
    ]) + "\n\nChat History:\n" + "\n\nUser: " + user_input + "\nAssistant:"

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

    return response_data['choices'][0]['message']['content'].strip()

@csrf_exempt  # Disable CSRF protection for Twilio's webhook
def whatsapp_reply(request):
    incoming_msg = request.POST.get('Body', '').strip()

    # Generate a response using OpenAI GPT
    response_text = generate_response(incoming_msg)

    # Create a Twilio MessagingResponse to reply to the user
    resp = MessagingResponse()
    resp.message(response_text)

    return HttpResponse(str(resp), content_type="text/xml")