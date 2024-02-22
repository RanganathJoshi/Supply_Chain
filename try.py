import subprocess

# Add files
subprocess.run(["git", "add", "."])

# Commit message
commit_message = "Docker File added"

# Commit changes
subprocess.run(["git", "commit", "-m", commit_message])

# Push changes to remote repository
subprocess.run(["git", "push","-u","origin","master"])
