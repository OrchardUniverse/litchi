
import openai
from openai import OpenAI
import os
import json
import sqlite3
from jinja2 import Template
import hashlib

from .sqlite_util import SqliteUtil
from .sqlite_util import SourceCodeIndex

def read_file(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    return code

def generate_prompt(programming_language, code):

    script_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_file = os.path.join(script_dir, "analyse_code_prompt.txt")

    with open(prompt_file, 'r') as file:
        template_content = file.read()

    template = Template(template_content)
    params = {
        'programming_language': programming_language,
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

    print(f"LLM request:\n {user_prompt}")
    print(f"LLM response:\n {completion}")

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

def llm_explain_code(programming_language, file_path):

    code = read_file(file_path)
    prompt = generate_prompt(programming_language, code)
    
    llm_output_json, tokens = chat_with_llm(prompt)

    json_string = remove_first_last_lines_if_quoted(llm_output_json)

    #output_json_file = "llm_analyse_code_output.json"
    #save_json_to_file(json, output_json_file)
    
    return json.loads(json_string), tokens

def read_json(json_file):
    # Read JSON data from file
    with open(json_file, 'r') as file:
        data = json.load(file)
    return data

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

    

    
class SourceFileIndexManager:
    def __init__(self, project_dir) -> None:
        self.project_dir = project_dir

        litchi_path = os.path.join(project_dir, ".litchi")
        if not os.path.exists(litchi_path):
            os.makedirs(litchi_path)

        db_name = os.path.join(litchi_path, "source_file_index.db")
        self.db_util = SqliteUtil(db_name)

    def generate_source_file_index(self, file, llm_output_json, tokens) -> SourceCodeIndex:
        absolute_file_path = os.path.join(self.project_dir, file)
        md5_hash, line_count = compute_md5_and_count_lines(absolute_file_path)

        classes = json.dumps(llm_output_json['classes'])

        # TODO: Make sure to get attributes from llm output json
        return SourceCodeIndex(file=file, lines=line_count, md5=md5_hash, 
                                name=llm_output_json['name'], purpose=llm_output_json['purpose'], 
                                classes=classes, tokens = tokens)

    def is_index_existed(self, file_path) -> bool:
        return self.db_util.row_exists(file_path)
    
    def create_index(self, file_path, programming_language="Unknown"):
        
        if self.is_index_existed(file_path):
            print("The index exists, skip creating.")
            return
        else:
            print(f"Try to create the index for {file_path}")
            absolute_file_path = os.path.join(self.project_dir, file_path)
            llm_output_json, tokens = llm_explain_code(programming_language, absolute_file_path)
            source_file_index = self.generate_source_file_index(file_path, llm_output_json, tokens)
            self.db_util.insert_index(source_file_index)

    def update_index(self, file_path):
        pass

    def delete_index(self, file_path):
        pass

