import os
from typing import List
from collections import defaultdict
import yaml

import os
import yaml

def load_ignore_rules(yaml_file):
    with open(yaml_file, 'r') as file:
        ignore_rules = yaml.safe_load(file)
    return ignore_rules

def should_ignore(path, ignore_rules):
    # Check directories
    if os.path.isdir(path):
        dir_name = os.path.basename(path)
        if dir_name in ignore_rules['directories']:
            return True
        for prefix in ignore_rules['directory_prefix']:
            if dir_name.startswith(prefix):
                return True
        for posfix in ignore_rules['directory_posfix']:
            if dir_name.endswith(posfix):
                return True

    # Check files
    if os.path.isfile(path):
        file_name = os.path.basename(path)
        if file_name in ignore_rules['files']:
            return True
        for prefix in ignore_rules['file_prefix']:
            if file_name.startswith(prefix):
                return True
        for posfix in ignore_rules['file_posfix']:
            if file_name.endswith(posfix):
                return True

    # Ignore hidden files or directories (starting with a dot)
    if os.path.basename(path).startswith('.'):
        return True

    return False

def list_files(directory, ignore_rules):
    result_files = []
    for root, dirs, files in os.walk(directory):
        # Filter directories in-place
        dirs[:] = [d for d in dirs if not should_ignore(os.path.join(root, d), ignore_rules)]
        for file in files:
            file_path = os.path.join(root, file)
            if not should_ignore(file_path, ignore_rules):
                result_files.append(file_path)
    return result_files

def main():
    ignore_rules = load_ignore_rules('ignore_rules.yaml')
    directory = "/Users/tobe/code/orchard_universe/basket/"
    files = list_files(directory, ignore_rules)
    
    for file in files:
        print(file)

if __name__ == "__main__":
    main()


