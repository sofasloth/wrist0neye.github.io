import os
import re
import sys

# dir = os.getcwd()
print(os.getcwd())
input_dir = '_posts'

def regex_rule(match) :
    alias = match.group(1)
    other_file = match.group(2)
    heading = match.group(3)


    other_file = "" if other_file is None else other_file # 빈 문자열도 false로 인식
    heading = "" if heading is None else heading 

    #1. %20 => "-" 그리고 소문자로 치환하기
    other_file = other_file.replace("%20", "-")
    heading = heading.replace("%20", "-").lower()

    #2. 특수문자 모두 제거
    other_file = re.sub(r"[^\w-]","",other_file) 
    heading = "#" + re.sub(r"[^\w-]","",heading) if heading != "" else ""

    if other_file :
        #3. .md 제거하기 #2에서 "." 이미 제거됨.
        other_file = other_file[:-2] if len(other_file)>2 and other_file[-2:] == "md" else other_file

        #4. 날짜를 다음 문자로 치환하기
        other_file = re.sub(r"\d{4}-\d{2}-\d{2}-", "{{baseurl}}/posts/", other_file)
    

    return alias + "(" + other_file + heading +")"

for filename in os.listdir(input_dir) :
    if filename.endswith(".md") :
        filepath = os.path.join(input_dir, filename)

        with open(filepath, "r", encoding="UTF-8") as file :
            content = file.read()
        content = re.sub(r"(?!\!)(\[[^\]]+\])\(((?!http)(?!www.)(?![/]*assets/img/res)[^\)]+\.md)?(#.+)?\)", regex_rule, content)

        if sys.platform.lower() == "linux" :
            with open(filepath, "w", encoding="UTF-8") as file : 
                file.write(content)
        else : 
            print(f"os platform error : {sys.platform}")
    


        
