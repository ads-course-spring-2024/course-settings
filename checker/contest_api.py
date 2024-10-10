import datetime
from requests import Session


class ContestAPI:
    api_root = "https://api.contest.yandex.net/api/public/v2"

    def __init__(self, token):
        self._session = Session()
        self._session.headers["Authorization"] = f"OAuth {token}"


    def get_all_submissions(self, contest_id):
        result = []
        i = 1
        while True:
            response = self._session.get(self.api_root + f"/contests/{contest_id}/submissions", params={"page": i, "pageSize": 100})
            response.raise_for_status()
            result += response.json()["submissions"]
            if response.json()["count"] < 100:
                break
            i += 1
        return result


    def get_submission_source(self, contest_id, submission_id):
        response = self._session.get(self.api_root + f"/contests/{contest_id}/submissions/{submission_id}/source")
        response.raise_for_status()
        return response.content.decode("utf-8")
    
    def get_standings(self, contest_id):
        response = self._session.get(self.api_root + f"/contests/{contest_id}/standings/my")
        response.raise_for_status()
        return response.json()
    
    def get_deadline(self, contest_id):
        response = self._session.get(self.api_root + f"/contests/{contest_id}")
        response.raise_for_status()
        start_date_str = response.json()["startTime"].replace("Z", "+00:00")
        start_date = datetime.datetime.fromisoformat(start_date_str)
        return start_date + response.json()["duration"]
