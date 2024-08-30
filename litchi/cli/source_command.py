
from ..source_util.source_file_manager import SourceFileManager
from ..config_util.litchi_config import LitchiConfigManager


def create_source_file():
    LitchiConfigManager.make_sure_in_project_path()
    
    source_file_manager = SourceFileManager()
    source_file_manager.create_source_file_yaml()
    print("Please check .litchi/source_file.yaml which contains all source files.")

def update_source_file():
    LitchiConfigManager.make_sure_in_project_path()

    source_file_manager = SourceFileManager()
    source_file_manager.update_source_file_yaml()
    print("Please check .litchi/source_file.yaml which contains all source files.")

def diff_from_source_file():
    LitchiConfigManager.make_sure_in_project_path()

    source_file_manager = SourceFileManager()
    source_file_manager.print_source_file_diff()
    