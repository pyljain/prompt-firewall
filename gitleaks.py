import tomllib
import re
from typing import List

def compileExpression(rule):
    try:
        return {
            # Regex is compiled here for faster execution
            "regex": re.compile(rule['regex']),
            "id": rule['id']
        }
    except:
        return {
            "regex": None,
            "id": rule['id']
        }

class GitLeaksDetector():
    def __init__(self) -> None:
        with open("./gitleaks.toml", "rb") as fp:
            data = tomllib.load(fp)
            self._rules = list(map(compileExpression, data['rules']))

    def classify(self, text: str) -> List[str]:
        failures = []
        for rule in self._rules:
            if rule['regex']:
                try:
                    if rule['regex'].search(text):
                        failures.append(rule['id'])
                except:
                    print(f"Could not run rule {rule['id']}")

        return failures 