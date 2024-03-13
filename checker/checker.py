import os
import subprocess
from contest_api import ContestAPI


class CheckerError(RuntimeError):
    pass


def security_stage(course_config):
    branch_name = os.environ.get("GITHUB_HEAD_REF")
    if branch_name is None:
        raise CheckerError("Branch name not set")
    print(f"Branch name is {branch_name}")
    branch_data = branch_name.split("_")
    if len(branch_data) != 2:
        raise CheckerError(f"Branch name not match format: {branch_name}")
    print(f"Contest alias is {branch_data[0]}")
    print(f"Task alias is {branch_data[1]}")
    # TODO: check one specific file changed

    problem_alias = branch_data[1][-1]
    contest_info = None
    for contest in course_config:
        if contest["id"] == int(branch_data[0][-1]):
            contest_info = contest
    
    if contest_info is None:
        raise CheckerError(f"Contest with name {branch_data[0]} not found in config")
    
    if problem_alias not in contest_info["tasks_for_review"]:
        raise CheckerError(f"Task {problem_alias} is not for review for contest {contest_info['id']}")
    return contest_info, problem_alias


def check_deadline_met(contest_api: ContestAPI, contest_id: int, problem_alias: str):
    standings = contest_api.get_standings(contest_id)
    task_index = 0
    for task in standings["titles"]:
        if task["title"] == problem_alias:
            print(f"For task {task['name']} with alias {problem_alias} index is {task_index}")
            break
        else:
            task_index += 1
    task_info = standings["rows"][0]["problemResults"][task_index]
    if task_info["status"] != "ACCEPTED":
        raise CheckerError(f"Deadline for {problem_alias} not met")
    print("Check deadline met OK")


def check_pass_tests(contest_api: ContestAPI, contest_id: int, problem_alias: str, contest_alias: str):
    submissions = contest_api.get_all_submissions(contest_id)["submissions"]
    submission_id = None
    for submit in submissions:
        if submit["problemAlias"] == problem_alias and submit["verdict"] == "OK":
            submission_id = submit["id"]
            print(f"Submission candidate: https://contest.yandex.ru/contest/{contest_id}/run-report/{submission_id}/")
            break
    if submission_id is None:
        raise CheckerError("Submission candidate not found")
    submission_source = contest_api.get_submission_source(contest_id, submission_id)
    github_filename = f"{contest_alias}/{problem_alias}.cpp"
    print(f"Checking for {github_filename}")
    with open(github_filename) as f:
        if submission_source.strip().splitlines() != f.read().strip().splitlines():
            raise CheckerError("Submission content differs from repo content")
    print("Check pass tests OK")


def check_linter(filename: str):
    print("Legacy linter disabled")
