import os
from openai import OpenAI

from ..config_util.litchi_config import LitchiConfigManager

class LlmUtil:

    def __init__(self, project_path: str = "./") -> None:
        config_manager = LitchiConfigManager(project_path)

        self.base_url = config_manager.litchi_config.LLM.BaseUrl
        self.api_key = config_manager.litchi_config.LLM.ApiKey
        self.index_model = config_manager.litchi_config.Index.Model
        self.query_model = config_manager.litchi_config.Query.Model

    def chat_with_llm(self, user_prompt):

        client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )

        completion = client.chat.completions.create(
            #model="gpt-4-1106-preview",
            model=self.index_model,
            messages=[
                {"role": "system", "content": "As a professional programming expert, analyze the given source code file. Your goal is to thoroughly understand the content and purpose of the code. Your response should be in JSON format."},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
        )

        json_string = completion.choices[0].message.content
        tokens = completion.usage.total_tokens

        # print(f"LLM request:\n {user_prompt}")
        # print(f"LLM response:\n {completion}")

        return json_string, tokens

    def adhoc_chat_with_llm(self, user_prompt):
        client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )

        completion = client.chat.completions.create(
            model=self.query_model,
            messages=[
                {"role": "system", "content": "You are a helpful assitant. You are good at programming and understand the given source code. Your goal is to understand user's query and provide reasonable and understandable response."},
                #  Please always response in Chinese.
                {"role": "user", "content": user_prompt}
            ]
        )

        json_string = completion.choices[0].message.content
        tokens = completion.usage.total_tokens

        # TODO: enable for debug log
        # print(f"LLM request:\n {user_prompt}")
        # print(f"LLM response:\n {completion}")

        return json_string, tokens
        
