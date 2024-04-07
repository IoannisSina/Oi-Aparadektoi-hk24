import os
import json

from descriptor import get_description
from generator import generate_json

import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ.get('OPENAI_API_KEY')

def pseudo_changes(description, changes):
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"{description} \n----------\n {changes}"},
            ],
            temperature=0.2,
            n=3,
    )

    return completion.choices[0].message.content


if __name__ == '__main__':

    input_repo = input("Enter the URL of the GitHub repository to convert: ")
    project_name = input_repo.split('/')[-1]
    if not os.path.exists(project_name): os.makedirs(project_name)
    
    description = get_description(input_repo)

    while True:
        print(description)
        changes = input("\n\nWrite the changes you want to make to the pseudocode. Else write no: ")
        if changes == "no":
            break
        else:
            description = pseudo_changes(description, changes)
    
    with open(f'{project_name}/response.md', 'w') as f:
        f.write(description)

    
    new_programming_language = input("\n\nEnter the programming language to convert the code to: ")

    json_datas = generate_json(description, new_programming_language)
    for i, json_data in enumerate(json_datas):
        try:
            # json_data = json_data.replace('\n', '')
            data = json.loads(json_data, strict=False)
            break
        except json.JSONDecodeError:
            pass

    for file_name, content in data.items():
        with open(f'{project_name}/{file_name}', 'w') as f:
            f.write(content)
