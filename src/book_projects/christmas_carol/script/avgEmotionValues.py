import pandas as pd
import nltk
from general_functions.file_operations import read_json_file
from general_functions.file_operations import write_json_file
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet


class DialogueProcessor:
    def __init__(self, lexicons, valence_lexicon):
        self.lexicons = lexicons
        self.valence_lexicon = valence_lexicon
        self.LEXNAMES = list(lexicons.keys())

    def get_wordnet_pos(self, word):
        """Map POS tag to first character lemmatize() accepts"""
        tag = nltk.pos_tag([word])[0][1][0].upper()
        tag_dict = {
            "J": wordnet.ADJ,
            "N": wordnet.NOUN,
            "V": wordnet.VERB,
            "R": wordnet.ADV,
        }

        return tag_dict.get(tag, wordnet.NOUN)

    def get_vals(self, dialogue):
        lemmatizer = WordNetLemmatizer()
        tt = word_tokenize(dialogue["text"].lower())
        tt = [lemmatizer.lemmatize(w, self.get_wordnet_pos(w)) for w in tt]
        emotionWords = {}
        valence_values = []
        lexdf = pd.DataFrame(
            {name: pd.Series(self.lexicons[name]) for name in self.LEXNAMES}
        )
        for lexicon in lexdf.columns:
            lexdf[lexicon] = lexdf[lexicon].fillna(
                0
            )  # Fill NaN values with 0 in the lexicon
            pw = [x for x in tt if x in lexdf[lexicon].index]
            pv = [lexdf[lexicon].loc[w] for w in pw]
            emotionWords[lexicon] = sum(pv)
            valence_values.extend(pv)

        valence = sum(valence_values) / len(valence_values) if valence_values else 0
        word_count = len(tt)

        return {
            "emotionWords": emotionWords,
            "valence": valence,
            "word_count": word_count,
        }

    def process_list(self, dialogues):
        for dialogue in dialogues:
            dialogue.update(self.get_vals(dialogue))
        return dialogues

    def process(self, dialogues):
        return self.process_list(dialogues)


emotion_words_lexicon = {
    "anger": read_json_file("src/general_functions/lexicons/NRC_EmoLex_anger.json"),
    "disgust": read_json_file("src/general_functions/lexicons/NRC_EmoLex_disgust.json"),
    "positive": read_json_file(
        "src/general_functions/lexicons/NRC_EmoLex_positive.json"
    ),
    "negative": read_json_file(
        "src/general_functions/lexicons/NRC_EmoLex_negative.json"
    ),
    "joy": read_json_file("src/general_functions/lexicons/NRC_EmoLex_joy.json"),
    "sadness": read_json_file("src/general_functions/lexicons/NRC_EmoLex_sadness.json"),
}

valence_lexicon = read_json_file("src/general_functions/lexicons/NRC_VAD_valence.json")

dialogues = read_json_file(
    "src/book_projects/christmas_carol/data/christmas_carol_only_dialogues_without_sound_descriptions.json"
)

processor = DialogueProcessor(emotion_words_lexicon, valence_lexicon)
processed_dialogues = processor.process(dialogues)

write_json_file(
    "src/book_projects/christmas_carol/data/christmas_carol_only_dialogues_without_sound_descriptions_with_emotion_values.json",
    processed_dialogues,
)
