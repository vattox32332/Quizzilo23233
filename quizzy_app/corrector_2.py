import google.generativeai as genai
from .models import *
import re


# Function to process the array with AI
def process_with_ai(Exam):
    # Configure the Google Generative AI
    genai.configure(api_key='AIzaSyCLeDS3QDsKfTH5Ri9FSjnFiWC-oBgr7hw')

    # Create the model
    generation_config = {
        "temperature": 0.9,
        "top_p": 0.9,
        "top_k": 0,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(model_name="gemini-1.5-pro",
                                  generation_config=generation_config,
                                  safety_settings=[])

    chat_session = model.start_chat(history=[])

    # Send the array to the AI model
    response = chat_session.send_message(f""" 
    
        You are a highly logical AI system specialized in evaluating structured exam arrays and determining the correctness of each proposition.
        
        Your task is to process the given nested array of exam questions and multiple-choice answers. For each question:
        
        Identify the correct answer(s) as true (1) and the incorrect ones as false (0).
        
        Return the output strictly in the following structured format:
        
        Begin each question block with:
        $1/1$ <question_id> $1/1$
        
        For each choice under that question, return:
        
        $2/2$ <choice_id> $2/2$
        
        $3/3$ 0 or 1 $3/3$ (where 1 = true, 0 = false)
        
        Requirements:
        
        You must preserve the exact sequence and formatting.
        
        Return only the answer block, without any explanations or commentary.
        
        Maintain strict nesting logic and label pairing as per the format.
        
        Input variable: Exam
        Input structure:
        
        [
          [
            ['question_id', 'question_text'],
            ['choice_id1', 'choice_text1', ''],
            ['choice_id2', 'choice_text2', ''],
            ...
          ],
          ...
        ]
        You are to analyze each choice for its factual accuracy and return the response as:
        
        
        $1/1$ <question_id> $1/1$
        $2/2$ <choice_id1> $2/2$
        $3/3$ <0 or 1> $3/3$
        $2/2$ <choice_id2> $2/2$
        $3/3$ <0 or 1> $3/3$
        ...

    """)

    txt_correction = response.text

    # Clean the string by removing '```python' and '```'
    cleaned_string = txt_correction.replace('```python',
                                            '').replace('```', '').strip()

    return cleaned_string
