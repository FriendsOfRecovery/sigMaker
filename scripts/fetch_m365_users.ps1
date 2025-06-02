# Fetch M365 Users with Business Premium License
# Requires: MS Graph PowerShell SDK, admin consent
# Exports user data to ../output/users.json

param(
    [string]$OutputPath = "",
    [switch]$DebugOutput
)

# Always resolve output path relative to the application root
if ([string]::IsNullOrWhiteSpace($OutputPath)) {
    $OutputPath = Join-Path $PSScriptRoot "..\output\users.json"
}

# Ensure output directory exists
$outputDir = Split-Path -Parent $OutputPath
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
}

function Get-FORAMailboxUsers {
    # Connect to Microsoft Graph interactively (uses default browser)
    Connect-MgGraph -Scopes "User.Read.All", "Directory.Read.All"

    # DEBUG: Output all UPNs before filtering
    $allUsers = Get-MgUser -All
    $allUsers | ForEach-Object { Write-Host "UPN: $($_.UserPrincipalName)" }

    # Get all users with a user mailbox and UPN ending with @friendsofrecovery.com, excluding shared mailboxes
    $users = $allUsers | Where-Object {
        $_.UserPrincipalName -imatch '^[a-z]\.[a-z]+@friendsofrecovery\.com$'
    }

    $userCount = $users.Count
    Write-Host "Found $userCount users matching the regex pattern."

    $writeFile = $true
    if ($DebugOutput) {
        $users | Select-Object DisplayName, UserPrincipalName, JobTitle | Format-Table -AutoSize | Out-String | Write-Host
        $confirm = Read-Host "\nReview the above user data. Press Enter to continue and write users.json, or type 'n' to abort."
        if ($confirm -eq 'n') {
            Write-Host "Aborted by user. No file written."
            $writeFile = $false
        }
    }

    if ($writeFile) {
        # Select relevant properties
        $userData = $users | Select-Object `
            DisplayName, GivenName, Surname, UserPrincipalName, JobTitle, Department, OfficeLocation, BusinessPhones, MobilePhone, CompanyName, StreetAddress, City, State, PostalCode

        # Add pronouns and photo URL if available (optional, can be extended)
        $userData | ConvertTo-Json -Depth 4 | Out-File -Encoding utf8 $OutputPath

        Write-Host "Exported $($userData.Count) users to $OutputPath"
    }
}

Get-FORAMailboxUsers 