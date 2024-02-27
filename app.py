import streamlit as st
import nltk
nltk.download("stopwords")
nltk.download("punkt")
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import stopwords
from collections import Counter
import heapq
import json
import time
from deep_translator import GoogleTranslator
from firestore_app import db
import random


def translate_to_spanish(text):
    """Translate text to spanish
    Args:
        text (str): The text to be translated
    Returns:
        str: The translated text
    """
    translated_text = GoogleTranslator(source='english', target='spanish').translate(text)
    return translated_text


def generate_wordcloud_data(input_text, top_n, categoriesToInclude=["Noun", "Verb", "Adjective"]):
    """
    Generates a word cloud data file from a text file

    Parameters:
    input_path (str): Path to the input text file
    top_n (int): Number of words to include in the word cloud
    categoriesToInclude (list): List of word categories to include in the word cloud
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
        pos_tagged_words = [
            (word, pos) for word, pos in pos_tagged_words if pos in categoriesToInclude
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

def addDataToFirestore(chart_title, documentName,data):
    db.collection("wordclouds").document(documentName).set({"chartTitle":chart_title,"data":data})

def checkIfDocumentExists(documentName):
    doc_ref = db.collection("wordclouds").document(documentName)
    doc = doc_ref.get()
    if doc.exists:
        return True
    else:
        return False

st.title("Elalytics Chart Creator")
uploaded_file = st.file_uploader("Upload a text file", type=["txt"])
chart_title = st.text_input("Chart Title", value="")
word_count = st.number_input("Number of words to include in word cloud", min_value=1, max_value=250, value=30)
options = st.multiselect(
    'Select the POS Categories to include in the word cloud',
    ['Adjective', 'Adverb', 'Conjunction', 'Determiner', 'Existential', 'Foreign Word', 'Interjection', 'List Marker', 'Modal', 'Noun', 'Numeral', 'Particle', 'Possessive Ending', 'Possessive Wh-Pronoun', 'Preposition', 'Predeterminer', 'Pronoun', 'To', 'Verb', 'Wh-Adverb', 'Wh-Determiner', 'Wh-Pronoun']
,
    ['Adjective', 'Noun', 'Verb', 'Adverb'])
start_button = st.button('Generate Word Cloud Page', disabled=uploaded_file is None)
if start_button:
    file_text = uploaded_file.read().decode("utf-8")
    st.write("Generating word cloud...")
    word_cloud_data = generate_wordcloud_data(file_text, word_count, options)
    st.write("Adding word cloud to firestore...")

    random_number = random.randint(100000, 999999)
    document_name = f"w{random_number}"
    while checkIfDocumentExists(document_name):
        random_number = random.randint(100000, 999999)
        document_name = f"w{random_number}"
    addDataToFirestore(chart_title,document_name,word_cloud_data)

    st.write("Word Cloud Generated!")
    st.write("View your word cloud here:")
    st.markdown(f"https://elalytics.vercel.app/wordcloud/{document_name}")



