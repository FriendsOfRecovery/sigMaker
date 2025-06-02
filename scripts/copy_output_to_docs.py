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
        # Build file list as card divs
        file_cards = [f'<div class="card"><a href="{u["UserPrincipalName"]}.html">{u["UserPrincipalName"]}.html</a></div>' for u in real_users]
    else:
        file_cards = []

    # Modern card-style HTML template
    index_html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Signature Index</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f5f7fa; margin: 0; padding: 40px; }}
        .container {{ max-width: 900px; margin: auto; background: #fff; border-radius: 16px; box-shadow: 0 4px 24px #0002; padding: 40px 32px 32px 32px; }}
        h1 {{ color: #5F07B3; margin-bottom: 32px; }}
        .card-grid {{ display: flex; flex-wrap: wrap; gap: 24px; justify-content: flex-start; margin-bottom: 32px; }}
        .card {{
            background: #fafbfc;
            border-radius: 12px;
            box-shadow: 0 2px 8px #0001;
            padding: 24px 20px;
            min-width: 260px;
            max-width: 320px;
            flex: 1 1 260px;
            display: flex;
            align-items: center;
            transition: box-shadow 0.2s;
        }}
        .card:hover {{
            box-shadow: 0 6px 24px #5f07b320;
        }}
        .card a {{
            color: #008DBB;
            text-decoration: none;
            font-size: 1.08em;
            font-weight: 500;
            word-break: break-all;
        }}
        .card a:hover {{
            text-decoration: underline;
        }}
        hr {{ margin: 40px 0 32px 0; border: none; border-top: 2px solid #eee; }}
        h2 {{ color: #333; margin-top: 0; }}
        h3 {{ color: #5F07B3; margin-bottom: 8px; }}
        .instructions {{ background: #f0f4fa; border-radius: 10px; padding: 24px 20px; margin-top: 0; box-shadow: 0 1px 4px #0001; }}
        .instructions ul {{ margin: 0 0 12px 0; padding-left: 20px; }}
        .instructions li {{ margin-bottom: 6px; }}
    </style>
</head>
<body>
<div class="container">
    <h1>Signature Files</h1>
    <div class="card-grid">
        {''.join(file_cards) if file_cards else '<p>No user signatures found.</p>'}
    </div>
    <p style="margin-top: 24px;">Click your email to view or copy your Outlook signature.</p>
    <hr>
    <div class="instructions">
        <h2>How to Add Your Signature in Outlook</h2>
        <h3>New Outlook</h3>
        <ul>
            <li>See official guide: <a href="https://support.microsoft.com/en-us/office/add-a-signature-in-new-outlook-4c3f5fdb-5c1e-4d3e-9b3c-4a2c7a5b5c0a" target="_blank">Add a signature in New Outlook</a></li>
            <li>Go to <b>Settings</b> &gt; <b>Mail</b> &gt; <b>Compose and reply</b> and paste your signature.</li>
        </ul>
        <h3>Classic Outlook</h3>
        <ul>
            <li>See official guide: <a href="https://support.microsoft.com/en-us/office/create-and-add-a-signature-to-messages-8ee5d4f4-68fd-464a-a1c1-0e1c80bb27f2" target="_blank">Create and add a signature to messages</a></li>
            <li>Go to <b>File</b> &gt; <b>Options</b> &gt; <b>Mail</b> &gt; <b>Signatures</b> and paste your signature.</li>
        </ul>
    </div>
</div>
</body>
</html>\n'''

    with open(index_html, 'w', encoding='utf-8') as f:
        f.write(index_html_content)
        print(f'Generated {index_html} with {len(file_cards)} user links.')

if __name__ == '__main__':
    main() 