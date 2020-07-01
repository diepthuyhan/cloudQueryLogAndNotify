import json
import requests
# import slack

from .settings import logger
from .notificationMessageFormat import DefaultSlackFormatMessage
from .customExceptions import (
    IgnoreMessage,
    MissingArgs
)


class BaseNotification:

    def __init__(self):
        self._format_message_objs = self.init_format_message()
    
    def init_format_message(self):
        return []

    def add_formater(self, format_message_object):
        self._format_message_objs.append(format_message_object)

    def _format_message(self, message):
        for formater in self._format_message_objs:
            try:
                new_message = formater.format(message)
                if new_message:
                    return new_message
            except IgnoreMessage:
                continue
        return message

    def post(self, message):
        return False

    def notify(self, messages, thread_ts=None):
        res = []
        if not messages:
            logger.info("Message empty")
        for message in messages:
            try:
                formarted_message = self._format_message(message)
                if thread_ts:
                    formarted_message["thread_ts"] = thread_ts
                post_result = self.post(formarted_message)
                res.append(post_result)
            except Exception as e:
                logger.error(f"Cant not send notification {self.__class__.__name__} Error: {e}")
                res.append(False)
        return res


class SlackNotification(BaseNotification):

    def __init__(self, slack_web_hook=None, slack_token=None, channel=None):
        super().__init__()
        
        self.http_client = requests.Session()

        if not any([slack_token, slack_web_hook]):
            logger.error("Missing slack_web_hook or slack_token")
            raise MissingArgs(f"{self.__class__.__name__} missing slack_web_hook or slack_token")
        self.slack_web_hook = slack_web_hook
        self.slack_token = slack_token
        self.slack_channel = channel
        if slack_token:
            self._headers = {
                "Authorization": f"Bearer {slack_token}",
                "User-Agent": "Simple-Slack-Application-Notify-Alarm"
            }
            self.http_client.headers.update(self._headers)
        

    def init_format_message(self):
        return [DefaultSlackFormatMessage()]

    def post(self, message):
        try:
            del message["token"]
        except KeyError:
            pass
            
        if self.slack_web_hook:
            res = self.http_client.post(
                self.slack_web_hook,
                json=message
            )
            if str(res.text) == "ok":
                logger.info(f"[{self.__class__.__name__}] Send notification success")
                return True
            else:
                logger.error(f"[{self.__class__.__name__}] Send notification fail, Message: {res.text}")
                return False
        elif self.slack_token:
            message["channel"] = self.slack_channel
            if "text" not in message:
                message["text"] = "Notification"
            response = self.http_client.post(
                "https://slack.com/api/chat.postMessage",
                json=message
            )
            if response.status_code == 200:
                res_json = response.json()
                if res_json["ok"]:
                    logger.info(f"[{self.__class__.__name__}] Send notification success")
                    return res_json["ts"]
                else:
                    logger.error(f"[{self.__class__.__name__}] Send notification fail, Message: {response.text}")
                    return False
            else:
                return False
