"""Push VulnSight fixes"""
import subprocess

# Get token
result = subprocess.run(["git", "credential", "fill"],
    input="protocol=https\nhost=github.com\n\n",
    capture_output=True, text=True, timeout=10)
token = ""
for line in result.stdout.split("\n"):
    if line.startswith("password="):
        token = line[9:].strip()
        break

if not token:
    print("No token")
    exit()

import os
os.chdir(r"C:\Users\HZR\Desktop\VulnSight")

# Reinstall to make sure it works
r = subprocess.run(["pip", "install", "-e", "."], capture_output=True, text=True, timeout=30)
print("Install:", r.returncode)

# Test CLI
r = subprocess.run(["vulnsight", "-V"], capture_output=True, text=True, timeout=10)
print(f"CLI test: {r.stdout.strip()}")

# Add, commit, push
subprocess.run(["git", "add", "-A"], capture_output=True)
r = subprocess.run(["git", "commit", "-m", "Fix flake8: encoding, E402, E231, E501, F541 issues"], 
    capture_output=True, text=True, timeout=10)
print(r.stdout.strip())

subprocess.run(["git", "remote", "set-url", "origin",
    f"https://xiabai2004:{token}@github.com/xiabai2004/VulnSight.git"], capture_output=True)
r = subprocess.run(["git", "push"], capture_output=True, text=True, timeout=30)
print(r.stdout[-200:] if r.stdout else "Pushed!")
