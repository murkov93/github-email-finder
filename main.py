import requests
import sys
import json
from datetime import datetime

class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    GRAY = '\033[90m'

class GitHubEmailFinder:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'GitHub-Email-Finder/1.0'
        })

    def print_header(self):
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}")
        print(f"           GitHub Email Finder")
        print(f"{'='*60}{Colors.END}\n")
        print(f"{Colors.GRAY}Search for public GitHub information{Colors.END}\n")

    def print_separator(self):
        print(f"{Colors.GRAY}{'-'*60}{Colors.END}")

    def get_user_info(self, username):
        try:
            response = self.session.get(f"https://api.github.com/users/{username}")
            
            if response.status_code == 404:
                return None, "User not found"
            elif response.status_code == 403:
                return None, "API rate limit exceeded"
            elif response.status_code != 200:
                return None, f"API error: {response.status_code}"
                
            return response.json(), None
        except requests.RequestException as e:
            return None, f"Network error: {str(e)}"

    def get_user_email(self, username):
        try:
            headers = {
                'Accept': 'application/vnd.github.cloak-preview+json',
            }
            
            url = f"https://api.github.com/search/commits?q=author:{username}&per_page=1&sort=author-date&order=desc"
            response = self.session.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('items') and len(data['items']) > 0:
                    return data['items'][0]['commit']['author'].get('email', 'Not available')
            
            return 'Not found'
        except Exception:
            return 'Not available'

    def get_latest_repo(self, username):
        try:
            url = f"https://api.github.com/users/{username}/repos?sort=updated&per_page=1"
            response = self.session.get(url)
            
            if response.status_code == 200:
                repos = response.json()
                if repos and len(repos) > 0:
                    repo = repos[0]
                    return {
                        'name': repo.get('name', 'N/A'),
                        'description': repo.get('description') or 'No description',
                        'updated_at': repo.get('updated_at', ''),
                        'language': repo.get('language') or 'N/A',
                        'stars': repo.get('stargazers_count', 0)
                    }
            
            return None
        except Exception:
            return None

    def format_date(self, date_string):
        try:
            if date_string:
                dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
                return dt.strftime("%m/%d/%Y at %H:%M")
            return "Unknown date"
        except Exception:
            return "Invalid date"

    def display_user_info(self, user_data, email, latest_repo):
        print(f"{Colors.BOLD}{Colors.GREEN}Information found{Colors.END}\n")
        
        print(f"{Colors.BOLD}PROFILE{Colors.END}")
        print(f"   {Colors.CYAN}Username:{Colors.END} {user_data.get('login', 'N/A')}")
        print(f"   {Colors.CYAN}Full name:{Colors.END} {user_data.get('name') or 'Not provided'}")
        print(f"   {Colors.CYAN}Email:{Colors.END} {email}")
        
        if user_data.get('bio'):
            bio = user_data['bio'][:80] + '...' if len(user_data['bio']) > 80 else user_data['bio']
            print(f"   {Colors.CYAN}Bio:{Colors.END} {bio}")
        
        if user_data.get('location'):
            print(f"   {Colors.CYAN}Location:{Colors.END} {user_data['location']}")
        
        if user_data.get('company'):
            print(f"   {Colors.CYAN}Company:{Colors.END} {user_data['company']}")
        
        print()
        
        print(f"{Colors.BOLD}STATISTICS{Colors.END}")
        print(f"   {Colors.CYAN}Public repos:{Colors.END} {user_data.get('public_repos', 0)}")
        print(f"   {Colors.CYAN}Followers:{Colors.END} {user_data.get('followers', 0)}")
        print(f"   {Colors.CYAN}Following:{Colors.END} {user_data.get('following', 0)}")
        
        created_at = self.format_date(user_data.get('created_at'))
        print(f"   {Colors.CYAN}Member since:{Colors.END} {created_at}")
        
        print()
        
        if latest_repo:
            print(f"{Colors.BOLD}LATEST REPOSITORY{Colors.END}")
            print(f"   {Colors.CYAN}Name:{Colors.END} {latest_repo['name']}")
            
            if latest_repo['description'] and latest_repo['description'] != 'No description':
                desc = latest_repo['description'][:60] + '...' if len(latest_repo['description']) > 60 else latest_repo['description']
                print(f"   {Colors.CYAN}Description:{Colors.END} {desc}")
            
            print(f"   {Colors.CYAN}Language:{Colors.END} {latest_repo['language']}")
            print(f"   {Colors.CYAN}Stars:{Colors.END} {latest_repo['stars']}")
            
            updated_at = self.format_date(latest_repo['updated_at'])
            print(f"   {Colors.CYAN}Last updated:{Colors.END} {updated_at}")
        
        print()
        self.print_separator()
        
        print(f"{Colors.GRAY}Profile: https://github.com/{user_data.get('login')}{Colors.END}\n")

    def search_user(self, username):
        if not username or not username.strip():
            print(f"{Colors.RED}Username required{Colors.END}\n")
            return False
            
        username = username.strip()
        print(f"{Colors.YELLOW}Searching for '{username}'...{Colors.END}\n")
        
        user_data, error = self.get_user_info(username)
        if error:
            print(f"{Colors.RED}Error: {error}{Colors.END}\n")
            return False
        
        print(f"{Colors.GRAY}   Searching for email...{Colors.END}")
        email = self.get_user_email(username)
        
        print(f"{Colors.GRAY}   Fetching repositories...{Colors.END}")
        latest_repo = self.get_latest_repo(username)
        
        print()
        self.print_separator()
        print()
        
        self.display_user_info(user_data, email, latest_repo)
        return True

    def run_interactive(self):
        self.print_header()
        
        while True:
            try:
                username = input(f"{Colors.BOLD}GitHub username{Colors.END} (or 'quit' to exit): ")
                
                if username.lower() in ['quit', 'q', 'exit']:
                    print(f"\n{Colors.CYAN}Goodbye!{Colors.END}\n")
                    break
                
                print()
                success = self.search_user(username)
                
                if success:
                    continue_search = input(f"{Colors.GRAY}Search for another user? (y/n): {Colors.END}")
                    if continue_search.lower() not in ['o', 'oui', 'y', 'yes', '']:
                        print(f"\n{Colors.CYAN}Goodbye!{Colors.END}\n")
                        break
                
                print()
                
            except KeyboardInterrupt:
                print(f"\n\n{Colors.CYAN}Goodbye!{Colors.END}\n")
                break
            except EOFError:
                print(f"\n\n{Colors.CYAN}Goodbye!{Colors.END}\n")
                break

    def run_single(self, username):
        self.print_header()
        self.search_user(username)

def main():
    finder = GitHubEmailFinder()
    
    if len(sys.argv) > 1:
        username = sys.argv[1]
        finder.run_single(username)
    else:
        finder.run_interactive()

if __name__ == "__main__":
    main()