from typing import Optional
from pydantic import BaseModel
import yaml
import platform
import os
import json

class OS(BaseModel):
    Type: str
    Version: str
    Arch: str

class LLM(BaseModel):
    BaseUrl: str
    ApiKey: str

class Index(BaseModel):
    Lanauage: str
    Model: str
    MaxRetrivalSize: int
    RetrivalMethod: str

class Query(BaseModel):
    Lanauage: str
    Model: str

class LitchiConfig(BaseModel):
    OS: OS
    LLM: LLM
    Index: Index
    Query: Query

def create_litchi_config(os_data: dict, llm_data: dict, index_data: dict, query_data: dict) -> LitchiConfig:
    os = OS(**os_data)
    llm = LLM(**llm_data)
    index = Index(**index_data)
    query = Query(**query_data)
    config = LitchiConfig(OS=os, LLM=llm, Index=index, Query=query)
    return config


def get_os_info() -> dict:
    """
    Retrieves the operating system's name, version, and architecture.

    :return: A dictionary containing the OS name, version, and architecture.
    """
    os_info = {
        "Type": platform.system(),
        "Version": platform.release(),
        "Arch": platform.machine()
    }

    return os_info

def create_default_litchi_config(language: str = "English") -> LitchiConfig:
    os_data = get_os_info()

    llm_data = {
        "BaseUrl": "https://api.openai.com",
        "ApiKey": "your-api-key"
    }
    index_data = {
        "Lanauage": language,
        "Model": "gpt-3.5-turbo-1106",
        "MaxRetrivalSize": 3,
        "RetrivalMethod": "LLM"
    }
    query_data = {
        "Lanauage": language,
        "Model": "gpt-3.5-turbo-1106"
    }
    return create_litchi_config(os_data, llm_data, index_data, query_data)


def save_config_to_yaml(litchi_config: LitchiConfig, file_path: str):
    config_dict = litchi_config.dict()

    try:
        with open(file_path, 'w') as yaml_file:
            yaml.dump(config_dict, yaml_file, default_flow_style=False)
        print(f"Save litchi config to {file_path}")
    except Exception as e:
        print(f"Error saving config to YAML file: {e}")



class LitchiConfigManager:
    def __init__(self, project_path: str = "./") -> None:
        self.litchi_path = os.path.join(project_path, ".litchi")
        self.litchi_config_path = os.path.join(self.litchi_path, "litchi.yaml")
        if not os.path.exists(self.litchi_path):
            os.makedirs(self.litchi_path)

        if self.is_initialized():
            with open(self.litchi_config_path, 'r') as file:
                yaml_content = yaml.safe_load(file)
                self.litchi_config = LitchiConfig(**yaml_content)
        else:
            self.litchi_config = None
    
    def is_initialized(self) -> bool:
        return os.path.exists(self.litchi_config_path)
    
    def create_config_yaml(self, language: str = "English"):
        if self.is_initialized():
            print("Litchi config already exists. Skip creating.")
        else:        
            self.litchi_config = create_default_litchi_config(language)
            save_config_to_yaml(self.litchi_config, self.litchi_config_path)


    def print_config(self):
        print(self.litchi_config.json(indent=4))

    @staticmethod
    def is_in_project_path() -> bool:
        return os.path.exists("./.litchi/")
    
    @staticmethod
    def make_sure_in_project_path():
        if LitchiConfigManager.is_in_project_path():
            pass
        else:
            print("Current not in a litchi project path, please cd to project root path or using litchi init.")
            exit(-1)


if __name__ == "__main__":
    config_manager = LitchiConfigManager("/Users/tobe/code/orchard_universe/basket/")
    config_manager.print_config()