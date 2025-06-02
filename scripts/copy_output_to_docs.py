import os
import shutil
import json

def main():
    output_dir = 'output'
    docs_dir = 'docs'
    users_json = os.path.join(output_dir, 'users.json')
    index_html = os.path.join(docs_dir, 'index.html')

    # Clean up docs directory: remove all .html files except index.html
    for filename in os.listdir(docs_dir):
        if filename.endswith('.html') and filename != 'index.html':
            file_path = os.path.join(docs_dir, filename)
            try:
                os.remove(file_path)
                print(f'Removed old {filename} from docs/')
            except Exception as e:
                print(f'Could not remove {filename}: {e}')

    # Copy signature files
    to_copy = []
    for filename in os.listdir(output_dir):
        if filename.endswith('.html'):
            src = os.path.join(output_dir, filename)
            dst = os.path.join(docs_dir, filename)
            shutil.copy2(src, dst)
            print(f'Copied {filename} to docs/')
            to_copy.append(filename)

    # Generate index.html dynamically from users.json (excluding shared inboxes)
    if os.path.isfile(users_json):
        with open(users_json, encoding='utf-8') as f:
            users = json.load(f)
        # Only include users with real names (not shared inboxes)
        real_users = [u for u in users if u.get('GivenName') and u.get('Surname')]
        # Sort by DisplayName or email
        real_users.sort(key=lambda u: (u.get('DisplayName') or u.get('UserPrincipalName', '')))
        # Build file list
        file_links = [f"<li><a href=\"{u['UserPrincipalName']}.html\">{u['UserPrincipalName']}.html</a></li>" for u in real_users]
    else:
        file_links = []

    # HTML template (matches current style)
    index_html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Signature Index</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: #f5f5f5; margin: 0; padding: 40px; }}
        .container {{ max-width: 800px; margin: auto; background: #fff; border-radius: 8px; box-shadow: 0 2px 8px #0001; padding: 32px; }}
        h1 {{ color: #5F07B3; }}
        ul {{ list-style: none; padding: 0; }}
        li {{ margin: 12px 0; }}
        a {{ color: #008DBB; text-decoration: none; font-size: 1.1em; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
<div class="container">
    <h1>Signature Files</h1>
    <ul>
        {''.join(file_links) if file_links else '<li>No user signatures found.</li>'}
    </ul>
    <p>Click your email to view or copy your Outlook signature.</p>
</div>
</body>
</html>\n'''

    with open(index_html, 'w', encoding='utf-8') as f:
        f.write(index_html_content)
        print(f'Generated {index_html} with {len(file_links)} user links.')

if __name__ == '__main__':
    main() 