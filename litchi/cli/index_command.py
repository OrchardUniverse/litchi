
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
        index_manager.create_index(file_path, language)
    else:
        file_count = source_file_manager.get_source_file_count()
        prompt = f"Are you sure to create index for {file_count} files? (yes/no): "
        response = input(prompt).strip().lower()
        if response in ['yes', 'y']:
            language_files_map = source_file_manager.get_language_files_map()
            for language, files in language_files_map.items():
                for file_name in files:
                    index_manager.create_index(file_name, language)
        else:
            print("Cancel creating index.")


    