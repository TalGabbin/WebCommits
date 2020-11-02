from github import Github

# authentication of user name and password
def authenticate_user(submit_info):
    try:
        # using username and password to log in to GitHub
        git = Github(submit_info['user'], submit_info['password'])
        [(s.name, s.name) for s in git.get_user().get_repos()]
        return True

    except:
        return False


# getting data from user info
def get_git_data(submit_info):
    git = Github(submit_info['user'], submit_info['password'])
    try:
        repo = git.get_repo(f"{submit_info['user']}/{submit_info['repository']}")

    except:
        return {"Error": 'An Error has accord on the server'}

    # num of commits to return
    top_x = 5
    data = {}

    for commit in repo.get_commits()[:top_x]:
        data[str(commit.commit.author.date)] = {'user': commit.author.login,
                                                'sha': commit.sha,
                                                'message': commit.commit.message.replace('\n\n', ': '),
                                                'additions': commit.stats.additions,
                                                'deletions': commit.stats.deletions
                                                }
    return data
