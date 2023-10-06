import os
import glob
from booknlp.booknlp import BookNLP

def run_booknlp(input_file_location, output_directory, book_id, pipeline="entity", model="big"):
    """
    This function runs the BookNLP tool on a given text.

    Parameters:
    input_file_location (str): The location of the input file.
    output_directory (str): The directory where the output should be saved.
    book_id (str): The ID of the book.
    pipeline (str, optional): The pipeline to use. Defaults to "entity".
    model (str, optional): The model to use. Defaults to "big".

    Returns:
    The booknlp return files are saved in the output_directory.
    """   

    # Check if there are already files in the output directory
    # Define the list of BookNLP file extensions
    booknlp_extensions = ['.book', '.book.html', '.entities', '.quotes', '.supersense', '.tokens']

    # Check if there are already BookNLP files in the output directory
    existing_files = glob.glob(os.path.join(output_directory, '*'))
    existing_booknlp_files = [file for file in existing_files if any(file.endswith(ext) for ext in booknlp_extensions)]

    if existing_booknlp_files:
        print("The following BookNLP files already exist in the output directory:")
        for file in existing_booknlp_files:
            print(file)
        proceed = input("Looks like there are already BookNLP files in the given folder. Do you still want to run BookNLP? (y/n): ")
        if proceed.lower() != 'y':
            return
        
    # Run BookNLP    
    model_params={
            "pipeline":pipeline, 
            "model":model
        }        
    booknlp_load=BookNLP("en", model_params)
    # File within this directory will be named ${book_id}.entities, ${book_id}.tokens, etc.
    booknlp_load.process(input_file_location, output_directory, book_id)
    print("BookNLP processing complete.")