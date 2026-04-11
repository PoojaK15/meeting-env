# util.py

# -------- BASIC SUMMARY --------
def basic_summary(text):
    """
    Simple summary: takes first 2 sentences
    """
    sentences = text.split(".")
    sentences = [s.strip() for s in sentences if s.strip()]
    
    summary = ". ".join(sentences[:2])
    return summary


# -------- TASK EXTRACTION --------
def extract_tasks(text):
    """
    Extract tasks using simple rules
    """
    tasks = []
    sentences = text.split(".")

    for s in sentences:
        s = s.strip()
        if not s:
            continue

        s_lower = s.lower()

        if "will" in s_lower or "shall" in s_lower or "need to" in s_lower:
            tasks.append(s)

    return tasks


# -------- AI SUMMARY --------
import os
from openai import OpenAI

def ai_summary(text):
    try:
        client = OpenAI(
            base_url=os.environ["API_BASE_URL"],
            api_key=os.environ["API_KEY"]
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Summarize the meeting text briefly."},
                {"role": "user", "content": text}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        print("⚠ AI failed, using basic summary.")
        return basic_summary(text)

# -------- MAIN FUNCTION --------
def run_inference(text, mode="basic"):
    """
    Main function → used by env.py / main.py
    """

    if mode == "basic":
        summary = basic_summary(text)
        tasks = extract_tasks(text)

    elif mode == "ai":
        summary = ai_summary(text)
        tasks = extract_tasks(text)

    else:
        raise ValueError("Mode must be 'basic' or 'ai'")

    return {
        "summary": summary,
        "tasks": tasks,
        "original_text": text   
    }

