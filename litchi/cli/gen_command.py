from prettytable import PrettyTable
import os
import logging

from ..source_util.source_file_manager import SourceFileManager
from ..config_util.litchi_config import LitchiConfigManager
from ..index_util.index_manager import SourceFileIndexManager
from ..index_util.llm_util import LlmUtil
from .common_util import CommandCommonUtil

def generate_source_file(query_or_file, file: str = "", files: str = "", should_run: bool = False, language: str = ""):
    LitchiConfigManager.make_sure_in_project_path()

    query = CommandCommonUtil.extract_query(query_or_file)

    llm_util = LlmUtil()
    gen_output = llm_util.call_llm_to_gencode(query, file, files, language)

    if gen_output.output_file == "":
        logging.error("Error: output file path is empty.")
        return ""
    else:
        logging.info(f"Generate file path: {gen_output.output_file}")

    try:
        # Create directory if not exists
        directory = os.path.dirname(gen_output.output_file)
        if directory != "" and not os.path.exists(directory):
            os.makedirs(directory)
            logging.info(f"Create directory {directory} before writing to the file")

        with open(gen_output.output_file, 'w') as file:
            file.write(gen_output.content)
            logging.info(f"Generate content and write to {gen_output.output_file}")
    except Exception as e:
        logging.error(f"An error occurred while writing to the file: {e}")
        return

    if should_run:
        run_generated_file(gen_output.output_file)


def run_generated_file(filename: str):
    
    if filename.lower().endswith(".sh"):
        command = f"bash {filename}"
    elif filename.lower().endswith(".py"):
        command = f"python {filename}"
    else:
        logging.error("Only support for python and bash script")
        return

    logging.info(f"Try to run generated file with command: {command}")
    os.system(command)


def generate_ut():
    pass

def implment_todo():
    pass

def generate_document():
    pass

def generate_sdk_document():
    pass

def generate_usecase():
    pass

def add_annotation():
    pass

def brain_strom():
    pass

def refactor_code():
    pass

def format_code():
    pass

def optmize_code():
    pass


def run_script():
    pass

def review_patch():
    pass

def generate_cicd_config():
    pass

def find_bug():
    pass

def inspect_code():
    pass

def generate_prompt():
    pass

def generate_test_data():
    pass
