import os
from jinja2 import Template

def generate_prompt(programming_language, code):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_file = os.path.join(script_dir, "analyse_source_file.prompt")

    with open(prompt_file, 'r') as file:
        template_content = file.read()

    template = Template(template_content)
    params = {
        'programming_language': programming_language,
        'code': code
    }
    return template.render(params)

def generate_get_related_source_files_prompt(query, source_file_indexes, max_file_count):
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
    return template.render(params)

def generate_chat_with_realted_source_files_prompt(query, file_content_list):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_file = os.path.join(script_dir, "chat_with_realted_source_files.prompt")

    with open(prompt_file, 'r') as file:
        template_content = file.read()

    template = Template(template_content)
    params = {
        'query': query,
        'file_content_list': file_content_list
    }
    return template.render(params)
