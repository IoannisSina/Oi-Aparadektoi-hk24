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
                {"role": "system", "content": "Explain the given code in pseudocode form. It must be in a form where another machine can process it and create the same logic in multiple programming languages. Include all variables and dependencies needed. Include the files structure."},
                {"role": "user", "content": prompt},
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

get_description('xxx')

# repo = 'https://github.com/kounelisagis/Arrivals-of-non-residents-in-Greece'

# Use tkinter for the GUI. One input with a button and one text field.
# The user will input the GitHub URL and click the button.
# The output will be displayed in the text field.

# window = tk.Tk()
# window.title('GitHub GPT')
# window.geometry('600x600')

# def get_desc():
#     repo = entry.get()
#     get_description(repo)
#     text.insert(tk.END, get_description(repo))

# def save():
#     with open('response.md', 'w') as f:
#         f.write(text.get('1.0', tk.END))
#     window.destroy()

# label = tk.Label(window, text='Enter the GitHub URL:')
# label.pack()

# entry = tk.Entry(window)
# entry.pack()
# button = tk.Button(window, text='Get Description', command=get_desc)
# button.pack()
# text = tk.Text(window)
# text.pack()

# # save button to save the output to a file (response.md)
# button = tk.Button(window, text='Save', command=save)
# button.pack()

# window.mainloop()
