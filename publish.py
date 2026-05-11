"""Create GitHub repo for VulnSight"""
import json, subprocess, urllib.request, urllib.error

# Get token from git credential store
result = subprocess.run(
    ["git", "credential", "fill"],
    input="protocol=https\nhost=github.com\n\n",
    capture_output=True, text=True, timeout=10,
    cwd=r"C:\Users\HZR\Desktop\VulnSight"
)

token = None
for line in result.stdout.split("\n"):
    if line.startswith("password="):
        token = line[9:].strip()
        break

if not token:
    print("Could not get GitHub token. Trying alternative...")
    print("stdout:", result.stdout[:200])
    
    # Try using stored creds directly
    result2 = subprocess.run(
        ["cmd", "/c", "git credential fill"],
        input="protocol=https\nhost=github.com\n\n",
        capture_output=True, text=True, timeout=10
    )
    for line in result2.stdout.split("\n"):
        if line.startswith("password="):
            token = line[9:].strip()
            break

if token:
    print(f"Token found ({token[:8]}...)")
    
    data = json.dumps({
        "name": "VulnSight",
        "description": "AI-powered vulnerability report analyzer",
        "public": True
    }).encode()
    
    req = urllib.request.Request(
        "https://api.github.com/user/repos",
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
        },
        method="POST"
    )
    
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        rd = json.loads(resp.read())
        name = rd.get("full_name", "?")
        url = rd.get("html_url", "?")
        print(f"OK: {name}")
        print(f"URL: {url}")
        
        # Push
        import os
        os.chdir(r"C:\Users\HZR\Desktop\VulnSight")
        subprocess.run(["git", "remote", "add", "origin",
            f"https://xiabai2004:{token}@github.com/xiabai2004/VulnSight.git"],
            capture_output=True)
        r = subprocess.run(["git", "push", "-u", "origin", "master"],
            capture_output=True, text=True, timeout=30)
        print(r.stdout[-200:] if r.stdout else r.stderr[-200:])
    except urllib.error.HTTPError as e:
        print(f"API error {e.code}: {e.read().decode()[:200]}")
else:
    print("Token not found")
    print("Attempting gh auth login...")
