import google.generativeai as genai
from pathlib import Path

# Assuming you have the API key stored somewhere securely or passed as an argument
genai.configure(api_key="Gemini_Api_key")


def text_ai(question):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(question)
        answer = response.text
        return answer
    except Exception as e:
        feedback = response.prompt_feedback
        if feedback:
            if "SAFETY" in feedback:
                # return "Sorry, this propmt was blocked for safety."
                print(feedback)
            else:
                # return "Sorry, this propmt was blocked for safety."
                # return feedback
                print(feedback)
        else:
            # return "Sorry, this propmt was blocked for safety."
            print(feedback)
            # return feedback
            
    

def image_ai(image_path, quest):
    try:
        model = genai.GenerativeModel('gemini-pro-vision')

        with open(image_path, 'rb') as image_file:
            image_bytes = image_file.read()

        cookie_picture = {
            'mime_type': 'image/png',
            'data': image_bytes
        }
        prompt = quest

        response = model.generate_content(
            contents=[prompt, cookie_picture]
        )
        return response.text
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print(response.prompt_feedback)  # This line for printing prompt_feedback
        return f"An error occurred: {str(e)}"
