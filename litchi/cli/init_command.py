import logging

from ..config_util.litchi_config import LitchiConfigManager

def init_project(project_path, language):
    config_manager = LitchiConfigManager(project_path)

    if config_manager.is_initialized():
        logging.warning("Project has been initialized. No need to initilize again.")
    else:
        if language is None or language == "":
            language = input("Please enter the language (default is 'English'): ") or "English"
        logging.info(f"Use the language '{language}' to initialize the config file.")
        config_manager.create_config_yaml(language)

    logging.info(f"Current litchi config in {config_manager.litchi_config_path}:")
    config_manager.print_config()


    