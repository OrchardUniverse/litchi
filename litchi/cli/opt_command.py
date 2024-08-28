from prettytable import PrettyTable
import tempfile
import os

from ..source_util.source_file_manager import SourceFileManager
from ..config_util.litchi_config import LitchiConfigManager
from ..index_util.index_manager import SourceFileIndexManager
from ..index_util.llm_util import LlmUtil

def optimize_code(file, query, inplace, diff):
    LitchiConfigManager.make_sure_in_project_path()

    llm_util = LlmUtil()
    optimized_code = llm_util.llm_optimize_code(file, query)

    print(optimized_code)
    if inplace:
        with open(file, 'w') as f:
            f.write(optimized_code)
        print(f"Optimized code and saved into {file}")
    elif diff:

        with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_file:
            temp_file.write(optimized_code)
            temp_file_name = temp_file.name
            print(f"Optimized code and saved into {temp_file_name}")
            
        diff_commnd = f"git diff {file} {temp_file_name}"
        print(f"Try to run diff command: {diff_commnd}")
        os.system(diff_commnd)


        response = input("Do you want to overwrite with diff file? (yes/no): ").strip().lower()
        if response in ['yes', 'y']:
            with open(file, 'w') as opened_file:
                opened_file.write(optimized_code)
            print(f"The file '{file}' has been overwritten with the optimized code.")
        else:
            print(f"Do not overwrite source file and you can find optmized code in {temp_file_name}.")



def generate_source_file(query_or_file, file: str = "", should_run: bool = False, language: str = ""):
    LitchiConfigManager.make_sure_in_project_path()

    if query_or_file.lower().endswith(".txt"):
        query = open(query_or_file, "r").read()
        print(f"Read the requiremtn file in {query_or_file} to get actual querty:\n{query}")
    else:
        query = query_or_file

    llm_util = LlmUtil()
    gencode_output = llm_util.call_llm_to_gencode(query, file, language)

    try:
        with open(gencode_output.output_file, 'w') as file:
            file.write(gencode_output.code)
            print(f"Generate code and write to {gencode_output.output_file}")
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")

    if should_run:
        run_generated_file(gencode_output.output_file)


def run_generated_file(filename: str):
    
    if filename.lower().endswith(".sh"):
        command = f"bash {filename}"
    elif filename.lower().endswith(".py"):
        command = f"python {filename}"
    else:
        print("Error: only support for python and bash script")
        return

    print(f"Try to run generated file with command: {command}")
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
