
import openai
from openai import OpenAI
import os
import json
import sqlite3

def read_python_file(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    return code



def generate_prompt2(code):
    prompt = f"""
    I have the following Python code:
    
    {code}
    
    Could you please explain what this code does, including the purpose of each function, class, and key part of the code?
    """
    return prompt

def generate_prompt(code):
    prompt = f"""
    I have the following Python code:
    
    {code}
    
    Could you please explain what this code does, including the purpose of each function, class, and key part of the code?
    
    Make sure the JSON output is structured as follows:

    ```
    {{
    "name": "string",
    "purpose": "string",
    "classes": [
        {{
        "name": "string",
        "purpose": "string"
        }}
    ],
    "functions": [
        {{
        "name": "string",
        "purpose": "string"
        }}
    ]
    }}
    ```

    This JSON output will help us understand the structure and functionality of the source code file in a clear and concise manner.
    """
    return prompt


def chat_with_llm(user_prompt):
    client = OpenAI(
        base_url="https://api.gptsapi.net/v1",
        api_key="sk-bMc085e38ed3500c7839ad50ae35ddf19a61c134df80KGqT"
    )

    completion = client.chat.completions.create(
    #model="gpt-4-1106-preview",
    model="gpt-3.5-turbo-1106",
    messages=[
        {"role": "system", "content": "As a professional source code expert, analyze the given source code file. Your goal is to thoroughly understand the content and purpose of the code. Your response should be in JSON format."},
        {"role": "user", "content": user_prompt}
    ],
    response_format={"type": "json_object"}
    )

    #print(completion.choices[0].message.content)
    return completion.choices[0].message.content


def save_json_to_file(json_str, file_path):
    """
    Load a JSON string and save it to a local file.
    
    Args:
        json_str (str): The JSON string to be loaded.
        file_path (str): The path to the file where the JSON data should be saved.
    
    Returns:
        None
    """
    try:
        # Load the JSON string into a Python dictionary
        data = json.loads(json_str)
        
        # Write the dictionary to a JSON file
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        
        print(f"JSON data has been successfully saved to {file_path}")
    
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


def remove_first_and_last_line(input_string):
    """
    Removes the first and last lines from a given string.

    Args:
        input_string (str): The input string with multiple lines.

    Returns:
        str: The string with the first and last lines removed.
    """
    # Split the string into a list of lines
    lines = input_string.splitlines()

    # Check if the string has more than one line
    if len(lines) > 2:
        # Remove the first and last lines
        trimmed_lines = lines[1:-1]
        # Join the remaining lines back into a single string
        return '\n'.join(trimmed_lines)
    else:
        # Return an empty string if there are less than 3 lines
        return ''

def explain_code(file_path):

    code = read_python_file(file_path)
    prompt = generate_prompt(code)
    
    llm_output_json = chat_with_llm(prompt)

    json = remove_first_and_last_line(llm_output_json)

    output_json_file = "llm_analyse_code_output.json"
    save_json_to_file(json, output_json_file)

    print(json)
    return


def insert_json_to_db(json_file, db_file):
    # Read JSON data from file
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    # Connect to SQLite3 database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Create table if it does not exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS maas_tools (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            purpose TEXT,
            classes TEXT,
            functions TEXT
        )
    ''')
    
    # Prepare data for insertion
    name = data['name']
    purpose = data['purpose']
    
    # Convert lists of classes and functions to JSON strings for storage
    classes = json.dumps(data['classes'])
    functions = json.dumps(data['functions'])
    
    # Insert data into the database
    cursor.execute('''
        INSERT INTO maas_tools (name, purpose, classes, functions)
        VALUES (?, ?, ?, ?)
    ''', (name, purpose, classes, functions))
    
    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

def insert_explain_to_database():
    output_json_file = "llm_analyse_code_output.json"
    #save_json_to_file(json, output_json_file)
    insert_json_to_db(output_json_file, 'code_index.db')


    

class IndexUtil:
    def __init__(self) -> None:
        pass



# Example usage
if __name__ == "__main__":
    #file_path = "/Users/tobe/code/orchard_universe/basket/basket/cli.py"
    #explain_code(file_path)
    insert_explain_to_database()
