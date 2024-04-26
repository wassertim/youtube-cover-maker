FROM python:3.12.2-slim

RUN apt-get update && apt-get install gcc python3-dev graphviz wget git -y

# Create a user named 'vscode' and switch to it
RUN useradd -m vscode

USER vscode

# Set the working directory in the container to /workspace
WORKDIR /workspace

# Copy the file from your host to your current location
COPY --chown=vscode:vscode requirements.txt /workspace/

# Install any dependencies in the requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
