from ..config_util.litchi_config import LitchiConfigManager
from ..watcher_util.file_watcher import FileWatcher
def watch_file(requirement_file):
    LitchiConfigManager.make_sure_in_project_path()

    file_watcher = FileWatcher(requirement_file)
    file_watcher.start_watching()


    