import logging
import getpass
import os
from ..config_util.litchi_config import LitchiConfigManager

def init_project(project_path, language):
    config_manager = LitchiConfigManager(project_path)

    if config_manager.is_initialized():
        logging.warning("Project has been initialized. No need to initilize again.")
    else:
        if language is None or language == "":
            language = input("Please enter the language (default is 'English'): ") or "English"
        logging.info(f"Use the language '{language}' to initialize the config file.")
        
        if os.environ.get("OPENAI_BASE_URL") and os.environ.get("OPENAI_API_KEY"):
            base_url = os.environ.get("OPENAI_BASE_URL")
            api_key = os.environ.get("OPENAI_API_KEY")
            config_manager.create_config_yaml(base_url, api_key, language)
        else:
            is_init_apikey = input("Do you want to initialize the API key for LLM? ").strip().lower()
            if is_init_apikey in ['y', 'yes']:
                base_url = input("Please enter the model base url (default is 'https://api.gptsapi.net/v1'): ") or "https://api.gptsapi.net/v1"
                api_key = getpass.getpass("Please enter your API key: ")
                print("API key initialized successfully.")
                config_manager.create_config_yaml(base_url, api_key, language)
            else:
                config_manager.create_config_yaml_without_apikey(language)

    logging.info(f"Current litchi config in {config_manager.litchi_config_path}:")
    config_manager.print_config()


    