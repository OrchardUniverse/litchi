from prettytable import PrettyTable
import os

from ..source_util.source_file_manager import SourceFileManager
from ..config_util.litchi_config import LitchiConfigManager
from ..index_util.index_manager import SourceFileIndexManager
from ..index_util.llm_util import LlmUtil

def generate_source_file(query, file: str = ""):
    LitchiConfigManager.make_sure_in_project_path()

    llm_util = LlmUtil()
    gencode_output = llm_util.call_llm_to_gencode(query, file)

    try:
        with open(gencode_output.output_file, 'w') as file:
            file.write(gencode_output.code)
            print(f"Generate code and write to {gencode_output.output_file}")
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")


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
