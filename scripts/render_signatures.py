import os
import sys
import json
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

# Paths
APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_PATH = os.path.join(APP_ROOT, 'output', 'users.json')
TEMPLATE_PATH = os.path.join(APP_ROOT, 'templates')
OUTPUT_DIR = os.path.join(APP_ROOT, 'output')
TEMPLATE_FILE = 'signature_template.html'

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Check users.json exists
if not os.path.isfile(DATA_PATH):
    print(f"Error: User data file not found: {DATA_PATH}")
    sys.exit(1)

# Load user data
with open(DATA_PATH, encoding='utf-8') as f:
    try:
        users = json.load(f)
    except Exception as e:
        print(f"Error reading user data: {e}")
        sys.exit(1)
if not users:
    print("No users found in users.json.")
    sys.exit(1)

# Setup Jinja2 environment and check template exists
try:
    env = Environment(loader=FileSystemLoader(TEMPLATE_PATH))
    template = env.get_template(TEMPLATE_FILE)
except TemplateNotFound:
    print(f"Error: Template file not found: {os.path.join(TEMPLATE_PATH, TEMPLATE_FILE)}")
    sys.exit(1)

for user in users:
    # Map user fields to template variables
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
    }
    output_path = os.path.join(OUTPUT_DIR, f"{context['email']}.html")
    try:
        with open(output_path, 'w', encoding='utf-8') as out:
            out.write(template.render(**context))
    except Exception as e:
        print(f"Error writing signature for {context['email']}: {e}")
        continue 