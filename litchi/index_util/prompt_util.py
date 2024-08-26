import os
from jinja2 import Template

from ..config_util.litchi_config import LitchiConfigManager

class PromptUtil:

    def __init__(self, project_path: str = "./") -> None:
        config_manager = LitchiConfigManager(project_path)
        self.index_language = config_manager.litchi_config.Index.Language
        self.query_language = config_manager.litchi_config.Query.Language
        
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