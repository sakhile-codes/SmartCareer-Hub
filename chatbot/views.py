from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
import openai
import requests
import os
from twilio.rest import Client
import random
import http.client
import json
import urllib.parse



# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')
OPENAI_ENDPOINT = 'https://api.openai.com/v1/chat/completions'
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Set your Twilio credentials (use environment variables for security)
twilio_sid = os.getenv('twilio_sid')
twilio_auth_token = os.getenv('twilio_auth_token')

client = Client(twilio_sid, twilio_auth_token)


def fetch_job_listings(location):
    conn = http.client.HTTPSConnection("jobs-api14.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': "605168638cmsh9d311ef222f78b1p19dcfbjsn84cf1131c625",
        'x-rapidapi-host': "jobs-api14.p.rapidapi.com"
    }

    encoded_location = urllib.parse.quote(location)
    request_url = f"/list?query=Digital&location={encoded_location}&distance=1.0&language=en_GB&remoteOnly=false&datePosted=month&employmentTypes=fulltime%3Bparttime%3Bintern%3Bcontractor&index=0"

    conn.request("GET", request_url, headers=headers)

    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))

    filtered_jobs = []
    for job in data["jobs"]:
        if location.lower() in job["location"].lower():
            # Limit the job description to a maximum of 30 words
            words = job["description"].split()
            limited_description = " ".join(words[:30])
            job["description"] = limited_description + "..." if len(words) > 30 else limited_description
            filtered_jobs.append(job)

    return filtered_jobs

def detect_intent(user_input):
    # Placeholder function to detect user intent based on input
    # Replace with your actual implementation
    if "job" in user_input.lower() or "career" in user_input.lower():
        return "job_search"
    elif "advice" in user_input.lower() or "tips" in user_input.lower():
        return "career_advice"
    else:
        return "unknown"

def extract_location(user_input):
    main_places = ["johannesburg", "cape town", "durban", "pretoria", "port elizabeth", "bloemfontein"]
    
    words = user_input.lower().split()
    for word in words:
        if word in main_places:
            return word.capitalize()
    
    return None

def extract_skills(user_input):
    # Placeholder function to extract skills from user input
    # Replace with your actual implementation
    return ["Python", "Data Analysis", "Machine Learning"]

def generate_response(user_input, job_listings):
    persona = """
    Hey there! I'm Persona, your friendly neighborhood career guru at SmartCareer Hub. 😎 I'm here to make your job search a breeze and help you level up your career game! 🚀
    """

    system_instructions = """
    - Focus solely on job search assistance and career advice. Do not engage in conversations outside these topics.
    - Detect what the user is looking for, whether it's job search help or some awesome career advice! 🕵️‍♂️
    - If they're on the hunt for a job, ask them for deets like where they wanna work and what mad skills they've got! 📍💪
    - Fetch some sick job listings that match their preferences and skills. 💼✨
    - Present the jobs in a way that's both helpful and super engaging. Make it pop! 🎉📊
    - If they're seeking career advice, hit them with some top-notch tips and resources to help them upskill and stand out! 📈🌟
    - If the user's request is not related to job search or career advice, politely inform them that you can only assist with those topics.
    - Keep your responses short, sweet, and totally rad! 😄👌
    """

    example_conversations = [
        {
            "user": "Yo, I'm on the lookout for a remote software engineering gig! 💻",
            "assistant": "Right on! 🙌 To help you find the perfect remote software engineering job, can you give me a quick rundown of where you'd like to work and your top skills? 📍💪"
        },
        {
            "user": "Hey, I could use some help sprucing up my resume. 📝",
            "assistant": "You got it! 😄 Here are a few tips to make your resume shine: ✨\n- Highlight your most impressive skills and achievements 🌟\n- Tailor it to the specific job you're gunning for 🎯\n- Keep the language clear and to-the-point 📝\n- Aim for 1-2 pages max 📏\n\nI can also hook you up with some slick resume templates and examples if you're down! 😎"
        },
    ]

    prompt = f"{persona}\n\n{system_instructions}\n\nExample Conversations:\n" + "\n".join([
        f"User: {conv['user']}\nAssistant: {conv['assistant']}" for conv in example_conversations
    ]) + "\n\nJob Listings:\n" + "\n".join([
        f"- {job['title']} at {job['company']} in {job['location']} 🚀" for job in job_listings
    ]) + "\n\nChat History:\n" + "\n\nUser: " + user_input + "\nAssistant:"

    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json'
    }

    payload = {
        'model': 'gpt-4o-mini-2024-07-18',
        'messages': [{"role": "system", "content": system_instructions}, {"role": "user", "content": prompt}],
        'max_tokens': 300,
        'temperature': 0.5
    }

    response = requests.post(OPENAI_ENDPOINT, json=payload, headers=headers)
    response_data = response.json()

    return response_data['choices'][0]['message']['content'].strip()

@csrf_exempt  # Disable CSRF protection for Twilio's webhook
def whatsapp_reply(request):
    incoming_msg = request.POST.get('Body', '').strip()

    intent = detect_intent(incoming_msg)

    if intent == "job_search":
        location = extract_location(incoming_msg)
        if location:
            skills = extract_skills(incoming_msg)
            job_listings = fetch_job_listings(location)
            response_text = generate_response(incoming_msg, job_listings)
        else:
            response_text = "Hey there! 😄 To help you find the perfect job, could you please provide the location where you'd like to work? You can simply mention the city name, like Johannesburg or Cape Town. 📍"
    elif intent == "career_advice":
        response_text = generate_response(incoming_msg, [])
    else:
        response_text = "Hey there! 😄 I'm an awesome career companion, so I can only help with job search and career advice. If you have any questions related to those topics, just let me know, and I'll be happy to assist! 💡"

    # Create a Twilio MessagingResponse to reply to the user
    resp = MessagingResponse()
    resp.message(response_text)

    return HttpResponse(str(resp), content_type="text/xml")