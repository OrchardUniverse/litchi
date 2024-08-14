
import yaml
import os
import shutil

from .file_util import FileUtil



def save_to_yaml(data, output_file):
    with open(output_file, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

def read_from_yaml(yaml_file):
    with open(yaml_file, 'r') as file:
        classified_files = yaml.safe_load(file)
        return classified_files
    
def print_language_and_file(yaml_file):
    classified_files = read_from_yaml(yaml_file)

    for language, files in classified_files.items():
        print(f"Language: {language}")
        for file_name in files:
            print(f"  - {file_name}")

def load_language_extensions(yaml_file):
    with open(yaml_file, 'r') as file:
        language_extensions = yaml.safe_load(file)
    return language_extensions

def classify_files_by_extension(files, language_extensions):
    classified_files = {}

    # Invert the language_extensions to map extensions to languages
    extension_to_language = {}
    for language, extensions in language_extensions.items():
        for extension in extensions:
            extension_to_language[extension] = language

    # Classify each file
    for file in files:
        _, ext = os.path.splitext(file)
        if ext in extension_to_language:
            language = extension_to_language[ext]
        else:
            #language = ext  # Use the extension itself as the key
            language = 'Unknown'  # Use 'unknown' for files with no known extension

        if language not in classified_files:
            classified_files[language] = []

        classified_files[language].append(file)

    return classified_files


def make_hashable(value):
    if isinstance(value, dict):
        return tuple((k, make_hashable(v)) for k, v in value.items())
    elif isinstance(value, list):
        return tuple(make_hashable(v) for v in value)
    else:
        return value
        

class SourceFileManager:
    def __init__(self, project_path: str = "./"):
        self.project_path = project_path
        self.litchi_path = os.path.join(project_path, ".litchi")
        self.source_file_path = os.path.join(self.litchi_path, 'source_files.yaml')
        self.setup_litchi_files()

    def setup_litchi_files(self):
        if not os.path.exists(self.litchi_path):
            os.makedirs(self.litchi_path)

        ignore_rules_yaml_file = 'ignore_rules.yaml'
        ignore_rules_yaml_path = os.path.join(self.litchi_path, ignore_rules_yaml_file)

        if not os.path.exists(ignore_rules_yaml_path):
            script_dir = os.path.dirname(os.path.abspath(__file__))
            default_ignore_rules_yaml_path = os.path.join(script_dir, ignore_rules_yaml_file)
            print(f"File ignore_rules.yaml does not exist, copy from {default_ignore_rules_yaml_path} to {ignore_rules_yaml_path}")
            shutil.copy(default_ignore_rules_yaml_path, ignore_rules_yaml_path)

        language_extensions_yaml_file = 'language_extensions.yaml'
        language_extensions_yaml_path = os.path.join(self.litchi_path, language_extensions_yaml_file)

        if not os.path.exists(language_extensions_yaml_path):
            script_dir = os.path.dirname(os.path.abspath(__file__))
            default_language_extensions_yaml_path = os.path.join(script_dir, language_extensions_yaml_file)
            print(f"File language_extensions.yaml does not exist, copy from {default_language_extensions_yaml_path} to {language_extensions_yaml_path}")
            shutil.copy(default_language_extensions_yaml_path, language_extensions_yaml_path)

    def generate_language_file_map(self, files):

        language_extensions_yaml_file = os.path.join(self.litchi_path, 'language_extensions.yaml')

        language_extensions = load_language_extensions(language_extensions_yaml_file)
        return classify_files_by_extension(files, language_extensions)


    def create_source_file_yaml(self):
        if os.path.exists(self.source_file_path):
            print(f"Source file yaml already exists in {self.source_file_path}, do not create again")
        else:
            self.update_source_file_yaml()

    def update_source_file_yaml(self):
        file_util = FileUtil(self.project_path)
        file_list = file_util.get_files()

        language_file_map = self.generate_language_file_map(file_list)

        print(f"Save the source file yaml in {self.source_file_path}")
        save_to_yaml(language_file_map, self.source_file_path)


    def print_language_and_file(self):
        classified_files = read_from_yaml(self.source_file_path)

        for language, files in classified_files.items():
            print(f"Language: {language}")
            for file_name in files:
                print(f"  - {file_name}")
    
    def get_language_files_map(self):
        file_util = FileUtil(self.project_path)
        file_list = file_util.get_files()
        language_file_map = self.generate_language_file_map(file_list)
        return language_file_map
    
    def print_source_file_diff(self):
        yaml1 = make_hashable(read_from_yaml(self.source_file_path))
        yaml2 = make_hashable(self.get_language_files_map())

        diff_output = []

        # Compare the two YAML objects
        if yaml1 != yaml2:
            set1 = set([yaml1]) if isinstance(yaml1, tuple) else set(make_hashable(yaml1))
            set2 = set([yaml2]) if isinstance(yaml2, tuple) else set(make_hashable(yaml2))


            diff1 = set1 - set2
            diff2 = set2 - set1

            for diff in diff1:
                diff_output.append(f"- {diff}")
            for diff in diff2:
                diff_output.append(f"+ {diff}")
        else:
            diff_output.append("The files are identical.")

        """ TODO: change to better display
        - (('Python', ('basket/cli.py', 'basket/openai_util/openai_util.py')),)
        + (('Python', ('basket/cli.py', 'basket/basket_config/auths_config.py', 'basket/basket_config/maas_config.py', 'basket/openai_util/openai_util.py')),)
        (tobepython)
        """
        for diff in diff_output:
            print(diff)
