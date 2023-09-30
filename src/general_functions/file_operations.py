import json
import os

# Read a text file from a given path
def read_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()
    return data

# Write a text file to a given path
# file path is relative to the current working directory. It can be data/output.txt 
def write_txt_file(file_path, data):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(data)
    print("Successfully written to file.")

# Read a json file from a given path
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Write a json file to a given path
def write_json_file(file_path, data):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)    
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
    print("Successfully written to file.")

# read all files from a folder
def read_files_from_folder(folder_path):
    files = os.listdir(folder_path)
    return files

