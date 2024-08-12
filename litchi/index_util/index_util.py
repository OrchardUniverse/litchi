
import openai
from openai import OpenAI
import os
import json
import sqlite3
from jinja2 import Template
import hashlib

from sqlite_util import SqliteUtil
from sqlite_util import SourceCodeIndex

def read_file(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    return code

def generate_prompt_old(code):
    prompt = f"""
    I have the following Python code:
    
    {code}
    
    Could you please explain what this code does, including the purpose of each function, class, and key part of the code?
    """
    return prompt

def generate_prompt(code):
    prompt_file = "./analyse_code_prompt.txt"
    with open(prompt_file, 'r') as file:
        template_content = file.read()

    template = Template(template_content)
    params = {
        'code': code
    }
    return template.render(params)


def chat_with_llm(user_prompt):

    client = OpenAI(
        base_url="https://api.gptsapi.net/v1",
        # TODO: change to read config file or use envrinment variable
        api_key="sk-bMc085e38ed3500c7839ad50ae35ddf19a61c134df80KGqT"
    )

    completion = client.chat.completions.create(
    #model="gpt-4-1106-preview",
    model="gpt-3.5-turbo-1106",
    messages=[
        {"role": "system", "content": "As a professional source code expert, analyze the given source code file. Your goal is to thoroughly understand the content and purpose of the code. Your response should be in JSON format."},
        {"role": "user", "content": user_prompt}
    ],
    response_format={"type": "json_object"}
    )

    json_string = completion.choices[0].message.content
    tokens = completion.usage.total_tokens
    return json_string, tokens


def save_json_to_file(json_str, file_path):
    """
    Load a JSON string and save it to a local file.
    
    Args:
        json_str (str): The JSON string to be loaded.
        file_path (str): The path to the file where the JSON data should be saved.
    
    Returns:
        None
    """
    try:
        # Load the JSON string into a Python dictionary
        data = json.loads(json_str)
        
        # Write the dictionary to a JSON file
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        
        print(f"JSON data has been successfully saved to {file_path}")
    
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def remove_first_last_lines_if_quoted(text):
    lines = text.splitlines()
    if len(lines) >= 2 and lines[0].strip().startswith("```") and lines[-1].strip().startswith("```"):
        return '\n'.join(lines[1:-1])
    return text

def llm_explain_code(file_path):

    code = read_file(file_path)
    prompt = generate_prompt(code)
    
    llm_output_json, tokens = chat_with_llm(prompt)

    json_string = remove_first_last_lines_if_quoted(llm_output_json)

    #output_json_file = "llm_analyse_code_output.json"
    #save_json_to_file(json, output_json_file)
    
    #import ipdb;ipdb.set_trace()
    print(json_string)

    return json.loads(json_string), tokens

def read_json(json_file):
    # Read JSON data from file
    with open(json_file, 'r') as file:
        data = json.load(file)
    return data

def insert_source_code_index_to_db(data, db_file):
        
    # Prepare data for insertion
    file = data['file']
    lines = data['lines']
    md5 = data['md5']
    name = data['name']
    purpose = data['purpose']
    # Convert lists of classes and functions to JSON strings for storage
    classes = json.dumps(data['classes'])

    db_util = SqliteUtil(db_file)
    db_util.insert_row(file, lines, md5, name, purpose, classes)

def compute_md5_and_count_lines(filename):
    hash_md5 = hashlib.md5()
    line_count = 0

    with open(filename, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_md5.update(chunk)
            line_count += chunk.count(b'\n')

    return hash_md5.hexdigest(), line_count


def dict_to_json_file(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def generate_source_code_index(file, llm_output_json, tokens) -> SourceCodeIndex:
    md5_hash, line_count = compute_md5_and_count_lines(file)

    classes = json.dumps(llm_output_json['classes'])

    # TODO: Make sure to get attributes from llm output json
    return SourceCodeIndex(file=file, lines=line_count, md5=md5_hash, 
                            name=llm_output_json['name'], purpose=llm_output_json['purpose'], 
                            classes=classes, tokens = tokens)


    

    
class SourceCodeIndexManager:
    def __init__(self, db_name) -> None:
        self.db_util = SqliteUtil(db_name)

    def is_index_existed(self, file_path) -> bool:
        return self.db_util.row_exists(file_path)
    
    def create_index(self, file_path):
        if self.is_index_existed(file_path):
            print("The index exists, skip creating")
            return
        else:
            print(f"Try to create the index for {file_path}")
            llm_output_json, tokens = llm_explain_code(file_path)
            source_code_index = generate_source_code_index(file_path, llm_output_json, tokens)
            self.db_util.insert_index(source_code_index)

    def update_index(self, file_path):
        pass

    def delete_index(self, file_path):
        pass



if __name__ == "__main__":
    db_name = "source_code_index.db"
    index_manager = SourceCodeIndexManager(db_name)

    source_file = "/Users/tobe/code/orchard_universe/basket/basket/cli.py"
    print(index_manager.is_index_existed(source_file))

    source_file = "/Users/tobe/code/orchard_universe/basket/basket/basket_config/auths_config.py"
    index_manager.create_index(source_file)
