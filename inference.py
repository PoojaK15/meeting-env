# inference.py
#from transformers import pipeline
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
def ai_summary(text):
    """
    AI-based summary using HuggingFace
    (fallback to basic if not available)
    """
    try:
        from transformers import pipeline

        summarizer = pipeline("summarization")
        result = summarizer(text, max_length=60, min_length=20, do_sample=False)

        return result[0]['summary_text']

    except Exception:
        print("⚠ AI model not available, using basic summary.")
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