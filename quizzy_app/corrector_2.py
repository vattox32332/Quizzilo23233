import google.generativeai as genai
from .models import *
import re


# Function to process the array with AI
def process_with_ai(Exam):
    print(f"[DEBUG] process_with_ai called with Exam: {Exam}")
    print(f"[DEBUG] Exam type: {type(Exam)}")
    print(f"[DEBUG] Exam length: {len(Exam) if hasattr(Exam, '__len__') else 'N/A'}")
    
    # Configure the Google Generative AI
    genai.configure(api_key='AIzaSyCUVg8SJPMHgIY5bCMtUqk5I0tuxNc9o9E')
    print("[DEBUG] AI configured")

    # Create the model
    generation_config = {
        "temperature": 0.9,
        "top_p": 0.9,
        "top_k": 0,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(model_name="gemini-2.0-flash",
                                  generation_config=generation_config,
                                  safety_settings=[])
    print("[DEBUG] Model created")

    chat_session = model.start_chat(history=[])
    print("[DEBUG] Chat session started")

    # Send the array to the AI model
    print("[DEBUG] Sending message to AI...")
    response = chat_session.send_message(f""" 
        You are a medical expert AI system. Analyze each multiple choice question and determine which choices are correct (1) or incorrect (0).

        CRITICAL: You must return ONLY the formatted output below. Do NOT include any explanations, code, or other text.

        For each question in the exam data, output EXACTLY this format:

        $1/1$ question_id $1/1$
        $2/2$ choice_id $2/2$
        $3/3$ 0_or_1 $3/3$
        $2/2$ choice_id $2/2$
        $3/3$ 0_or_1 $3/3$
        (repeat for all choices)

        Where:
        - question_id is the actual ID from the first element of each question array
        - choice_id is the actual ID from the first element of each choice array
        - 0_or_1 is either 0 (incorrect) or 1 (correct) based on medical knowledge

        Example input: [[[123, "Question text"], [456, "Choice A text", ""], [789, "Choice B text", ""]]]
        Example output:
        $1/1$ 123 $1/1$
        $2/2$ 456 $2/2$
        $3/3$ 1 $3/3$
        $2/2$ 789 $2/2$
        $3/3$ 0 $3/3$

        Now analyze this exam data: {Exam}

        Return ONLY the formatted output with the special markers. NO other text.
    """)

    print("[DEBUG] AI response received")
    txt_correction = response.text
    print(f"[DEBUG] AI response text length: {len(txt_correction)}")
    print(f"[DEBUG] AI response first 200 chars: {txt_correction[:200]}...")

    # Clean the string by removing '```python' and '```'
    cleaned_string = txt_correction.replace('```python',
                                            '').replace('```', '').strip()
    
    print(f"[DEBUG] Cleaned string length: {len(cleaned_string)}")
    print(f"[DEBUG] Cleaned string first 200 chars: {cleaned_string[:200]}...")
    print(f"[DEBUG] Returning cleaned_string")

    return cleaned_string
