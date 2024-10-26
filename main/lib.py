import requests
from main.models import Task
import os
import re
from dotenv import load_dotenv

load_dotenv(".env")

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

def get_git_diff():
    """Fetch all PRs from GitHub."""
    diff_text = "TODO: Update"
    return diff_text


def get_all_prs():
    """Fetch all PRs for a GitHub repository, handling pagination."""
    # Set up the GitHub repository URL for pull requests
    url = 'https://api.github.com/repos/palakmehta7/tasks/pulls'

    # Optionally, add your GitHub personal access token for authentication if needed
    token = GITHUB_TOKEN
    headers = {'Authorization': f'Bearer {token}','Accept': 'application/vnd.github.v3+json'}
    params = {
        "state": "all",  # "open", "closed", or "all"
        "per_page": 100,  # Number of PRs per page (max 100)
        "page": 1         # Starting page number
    }
    # Make the GET request
    response = requests.get(url, params=params)
    pattern = "^.*TASK_TRACK_ID:\s*(?P<ticket_no>\d+).*$"

    # TASK_TRACK_ID: <number>
    # Check if the request was successful
    if response.status_code == 200:
        pr_data = response.json()
        return [
            {
                "pr_id": pr["url"].split("/")[-1],
                'pr_url': pr['url'], 
                'pr_description': pr['body'], 
                'pr_diff_url': pr['diff_url'],
                'ticket_id': re.match(pattern, pr["body"]).groupdict()["ticket_no"]
            } 
            for pr in pr_data
            if pr.get("body") and re.match(pattern, pr.get("body", ""))
        ]  # Extract PR title and URL

    else:
        print(f'Error: {response.status_code} - {response.text}')
        return []


def extract_task_id(description):
    """Extract the task ID from the PR description."""
    # Replace with your actual logic to extract the task ID
    # Example: assuming task ID follows a certain pattern
    import re
    match = re.search(r'Task ID: (\w+)', description)
    return match.group(1) if match else None

def process_prs(projects):
    """Main function to process PRs and link them to task IDs."""
    is_process_success = False
    try:
        print(f"\n debug_logs - 30 - process_prs() - projects = {projects}")
        all_pr_details = get_all_prs()
        print(all_pr_details)
        for pr_data in all_pr_details:
            pr_url = pr_data['pr_url']
            pr_description = pr_data['pr_description']
            pr_diff_url = pr_data['pr_diff_url']
            if pr_description:
                task_id = pr_data["ticket_id"]
            else:
                print(f"pr_description: {pr_description}---pr_data: {pr_data}")
                continue
            if task_id:
                # Check if the PR is already linked in the database
                task_record = Task.objects.filter(id=task_id).first()
                if task_record:
                    task_record.pr_id = pr_data["pr_id"]
                    task_record.save()
                    is_process_success = True
                else:
                    print("Error - in process_prs")

    except Exception:
        print("Error in process_prs")
    
    return is_process_success