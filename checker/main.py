from contest_api import ContestAPI
import checker
import config


def main():
    student_config = config.load_student_config()
    course_config = config.load_course_config()

    contest_api = ContestAPI(student_config["token"])
    contest_info, problem_alias = checker.security_stage(course_config)
    contest_id = contest_info["yandex_contest_id"]
    contest_alias = "contest" + str(contest_info["id"])
    
    checker.check_linter()
    checker.check_deadline_met(contest_api, contest_id, problem_alias)
    checker.check_pass_tests(contest_api, contest_id, problem_alias, contest_alias)


if __name__ == "__main__":
    main()
