import os
from jinja2 import Template
from pydantic import BaseModel

from ..config_util.litchi_config import LitchiConfigManager

class PromptUtil:

    def __init__(self, project_path: str = "./") -> None:
        self.config_manager = LitchiConfigManager(project_path)
        self.index_language = self.config_manager.litchi_config.Index.Language
        self.query_language = self.config_manager.litchi_config.Query.Language
        
    def add_output_language_to_prompt(self, language, prompt):
        return f"{prompt}\n\nMake sure all the output contents are in {language}."

    def render_local_template(self, local_file, params):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        template_file = os.path.join(current_dir, local_file)

        with open(template_file, 'r') as file:
            template = Template(file.read())
            return template.render(params)
    
    def get_analyse_code_prompt(self, programming_language, code):
        params = {
            'programming_language': programming_language,
            'code': code
        }
        prompt = self.render_local_template("analyse_source_file.prompt", params)
        return self.add_output_language_to_prompt(self.index_language, prompt)

    def get_related_source_files_prompt(self, source_file_indexes, max_file_count):
        params = {
            'source_file_indexes': source_file_indexes,
            'max_file_count': max_file_count
        }
        prompt = self.render_local_template("get_related_source_files.prompt", params)
        return self.add_output_language_to_prompt(self.index_language, prompt)

    def get_chat_source_files_prompt(self, query, file_content_list):
        params = {
            'query': query,
            'file_content_list': file_content_list
        }
        prompt = self.render_local_template("chat_with_realted_source_files.prompt", params)
        return self.add_output_language_to_prompt(self.query_language, prompt)


    def get_gencode_prompt(self, output_object: BaseModel, reference_filename="", reference_files="", language=""):
        os_info = self.config_manager.litchi_config.OS
        
        reference_source_codes = []

        if reference_filename and reference_filename != "":
            with open(reference_filename, 'r') as file:
                reference_source_codes.append({"name": reference_filename, "code": file.read()})
        elif reference_files and reference_files != "":
            with open(reference_files, 'r') as file:
                lines = file.readlines()
                filenames = [line.strip() for line in lines]
                for filename in filenames:
                    with open(filename, 'r') as file:
                        reference_source_codes.append({"name": filename, "code": file.read()})
        
        if language == "":
            programming_language = self.config_manager.litchi_config.Query.ProgrammingLanguage
        else:
            programming_language = language

        params = {
            'operator_system_type': os_info.Type,
            'operator_system_version': os_info.Version,
            'operator_system_arch': os_info.Arch,
            'reference_source_codes': reference_source_codes,
            'programming_language': programming_language,
            'output_json': output_object.model_json_schema()
        }
        prompt = self.render_local_template("gencode.prompt", params)
        return self.add_output_language_to_prompt(self.query_language, prompt)
            
    def get_optcode_prompt(self, reference_code):
        params = {
            'reference_code': reference_code
        }
        prompt = self.render_local_template("optcode.prompt", params)
        return prompt

    def get_optfile_prompt(self, content):
        params = {
            'content': content
        }
        prompt = self.render_local_template("optfile.prompt", params)
        return prompt