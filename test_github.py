import os
from dotenv import load_dotenv
from github import Github, Auth

load_dotenv()
nom_depot = os.getenv("GITHUB_REPO")
token = os.getenv("GITHUB_TOKEN")

print("Dépôt lu :", repr(nom_depot))
print("Token lu :", "oui" if token else "NON (None)")

gh = Github(auth=Auth.Token(token))
print("Connecté en tant que :", gh.get_user().login)
print("Dépôts accessibles avec ce token :")
print("Début :", token[:11], "| longueur :", len(token))
for r in gh.get_user().get_repos():
    print(" -", r.full_name)
