from transformers import pipeline


def get_emotion_scores_j_hartmann_bert(input_text):
    classifier = pipeline(
        "text-classification",
        model="j-hartmann/emotion-english-distilroberta-base",
        top_k=None,
    )
    result = classifier(input_text)

    def get_score(result, emotion):
        for item in result[0]:
            if item["label"] == emotion:
                return item["score"]
        return None

    emotion_scores = {
        "anger": get_score(result, "anger"),
        "disgust": get_score(result, "disgust"),
        "fear": get_score(result, "fear"),
        "joy": get_score(result, "joy"),
        "sadness": get_score(result, "sadness"),
        "surprise": get_score(result, "surprise"),
        "neutral": get_score(result, "neutral"),
    }

    return emotion_scores
