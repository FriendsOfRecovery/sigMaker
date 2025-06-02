# sigMaker Planning Document

## Overview
This project generates Outlook-compatible HTML signature files for users in an organization, using their Microsoft 365 (Exchange) data. The process is automated using PowerShell (for data fetching) and Python (for template rendering and file output). The goal is to allow users to copy and paste their signature into Outlook without manual editing of links or contact details.

## Requirements
- Fetch user data for all users with a Business Premium license via Microsoft Graph API.
- Use PowerShell for authentication and data retrieval.
- Use Python to process user data and render HTML signatures from a template.
- Output ready-to-copy HTML files for each user.
- Ensure all links (email, phone, etc.) are functional and do not require user editing.
- Follow DRY principles and modular code structure.

## User Data Fields (Variables)
The following fields will be required for each user:
- display_name
- given_name
- surname
- email
- job_title
- department
- office_location
- business_phones (list)
- mobile_phone
- company_name
- address (street, city, state, zip)
- website_url
- pronouns (if available)
- photo_url (optional)

## Template Structure
- Use Jinja2-style placeholders (e.g., {{ display_name }}) in the HTML template.
- Template will be based on the provided sample.html, with all user-specific fields replaced by variables.
- All links (mailto, tel, website) must be dynamically generated.
- Images (e.g., logo, user photo) must use absolute URLs.

## Data Flow
1. PowerShell script authenticates to Microsoft Graph API and fetches user data for all users with a Business Premium license.
2. User data is exported to a JSON or CSV file.
3. Python script reads the exported data, loads the HTML template, and renders a signature for each user.
4. Rendered signatures are saved as individual HTML files in the /output directory.

## API Usage
- Use Microsoft Graph API endpoints:
  - /users (with $filter for license)
  - /users/{id}/photo (optional)
- Required permissions: User.Read.All, Directory.Read.All
- Authentication via delegated permissions (admin consent required)

## Output Strategy
- Each user gets a separate HTML file: /output/{email}.html
- Files are validated for Outlook compatibility.
- Instructions for users: Open the HTML file, copy all, and paste into Outlook signature editor.

## Next Steps
- Define the PowerShell script for data fetching.
- Define the Python script for template rendering.
- Create the HTML template with all required placeholders.
- Test end-to-end with a sample user. 