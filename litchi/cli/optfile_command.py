import os
import tempfile
import logging

from .common_util import CommandCommonUtil
from ..config_util.litchi_config import LitchiConfigManager
from ..index_util.llm_util import LlmUtil


def optimize_file(file, query_or_file, inplace, dry_run):
    LitchiConfigManager.make_sure_in_project_path()

    llm_util = LlmUtil()
    query = CommandCommonUtil.extract_query(query_or_file)
    optimized_code = llm_util.llm_optimize_file(file, query)

    if inplace:
        with open(file, 'r+') as f:
            with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_file:
                temp_file.write(f.read())
                logging.info(f"Backup original file into: {temp_file.name}")
        
            f.write(optimized_code)
        logging.info(f"Optimized file and saved into {file}")
    elif dry_run:
        logging.info(optimized_code)
    else:
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_file:
            temp_file.write(optimized_code)
            temp_file_name = temp_file.name
        logging.info(f"Optimized file and saved into {temp_file_name}")

        diff_command = f"git diff {file} {temp_file_name}"
        logging.info(f"Try to run diff command: {diff_command}")
        os.system(diff_command)

        response = input("Do you want to overwrite with diff file? (yes/no): ")
        response = response.strip().lower()
        if response in ['yes', 'y']:
            with open(file, 'r+') as opened_file:
                with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_file:
                    temp_file.write(opened_file.read())
                    logging.info(f"Backup original file into: {temp_file.name}")
            
                opened_file.write(optimized_code)
            logging.info(f"The file '{file}' has been overwritten with the optimized code.")
        else:
            logging.info(f"Do not overwrite file and you can find optimized code in {temp_file_name}.")

