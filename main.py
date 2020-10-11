from flask import Flask
from github import Github
import json

app = Flask(__name__)

@app.route("/")
def home():
    return "add username/password/repository to path"

@app.route("/<user>/<password>/<repo_name>")
def login(user,password,repo_name):
    # using username and password
    
    git = Github(user, password)

    # getting repo
    repo = git.get_repo(f"{user}/{repo_name}")

    # taking each commit from the last top_x and getting their data
    top_x = 5
    data = {}

    for commit in repo.get_commits()[:top_x]:
        data[str(commit.commit.author.date)]={'user':commit.author.login
                                             ,'sha':commit.sha
                                             ,'message':commit.commit.message.replace('\n\n',': ')
                                             ,'additions':commit.stats.additions
                                             ,'deletions':commit.stats.deletions
                                             }
    # check if data is empty
    if len(data)==0:
        return 'there are no commits in this repository'
    return json.dumps(data)

if __name__ == "__main__":
    app.run()
