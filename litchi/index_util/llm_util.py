import os
from openai import OpenAI
from pydantic import BaseModel, Field

from ..config_util.litchi_config import LitchiConfigManager
from . import prompt_util

class GencodeOutput(BaseModel):
    output_file: str = Field(description="The output file name.")
    code: str = Field(description="The generated code.")

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
    


    def call_llm_to_gencode(self, prompt, reference_file=""):
        client = self.create_openai_client()

        json_mode_supported_models = ["gpt-4-1106-preview", "gpt-3.5-turbo-1106"]
        if self.query_model in json_mode_supported_models:
            response_format = {"type": "json_object"}
        else:
            response_format = None

        output_object = GencodeOutput(output_file="", code="")
        system_message = self.prompt_util.geneate_gencode_system_message(output_object, reference_file)

        completion = client.chat.completions.create(
            model=self.index_model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            response_format=response_format,
            timeout=self.timeout
        )


        llm_output_string = completion.choices[0].message.content


        # TODO: add debug log
        print(f"LLM system message:\n {system_message}")
        print(f"LLM response:\n {llm_output_string}")

        try:
            output_object = GencodeOutput.model_validate_json(remove_first_last_lines_if_quoted(llm_output_string))
        except:
            print("Error: failed to parse the response to GencodeOutput.")

        return output_object
    
    def call_llm(self, prompt, is_json_mode: bool = False):
        client = self.create_openai_client()

        json_mode_supported_models = ["gpt-4-1106-preview", "gpt-3.5-turbo-1106"]
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
                print(f"Warning, you should use json mode supported models in {json_mode_supported_models}")
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

        # TODO: add debug log
        # print(f"LLM request:\n {user_prompt}")
        # print(f"LLM response:\n {completion}")

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