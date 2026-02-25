import requests
import argparse
import os
import sys
from dotenv import load_dotenv

# Chargement de la configuration
load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {TOKEN}"} if TOKEN else {}

# Couleurs pour le terminal
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

def get_user_repos(username):
    """Récupère la liste de tous les repos publics d'un utilisateur."""
    repos = []
    page = 1
    print(f"[*] Récupération de la liste des dépôts pour {Colors.CYAN}{username}{Colors.RESET}...")
    
    while True:
        url = f"https://api.github.com/users/{username}/repos?page={page}&per_page=100"
        try:
            res = requests.get(url, headers=HEADERS)
            if res.status_code != 200:
                break
            
            data = res.json()
            if not data:
                break
                
            for repo in data:
                if not repo['fork']: # Optionnel : on ignore les forks pour se concentrer sur le code de l'user
                    repos.append(repo['name'])
            page += 1
        except Exception as e:
            print(f"{Colors.RED}[!] Erreur réseau : {e}{Colors.RESET}")
            break
            
    return repos

def scan_commits(username, repo, limit=20):
    """Scanne les N derniers commits d'un repo pour trouver des emails."""
    url = f"https://api.github.com/repos/{username}/{repo}/commits?per_page={limit}"
    findings = []
    
    try:
        res = requests.get(url, headers=HEADERS)
        if res.status_code == 200:
            commits = res.json()
            for c in commits:
                sha = c['sha'][:7] # On garde le hash court (ex: 7fe0709)
                commit_data = c['commit']
                
                # On vérifie l'auteur et le committer
                people = [commit_data['author'], commit_data['committer']]
                
                for p in people:
                    email = p.get('email')
                    name = p.get('name')
                    
                    # Filtre anti-spam / noreply
                    if email and "noreply" not in email:
                        findings.append({
                            'email': email,
                            'name': name,
                            'sha': sha,
                            'repo': repo
                        })
    except Exception:
        pass
        
    return findings

def main():
    parser = argparse.ArgumentParser(description="Scan complet d'un profil GitHub pour extraire les emails.")
    parser.add_argument("username", help="Nom de l'utilisateur GitHub (ex: octocat)")
    parser.add_argument("--limit", type=int, default=20, help="Nombre de commits à scanner par repo (défaut: 20)")
    args = parser.parse_args()

    # 1. Récupérer les repos
    repos = get_user_repos(args.username)
    
    if not repos:
        print(f"{Colors.RED}[-] Aucun repository trouvé ou utilisateur inexistant.{Colors.RESET}")
        return

    print(f"[*] {len(repos)} repositories trouvés. Démarrage de l'extraction...\n")
    print(f"{'EMAIL':<40} | {'REPOSITORY':<25} | {'COMMIT ID':<10}")
    print("-" * 80)

    unique_emails = set()
    
    # 2. Boucle sur chaque repo
    for repo in repos:
        results = scan_commits(args.username, repo, args.limit)
        
        for res in results:
            # On affiche seulement si c'est une nouvelle découverte pour ce run
            # (pour éviter de spammer le terminal si le mec a fait 50 commits avec le même mail)
            identifier = f"{res['email']}_{res['repo']}"
            
            if identifier not in unique_emails:
                print(f"{Colors.GREEN}{res['email']:<40}{Colors.RESET} | {res['repo']:<25} | {Colors.YELLOW}{res['sha']}{Colors.RESET}")
                unique_emails.add(identifier)

    print("-" * 80)
    print(f"[*] Scan terminé.")

if __name__ == "__main__":
    main()

