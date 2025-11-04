import json
import os
from difflib import SequenceMatcher

def match_template(data):
    templates = []
    for f in os.listdir(r"D:\PycharmProjects\ASG_ComputerView\test\chains\templates"):
        with open(os.path.join("templates", f)) as file:
            templates.append(json.load(file))

    best = max(templates, key=lambda t: SequenceMatcher(None, str(data), str(t)).ratio())
    return best
