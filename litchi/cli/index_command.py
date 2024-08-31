from prettytable import PrettyTable
import os
import logging

from ..source_util.source_file_manager import SourceFileManager
from ..config_util.litchi_config import LitchiConfigManager
from ..index_util.index_manager import SourceFileIndexManager

def create_index(file_path, is_all):
    LitchiConfigManager.make_sure_in_project_path()

    if (file_path == None and is_all == False) or (file_path != None and is_all == True):
        logging.warming("Please specify a file path or use --all to create index for all files.")
        return
    
    source_file_manager = SourceFileManager()
    index_manager = SourceFileIndexManager()

    if file_path != None:
        language = source_file_manager.get_language(file_path)
        index = index_manager.create_index_and_save(file_path, language)
        if index != None:
            index.print()
            logging.info(f"Create index by consuming token: {index.tokens}")
    else:
        file_count = source_file_manager.get_source_file_count()
        prompt = f"Are you sure to create index for {file_count} files? (yes/no): "
        response = input(prompt).strip().lower()
        if response in ['yes', 'y']:
            language_files_map = source_file_manager.get_language_files_map()
            for language, files in language_files_map.items():
                for file_name in files:
                    index_manager.create_index_and_save(file_name, language)

            logging.info(f"Create all indexes by consuming token: {index_manager.count_indexes_tokens()}")
        else:
            logging.warning("Cancel creating index.")



def show_index(file_path, is_all):
    LitchiConfigManager.make_sure_in_project_path()

    if (file_path == None and is_all == False) or (file_path != None and is_all == True):
        logging.info.warming("Please specify a file path or use --all to create index for all files.")
        return
    
    index_manager = SourceFileIndexManager()

    if file_path != None:
        index_manager.print_index(file_path)
    else:
        indexes = index_manager.get_all_indexes()


        def truncate(text):
            max_length = 10
            if len(text) > max_length:
                return text[:max_length-3] + "..."  # Truncate and add ellipsis
            return text

        # Print the result in a table
        table = PrettyTable()
        table.field_names = ["File", "Lines", "Name", "Purpose"]
        for index in indexes:
            table.add_row([index.file, index.lines, index.name, truncate(index.purpose)])
        table.align = "l"
        print(table)

def show_index_diff(file_path, is_all):
    LitchiConfigManager.make_sure_in_project_path()

    if (file_path == None and is_all == False) or (file_path != None and is_all == True):
        logging.warning("Please specify a file path or use --all to create index for all files.")
        return
    
    index_manager = SourceFileIndexManager()

    if file_path != None:
        index_manager.print_index_diff(file_path)

    else:
        indexes = index_manager.get_all_indexes()
        for index in indexes:
            index_manager.print_index_diff(index.file)


def update_index(file_path, is_all):
    LitchiConfigManager.make_sure_in_project_path()

    if (file_path == None and is_all == False) or (file_path != None and is_all == True):
        logging.warning("Please specify a file path or use --all to create index for all files.")
        return
    
    index_manager = SourceFileIndexManager()

    if file_path != None:
        index_manager.update_index(file_path)
    else:
        indexes = index_manager.get_all_indexes()
        for index in indexes:
            index_manager.print_index_diff(index.file)

def delete_index(file_path, is_all):
    LitchiConfigManager.make_sure_in_project_path()

    if (file_path == None and is_all == False) or (file_path != None and is_all == True):
        logging.warning("Please specify a file path or use --all to create index for all files.")
        return
    
    index_manager = SourceFileIndexManager()

    if file_path != None:
        index_manager.delete_index(file_path)
    else:
        indexes = index_manager.get_all_indexes()
        for index in indexes:
            index_manager.delete_index(index.file)

def query_indexes(user_query, output_file: str =""):
    LitchiConfigManager.make_sure_in_project_path()

    # Check if file is valid
    if output_file and output_file != "":
        output_directory = os.path.dirname(output_file)
        if not os.path.exists(output_directory):
            logging.error(f"The directory {output_directory} does not exist.")
            return

    config_manager = LitchiConfigManager()
    max_retrival_size = config_manager.litchi_config.Index.MaxRetrivalSize

    index_manager = SourceFileIndexManager()

    file_reason_list = index_manager.get_related_file_reason_list(user_query, max_retrival_size)

    # Print the result in a table
    table = PrettyTable()
    table.field_names = ["File", "Reason"]
    for file_reason_map in file_reason_list:
        table.add_row([file_reason_map['file'], file_reason_map['reason']])

    print(table)

    if output_file and output_file != "":
        with open(output_file, 'w') as file:
            for file_reason_map in file_reason_list:
                file.write(file_reason_map["file"] + '\n')
        logging.info(f"Successfully saved {len(file_reason_list)} file names into {output_file}")


def copy_indexes_to_source_code():
    LitchiConfigManager.make_sure_in_project_path()

    index_manager = SourceFileIndexManager()
    indexes = index_manager.get_all_indexes()
    for index in indexes:
        index_manager.copy_index_to_source_code(index)


def delete_indexes_from_source_code():
    LitchiConfigManager.make_sure_in_project_path()

    index_manager = SourceFileIndexManager()
    indexes = index_manager.get_all_indexes()
    for index in indexes:
        index_manager.delete_index_from_source_code(index)
   