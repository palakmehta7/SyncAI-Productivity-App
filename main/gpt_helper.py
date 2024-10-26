import requests
import re
import time
import os
from dotenv import load_dotenv
from gpt_calls import KShots

load_dotenv(".env")


# Replace these variables
owner = 'palakmehta7'
repo = 'tasks'
pull_number = '2'
token = os.environ.get("GITHUB_TOKEN")

model = KShots(1)


# Function to get changed files with diffs in a PR
def get_paginated_diffs(owner, repo, pull_number, token, jira_description=""):
    # API URL to get the diff for the pull request
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}/files"

    # Set headers, including authorization and accept headers for the diff format
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3.diff"
    }

    # Send GET request to GitHub API to get the PR diff
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        diff_text = response.text  # This contains the diff output
        print("Git Diff for PR:")
        pattern = r"done\s*=\s*(\d+)%\s*&\s*pending\s*=\s*(\d+)%"
        evals = model.evaluate(jira_description, diff_text)
        print("Results: ", evals)
        percentages = re.findall(pattern, evals)
        return percentages
    else:
        print(f"Failed to retrieve diff: {response.status_code}")
        print(response.json())  # Print error message if available
