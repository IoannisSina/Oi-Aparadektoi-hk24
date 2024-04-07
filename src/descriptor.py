import os
import tkinter as tk

import base64
from github import Github
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ.get('OPENAI_API_KEY')

class GitHubGPT:
    def __init__(self, access_token, repo_url):
        self.access_token = access_token
        self.repo_url = repo_url
        self.owner, self.repo_name = self._extract_repo_info()
        self.github = Github(self.access_token)
        self.repo = self._get_repo()
        self.file_contents = []

    def _extract_repo_info(self):
        repo_info = self.repo_url.split('/')[-2:]
        return repo_info[0], repo_info[1]

    def _get_repo(self):
        return self.github.get_user(self.owner).get_repo(self.repo_name)

    def read_files(self, contents=None):
        if contents is None:
            contents = self.repo.get_contents('')

        for content in contents:
            if content.type == 'dir':
                self.read_files(self.repo.get_contents(content.path))
            elif content.name.endswith(('.py', '.java', '.c', '.cpp', '.cbl', '.js', '.html', '.css', '.php', '.rb', '.yaml')):
                try:
                    # We use try/except to handle the case where the file is not a source code file
                    self.file_contents.append({
                        'name': content.path,
                        'content': base64.b64decode(content.content).decode('utf-8')
                    })
                except:
                    pass


    def generate_response(self):

        prompt = ""
        for file_content in self.file_contents:
            prompt += f"File {file_content['name']}:\n{file_content['content']}\n\n"


        completion = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"{prompt} \n----------\n Convert the given code in pseudocode. It must be in a form where it can be reconstructed in any programming language. Include all variables and the file structure."},
                ],
                temperature=0.2,
                n=1,
        )

        return completion.choices[0].message.content

def get_description(repo):
    xxx = GitHubGPT(os.environ.get('GH_TOKEN'), repo)
    xxx.read_files()
    response = xxx.generate_response()
    with open('response.md', 'w') as f:
        f.write(response)
    return response
