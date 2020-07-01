import json
import datetime
from dataclasses import dataclass


@dataclass
class AlarmData:
    status: str
    alert_name: str
    alert_level: str
    alert_description: str
    current_state: str
    old_state: str
    alert_reason: str
    state_change_utc_time: str
    metric_name: str
    statistic: str
    unit: str
    region: str
    period: str
    evaluation_periods: str
    comparison_operator: str
    threshold: str
    state_change_time: str
    state_change_time_timestamp: str
    alert_url: str
    
    
import json
import time
import cloudQueryLogAndNotify


class SlackFormatAlertMessage(cloudQueryLogAndNotify.BaseSlackFormartMessage):
    def __init__(self, slack_bot_username=None, slack_bot_icon_emoji=None):
        self.slack_bot_metadata_info = {}
        if slack_bot_username:
            self.slack_bot_metadata_info["username"] = slack_bot_username
        if slack_bot_icon_emoji:
            self.slack_bot_metadata_info["icon_emoji"] = slack_bot_icon_emoji
    
    def validate(self, message):
        try:
            if message.pop("is_alert") == True:
                return True
        except KeyError:
            pass
        return False
    
    def format_message(self, message):        
        if message["status"] == "ok":
            color = "#ffc1e3"
        elif message["status"] == "warn":
            color = "#ffe97d"
        elif message["status"] == "error":
            color = "#870000"
        else:
            color = "#c1d5e0"
            
        res = {
            "attachments": [
                {
                    "color": color,
                    "fields": [
                        {
                            "title": "Alarm Name",
                            "value": message["alert_name"]
                        },
                        {
                            "title": "Alarm Description",
                            "value": message["alert_description"]
                        },
                        {
                            "title": "Trigger",
                            "value": ( f"{message['statistic']} {message['metric_name']} {message['comparison_operator']} "
                                    f"{message['threshold']} for {message['evaluation_periods']} period(s) of {message['period']} seconds."
                                    )
                        },
                        {
                            "title": "Alert time",
                            "value": message["state_change_time"]
                        },
                        {
                            "title": "Old State",
                            "value": message["old_state"],
                            "short": True
                        },
                        {
                            "title": "Current State",
                            "value": message["current_state"],
                            "short": True
                        },
                        {
                            "title": "Link to Alarm",
                            "value": message["alert_url"]
                        }
                    ],
                    "footer": "AWS CloudWatch Notification",
                    "footer_icon": ":aws_cloudwatch:",
                    "ts": round(time.time())
                }
            ]
        }
        res.update(self.slack_bot_metadata_info)
        return res


class SlackSendAlertNotification(cloudQueryLogAndNotify.SlackNotification):
    
    def init_format_message(self):
        return [
            SlackFormatAlertMessage(),
            cloudQueryLogAndNotify.DefaultSlackFormatMessage()
        ]
        

def parse_cloudwatch_alert(event):
    result = {}
    sns_data = event["Records"][0]["Sns"]
    
    alert_message = json.loads(sns_data["Message"])
    if alert_message["NewStateValue"] == "OK":
        result["status"] = "ok"
    elif "ERROR" in alert_message["AlarmName"]:
        result["status"] = "error"
    elif "WARN" in alert_message["AlarmName"]:
        result["status"] = "warn"
    else:
        result["status"] = "unknow"
    
    result["alert_name"] = alert_message["AlarmName"]
    result["alert_level"] = str(alert_message["AlarmName"].split("-")[-1]).upper()
    result["alert_description"] = alert_message["AlarmDescription"]
    result["current_state"] = alert_message["NewStateValue"]
    result["old_state"] = alert_message["OldStateValue"]
    result["alert_reason"] = alert_message["NewStateReason"]
    result["state_change_utc_time"] = alert_message["StateChangeTime"]
    result["metric_name"] = alert_message["Trigger"]["MetricName"]
    result["statistic"] = alert_message["Trigger"]["Statistic"]
    result["unit"] = alert_message["Trigger"]["Unit"]
    result["region"] = alert_message["Region"]
    result["period"] = alert_message["Trigger"]["Period"]
    result["evaluation_periods"] = alert_message["Trigger"]["EvaluationPeriods"]
    result["comparison_operator"] = alert_message["Trigger"]["ComparisonOperator"]
    result["threshold"] = alert_message["Trigger"]["Threshold"]
    time_str = alert_message["StateChangeTime"]
    result["state_change_time"] = f"{time_str[:19]}+{time_str[-4:-2]}:{time_str[-2:]}"
    
    result["state_change_time_timestamp"] = datetime.datetime.fromisoformat(result["state_change_time"]).timestamp()
    
    result["alert_url"] = f"https://console.aws.amazon.com/cloudwatch/home?region={os.getenv('AWS_REGION')}#alarm:alarmFilter=ANY;name={alert_message['AlarmName']}"
    
    return result
