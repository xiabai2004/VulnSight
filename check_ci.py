"""Check GitHub Actions run status"""
import subprocess, json, urllib.request

result = subprocess.run(["git", "credential", "fill"],
    input="protocol=https\nhost=github.com\n\n",
    capture_output=True, text=True, timeout=10)

token = ""
for line in result.stdout.split("\n"):
    if line.startswith("password="):
        token = line[9:].strip()
        break

if token:
    req = urllib.request.Request(
        "https://api.github.com/repos/xiabai2004/VulnSight/actions/runs?per_page=5",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}
    )
    resp = json.loads(urllib.request.urlopen(req, timeout=15).read())
    
    for run in resp.get("workflow_runs", []):
        status = run.get("conclusion", run.get("status", "?"))
        print(f"  [{status:>10}] {run['name']} ({run['head_branch']})")
        print(f"         {run['html_url']}")
    
    # Check latest run for details
    latest = resp.get("workflow_runs", [{}])[0]
    run_id = latest.get("id")
    if run_id and latest.get("conclusion") == "failure":
        print(f"\n--- Latest failed run details ---")
        jobs_req = urllib.request.Request(
            f"https://api.github.com/repos/xiabai2004/VulnSight/actions/runs/{run_id}/jobs",
            headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}
        )
        jobs = json.loads(urllib.request.urlopen(jobs_req, timeout=10).read())
        for job in jobs.get("jobs", []):
            print(f"  Job: {job['name']} [{job['conclusion']}]")
            for step in job.get("steps", []):
                if step["conclusion"] == "failure":
                    print(f"    FAIL: {step['name']}")
                    # Get log
                    log_req = urllib.request.Request(step["logs_url"], headers={"Authorization": f"Bearer {token}"})
                    try:
                        log = urllib.request.urlopen(log_req, timeout=10).read().decode()
                        print(f"    {log[-500:]}")
                    except:
                        pass
else:
    print("No token available")
