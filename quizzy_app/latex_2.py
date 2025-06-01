import google.generativeai as genai

def MathExpressions_2(Exam):
    print(f"[DEBUG] MathExpressions_2 called with Exam: {type(Exam)}")
    print(f"[DEBUG] Exam length: {len(Exam) if hasattr(Exam, '__len__') else 'N/A'}")
    genai.configure(api_key='AIzaSyCUVg8SJPMHgIY5bCMtUqk5I0tuxNc9o9E')
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
        model_name="gemini-2.0-flash",
        generation_config=generation_config,
        safety_settings=[]
    )

    chat_session = model.start_chat(history=[])
    print("[DEBUG] Sending LaTeX processing request to AI...")

    try:
        response = chat_session.send_message(f"""
        Convert math to LaTeX in array format:

        Input: [[[id, 'text'], [id, 'text']], ...]
        Output: Same with LaTeX math using $$ for display, $ for inline

        Data: {Exam}
        """)
    except Exception as e:
        print(f"[DEBUG] Error with AI request: {e}")
        return str(Exam)  # Return original data if AI fails

    # Process the response from the AI
    print("[DEBUG] LaTeX AI response received")
    txt_ai = response.text
    print(f"[DEBUG] LaTeX response length: {len(txt_ai)}")
    print(f"[DEBUG] LaTeX response first 200 chars: {txt_ai[:200]}...")
    
    return txt_ai
