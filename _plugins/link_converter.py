import os
import re
import sys
import urllib.parse

# dir = os.getcwd()
# print(os.getcwd()) 
input_dir = '_posts'

islinux = (sys.platform.lower() == "linux")

def regex_rule(match) :
    prefix = match.group(1)
    alias = match.group(2)
    other_file = match.group(3)
    heading = match.group(4)

    if prefix is not None and prefix != "":
        # !, ` 같은 문자가 오면 원문 그대로 반환할 것.
        other_file = "" if other_file is None else other_file
        heading = "" if heading is None else heading
        print(f'- prefix escape : {prefix + alias + "(" + other_file + heading + ")"}')
        return prefix + alias + "(" + other_file + heading + ")"

    other_file = "" if other_file is None else other_file # 빈 문자열도 false로 인식
    heading = "" if heading is None else heading 

    #1. %20 => "-" 그리고 소문자로 치환하기
    other_file = other_file.replace("%20", "-").replace(" ","-")
    heading = heading.replace("%20", "-").lower()

    #2. 특수문자 모두 제거
    other_file = re.sub(r"[^\w\-/\.\!]","",other_file) if "baseurl}}" not in other_file else other_file
    heading = "#" + re.sub(r"[^\w\-]","",heading) if heading != "" else ""

    #3. .md 제거하기 #2에서 "." 이미 제거됨.
    other_file = other_file[:-3] if len(other_file)>3 and other_file[-3:] == ".md" else other_file

    #4. 날짜를 다음 문자로 치환하기
    other_file = re.sub(r"\d{4}-\d{2}-\d{2}-", "", other_file)
    abs_path = "" if other_file == "" else "{{baseurl}}/posts/"
    file_path = urllib.parse.quote(other_file)+"/" if other_file != "" else ""
    heading_path = "" if heading == "" else "#" + urllib.parse.quote(heading[1:]) 
    ret = alias + "(" + abs_path + file_path + heading_path + ")"
    print(f'+ conversion result : {ret}')
    return ret

for filename in os.listdir(input_dir) :
    if filename.endswith(".md") :
        filepath = os.path.join(input_dir, filename)

        print(filename)
        with open(filepath, "r", encoding="UTF-8") as file :
            content = file.read()
        content = re.sub(r"([!`]?)(\[[^\]]+\])\(((?!http)(?!www.)(?![/]*assets/img/res)[^\)]+\.md)?(#.+)?\)", regex_rule, content)

        if islinux :
            with open(filepath, "w", encoding="UTF-8") as file : 
                file.write(content)
        else : 
            print(f"os platform error : {sys.platform}")

        print("\n=====================\n")