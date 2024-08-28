import os
import tempfile

from .common_util import CommandCommonUtil
from ..config_util.litchi_config import LitchiConfigManager
from ..index_util.llm_util import LlmUtil


def optimize_code(file, query_or_file, inplace, dry_run):
    LitchiConfigManager.make_sure_in_project_path()

    llm_util = LlmUtil()
    query = CommandCommonUtil.extract_query(query_or_file)
    optimized_code = llm_util.llm_optimize_code(file, query)

    if inplace:
        with open(file, 'w') as f:
            f.write(optimized_code)
        print(f"Optimized code and saved into {file}")
    elif dry_run:
        print(optimized_code)
    else:
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_file:
            temp_file.write(optimized_code)
            temp_file_name = temp_file.name
        print(f"Optimized code and saved into {temp_file_name}")

        diff_command = f"git diff {file} {temp_file_name}"
        print(f"Try to run diff command: {diff_command}")
        os.system(diff_command)

        response = input("Do you want to overwrite with diff file? (yes/no): ")
        response = response.strip().lower()
        if response in ['yes', 'y']:
            with open(file, 'w') as opened_file:
                opened_file.write(optimized_code)
            print(f"The file '{file}' has been overwritten with the optimized code.")
        else:
            print(f"Do not overwrite source file and you can find optimized code in {temp_file_name}.")

