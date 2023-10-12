import json
import os

# Read a text file from a given path
def read_txt_file(file_path):
    """Read a text file from a given path
    Args:
        file_path (str): The path to the file to be read. Example: "data/input.txt"

    Returns:
        str: The contents of the file
    """

    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()
    return data

# Write a text file to a given path
def write_txt_file(file_path, data):
    """Write a text file to a given path
    Args:
        file_path (str): The path to the file to be written. Example: "data/test_output.txt"
        data (str): The data to be written to the .txt file
    """
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(data)
    print("Successfully written to file.")

# Read a json file from a given path
def read_json_file(file_path):
    """Read a json file from a given path
    Args:
        file_path (str): The path to the file to be read. Example: "data/input.json"

    Returns:
        dict: The contents of the json file
    """

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Write a json file to a given path
def write_json_file(file_path, data):
    """Write a json file to a given path
    Args:
        file_path (str): The path to the file to be written. Example: "data/test_output.json"
        data (dict): The data to be written to the .json file
    """

    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)    
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
    print("Successfully written to file.")

# read all files from a folder
def read_files_from_folder(folder_path):
    """Read all files from a folder
    Args:
        folder_path (str): The path to the folder to be read. Example: "data/input"

    Returns:
        list: A list of all the files in the folder
    """

    files = os.listdir(folder_path)
    return files

#check if a file is utf-8 encoded
def is_utf8(file_path):
    """Check if a file is utf-8 encoded
    Args:
        file_path (str): The path to the file to be checked. Example: "data/input.txt"

    Returns:
        bool: True if the file is utf-8 encoded, False otherwise
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file.read()
        return True
    except UnicodeDecodeError:
        return False

