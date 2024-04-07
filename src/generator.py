import os
import json
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ.get('OPENAI_API_KEY')


def generate_json(description, language):

    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"{description} \n----------\n make it {language} programming language. The output must be in JSON format where keys are relative file paths and values are content of this file."},
        ],
        temperature=0.2,
        n=5,
    )

    return [completion.choices[x].message.content for x in range(5)]

with open('response.md') as f:
    description = f.read()

def extract_between_curly_braces(input_str):
    # Search for the first opening curly brace and the last closing curly brace
    first_opening_brace = input_str.find('{')
    last_closing_brace = input_str.rfind('}') + 1
    
    # If either the first opening brace or the last closing brace is not found, return an empty string
    if first_opening_brace == 0 or last_closing_brace == -1:
        return ""
    
    # Extract the substring between the first opening brace and the last closing brace
    substring_between_braces = input_str[first_opening_brace:last_closing_brace]
    
    return substring_between_braces

if __name__ == '__main__':

    new_programming_language = input("Enter the programming language to convert the code to: ")
    json_data = generate_json(description, new_programming_language)
    # delete new lines from json_data
    

    for file_name, content in data.items():
        with open(f'{file_name}', 'w') as f:
            f.write(content)
