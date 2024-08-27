from ..config_util.litchi_config import LitchiConfigManager
from ..watcher_util.file_watcher import FileWatcher
def watch_file(file):
    file_watcher = FileWatcher(file)
    file_watcher.start_watching()


    