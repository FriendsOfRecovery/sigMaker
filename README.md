# sigMaker: Outlook Signature Generator

This project generates Outlook-compatible HTML signature files for your organization using Microsoft 365 (Exchange) user data. It automates the process with PowerShell (for data fetching) and Python (for template rendering and file output).

## Features
- Fetches user data for all users with a Business Premium license via Microsoft Graph API
- Generates ready-to-copy HTML signatures for each user
- Uses a customizable HTML template
- Outputs signatures for easy copy-paste into Outlook
- One-command setup and execution (local or Docker)

## Prerequisites (for local use)
- **PowerShell 7+**
- **Python 3.8+**
- **Microsoft Graph PowerShell SDK** (`Install-Module Microsoft.Graph -Scope CurrentUser`)
- Global admin or sufficient permissions to read user data in Microsoft 365

## Usage

### Option 1: All-in-One Local Script
1. Clone this repository.
2. Run the all-in-one wrapper script:
   ```
   python scripts/all_in_one.py
   ```
   - This will fetch user data and generate signatures in one step.
   - The script will install any required Python dependencies if missing.
   - Generated HTML files will appear in the `output/` directory.

### Option 2: Docker (Recommended for Cross-Platform)
1. Build the Docker image:
   ```
   docker build -t sigmaker .
   ```
2. Run the container (mounts your local output directory):
   ```
   docker run -it --rm -v $(pwd)/output:/app/output sigmaker
   ```
   - On Windows (PowerShell):
     ```
     docker run -it --rm -v ${PWD}/output:/app/output sigmaker
     ```
   - This will fetch user data and generate signatures in one step.
   - Generated HTML files will appear in your local `output/` directory.

### Customizing the Template
- Edit `templates/signature_template.html` to change the signature layout or branding.
- Use Jinja2-style placeholders (e.g., `{{ display_name }}`) for dynamic fields.

## Output
- Each user gets a separate HTML file: `output/{email}.html`
- Open the HTML file, copy all, and paste into Outlook's signature editor.

## Notes
- The address is currently hardcoded for all users. For area/region support, see comments in the template.
- No sensitive information is hardcoded; authentication is interactive and secure.

## Troubleshooting
- If you get errors about missing modules, just re-run the wrapper script; it will install them automatically.
- For API permission issues, ensure you have admin consent for the required Microsoft Graph scopes.
- For Docker, ensure you have Docker Desktop or Docker Engine installed and running.

## License
MIT

## Testing

This project uses `pytest` for automated testing of core functionality.

To run tests:

1. Install test dependencies (if not already):
   ```
   pip install -r requirements.txt
   ```
2. Run tests from the project root:
   ```
   pytest
   ```

Tests cover user data loading, template rendering, and error handling for missing files.

## Accessing Signatures via GitHub Pages

Signatures are now available online via GitHub Pages. Employees can access their signature by visiting:

    https://<your-username>.github.io/<repo-name>/

and selecting their email HTML file (e.g., `jane.doe@company.com.html`).

The `docs/` folder is automatically updated with the latest signatures.

## How to Use

1. **After generating new signatures**, run:
   ```
   python scripts/copy_output_to_docs.py
   ```
2. **Commit and push** the changes to GitHub.
3. Employees can access their signature at:
   ```
   https://<your-username>.github.io/<repo-name>/
   ```
   and click their email. 