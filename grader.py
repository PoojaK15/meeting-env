# grader.py

def keyword_match(summary, original_text):
    """
    Checks how many important words from original text
    are present in summary.
    """

    # Extract important words (basic filtering)
    words = original_text.lower().split()
    important_words = list(set([w for w in words if len(w) > 4]))

    if not important_words:
        return 0

    match_count = 0
    for word in important_words:
        if word in summary.lower():
            match_count += 1

    return match_count / len(important_words)


def check_task_relevance(summary, tasks):
    """
    Checks if extracted tasks are relevant to summary
    """

    if not tasks:
        return 0

    score = 0

    for task in tasks:
        task_words = task.lower().split()

        # If any word of task is present in summary → relevant
        if any(word in summary.lower() for word in task_words):
            score += 1

    return score / len(tasks)


def compression_score(summary, original_text):
    """
    Checks if summary length is balanced
    """

    if len(original_text) == 0:
        return 0

    ratio = len(summary) / len(original_text)

    if 0.3 <= ratio <= 0.7:
        return 1.0
    elif ratio < 0.2:
        return 0.3
    else:
        return 0.5


def grade_summary(summary, original_text, tasks, mode="basic"):
    """
    Final scoring function
    """

    k_score = keyword_match(summary, original_text)
    t_score = check_task_relevance(summary, tasks)
    c_score = compression_score(summary, original_text)

    # Weighted scoring
    final_score = (0.4 * k_score) + (0.4 * t_score) + (0.2 * c_score)

    # Small boost for AI mode
    if mode == "ai":
        final_score += 0.05

    # Cap score at 1
    final_score = min(final_score, 1.0)

    return round(final_score, 2)


# Detailed report 
def detailed_report(summary, original_text, tasks):
    return {
        "keyword_score": round(keyword_match(summary, original_text), 2),
        "task_score": round(check_task_relevance(summary, tasks), 2),
        "compression_score": round(compression_score(summary, original_text), 2)
    }