import time
import boto3


class AWSCloudWatchLogInsightQuery:

    def __init__(self, client=None, access_key_id=None, secret_key=None, region=None, log_groups=None, log_limit=10):
        if client:
            self.client = client
        elif access_key_id and secret_key and region:
            self.session = session = boto3.Session(
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_key,
                region_name=region
            )
            self.client = self.session.client("logs")
        else:
            self.session = session = boto3.Session()
            self.client = self.session.client("logs")

        self.access_key_id = access_key_id
        self.secret_key = secret_key
        self.region = region
        self.log_groups = log_groups
        self.log_limit = log_limit
        self.query_results = {}

    def build_query(self, **kwargs):
        query_str = """fields @timestamp, @message filter @message like /{query_keyword}/"""
        return query_str

    def start_query(self, query_string, start_timestamp, end_timestamp, limit=None):
        current_query_id = self.client.start_query(
            logGroupNames=self.log_groups,
            startTime=start_timestamp,
            endTime=end_timestamp,
            queryString=query_string,
            limit=limit or self.log_limit
        )["queryId"]
        self.query_results[current_query_id] = None
        return current_query_id

    def get_query_results(self, query_id=None):
        if query_id not in self.query_result:
            return None
        if self.query_results[query_id]:
            return self.query_results[query_id]
        query_result = self.client.get_query_results(
            queryId=query_id
        )
        if query_result["status"] == "Complete":
            result = {
                "status": query_result["status"],
                "results": {}
            }
            for field in results["results"]:
                result["results"][field["field"]] = field["value"]
            self.query_results[query_id] = result
            return result
        elif query_result["status"] in ["Failed", "Cancelled"]:
            self.query_results[query_id] = {
                "status": query_result["status"],
                "results": {}
            }
            return self.query_results[query_id]
        else:
            return {
                "status": query_result["status"],
                "results": None
            }

    def get_queries_results_block(self, timeout=None):
        end_time = time.time() + int(timeout)
        while time.time() < end_time:
            for query_id in self.query_results:
                self.get_query_results(query_id)
            if all(self.query_results.values()):
                break
            time.sleep(1)
        return self.query_results

    def get_queries_results(self, timeout=None):
        for query_id in self.query_results:
            self.get_query_results(query_id)
        return self.query_results
