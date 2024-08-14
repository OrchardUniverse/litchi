import os

from index_util.index_manager import SourceFileIndexManager
from source_util.source_file_manager import SourceFileManager

def main():
    project_path = "/Users/tobe/code/orchard_universe/basket"

    source_file_manager = SourceFileManager(project_path)
    index_manager = SourceFileIndexManager(project_path)

    """
    # Step1: Generate source file
    source_file_manager.generate_source_file_yaml()

    # Step2: Read source file and generate index
    
    language_files_map = source_file_manager.get_language_files_map()

    for language, files in language_files_map.items():
        for file_name in files:
            index_manager.create_index(file_name, language)
    

    # Step3: Get related files
    user_query = "How to set llm model in cli?"
    llm_output_map = index_manager.get_related_files(user_query, 1)
    files = llm_output_map["files"]
    print(files)
    """

    # Step4: Chat with related files
    user_query = "这个项目是用什么编程语言实现的？"
    print(index_manager.chat_with_related_files(user_query, 1))

    

    

if __name__ == "__main__":
    main()