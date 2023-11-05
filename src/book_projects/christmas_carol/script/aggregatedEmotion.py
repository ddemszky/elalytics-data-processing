import json

# Load the data
with open(
    "src/book_projects/christmas_carol/data/christmas_carol_only_dialogues_without_sound_descriptions_with_emotion_values.json",
    "r",
) as f:
    data = json.load(f)

# Initialize a list to store the aggregate values
aggregate_values = []

# Specify the character
character = "Scrooge"

# Add a dialogue count to each scene
for item in data:
    # Only include dialogues from the specified character
    if item["character"] == character:
        act = item["act"]
        scene = item["scene"]
        act_scene = f"{act} {scene}"

        # Check if the act and scene already exist in the aggregate values
        for value in aggregate_values:
            if value["actScene"] == act_scene:
                break
        else:
            aggregate_values.append(
                {
                    "actScene": act_scene,
                    "word_count": 0,
                    "dialogue_count": 0,
                    "emotionWords": {
                        "anger": 0,
                        "disgust": 0,
                        "positive": 0,
                        "negative": 0,
                        "joy": 0,
                        "sadness": 0,
                    },
                    "valence": 0,
                }
            )

        # Update the aggregate values for the act and scene
        for value in aggregate_values:
            if value["actScene"] == act_scene:
                value["word_count"] += item["word_count"]
                value["dialogue_count"] += 1
                for emotion in item["emotionWords"]:
                    value["emotionWords"][emotion] += item["emotionWords"][emotion]
                value["valence"] += item["valence"]

# Calculate the average values
for value in aggregate_values:
    for emotion in value["emotionWords"]:
        value["emotionWords"][emotion] /= value["word_count"]
    value["valence"] /= value["dialogue_count"]


# Save the aggregate values to a JSON file
with open(
    "src/book_projects/christmas_carol/data/aggregated_emotion_values_scrooge.json", "w"
) as f:
    json.dump(aggregate_values, f)
