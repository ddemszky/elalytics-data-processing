import nltk
from nltk.corpus import stopwords
from collections import Counter
import heapq
import json
import time
from general_functions.translation import translate_to_spanish


def generate_wordcloud_data(input_path, output_path, top_n):
    """
    Generates a word cloud data file from a text file

    Parameters:
    input_path (str): Path to the input text file
    output_path (str): Path to the output json file
    top_n (int): Number of words to include in the word cloud
    """

    def top_n_values(dictionary, n):
        top_items = heapq.nlargest(n, dictionary.items(), key=lambda item: item[1])
        return dict(top_items)

    def tokenize_and_filter(text):
        STOP_WORDS = set(stopwords.words("english"))
        words = nltk.word_tokenize(text)
        pos_tagged_words = nltk.pos_tag(words)
        pos_tag_mapping = {
            "CC": "Conjunction",
            "CD": "Numeral",
            "DT": "Determiner",
            "EX": "Existential",
            "FW": "Foreign Word",
            "IN": "Preposition",
            "JJ": "Adjective",
            "JJR": "Adjective",
            "JJS": "Adjective",
            "LS": "List Marker",
            "MD": "Modal",
            "NN": "Noun",
            "NNS": "Noun",
            "NNP": "Noun",
            "NNPS": "Noun",
            "PDT": "Predeterminer",
            "POS": "Possessive Ending",
            "PRP": "Pronoun",
            "PRP$": "Pronoun",
            "RB": "Adverb",
            "RBR": "Adverb",
            "RBS": "Adverb",
            "RP": "Particle",
            "TO": "To",
            "UH": "Interjection",
            "VB": "Verb",
            "VBD": "Verb",
            "VBG": "Verb",
            "VBN": "Verb",
            "VBP": "Verb",
            "VBZ": "Verb",
            "WDT": "Wh-Determiner",
            "WP": "Wh-Pronoun",
            "WP$": "Possessive Wh-Pronoun",
            "WRB": "Wh-Adverb",
        }
        pos_tagged_words = [
            (word, pos_tag_mapping.get(pos, pos)) for word, pos in pos_tagged_words
        ]
        return [
            (word.lower(), pos)
            for word, pos in pos_tagged_words
            if word.isalpha() and word not in STOP_WORDS
        ]

    def word_frequencies(words):
        return Counter(words)

    def process_word(word_pos):
        word_pos_unit, count = word_pos
        word, pos = word_pos_unit
        time.sleep(0.1)  # delay to avoid hitting API limits
        try:
            value = count
        except KeyError:
            return None  # or some default value
        return {
            "word": word,
            "value": value,
            "category": pos,
            "translation": translate_to_spanish(word),
        }

    with open(input_path, "r", encoding="utf-8") as file:
        print("Reading input file...")
        text_data = file.read().replace("\n", " ")
    print("Tokenizing and filtering stopwords...")
    word_freq_data = word_frequencies(tokenize_and_filter(text_data))
    word_freq_data = dict(word_freq_data)

    print(f"Getting top {top_n} words...")
    word_freq_data = top_n_values(word_freq_data, top_n)

    word_cloud_data = []
    print("Translate words and format output process started...")
    for i, word_pos_count in enumerate(word_freq_data.items()):
        word = process_word(word_pos_count)
        word_cloud_data.append(word)
        if (i + 1) % 10 == 0:  # print progress every 10 words
            print(f"Processed {i+1} words...")

    print("Writing to output file...")
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(word_cloud_data, file, indent=4)
    print(f"Word cloud data saved to {output_path}")
