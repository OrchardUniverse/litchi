import os
from openai import OpenAI
from pydantic import BaseModel, Field
import logging

from ..config_util.litchi_config import LitchiConfigManager
from ..prompt_util import prompt_util

json_mode_supported_models = ["gpt-4-1106-preview", "gpt-3.5-turbo-1106"]

class GenOutput(BaseModel):
    output_file: str = Field(description="The output file name.")
    content: str = Field(description="The content of generated file.")

def remove_first_last_lines_if_quoted(text):
    lines = text.splitlines()
    if len(lines) >= 2 and lines[0].strip().startswith("```") and lines[-1].strip().startswith("```"):
        return '\n'.join(lines[1:-1])
    return text


class LlmUtil:

    def __init__(self, project_path: str = "./") -> None:
        config_manager = LitchiConfigManager(project_path)

        self.prompt_util = prompt_util.PromptUtil(project_path)

        self.base_url = config_manager.litchi_config.LLM.BaseUrl
        self.api_key = config_manager.litchi_config.LLM.ApiKey
        self.timeout = config_manager.litchi_config.LLM.Timeout
        self.index_model = config_manager.litchi_config.Index.Model
        self.query_model = config_manager.litchi_config.Query.Model

    def create_openai_client(self):
        client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )
        return client
    

    def call_llm_to_gencode(self, prompt, reference_file="", reference_files="", language=""):
        client = self.create_openai_client()

        if self.query_model in json_mode_supported_models:
            response_format = {"type": "json_object"}
        else:
            response_format = None

        output_object = GenOutput(output_file="", content="")

        system_message = self.prompt_util.get_gencode_prompt(output_object, reference_file, reference_files, language)

        completion = client.chat.completions.create(
            model=self.query_model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            response_format=response_format,
            timeout=self.timeout
        )

        llm_output_string = completion.choices[0].message.content

        try:
            output_object = GenOutput.model_validate_json(remove_first_last_lines_if_quoted(llm_output_string))
        except:
            logging.error("Error: failed to parse the response to GenOutput.")
            logging.error(f"LLM system message:\n {system_message}")
            logging.error(f"LLM response:\n {llm_output_string}")

        return output_object


    def llm_optimize_code(self, file, prompt):
        client = self.create_openai_client()

        with open(file, 'r') as file:
            reference_code = file.read()

        system_message = self.prompt_util.get_optcode_prompt(reference_code)

        completion = client.chat.completions.create(
            model=self.query_model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            timeout=self.timeout
        )

        llm_output_string = completion.choices[0].message.content

        return remove_first_last_lines_if_quoted(llm_output_string)

    def llm_optimize_file(self, file, prompt):
        client = self.create_openai_client()

        with open(file, 'r') as file:
            content = file.read()

        system_message = self.prompt_util.get_optfile_prompt(content)

        completion = client.chat.completions.create(
            model=self.query_model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            timeout=self.timeout
        )

        llm_output_string = completion.choices[0].message.content
        return llm_output_string

    def call_llm_with_system_prompt(self, model, system_message, prompt, is_json_mode: bool = False):
        client = self.create_openai_client()

        if is_json_mode and (model in json_mode_supported_models):
            response_format={"type": "json_object"}
        else:
            response_format={},

        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            response_format=response_format,
            timeout=self.timeout
        )

        output_string = completion.choices[0].message.content
        tokens = completion.usage.total_tokens

        return output_string, tokens
    

    def stream_call_llm_with_system_prompt(self, model, system_message, prompt):
        client = self.create_openai_client()

        stream = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            stream=True,
            timeout=self.timeout
        )

        for chunk in stream:
            # Print result in stdout
            print(chunk.choices[0].delta.content or "", end="")


    def call_llm(self, prompt, is_json_mode: bool = False):
        client = self.create_openai_client()

        if is_json_mode:
            if self.index_model in json_mode_supported_models:
                completion = client.chat.completions.create(
                    model=self.index_model,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    timeout=self.timeout
                )
            else:
                logging.warning(f"You should use json mode supported models in {json_mode_supported_models}")
                completion = client.chat.completions.create(
                model=self.index_model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                timeout=self.timeout
            )
        else:
            completion = client.chat.completions.create(
                model=self.index_model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                timeout=self.timeout
            )

        output_string = completion.choices[0].message.content
        tokens = completion.usage.total_tokens
        return output_string, tokens


    def stream_call_llm(self, prompt) -> None:
        client = self.create_openai_client()

        stream = client.chat.completions.create(
            model=self.query_model,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
            timeout=self.timeout
        )

        for chunk in stream:
            # Print result in stdout
            print(chunk.choices[0].delta.content or "", end="")
        
        return