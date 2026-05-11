"""Commit and push VulnSight updates"""
import subprocess, os

os.chdir(r"C:\Users\HZR\Desktop\VulnSight")

# Add all files
subprocess.run(["git", "add", "-A"], capture_output=True)

# Commit
r = subprocess.run(
    ["git", "commit", "-m", "Add CI workflow, English README with shields.io badges, Chinese README"],
    capture_output=True, text=True
)
print(r.stdout)
if r.stderr:
    print(r.stderr)

# Push using stored token
result = subprocess.run(
    ["git", "credential", "fill"],
    input="protocol=https\nhost=github.com\n\n",
    capture_output=True, text=True, timeout=10
)

token = None
for line in result.stdout.split("\n"):
    if line.startswith("password="):
        token = line[9:].strip()
        break

if token:
    subprocess.run(["git", "remote", "set-url", "origin",
        f"https://xiabai2004:{token}@github.com/xiabai2004/VulnSight.git"],
        capture_output=True)
    r = subprocess.run(["git", "push"], capture_output=True, text=True, timeout=30)
    print(r.stdout[-300:] if r.stdout else r.stderr[-300:])
    print("Pushed!")
else:
    print("No token, push skipped")
