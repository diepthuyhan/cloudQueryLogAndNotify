import time
import json
from datetime import datetime
from .baseClass import BaseSlackFormartMessage
from .settings import DEFAULT_SLACK_MESSAGE_COLOR


class DefaultSlackFormatMessage(BaseSlackFormartMessage):

    def __init__(self):
        self.template = {
                "attachments": [
                    {
                        "color": DEFAULT_SLACK_MESSAGE_COLOR,
                        "blocks": [
                            {
                                "type": "section",
                                "text": {
                                    "type": "mrkdwn",
                                    "text": "*{subject}*"
                                }
                            },
                            {
                                "type": "context",
                                "elements": [
                                    {
                                        "type": "mrkdwn",
                                        "text": "*CurrentTime* {nowtime}"
                                    },
                                    {
                                        "type": "mrkdwn",
                                        "text": "*Timezone* {timezone}"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }

    def format_message(self, message):
        try:
            thread_ts = message.pop("thread_ts")
        except KeyError:
            thread_ts = None
        if isinstance(message, dict):
            try:
                color = message.pop("color")
            except KeyError:
                color = DEFAULT_SLACK_MESSAGE_COLOR
            subject = f"```\n{json.dumps(message, indent=4, ensure_ascii=False)}\n```"
        else:
            subject = f"*{str(message)}*"
        current_time = f'*CurrentTime*: {datetime.now().strftime("%Y-%m-%d:%H:%M")}'
        timezone = f"*Timezone* {time.tzname[0]}"
        self.template["attachments"][0]["blocks"][0]["text"]["text"] = subject
        self.template["attachments"][0]["blocks"][1]["elements"][0]["text"] = current_time
        self.template["attachments"][0]["blocks"][1]["elements"][1]["text"] = timezone
        self.template["attachments"][0]["color"] = color
        if thread_ts:
            self.template["thread_ts"] = thread_ts
        return self.template

