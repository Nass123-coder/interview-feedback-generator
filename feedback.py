import google.generativeai as genai
import json

# Replace with your valid Gemini API key from Makersuite
genai.configure(api_key="AIzaSyDcRAtoTu_hDhV_e8xdfQ_nsMwUTop1t1A")

def generate_interview_feedback(transcript_file, feedback_file="feedback.json"):
    with open(transcript_file, 'r', encoding='utf-8') as file:
        answer = file.read().strip()

    prompt = f"""
    You are an expert job interview evaluator.

    Analyze the following candidate response and return feedback in JSON format like this:
    {{
        "clarity": "...",
        "confidence": "...",
        "technical_accuracy": "...",
        "communication_skills": "...",
        "overall_feedback": "..."
    }}

    Interview Response:
    \"\"\"
    {answer}
    \"\"\"
    """

    try:
        model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
        response = model.generate_content(prompt)

        try:
            feedback_json = json.loads(response.text)
        except json.JSONDecodeError:
            print("⚠️ Gemini did not return valid JSON. Saving raw text instead.")
            feedback_json = { "raw_response": response.text }

        with open(feedback_file, 'w', encoding='utf-8') as f:
            json.dump(feedback_json, f, indent=4)

        print(f"✅ Feedback successfully saved to {feedback_file}")

    except Exception as e:
        print(f"❌ An error occurred: {e}")
