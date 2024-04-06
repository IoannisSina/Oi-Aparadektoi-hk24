import os

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
            else:
                try:
                    # We use try/except to handle the case where the file is not a source code file
                    self.file_contents.append({
                        'name': content.name,
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
                # {"role": "system", "content": "The following code must be converted to a fully descriptive markdown file so it can be reproduced."},
                {"role": "system", "content": "Explain the given code in pseudocode form. It must be in a form where another machine can read it and create the same logic in multiple programming languages. Include all variables and dependencies needed."},
                {"role": "user", "content": prompt},
                ],
                temperature=0.2,
                n=1,
        )

        return completion.choices[0].message.content


xxx = GitHubGPT(os.environ.get('GH_TOKEN'), 'https://github.com/kounelisagis/Arrivals-of-non-residents-in-Greece')
xxx.read_files()
with open('response.md', 'w') as f:
    f.write(xxx.generate_response())
