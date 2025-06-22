import requests

def get_API_repo_list(token=''):
    headers = {}
    headers['Authorization'] = f'token {token}'
    params = {
        "affiliation": "owner"}
    response = requests.get(f"https://api.github.com/user/repos",headers=headers,params=params)
    if response.status_code == 200:
        return response.json()
    return None

def get_API_repo_collaborators(owner,repo,token=''):
    headers = {}
    headers['Authorization'] = f'token {token}'   
    response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/collaborators",headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def get_API_repo_invitations(owner,repo,token=''):
    headers = {}
    headers['Authorization'] = f'token {token}'   
    response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/invitations",headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def get_all_unique_collaborators(owner, token):
    unique_collaborators = set()
    req_list = get_API_repo_list(token)
    if req_list is not None:
        for repo in req_list:
            repo_name = repo['name']
            req_collaborators = get_API_repo_collaborators(owner, repo_name, token)
            if req_collaborators is not None:
                for collaborator in req_collaborators:
                    login = collaborator.get("login")
                    if login:
                        unique_collaborators.add(login)
    return sorted(unique_collaborators)

def get_repos_with_this_collaborator(owner,token,user):
    collaborator_in_repos = dict()
    req_list = get_API_repo_list(token)
    if req_list is not None:
        for repo in req_list:
            repo_name = repo['name']
            req_collaborators = get_API_repo_collaborators(owner, repo_name, token)
            if req_collaborators is not None:
                for collaborator in req_collaborators:
                    login = collaborator.get("login")
                    if login == user:
                        collaborator_in_repos.update({repo['name']:repo['html_url']})
    return collaborator_in_repos

# GET /repos/{owner}/{repo}/invitations
def get_all_invitations(owner, token):
    invitation_in_repos = dict()
    req_list = get_API_repo_list(token)
    if req_list is not None:
        for repo in req_list:
            repo_name = repo['name']
            req_invitations = get_API_repo_invitations(owner, repo_name, token)
            if req_invitations is not None:
                key_count = 0
                for invitation in req_invitations:
                    key_count += 1
                    invitee=invitation.get("invitee")
                    key = f"{key_count} {repo['name']}"
                    invitation_in_repos.update({key:invitee['login']})
    return invitation_in_repos

# (delete) /repos/{owner}/{repo}/collaborators/{username}