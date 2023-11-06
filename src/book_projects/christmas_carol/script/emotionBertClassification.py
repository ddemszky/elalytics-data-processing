from general_functions.file_operations import read_json_file
from transformers import pipeline
from concurrent.futures import ThreadPoolExecutor


def classify_emotions(input_text):
    classifier = pipeline(
        "text-classification",
        model="lxyuan/distilbert-base-multilingual-cased-sentiments-student",
        return_all_scores=True,
    )
    result = classifier(input_text)

    def get_score(result, emotion):
        for item in result[0]:
            if item["label"] == emotion:
                return item["score"]
        return None

    emotion_scores = {
        "positive": get_score(result, "positive"),
        "neutral": get_score(result, "neutral"),
        "negative": get_score(result, "negative"),
    }

    return emotion_scores


dialogues = read_json_file(
    "src/book_projects/christmas_carol/data/christmas_carol_only_dialogues_without_sound_descriptions.json"
)

scrooge_dialogues = [
    dialogue for dialogue in dialogues if dialogue["character"] == "Scrooge"
]


def process_dialogue(dialogue):
    print("Processing dialogue: ", dialogue["text"])
    emotion_scores = classify_emotions(dialogue["text"])
    print("Emotion scores: ", emotion_scores)
    dialogue["emotion_scores"] = emotion_scores
    return dialogue


with ThreadPoolExecutor() as executor:
    scrooge_dialogues = list(executor.map(process_dialogue, scrooge_dialogues))


from general_functions.file_operations import write_json_file

write_json_file(
    "src/book_projects/christmas_carol/data/scrooge_dialogues_with_emotion_scores_lxyuan.json",
    scrooge_dialogues,
)
