LIKERT_SCALE = {
    "Strongly Disagree": 1,
    "Disagree": 2,
    "Neutral": 3,
    "Agree": 4,
    "Strongly Agree": 5
}

def compute_features(answers, questions):
    """
    answers: dict like {"q0": "10th", "q2": "Agree", "q8": "32", ...}
    questions: list of question docs from MongoDB (data/questions.json)
    Returns a clean dict of numeric features ready for the ML model.
    """
    features = {
        "realistic": 0, "investigative": 0, "artistic": 0,
        "social": 0, "enterprising": 0, "conventional": 0,
        "logical": 0, "numerical": 0, "verbal": 0, "spatial": 0
    }

    student_class = answers.get("q0", "")
    priority = answers.get("q1", "")

    for q in questions:
        qid = q["id"]
        if qid not in answers:
            continue
        answer = answers[qid]

        if q["type"] == "interest":
            score = LIKERT_SCALE.get(answer, 3)
            features[q["feature"]] = score

        elif q["type"] == "aptitude":
            is_correct = 1 if answer == q.get("correct") else 0
            features[q["feature"]] = is_correct

    return {
        "class": student_class,
        "priority": priority,
        **features
    }