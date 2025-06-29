# Github Assistant Python

## Description

A desktop application in Python that communicates with the GitHub API to help manage collaborators in the user's repositories.

## Instalation

1. Clone the repository

```bash
git clone https://github.com/Manssanito/Github_Assistant_Python.git
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Use:

Run main.py

```bash
python main.py
```

## API References and Token permissions

1. List repositories for the authenticated user [API Docs](https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#list-repositories-for-the-authenticated-user)

The fine-grained token must have the following permission set:
- "Metadata" repository permissions (read)


2. List repository collaborators [API Docs](https://docs.github.com/en/rest/collaborators/collaborators?apiVersion=2022-11-28#list-repository-collaborators)

The fine-grained token must have the following permission set:
- "Metadata" repository permissions (read)


3. List repository invitations [API Docs](https://docs.github.com/en/rest/collaborators/invitations?apiVersion=2022-11-28#list-repository-invitations)

The fine-grained token must have the following permission set:
- "Administration" repository permissions (read)