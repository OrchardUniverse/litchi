
from ..source_util.source_file_manager import SourceFileManager
from ..config_util.litchi_config import LitchiConfigManager
from ..index_util.index_manager import SourceFileIndexManager


def chat(user_query, without_index):
    LitchiConfigManager.make_sure_in_project_path()

    if user_query == None or user_query == "":
        print("Please input a query to chat with indexes.")
        return

    if without_index:
        chat_without_indexes(user_query)
    else:
        chat_with_indexes(user_query)

def chat_with_indexes(user_query):
    index_manager = SourceFileIndexManager()
    print(index_manager.chat_with_related_files(user_query))

def chat_without_indexes(user_query):
    index_manager = SourceFileIndexManager()
    print(index_manager.chat_with_model(user_query))
