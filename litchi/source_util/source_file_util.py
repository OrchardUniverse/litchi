
import yaml

from file_util import FileUtil

from language_util import LanguageUtil

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

def main():
    file_util = FileUtil("/Users/tobe/code/orchard_universe/basket/")
    file_list = file_util.get_files()

    language_file_map = LanguageUtil.generate_language_file_map(file_list)
    
    # Save the output to a YAML file
    output_yaml = 'source_files.yaml'
    save_to_yaml(language_file_map, output_yaml)

if __name__ == '__main__':
    main()