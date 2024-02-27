from general_functions.file_operations import read_json_file
from transformers import AutoTokenizer, AutoModelWithLMHead
from concurrent.futures import ThreadPoolExecutor

tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-emotion")
model = AutoModelWithLMHead.from_pretrained("mrm8488/t5-base-finetuned-emotion")


def classify_emotions(input_text):
    input_ids = tokenizer.encode(input_text + "</s>", return_tensors="pt")
    output = model.generate(input_ids=input_ids, max_length=2)

    dec = [tokenizer.decode(ids) for ids in output]
    print(dec)
    label = dec[0]
    print(label)
    return label

    # def get_score(result, emotion):
    #     for item in result[0]:
    #         if item["label"] == emotion:
    #             return item["score"]
    #     return None

    # emotion_scores = {
    #     "positive": get_score(result, "positive"),
    #     "neutral": get_score(result, "neutral"),
    #     "negative": get_score(result, "negative"),
    # }

    # return emotion_scores


dialogues = read_json_file(
    "src/book_projects/christmas_carol/data/christmas_carol_only_dialogues_without_sound_descriptions.json"
)

scrooge_dialogues = [
    dialogue for dialogue in dialogues if dialogue["character"] == "Scrooge"
]


def process_dialogue(dialogue):
    print("Processing dialogue: ", dialogue["text"])
    emotion_scores = classify_emotions(dialogue["text"])
    # print("Emotion scores: ", emotion_scores)
    # dialogue["emotion_scores"] = emotion_scores
    # return dialogue


process_dialogue(scrooge_dialogues[0])

# with ThreadPoolExecutor() as executor:
#     scrooge_dialogues = list(executor.map(process_dialogue, scrooge_dialogues))


# from general_functions.file_operations import write_json_file

# write_json_file(
#     "src/book_projects/christmas_carol/data/scrooge_dialogues_with_emotion_scores_t5.json",
#     scrooge_dialogues,
# )
