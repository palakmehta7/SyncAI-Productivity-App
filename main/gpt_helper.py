import requests
import re
import time
import os
from main.gpt_calls import KShots
from dotenv import load_dotenv


# Replace these variables
owner = 'palakmehta7'
repo = 'tasks'
load_dotenv(".env")

token = os.environ.get("GITHUB_TOKEN")

model = KShots(1)


# Function to get changed files with diffs in a PR
def get_paginated_diffs(task, task_desc=""):
    # API URL to get the diff for the pull request
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{task.pr_id}/files"

    # Set headers, including authorization and accept headers for the diff format
    # headers = {
    #     "Authorization": f"Bearer {token}",
    #     "Accept": "application/vnd.github.v3.diff"
    # }

    # Send GET request to GitHub API to get the PR diff
    # response = requests.get(url, headers=headers)
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        diff_text = response.text  # This contains the diff output
        print("Git Diff for PR:")
        pattern = r"done\s*=\s*(\d+)%\s*&\s*pending\s*=\s*(\d+)%"
        evals = model.evaluate(task_desc, diff_text)
        task.summary = evals
        task.save()
        print("Results: ", evals)
        percentages = re.findall(pattern, evals)
        return percentages[0]
    else:
        print(f"Failed to retrieve diff: {response.status_code}")
        print(response.json())  # Print error message if available
