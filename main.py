from flask import Flask,request,render_template,redirect,jsonify
from github import Github
import os

app = Flask(__name__,template_folder='template')

@app.route("/",methods=["POST","GET"])
def home():
    if request.method == "POST":
        submit_info=request.form
        if not '' in submit_info.values():
            return redirect('/'+os.path.join(submit_info['user'].strip()
                                    ,submit_info['password'].strip()
                                    ,submit_info['repository'].strip()))
    return render_template("home_page.html")

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
    return jsonify(data)

if __name__ == "__main__":
    app.run()
