import requests
import time
import os
from dotenv import load_dotenv
from gpt_calls import KShots

load_dotenv(".env")


# Replace these variables
owner = 'ashutosh-haptik'
repo = 'productivity_manager'
pull_number = '1'
token = os.environ.get("GITHUB_TOKEN")

model = KShots(1)


# Function to get changed files with diffs in a PR
def get_paginated_diffs(owner, repo, pull_number, token, per_page=1, jira_description=""):
    page = 1
    headers = {'Authorization': f'token {token}'}
    summary = ""
    
    while True:
        url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}/files'
        params = {'page': page, 'per_page': per_page}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        files = response.json()
        if not files:  # End of pages
            break

        # Process each file in the current batch
        for file in files:
            filename = file['filename']
            patch = file.get('patch', '')
            print(f"\n--- Diff for {filename} ---")

            if patch:
                # make a api call here...
                resp = model.evaluate(jira_description,patch)
                summary += resp
            else:
                print("No diff available (e.g., binary files or large diffs)")
        
        # Move to next page
        page += 1
        
        # Sleep briefly to avoid rate limiting
        time.sleep(1)  # Adjust this delay as needed
    
    return summary



jira_description = """
The email sending logic has been optimized to process recipients in batches rather than all at once. This change is likely to prevent issues that could arise from exceeding limits set by email services, thus ensuring more reliable email delivery.
- Error handling has been retained and improved by ensuring that logging occurs for each batch attempt, which aids in debugging.
- Write a code for better logging
- Add logs wherever possible
- send webhooks to some defined url in case of exceptions
- 
"""
# Run the function to process the PR diffs in batches
completed_summary = get_paginated_diffs(owner, repo, pull_number, token)
final_results = model.evaluate(jira_description, completed_summary, json_resp=True)