import json
import requests
# import slack

from .settings import logger
from .notificationMessageFormat import DefaultSlackFormatMessage


class BaseNotification:

    def __init__(self):
        self._format_message_obj = None
        self._validate = []

    def add_validate(self, validate_obj):
        self._validate.append(validate_obj)

    def _validate_message(self, message):
        for validate_obj in self._validate:
            if not validate_obj.validate(message):
                return False
        return True

    def set_format_message(self, format_message_object):
        self._format_message = format_message_object

    def _format_message(self, message):
        if self._format_message:
            return self._format_message_obj.format_message(message)
        return message

    def post(self, message):
        pass

    def notify(self, messages):
        res = []
        for message in messages:
            try:
                if self._validate_message(message):
                    post_result = self.post(self._format_message(message))
                    logger.info(f"Send notification {self.__class__.__name__} ok")
                    res.append(post_result)
                else:
                    logger.info(f"{self.__class__.__name__} message invalid")
                    res.append(False)
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
            exit(1)
        self.slack_web_hook = slack_web_hook
        self.slack_token = slack_token
        self.slack_channel = channel
        if slack_token:
            self._headers = {
                "Authorization": f"Bearer {slack_token}",
                "User-Agent": "Simple-Slack-Application-Notify-Alarm"
            }
            self.http_client.headers.update(self._headers)

        self._format_message_obj = DefaultSlackFormatMessage()

    def post(self, message):
        if self.slack_web_hook:
            res = self.http_client.post(
                self.slack_web_hook,
                json=message
            )
            return str(res.text) == "ok"
        elif self.slack_token:
            response = self.http_client.post(
                json=message
            )
            if response.status_code == 200:
                res_json = response.json()
                if res_json["ok"]:
                    return res_json["ts"]
            else:
                return False
