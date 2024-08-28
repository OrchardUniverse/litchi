import os
from jinja2 import Template
from pydantic import BaseModel

from ..config_util.litchi_config import LitchiConfigManager

class PromptUtil:

    def __init__(self, project_path: str = "./") -> None:
        self.config_manager = LitchiConfigManager(project_path)
        self.index_language = self.config_manager.litchi_config.Index.Language
        self.query_language = self.config_manager.litchi_config.Query.Language
        
    def append_output_language_prompt(self, prompt, language):
        return f"{prompt}\n\nMake sure all the output contents are in {language}."

    def analyse_source_file_prompt(self, programming_language, code):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_file = os.path.join(script_dir, "analyse_source_file.prompt")

        with open(prompt_file, 'r') as file:
            template_content = file.read()

        template = Template(template_content)
        params = {
            'programming_language': programming_language,
            'code': code
        }
        prompt = template.render(params)
        return self.append_output_language_prompt(prompt, self.index_language)

    def get_related_source_files_prompt(self, query, source_file_indexes, max_file_count):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_file = os.path.join(script_dir, "get_related_source_files.prompt")

        with open(prompt_file, 'r') as file:
            template_content = file.read()

        template = Template(template_content)
        params = {
            'query': query,
            'source_file_indexes': source_file_indexes,
            'max_file_count': max_file_count
        }
        prompt = template.render(params)
        return self.append_output_language_prompt(prompt, self.index_language)

    def chat_with_realted_source_files_prompt(self, query, file_content_list):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_file = os.path.join(script_dir, "chat_with_realted_source_files.prompt")

        with open(prompt_file, 'r') as file:
            template_content = file.read()

        template = Template(template_content)
        params = {
            'query': query,
            'file_content_list': file_content_list
        }
        prompt = template.render(params)
        return self.append_output_language_prompt(prompt, self.query_language)

    def chat_with_model(self, query):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_file = os.path.join(script_dir, "chat_with_model.prompt")

        with open(prompt_file, 'r') as file:
            template_content = file.read()

        template = Template(template_content)
        params = {
            'query': query
        }
        prompt = template.render(params)
        return self.append_output_language_prompt(prompt, self.query_language)
    
    def geneate_gencode_system_message(self, output_object: BaseModel, reference_filename="", language=""):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_file = os.path.join(script_dir, "gencode.prompt")

        os_info = self.config_manager.litchi_config.OS
        if reference_filename == "":
            reference_code = ""
        else:
            with open(reference_filename, 'r') as file:
                reference_code = file.read()
        if language == "":
            programming_language = self.config_manager.litchi_config.Query.ProgrammingLanguage
        else:
            programming_language = language

        params = {
            'operator_system_type': os_info.Type,
            'operator_system_version': os_info.Version,
            'operator_system_arch': os_info.Arch, 
            'reference_filename': reference_filename,
            'reference_code': reference_code,
            'programming_language': programming_language,
            'output_json': output_object.model_json_schema()
        }
    
        with open(prompt_file, 'r') as file:
            template_content = file.read()
            template = Template(template_content)
            return template.render(params)
            
    def geneate_optcode_system_message(self, reference_code=""):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_file = os.path.join(script_dir, "optcode.prompt")

        params = {
            'reference_code': reference_code
        }
    
        with open(prompt_file, 'r') as file:
            template_content = file.read()
            template = Template(template_content)
            return template.render(params)