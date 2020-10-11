from flask import Flask
from github import Github
import json

app = Flask(__name__)

@app.route("/")
def home():
    return "Please add username/password/repository to path"

@app.route("/<user>/<password>/<repo_name>")
def login(user,password,repo_name):
    # using username and password
    try:
        git = Github(user, password)
        #if  account not valid will send error
        [(s.name, s.name) for s in git.get_user().get_repos()]
    except:
        return 'There was a problem with your username or password'
        
    # getting repo
    try:
        repo = git.get_repo(f"{user}/{repo_name}")
    except:
        return "Repository was not found"
    
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
        return 'There are no commits in this repository'
    return json.dumps(data)

if __name__ == "__main__":
    app.run()
