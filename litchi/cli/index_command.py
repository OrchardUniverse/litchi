
from ..source_util.source_file_manager import SourceFileManager
from ..config_util.litchi_config import LitchiConfigManager
from ..index_util.index_manager import SourceFileIndexManager

def create_index(file_path, is_all):
    LitchiConfigManager.make_sure_in_project_path()

    if (file_path == None and is_all == False) or (file_path != None and is_all == True):
        print("Please specify a file path or use --all to create index for all files.")
        return
    
    source_file_manager = SourceFileManager()
    index_manager = SourceFileIndexManager()

    if file_path != None:
        language = source_file_manager.get_language(file_path)
        index_manager.create_index_and_save(file_path, language)
    else:
        file_count = source_file_manager.get_source_file_count()
        prompt = f"Are you sure to create index for {file_count} files? (yes/no): "
        response = input(prompt).strip().lower()
        if response in ['yes', 'y']:
            language_files_map = source_file_manager.get_language_files_map()
            for language, files in language_files_map.items():
                for file_name in files:
                    index_manager.create_index_and_save(file_name, language)
        else:
            print("Cancel creating index.")



def show_index(file_path, is_all):
    LitchiConfigManager.make_sure_in_project_path()

    if (file_path == None and is_all == False) or (file_path != None and is_all == True):
        print("Please specify a file path or use --all to create index for all files.")
        return
    
    index_manager = SourceFileIndexManager()

    if file_path != None:
        index = index_manager.get_index(file_path)
        if index == None:
            print(f"Index for {file_path} does not exist.")
        else:
            print(index)
    else:
        indexes = index_manager.get_all_indexes()
        for index in indexes:
            print(index)

def show_index_diff(file_path, is_all):
    LitchiConfigManager.make_sure_in_project_path()

    if (file_path == None and is_all == False) or (file_path != None and is_all == True):
        print("Please specify a file path or use --all to create index for all files.")
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
        print("Please specify a file path or use --all to create index for all files.")
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
        print("Please specify a file path or use --all to create index for all files.")
        return
    
    index_manager = SourceFileIndexManager()

    if file_path != None:
        index_manager.delete_index(file_path)
    else:
        indexes = index_manager.get_all_indexes()
        for index in indexes:
            index_manager.delete_index(index.file)

def query_indexes(user_query):
    LitchiConfigManager.make_sure_in_project_path()

    config_manager = LitchiConfigManager()
    max_retrival_size = config_manager.litchi_config.Index.MaxRetrivalSize

    index_manager = SourceFileIndexManager()

    file_reason_list = index_manager.get_related_file_reason_list(user_query, max_retrival_size)
    import ipdb;ipdb.set_trace()
    for file_reason_map in file_reason_list:
        print(f"File: {file_reason_map['file']}\nReason: {file_reason_map['reason']}")