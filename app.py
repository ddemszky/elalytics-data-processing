import streamlit as st
import nltk
from nltk.corpus import stopwords
from collections import Counter
import heapq
import json
import time
from deep_translator import GoogleTranslator


def translate_to_spanish(text):
    """Translate text to spanish
    Args:
        text (str): The text to be translated
    Returns:
        str: The translated text
    """
    translated_text = GoogleTranslator(source='english', target='spanish').translate(text)
    return translated_text


def generate_wordcloud_data(input_text, top_n):
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

    text_data = input_text
    status_box = st.status(label="Generating word cloud data...", state="running")
    word_freq_data = word_frequencies(tokenize_and_filter(text_data))
    word_freq_data = dict(word_freq_data)

    word_freq_data = top_n_values(word_freq_data, top_n)

    word_cloud_data = []
    my_bar = st.progress(0)
    with status_box:
        st.write("Translate words and format output process started...")

        for i, word_pos_count in enumerate(word_freq_data.items()):
            word = process_word(word_pos_count)
            word_cloud_data.append(word)
            if (i + 1) % 10 == 0:  # print progress every 10 words
                st.write(f"Processed {i+1} words...")
            my_bar.progress((i + 1) / top_n)
    status_box.update(label="Generating word cloud data... Done!", state="complete")

    return word_cloud_data


st.title("Elalytics Chart Creator")
uploaded_file = st.file_uploader("Upload a text file", type=["txt"])
if uploaded_file is not None:
    file_text = uploaded_file.read().decode("utf-8")
    text_container = st.container()
    with text_container:
        st.markdown(
            f"""<div style="height:300px;overflow-y:auto;padding:10px">{file_text}</div>""",
            unsafe_allow_html=True,
        )
    st.write("Generating word cloud...")
    word_cloud_data = generate_wordcloud_data(file_text, 50)
    st.write("Word cloud generated!")
    st.write(word_cloud_data)
