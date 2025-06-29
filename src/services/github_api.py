import requests

# API CALL (GET) api.github.com/user/repos
# Retrieve the list of all repos owned by the API token user
# https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#list-repositories-for-the-authenticated-user
def get_API_repo_list(token=''):
    headers = {}
    headers['Authorization'] = f'token {token}'
    params = {
        "affiliation": "owner"}
    response = requests.get(f"https://api.github.com/user/repos",headers=headers,params=params)
    if response.status_code == 200:
        return response.json()
    return None

# API CALL (GET) api.github.com/repos/{owner}/{repo}/collaborators
# Retrieve the list of collaborators for a given GitHub repository 
# https://docs.github.com/en/rest/collaborators/collaborators?apiVersion=2022-11-28#list-repository-collaborators
def get_API_repo_collaborators(owner,repo,token=''):
    headers = {}
    headers['Authorization'] = f'token {token}'   
    response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/collaborators",headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

# API CALL (GET) api.github.com/repos/{owner}/{repo}/invitations
# Retrieve a list of pending repository invitations
# https://docs.github.com/en/rest/collaborators/invitations?apiVersion=2022-11-28#list-repository-invitations
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