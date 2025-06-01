import google.generativeai as genai

def MathExpressions_2(Exam):
    print(f"[DEBUG] MathExpressions_2 called with Exam: {type(Exam)}")
    print(f"[DEBUG] Exam length: {len(Exam) if hasattr(Exam, '__len__') else 'N/A'}")
    genai.configure(api_key='AIzaSyBkMKT3lb8dXnEYqPFTg7pRh9sV47BKSbA')
    print("[DEBUG] AI configured for LaTeX processing")

    # Create the model
    generation_config = {
        "temperature": 0.1,
        "top_p": 0.9,
        "top_k": 0,
        "max_output_tokens": 16384,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
        safety_settings=[]
    )

    chat_session = model.start_chat(history=[])
    print("[DEBUG] Sending LaTeX processing request to AI...")

    response = chat_session.send_message(f"""
    Convert mathematical expressions to LaTeX format in this array structure:

    Input: [[[id, 'text'], [id, 'text']], ...]
    Output: Same structure with LaTeX formatting

    Use $$ for fractions, clean \\n and \\, keep IDs as integers.
    Return ONLY the formatted array, no explanations.

    Data: {Exam}
    """)

    # Process the response from the AI
    print("[DEBUG] LaTeX AI response received")
    txt_ai = response.text
    print(f"[DEBUG] LaTeX response length: {len(txt_ai)}")
    print(f"[DEBUG] LaTeX response first 200 chars: {txt_ai[:200]}...")
    
    return txt_ai
