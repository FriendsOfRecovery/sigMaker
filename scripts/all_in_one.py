import os
import sys
import subprocess
import argparse

FETCH_SCRIPT = os.path.join(os.path.dirname(__file__), 'fetch_m365_users.ps1')
GENERATE_SCRIPT = os.path.join(os.path.dirname(__file__), 'generate_signatures.py')
COPY_SCRIPT = os.path.join(os.path.dirname(__file__), 'copy_output_to_docs.py')

def main():
    parser = argparse.ArgumentParser(description='Fetch users and generate signatures.')
    parser.add_argument('--debug', action='store_true', help='Show user data before exporting and ask for confirmation')
    args = parser.parse_args()

    # Step 0: Ensure Microsoft.Graph PowerShell module is installed
    print('Checking for Microsoft Graph PowerShell SDK...')
    try:
        check_cmd = [
            'pwsh', '-Command',
            'if (-not (Get-Module -ListAvailable Microsoft.Graph)) { Install-Module Microsoft.Graph -Scope CurrentUser -Force -AllowClobber }'
        ]
        subprocess.run(check_cmd, check=True)
    except Exception as e:
        print(f'Error ensuring Microsoft Graph PowerShell SDK is installed: {e}')
        sys.exit(1)

    # Step 1: Run PowerShell fetch script
    print('Fetching user data from Microsoft 365...')
    fetch_cmd = ['pwsh', FETCH_SCRIPT]
    if args.debug:
        print('Debug mode: displaying user data before export.')
        fetch_cmd.append('-DebugOutput')
    try:
        result = subprocess.run(fetch_cmd, check=True)
    except Exception as e:
        print(f'Error running PowerShell fetch script: {e}')
        sys.exit(1)

    # Step 2: Run Python generate script
    print('\nGenerating signatures...')
    try:
        result = subprocess.run([
            sys.executable, GENERATE_SCRIPT
        ], check=True)
    except Exception as e:
        print(f'Error running signature generation script: {e}')
        sys.exit(1)

    # Step 3: Copy output to docs and generate index
    print('\nCopying signature files and generating index...')
    try:
        result = subprocess.run([
            sys.executable, COPY_SCRIPT
        ], check=True)
    except Exception as e:
        print(f'Error running copy_output_to_docs.py: {e}')
        sys.exit(1)

    print('\nAll done! Check the docs/ directory for generated signatures and index.')

if __name__ == '__main__':
    main() 