import nltk
from nltk.util import ngrams
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from general_functions.file_operations import read_txt_file
from general_functions.file_operations import write_json_file
from general_functions.translation import translate_to_spanish


def generate_ngramcloud_data(input_path, output_path, ngram_size=3, top_n=10):
    """
    Generates a ngram cloud data file from a text file

    Parameters:
    input_path (str): Path to the input text file
    output_path (str): Path to the output folder
    ngram_size (int): Size of the ngram
    top_n (int): Number of ngrams to include in the ngram cloud
    """

    print("Starting ngram generation...")

    # Your text data
    text = read_txt_file(input_path)

    # Tokenize the text into words
    words = word_tokenize(text)

    # Generate ngrams
    ngram_values = list(ngrams(words, ngram_size))

    print("Generated ngrams...")

    # Filter out ngram_values with punctuation
    ngram_values = [
        ngram for ngram in ngram_values if all(word.isalpha() for word in ngram)
    ]

    print("Filtered ngrams...")

    # Compute frequency distribution
    freq_dist = FreqDist(ngram_values)

    # Get the 10 most common ngram_values
    top_ngram_values = freq_dist.most_common(top_n)

    print("Computed frequency distribution...")

    output_data = []

    for ngram, count in top_ngram_values:
        if count > 1:
            print("Processing ngram: ", ngram)
            phrase = " ".join(ngram)
            output_data.append(
                {
                    "text": phrase,
                    "value": count,
                    "category": str(ngram_size) + "-gram",
                    "translation": translate_to_spanish(phrase),
                }
            )

    print("Generated output data...")

    # Customize output filename based on ngram_size
    output_filename = f"{output_path}/ngram_{ngram_size}_values.json"
    write_json_file(output_filename, output_data)
