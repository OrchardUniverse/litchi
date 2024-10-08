import os
from typing import List
import yaml
import shutil

def load_ignore_rules(yaml_file):
    with open(yaml_file, 'r') as file:
        ignore_rules = yaml.safe_load(file)
    return ignore_rules

def load_gitignore_rules(gitignore_file):
    ignore_patterns = []
    if os.path.exists(gitignore_file):
        with open(gitignore_file, 'r') as file:
            ignore_patterns = [line.strip() for line in file if line.strip() and not line.startswith('#')]
    return ignore_patterns

def should_ignore(path, ignore_rules, gitignore_patterns):
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

    # Check against .gitignore patterns
    for pattern in gitignore_patterns:
        if matches_pattern(path, pattern):
            return True

    return False

def matches_pattern(path, pattern):
    # Basic handling of .gitignore patterns
    if pattern.endswith('/'):  # Ignore directory
        return os.path.isdir(path) and path.endswith(pattern.rstrip('/'))
    if pattern.startswith('/'):  # Match from root
        return os.path.normpath(path).startswith(pattern.lstrip('/'))
    return os.path.basename(path) == pattern or pattern in path

def list_files(directory, ignore_rules, gitignore_patterns):
    result_files = []
    for root, dirs, files in os.walk(directory):
        # Filter directories in-place
        dirs[:] = [d for d in dirs if not should_ignore(os.path.join(root, d), ignore_rules, gitignore_patterns)]
        for file in files:
            # Absolute file path
            file_path = os.path.join(root, file)
            if not should_ignore(file_path, ignore_rules, gitignore_patterns):
                # Relative path to return
                relative_path = os.path.relpath(file_path, directory)
                result_files.append(relative_path)
    return result_files

class FileUtil:
    def __init__(self, project_path) -> None:
        self.project_path = project_path
        self.litchi_path = os.path.join(project_path, ".litchi")

    def get_files(self) -> List[str]:
        if os.path.exists(os.path.join(self.project_path, '.gitignore')):
            yaml_file_path = os.path.join(self.litchi_path, 'ignore_rules.yaml')
            ignore_rules = load_ignore_rules(yaml_file_path)
        else:
            ignore_rules = {
                'directories': [],
                'directory_prefix': [],
                'directory_posfix': [],
                'files': [],
                'file_prefix': [],
                'file_posfix': []
            }

        if os.path.exists(os.path.join(self.project_path, '.gitignore')):
            gitignore_patterns = load_gitignore_rules('.gitignore')
        else:
            gitignore_patterns = []
        
        files = list_files(self.project_path, ignore_rules, gitignore_patterns)
        return files

