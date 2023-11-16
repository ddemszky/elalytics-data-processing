from general_functions.file_operations import read_txt_file
from general_functions.file_operations import write_json_file
import nltk
from nltk.tokenize import sent_tokenize, TreebankWordTokenizer


def tokenize_text(input_text_file_location, output_json_file_location):
    """
    Tokenize the input text file and write the tokenized text to a json file.
    :param input_text_file_location: Location of the input text file
    :param output_json_file_location: Location of the output json file
    :return: None
    """
    input_text = read_txt_file(input_text_file_location)
    nltk.download("punkt")  # Download the Punkt tokenizer
    tokenizer = TreebankWordTokenizer()
    input_text = input_text.replace(
        "\n\n", "\n"
    )  # Replace two newlines with a single newline
    paragraphs = input_text.split("\n")  # Split text into paragraphs
    tokenized_text = []
    for i, para in enumerate(paragraphs):
        lines = sent_tokenize(para)
        tokenized_lines = []
        for j, line in enumerate(lines):
            words = tokenizer.tokenize(line)
            tokenized_lines.append({"line_text": line, "words": words})
        tokenized_text.append({"para_text": para, "lines": tokenized_lines})
    write_json_file(output_json_file_location, tokenized_text)
