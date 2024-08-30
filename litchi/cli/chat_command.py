
from ..source_util.source_file_manager import SourceFileManager
from ..config_util.litchi_config import LitchiConfigManager
from ..index_util.index_manager import SourceFileIndexManager


def chat(query:str, file:str = "", files:str = "", with_index:bool = False):
    LitchiConfigManager.make_sure_in_project_path()

    if query == None or query == "":
        print("Please input a query to chat with indexes.")
        return

    if with_index:
        chat_with_indexes(query)
    elif file and file != "":
        chat_with_single_file(query, file)
    elif files and files != "":
        chat_with_index_file(query, files)
    else:
        chat_without_index(query)

def chat_with_indexes(query):
    index_manager = SourceFileIndexManager()
    print(index_manager.chat_with_searched_related_files(query))

def chat_with_index_file(query, index_file):
    index_manager = SourceFileIndexManager()
    index_manager.chat_with_index_file(query, index_file)

def chat_with_single_file(query, index_file):
    index_manager = SourceFileIndexManager()
    index_manager.chat_with_file(query, index_file)

def chat_without_index(query):
    index_manager = SourceFileIndexManager()
    index_manager.stream_chat(query)
