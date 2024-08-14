
import openai
from openai import OpenAI
import os
import json
import sqlite3

import hashlib

from .sqlite_util import SqliteUtil
from .sqlite_util import SourceCodeIndex
from .prompt_util import generate_prompt, generate_get_related_source_files_prompt, generate_chat_with_realted_source_files_prompt

def read_file(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    return code


def chat_with_llm(user_prompt):

    client = OpenAI(
        base_url=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        api_key=os.environ.get("OPENAI_API_KEY")
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

def adhoc_chat_with_llm(user_prompt):
    client = OpenAI(
        base_url=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        api_key=os.environ.get("OPENAI_API_KEY")
    )

    completion = client.chat.completions.create(
        #model="gpt-4-1106-preview",
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": "You are a helpful assitant can summarize the source code and give the user a reasonable and understandable response."},
            #  Please always response in Chinese.
            {"role": "user", "content": user_prompt}
        ]
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

def read_file_content(file_path):
    """
    Reads the content of a file and returns it as a string.

    Parameters:
        file_path (str): The path to the file to be read.

    Returns:
        str: The content of the file as a string.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return f"Error: The file at {file_path} was not found."
    except IOError:
        return f"Error: An I/O error occurred while reading the file at {file_path}."
    

    
class SourceFileIndexManager:
    def __init__(self, project_dir: str = "./") -> None:
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

    def get_related_files(self, user_query, max_file_count=10):
        source_file_indexes = self.db_util.select_all_rows()
        
        prompt = generate_get_related_source_files_prompt(user_query, source_file_indexes, max_file_count)
        
        llm_output_json, tokens = chat_with_llm(prompt)

        json_string = remove_first_last_lines_if_quoted(llm_output_json)

        return json.loads(json_string)["files"]

    def chat_with_related_files(self, user_query, max_file_count=10):
        files = self.get_related_files(user_query, max_file_count)
        file_content_list = [{"file": file, "content": read_file_content(os.path.join(self.project_dir, file))} for file in files]
        prompt = generate_chat_with_realted_source_files_prompt(user_query, file_content_list)

        llm_output, tokens = adhoc_chat_with_llm(prompt)
        return llm_output



