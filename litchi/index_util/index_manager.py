
import os
import json
import sqlite3
import logging
import hashlib
from typing import List

from .sqlite_util import SqliteUtil
from .sqlite_util import SourceCodeIndex
from ..prompt_util.prompt_util import PromptUtil
from .llm_util import LlmUtil

from ..source_util.source_file_manager import SourceFileManager
from ..config_util.litchi_config import LitchiConfigManager

def read_file(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    return code

def remove_first_last_lines_if_quoted(text):
    lines = text.splitlines()
    if len(lines) >= 2 and lines[0].strip().startswith("```") and lines[-1].strip().startswith("```"):
        return '\n'.join(lines[1:-1])
    return text



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
        json.dump(data, json_file, indent=4, ensure_ascii=False)

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
        self.prompt_util = PromptUtil(project_dir)
        self.llm_util = LlmUtil(project_dir)
        self.config_manager = LitchiConfigManager(project_dir)


        litchi_path = os.path.join(project_dir, ".litchi")
        if not os.path.exists(litchi_path):
            os.makedirs(litchi_path)

        db_name = os.path.join(litchi_path, "source_file_index.db")
        self.db_util = SqliteUtil(db_name)

    def llm_explain_code(self, programming_language, file_path):
        code = read_file(file_path)
        prompt = self.prompt_util.get_analyse_code_prompt(programming_language, code)
        
        llm_output_json, tokens = self.llm_util.call_llm(prompt, True)

        json_string = remove_first_last_lines_if_quoted(llm_output_json)
        
        try:
            output_json = json.loads(json_string)
        except Exception as e:
            logging.error(f"Fail to parse llm output as json, set output_json as empty, exception: {e}")
            output_json = {
                "name": file_path,
                "purpose": "Unknown",
                "classes": [],
                "functions": []
            }
        return output_json, tokens

    def generate_source_file_index(self, file, llm_output_json, tokens) -> SourceCodeIndex:
        absolute_file_path = os.path.join(self.project_dir, file)
        md5_hash, line_count = compute_md5_and_count_lines(absolute_file_path)

        try:
            classes = json.dumps(llm_output_json['classes'], ensure_ascii=False)
        except Exception as e:
            classes = "[]"

        try:
            functions = json.dumps(llm_output_json['functions'], ensure_ascii=False)
        except Exception as e:
            functions = "[]"

        # TODO: Make sure to get attributes from llm output json
        return SourceCodeIndex(file=file, lines=line_count, md5=md5_hash, 
                                name=llm_output_json['name'], purpose=llm_output_json['purpose'], 
                                classes=classes, functions=functions, tokens = tokens)

    def is_index_existed(self, file_path) -> bool:
        return self.db_util.row_exists(file_path)
    
    def create_index(self, file_path, programming_language="Unknown"):
        if self.is_index_existed(file_path):
            logging.warning("The index exists, skip creating.")
            return None
        else:
            return self.create_new_index(file_path, programming_language)
        
    def create_new_index(self, file_path, programming_language="Unknown"):
        logging.info(f"Try to create the index for {file_path}")
        absolute_file_path = os.path.join(self.project_dir, file_path)
        llm_output_json, tokens = self.llm_explain_code(programming_language, absolute_file_path)
        return self.generate_source_file_index(file_path, llm_output_json, tokens)


    def count_indexes_tokens(self) -> int:
        return self.db_util.count_all_tokens()


    def create_index_and_save(self, file_path, programming_language="Unknown") -> SourceCodeIndex:
        index = self.create_index(file_path, programming_language)
        if index != None:
            self.db_util.insert_index(index)
        return index

    def get_index(self, file_path):
        return self.db_util.select_row(file_path)

    def print_index(self, file_path):
        index = self.get_index(file_path)

        if index is None:
            logging.warning("Index does not exist.")
        else:
            index.print()
    
    def get_all_indexes(self):
        return self.db_util.select_all_rows()
    
    def print_index_diff(self, file_path):
        index = self.db_util.select_row(file_path)

        if index is None:
            logging.warning("Index does not exist.")
            return
        else:
            absolute_file_path = os.path.join(self.project_dir, file_path)
            md5_hash, line_count = compute_md5_and_count_lines(absolute_file_path)
            if index.md5 != md5_hash:
                logging.warning(f"The file has been changed and need to update index: {file_path}")
                logging.warning(f"There are lines of code changes(index vs current): {index.lines} vs {line_count}")
            else:
                logging.info(f"The file has not been changed and no index diff: {file_path}")

    def get_index_diff_files(self):
        index_diff_files = []
        indexes = self.get_all_indexes()

        for index in indexes:
            absolute_file_path = os.path.join(self.project_dir, index.file)
            md5_hash, line_count = compute_md5_and_count_lines(absolute_file_path)
            if index.md5 != md5_hash:
                index_diff_files.append(index.file)

        return index_diff_files


    def is_index_diff(self, file_path):
        index = self.get_index(file_path)

        absolute_file_path = os.path.join(self.project_dir, file_path)
        md5_hash, _ = compute_md5_and_count_lines(absolute_file_path)
        return index.md5 != md5_hash

    def update_index(self, file_path):
        if not self.is_index_existed(file_path):
            logging.warning(f"Index for {file_path} does not exist and skip updating.")
            return

        if self.is_index_diff(file_path):
            source_file_manager = SourceFileManager(self.project_dir)
            language = source_file_manager.get_language(file_path)

            new_index = self.create_new_index(file_path, language)
            self.db_util.update_index(new_index)


    def delete_index(self, file_path):
        logging.info(f"Try to delete the index of {file_path}")

        if not self.is_index_existed(file_path):
            logging.error(f"Index for {file_path} does not exist and skip deleting.")
            return
        self.db_util.delete_row(file_path)


    def get_related_files(self, user_query, max_file_count=10):
        file_reason_list = self.get_related_file_reason_list(user_query, max_file_count)
        return [file_reason["file"] for file_reason in file_reason_list]


    def get_related_file_reason_list(self, query, max_file_count=10):
        source_file_indexes = self.db_util.select_all_rows()
        
        system_message = self.prompt_util.get_related_source_files_prompt(source_file_indexes, max_file_count)

        llm_output_json, tokens = self.llm_util.call_llm_with_system_prompt(self.config_manager.litchi_config.Index.Model, system_message, query, True)

        json_string = remove_first_last_lines_if_quoted(llm_output_json)

        # TODO: Return the reason about files and query
        try:
            return json.loads(json_string)["related_files"]
        except:
            logging.error(f"Fail to parse the json: {json_string}")
            exit(-1)


    def chat_with_index_file(self, user_query, index_file):
        with open(index_file, 'r') as file:
            lines = file.readlines()
            # Strip the newline characters from each line
            files = [line.strip() for line in lines]

        return self.chat_with_file_list(user_query, files)

    def chat_with_file_list(self, query, index_file_list: List[str]):
        # Read source code from files
        file_content_list = [{"file": file, "content": read_file_content(os.path.join(self.project_dir, file))} for file in index_file_list]
        system_message = self.prompt_util.get_chat_source_files_prompt(query, file_content_list)
        self.llm_util.stream_call_llm_with_system_prompt(self.config_manager.litchi_config.Query.Model, system_message, query)


    def chat_with_searched_related_files(self, user_query):
        max_file_count = self.config_manager.litchi_config.Index.MaxRetrivalSize

        files = self.get_related_files(user_query, max_file_count)
        logging.info(f"Get the related index file: {files}")

        return self.chat_with_file_list(user_query, files)
    
    def stream_chat(self, prompt):
        prompt = self.prompt_util.add_output_language_to_prompt(prompt, self.config_manager.litchi_config.Query.Language)
        self.llm_util.stream_call_llm(prompt)
        
    
    def generate_source_file_index_name(self, source_file_path: str) -> str:
    
        dir_path = os.path.dirname(source_file_path)
        base_name = os.path.splitext(os.path.basename(source_file_path))[0]
        new_file_name = base_name + "_index.json"
        new_index_file_path = os.path.join(self.project_dir, dir_path, new_file_name)

        return new_index_file_path

    def copy_index_to_source_code(self, index: SourceCodeIndex):
        index_file_path = self.generate_source_file_index_name(index.file)
        try:        
            with open(index_file_path, 'w') as file:
                file.write(index.to_printable_json())
                logging.info(f"Content successfully written to {index_file_path}")
        except IOError as e:
            logging.error(f"An error occurred while writing to the file: {e}")

    def delete_index_from_source_code(self, index: SourceCodeIndex) -> None:
        index_file_path = self.generate_source_file_index_name(index.file)

        try:
            if os.path.isfile(index_file_path):
                os.remove(index_file_path)
                logging.info(f"Index file '{index_file_path}' has been deleted successfully.")
            else:
                logging.warning(f"No index file found at '{index_file_path}'.")
        except Exception as e:
            logging.error(f"An error occurred while trying to delete the file: {e}")
