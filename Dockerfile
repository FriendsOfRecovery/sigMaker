# sigMaker Dockerfile
# Build with: docker build -t sigmaker .
# Run with:   docker run -it --rm -v $(pwd)/output:/app/output sigmaker

FROM python:3.11-slim

# Install PowerShell
RUN apt-get update && \
    apt-get install -y wget apt-transport-https software-properties-common && \
    wget -q https://packages.microsoft.com/config/debian/11/packages-microsoft-prod.deb && \
    dpkg -i packages-microsoft-prod.deb && \
    apt-get update && \
    apt-get install -y powershell && \
    rm packages-microsoft-prod.deb

# Set workdir
WORKDIR /app

# Copy files
COPY . /app

# Install Python requirements
RUN pip install --no-cache-dir -r requirements.txt

# Install Microsoft Graph PowerShell SDK
RUN pwsh -Command "Install-Module Microsoft.Graph -Scope AllUsers -Force -AllowClobber"

# Entrypoint: run the all-in-one script
ENTRYPOINT ["python", "scripts/all_in_one.py"] 