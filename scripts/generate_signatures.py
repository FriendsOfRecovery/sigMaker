import os
import sys
import json
import re
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

# Auto-install requirements if missing
try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    print("Jinja2 not found. Installing requirements...")
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', os.path.join(os.path.dirname(__file__), '..', 'requirements.txt')])
    from jinja2 import Environment, FileSystemLoader

APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_PATH = os.path.join(APP_ROOT, 'output', 'users.json')
TEMPLATE_PATH = os.path.join(APP_ROOT, 'templates')
OUTPUT_DIR = os.path.join(APP_ROOT, 'output')
TEMPLATE_FILE = 'signature_template.html'

def load_users():
    if not os.path.isfile(DATA_PATH):
        print(f"Error: User data file not found: {DATA_PATH}\nPlease run 'python scripts/all_in_one.py' or 'pwsh scripts/fetch_m365_users.ps1' to fetch user data.")
        sys.exit(1)
    with open(DATA_PATH, encoding='utf-8') as f:
        try:
            users = json.load(f)
        except Exception as e:
            print(f"Error reading user data: {e}")
            sys.exit(1)
    if not users:
        print("No users found in users.json.")
        sys.exit(1)
    return users

def print_user_index(users):
    print("\nAvailable users:")
    for idx, user in enumerate(users, 1):
        print(f"{idx}. {user.get('DisplayName', '')} <{user.get('UserPrincipalName', '')}>")

def parse_selection(selection, max_index):
    indices = set()
    for part in selection.split(','):
        part = part.strip()
        if '-' in part:
            start, end = part.split('-')
            indices.update(range(int(start), int(end) + 1))
        elif part.isdigit():
            indices.add(int(part))
    return sorted(i for i in indices if 1 <= i <= max_index)

def render_signatures(users, selected_indices):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    try:
        env = Environment(loader=FileSystemLoader(TEMPLATE_PATH))
        template = env.get_template(TEMPLATE_FILE)
    except TemplateNotFound as e:
        print(f"Error: Template file not found: {e}")
        sys.exit(1)

    for idx in selected_indices:
        user = users[idx - 1]
        context = {
            'display_name': user.get('DisplayName', ''),
            'given_name': user.get('GivenName', ''),
            'surname': user.get('Surname', ''),
            'email': user.get('UserPrincipalName', ''),
            'job_title': user.get('JobTitle', ''),
            'department': user.get('Department', ''),
            'office_location': user.get('OfficeLocation', ''),
            'business_phones': ', '.join(user.get('BusinessPhones', [])),
            'mobile_phone': user.get('MobilePhone', ''),
            'company_name': user.get('CompanyName', ''),
            'website_url': user.get('WebsiteUrl', ''),
            'pronouns': user.get('Pronouns', ''),
            'photo_url': user.get('PhotoUrl', ''),
            'street_address': user.get('StreetAddress', ''),
            'city': user.get('City', ''),
            'state': user.get('State', ''),
            'postal_code': user.get('PostalCode', ''),
        }
        output_path = os.path.join(OUTPUT_DIR, f"{context['email']}.html")
        try:
            with open(output_path, 'w', encoding='utf-8') as out:
                out.write(template.render(**context))
            print(f"Generated: {output_path}")
        except Exception as e:
            print(f"Error writing signature for {context['email']}: {e}")
            continue

def main():
    users = load_users()
    while True:
        print_user_index(users)
        selection = input("\nEnter user numbers to generate (e.g., 1-3,5,7) or 'q' to quit: ").strip()
        if selection.lower() == 'q':
            print("Exiting.")
            break
        selected_indices = parse_selection(selection, len(users))
        if not selected_indices:
            print("No valid selection. Try again.")
            continue
        render_signatures(users, selected_indices)
        print("\nDone.\n")

if __name__ == "__main__":
    main() 