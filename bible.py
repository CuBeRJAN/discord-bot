import json
import subprocess
import os
import sys

def get_verse(book, verse):
    os.system("rm -f bverse")
    subprocess.check_output(["wget", "-q", f"https://bible-api.com/{book}{verse}", "-O", "bverse"], encoding="utf-8")
    with open("bverse", "r") as f:
        x = json.loads(f.read())
        return x["text"]

print(get_verse(sys.argv[1], sys.argv[2]))
