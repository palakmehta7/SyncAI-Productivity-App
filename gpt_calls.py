import os
import openai
from dotenv import load_dotenv
import pandas as pd

load_dotenv(".env")

client = openai.OpenAI(
  api_key=os.environ.get("OPENAI_API_KEY"),
)


jira_description = """
The email sending logic has been optimized to process recipients in batches rather than all at once. This change is likely to prevent issues that could arise from exceeding limits set by email services, thus ensuring more reliable email delivery.
- Error handling has been retained and improved by ensuring that logging occurs for each batch attempt, which aids in debugging.
- Write a code for better logging
- Add logs wherever possible
- send webhooks to some defined url in case of exceptions
- 
"""

diff_text = """diff --git a/api/const.py b/api/const.py\\nindex d6c6fec0de8..761d5fbed31 100644\\n--- a/api/const.py\\n+++ b/api/const.py\\n@@ -2664,3 +2664,6 @@ class GPTRequests(enum.Enum):\\n \\n # Based on Feature toggle value above, offline status is marked False if FT is enabled.\\n EXPERT_ACTIVE_OFFLINE_STATUS_TRUE = "Expert Offline status is marked False, based on FT"\\n+\\n+# EmailMultiAlternatives() only supports recipients of length 50\\n+ATHENA_EMAIL_REPORT_RECIPIENTS_BATCH_SIZE = 50\\ndiff --git a/api/lib/athena_api/crux/generator_email.py b/api/lib/athena_api/crux/generator_email.py\\nindex f25d65f6925..d5a79483649 100644\\n--- a/api/lib/athena_api/crux/generator_email.py\\n+++ b/api/lib/athena_api/crux/generator_email.py\\n@@ -11,7 +11,7 @@\\n \\n from api.lib.athena_api.crux import const, helpers\\n from haptik_api.common.db import get_business_id_to_via_name_mapping\\n-from api.const import FEATURE_TOGGLE_ONGOING_CHAT_IN_REPORT\\n+from api.const import FEATURE_TOGGLE_ONGOING_CHAT_IN_REPORT, ATHENA_EMAIL_REPORT_RECIPIENTS_BATCH_SIZE\\n \\n from api.lib.feature_toggles_api.utils import is_enabled_for_partner\\n from analytics.utils.common import get_csv_url_expiry_time_in_utc_str, get_html_for_csv_files_s3_urls\\n@@ -175,25 +175,27 @@ def generate_email_success_daily_agent_report_eod(\\n \\n message = __get_email_body(timestamp_start, timestamp_end, time_zone, via_name, s3_urls_list)\\n \\n-        _email = EmailMultiAlternatives(\\n-            subject=subject,\\n-            body=message,\\n-            from_email=const.Email.SENDER,\\n-            to=recipients,\\n-            bcc=[],\\n-        )\\n-        _email.attach(filename=file_name, content=zip_file, mimetype='application/zip')\\n-\\n-        try:\\n-            response = _email.send()\\n-            _logger.info('report progress', type=logger_identifier, success=True, to_email=recipients,\\n-                         uuid=_uuid, response=response)\\n-        except SMTPDataError as err:\\n-            _logger.info("report progress", type=logger_identifier, success=False, smtp_code=err.smtp_code,\\n-                         smtp_error=err.smtp_error, to_email=recipients, uuid=_uuid)\\n-        except Exception as e:\\n-            _logger.info("report progress", type=logger_identifier, success=False, to_email=recipients,\\n-                         uuid=_uuid, exception=str(e))\\n+        batch_size = ATHENA_EMAIL_REPORT_RECIPIENTS_BATCH_SIZE\\n+        for idx in range(0, len(recipients), batch_size):\\n+            batch_recipients = recipients[idx:idx + batch_size]\\n+            try:\\n+                _email = EmailMultiAlternatives(\\n+                    subject=subject,\\n+                    body=message,\\n+                    from_email=const.Email.SENDER,\\n+                    to=batch_recipients,\\n+                    bcc=[],\\n+                )\\n+                _email.attach(filename=file_name, content=zip_file, mimetype='application/zip')\\n+                response = _email.send()\\n+                _logger.info('report progress', type=logger_identifier, success=True, to_email=batch_recipients,\\n+                            uuid=_uuid, response=response)\\n+            except SMTPDataError as err:\\n+                _logger.info("report progress", type=logger_identifier, success=False, smtp_code=err.smtp_code,\\n+                            smtp_error=err.smtp_error, to_email=batch_recipients, uuid=_uuid)\\n+            except Exception as e:\\n+                _logger.info("report progress", type=logger_identifier, success=False, to_email=batch_recipients,\\n+                            uuid=_uuid, exception=str(e))\\n \\n         _logger.info('report progress', type=logger_identifier, success=True, to_email=recipients, uuid=_uuid)\\n \\n"""

# Max - 5 shots


class KShots:
    def __init__(self, shot=0) -> None:
        self.shot = shot

    def __create_prompt(self):
        return """
            Act as a senior backend engineer
            This is my jira description.            
            We use django ORM Mongodb at backend
            I'll be giving you Jira description and git diff.
            Find how much tasks have been achieved.
            Please provide reasoning why you are marking a task as completed or not completed
            Also provide a conclusion on percentage of task done.
            Format the response in json as follows: {
                "tasks completed": ...,
                "tasks not completed": ...,
                "percentage of tasks completed": ...,
                "conclusion": ...
            }
        """
    
    def evaluate(self, jira_description, git_diff):
        # chain of thought ->
        # k-shot
        # PROMPT - MENTION CHAR LIMIT FOR GENERATED TWEETS - CHECK FOR TW LIMIT

        resp = client.chat.completions.create(
            model="gpt-4o-mini",  # or "gpt-4"
            messages=[
                {"role": "system", "content": self.__create_prompt() },
                {"role": "user", "content": f"jira description={jira_description} | git diff = {git_diff}"},
            ]
        )
        return resp.choices[0].message.content
    

model = KShots(shot=5)
print(model.evaluate(jira_description, diff_text))
# while True:
#     user_query = input("Enter Tweet: ")
#     response = model.evaluate(user_query)
#     print(f"Response: {response}")