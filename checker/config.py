import json

def load_course_config():
    with open("course-settings/course_config.json") as f:
        return json.load(f)


def load_student_config():
    with open("config.json") as f:
        return json.load(f)
