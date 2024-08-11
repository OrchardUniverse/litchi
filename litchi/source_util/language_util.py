import os
import yaml

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




class LanguageUtil:
    def __init__(self) -> None:
        pass

    @staticmethod
    def generate_language_file_map(files):
        language_extensions = load_language_extensions('language_extensions.yaml')
        return classify_files_by_extension(files, language_extensions)

def main():
    language_extensions = load_language_extensions('language_extensions.yaml')
    
    # Replace with the list of file paths you want to classify
    files = [
        'a/b.java',
        'a/b.js',
        'foo.abc',
        'test.py',
        'main.cpp',
        'header.hpp',
        'example.c',
        'module.jsx',
        'unknown.xyz'
    ]
    
    classified_files = classify_files_by_extension(files, language_extensions)
    print(classified_files)
    

if __name__ == "__main__":
    main()