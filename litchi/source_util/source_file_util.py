
import yaml

from file_util import FileUtil

from language_util import LanguageUtil

def save_to_yaml(data, output_file):
    with open(output_file, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

def main():
    file_util = FileUtil("/Users/tobe/code/orchard_universe/basket/")
    file_list = file_util.get_files()

    language_file_map = LanguageUtil.generate_language_file_map(file_list)
    
    # Save the output to a YAML file
    output_yaml = 'source_files.yaml'
    save_to_yaml(language_file_map, output_yaml)

if __name__ == '__main__':
    main()