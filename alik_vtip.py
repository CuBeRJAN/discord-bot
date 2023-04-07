import subprocess
import os


def get_random_joke(): # lol to lidl ten kód
    os.system("rm -f js?nahodne*")
    os.system("wget -q \"https://www.alik.cz/v/js?nahodne\"")
    ss = ""
    with open("js?nahodne", "r") as f:
        s = f.read()
        ptr = len(s)-1
        while s[ptr] != "[":
            ss = s[ptr] + ss
            ptr -= 1
        return ss.replace("<div>", "\n").replace("<br>", "\n").replace("\\\"", "\"").replace("\"]);", "").replace("</div>", "").replace("<!--nic-->", "").replace("\\n", "\n").replace("<p>","").replace("&quot;", "").replace("</p>", "").replace("\\r","")[1:]

print(get_random_joke())
