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

## License


This project is open source and available under the MIT License.
