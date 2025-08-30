# GitHub Email Finder

A minimalist console application to retrieve public information from GitHub users, including their email addresses through commit analysis.

## Features

- Retrieve user email addresses from commit history
- Display comprehensive user profile information
- Show latest repository details
- Clean, minimalist console interface
- Support for both interactive and command-line modes
- Color-coded output for better readability

## Information Retrieved

- **Profile**: Username, full name, email, bio, location, company
- **Statistics**: Public repositories, followers, following count, member since date
- **Repository**: Latest repository name, description, language, stars, last update

## Installation

1. Clone or download the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command Line Mode
```bash
python main.py <username>
```

Example:
```bash
python main.py octocat
```

### Interactive Mode
```bash
python main.py
```

Then enter usernames when prompted. Type `quit`, `q`, or `exit` to exit the program.

## Requirements

- Python 3.6+
- requests library

## API Limitations

- Uses GitHub's public API (no authentication required)
- Subject to GitHub's rate limiting (60 requests per hour for unauthenticated requests)
- Email retrieval depends on public commit history

## Legal Notice

This tool only accesses publicly available information through GitHub's official API. It respects GitHub's terms of service and rate limits.

## Example Output

```
============================================================
           GitHub Email Finder
============================================================
Search for public GitHub information

Searching for 'octocat'...
   Searching for email...
   Fetching repositories...
------------------------------------------------------------

Information found

PROFILE
   Username: octocat
   Full name: The Octocat
   Email: octocat@github.com
   Bio: GitHub mascot
   Location: San Francisco

STATISTICS
   Public repos: 8
   Followers: 4000
   Following: 9
   Member since: 01/25/2011 at 18:44

LATEST REPOSITORY
   Name: Hello-World
   Description: My first repository on GitHub!
   Language: N/A
   Stars: 1500
   Last updated: 05/20/2023 at 14:30

------------------------------------------------------------
Profile: https://github.com/octocat
```

## License

This project is open source and available under the MIT License.