---
title: obsidian link를 그대로 github.io에 적용하기
date: 2024-08-15 23:53:00 +0900
categories:
  - Doodle
  - Diary
tags:
  - diary
  - blog
  - github_action
comments: true
published: true
math: true
incomplete: false
image:
---
> \[2024-08-15\] [2024-08-08-Github 블로그 꾸며보기2](2024-08-08-Github%20블로그%20꾸며보기2.md) 파일이 지나치게 길어져 별도의 파일로 분리합니다.
#### (실패)jekyll-relative-links Plugin 적용
markdown `[다른 파일]({{ site.baseurl }}/)` 링크를 걸고 싶으면 [여기 플러그인](https://github.com/benbalter/jekyll-relative-links)을 설치해야 한다.

```ruby
gem install jekyll-relative-links
```

성공적으로 설치가 되었다면 `[이전 글]({{ site.baseurl }}/Github.io-)`을 참조해야 하는데.. 잘 안된다. 이 플러그인은 현재 주소 뒤(ex. `baseurl/posts/현재문서`)에 `/`을 붙이고 그대로 뒤에 주소를 붙이는 방식을 택하고 있는데, 이렇게 하면 엉뚱한 주소를 참조하게 된다.

#### (실패)Ruby 스크립트로 커스텀 플러그인 만들어보기
Ruby는 다뤄보지 않아서 위 규칙에 맞는 코드를 작성해달라고 chatGPT에게 도움을 요청했다.
- path : `/_plugins/obsidian_link_converter.rb`
- `_config.yml` 파일에 `plugins` 항목에 추가할 것.

```yaml
plugins:
  - obsidian_link_converter
```

그럼에도 불구하고 여전히 동작하지 않는다. 그리고 사실 **Github Action은 보안문제로 커스텀 plugin이 있으면 빌드취소**하고 에러를 뱉는다. 어쩔 수 없이 스크립트를 만들어서 Action에서 별도로 변환시켜주는 workflow를 추가해야만 한다.

---

## Python 스크립트 만들기
#### 아래 relative-link 구현하는 용도로 만든 dummy header 입니다. 특수문자 1!2@3#4$5%6^7&8*9.0,a;b c<>d+e{}f-g_ 어떻게 보일까요?

일단 obsidian의 규칙을 좀 더 파악해보자. 참고로 아래 링크는 옵시디언에서는 작동이 안 되는데 블로그에서는 정상적으로 작동된다.

```md
`[아래 relative-link 구현하는 용도로 만든 dummy header 입니다. 특수문자 1!2@3#4$5%6^7&8*9.0,a;b c<>d e{} 어떻게 보일까요?]({{ site.baseurl }}/spanspanclasssx#-relative-link----dummy-header---123-456-7amp890ab-cspanspanclassntltgtspand-e--)`
```

- 같은 문서 내 heading 참조 : `[1. File & links](#1-File-amp-links)`
- 다른 문서 참조 : `[2024-08-04-Github.io블로그 꾸며보기]({{ site.baseurl }}/Githubio-)`
- 다른 문서 내 heading 참조 : `[댓글 기능 구현하기]({{ site.baseurl }}/Githubio-#--)`

### 분석 및 설계
`()` 안의 문자열을 어떻게 수정할지 **변환 순서**를 고려해보면서 생각해보자.

> 1. `()`안에서 처음 시작하는 문자가 `http`나 `www`를 포함하면 안 된다.
>     1. 포함하면 해당 문자열은 변환하지 않는다.
> 2. 모든 영문자는 소문자로 치환한다.
> 3. 모든 `%20`은 `-`로 치환한다.
> 4. 다른 문서를 참조할 때
>     - 날짜형식 `yyyy-mm-dd-`은 제거한다.
>     - `.md` 문자열은 제거한다.
>     - `baseurl`인 `https://{id}.github.io/`, `localhost:4000/` 뒤 쪽에 주소를 붙여넣자.
> 5. 다른 heading을 참조할 때(다른 문서도 포함)
>     - `#` 문자가 포함되어 있을 경우 `/#`을 현재주소 뒤에 붙인다.
>         - 이미 다른 heading을 참조 중일 때는 `/#` 이전까지만 가져와서 주소를 이어붙인다.
>     - `!@#$%^&*()[]{},.{}()[]<>?+_/`등의 특수문자들은 그냥 제거한다.
>         - `-`는 `-`로 표기된다.
>         - obsidian의 경우 일부 문자열을 사용하지 않는다.
>         - 이 때의 `#`는 Heading이 아니라 특수문자로 취급한다.
>     - heading만 있을 경우 `baseurl/현재문서/`에 붙인다.
{: .prompt-info}

{% linkpreview "https://pythex.org/" %}

아래와 같이 expression 짜주면 `http`, `www`을 포함한 주소링크를 무시해준다.
![Pasted image 20240815234253](assets/img/res/Pasted%20image%2020240815234253.png)
그리고 위 정규표현식을 `[]`,`()` 해당하는 부분을 따로 소괄호로 묶어주면 2개의 결과물을 얻을 수 있다.

```regex
(\[[^\]]+\])(\((?!http)(?!www.)[^\)]+\))
```

우리는 저 두 번째 부분을 받아와서 변환해야 한다.

그러면 어떤 문자열로 변환해야 정확한 링크로 변환해줄까? 성공적으로 변환한 것만 체크해뒀다.

- [ ] 일반 링크 `[구현단계 ABC](#구현단계%20ABC)`
    - [구현단계 ABC](#구현단계%20ABC)
- [x] `%20` `-`로 치환 + 소문자 치환 `[구현단계 ABC](#-abc)`
    - [구현단계 ABC](#구현단계-abc)
    - [Python 스크립트 만들기](#python-스크립트-만들기)
    - **위 두 링크를 번갈아가며 클릭해도 정상적으로 동작한다.**
- [ ] liquid 문법1 `[구현단계 ABC]({{ post.url }}/posts#-ABC)`
    - `[구현단계 ABC]({{post.url | relative_url}}/posts/#구현단계%20ABC)`
    - `post.url` 문구가 접근이 안 된다.
- [x] liquid 문법2 + 소문자 치환 + `%20` 치환 `[구현단계 ABC](#-abc)]`
    - `[구현단계 ABC]({{site.baseurl}}/posts/relative-links/#구현단계-abc)`
	    - 오류 때문에 code block 처리
    - `site.baseurl`은 접근해도 괜찮다.
- [x] 다른 문서 참고하기 `[1. linkpreview.html]({{ site.baseurl }}/posts/linkpreview-#1-linkpreviewhtml)`
    - [1. linkpreview.html]({{site.baseurl}}/posts/linkpreview-구현하기/#1-linkpreviewhtml)


위 노가다를 통해 다음과 같이 정리할 수 있다.

![Pasted image 20240816020817](assets/img/res/Pasted%20image%2020240816020817.png)


![Pasted image 20240816020839](assets/img/res/Pasted%20image%2020240816020839.png)

위 요구사항을 만족하는 정규표현식은 다음과 같다.

![Pasted image 20240816023541](assets/img/res/Pasted%20image%2020240816023541.png)

```python
(?!\!)(\[[^\]]+\])\(((?!http)(?!www.)(?![/]*assets/img/res)[^\)]+\.md)?(#.+)?\)
```

### 구현단계 ABC
(ABC 붙인 이유는 `%20` 포함여부, 대문자 포함시 어떻게 되는지 확인하는 용도다.)

#### Step1. python 스크립트 작성하기
`_plugins` 아래에 `link_converter.py`를 만든다.

```python
import os
import re

dir = os.getcwd()
input_dir = dir + '/_posts/'

for filename in os.listdir(input_dir) :
    if filename.endswith(".md") :
        filepath = os.path.join(input_dir, filename)
        with open(filepath, "r", encoding="UTF-8") as file :
            content = file.read()
        content = re.sub(r"(\[[^\]]+\])\(((?!http)(?!www.)(?![/]*assets/img/res)[^\)]+\.md)?(#.+)?\)", regex_rule, content)
```

아까 위에서 `![]()`에서 `!`포함되면 제외하는 이유다. `print`로 결과창을 보면 `/assets`도 포함되어 있는데 보통 이미지 파일들이 `![](/assets/img/res/...)`으로 구현되어 있다. 그래서 `assets/img`을 제외하는 문구와 가장 앞에 `!`를 제외하도록 다시 수정한다.

#### Step2. python 정규표현식 `group` 메소드 활용하기

우리가 변환할 정규표현식은 까다롭다. 아래 첨부된 블로그 글을 보면 `str.replace` »» `re.sub`  » `str.translate` 순서로 빠른데 우리는 아무 문자를 붙잡고 `re.sub("\W", "", content)`치환할 수 없기 때문에 되도록이면 content 한 번만 읽고 모두 치환해야 한다.

{% linkpreview "https://dogsavestheworld.tistory.com/entry/python-%EB%AC%B8%EC%9E%90%EC%97%B4-%EC%B9%98%ED%99%98-%EC%B4%9D-%EC%A0%95%EB%A6%AC-%EB%B0%8F-%EC%84%B1%EB%8A%A5-%EB%B9%84%EA%B5%90%ED%95%98%EA%B8%B0strtranslate-strreplace-resub" %}

앞에서 정리한 두 케이스를 조금 더 보충하면서 한 눈에 보이도록 수정하겠다.
![Pasted image 20240816033031](assets/img/res/Pasted%20image%2020240816033031.png)

다행히도 `re.sub`안에 함수를 넣어 위 과정을 한 번에 처리할 [방법](https://stackoverflow.com/questions/12597370/python-replace-string-pattern-with-output-of-function)이 있다. 위 규칙에 맞는 함수를 만들어보자. 
```python
import os
import re
import sys

dir = os.getcwd()
input_dir = dir + '/_posts/'

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
```

`regex_rule` 함수는 `\1`, `\2`, `\3` 모두 따로 구분해서 인식한다. 반환하고 싶은 문자열이 있다면 `return`에 문자열을 반환하면 된다.

위 코드에서 마지막 코드 3줄만 수정하면 된다.

```python
with open(filepath, "r", encoding="UTF-8") as file :
	content = file.read()
content = re.sub(r"(?!\!)(\[[^\]]+\])\(((?!http)(?!www.)(?![/]*assets/img/res)[^\)]+\.md)?(#.+)?\)", regex_rule, content)
if sys.platform.lower() == "linux" :
	with open(filepath, "w", encoding="UTF-8") as file :
		file.write(content)
else :
	print(f"os platform error : {sys.platform}")
```


> `with open(filepath, "w") as file` 코드를 무턱대고 바로 실행시키면 `_posts` 내 모든 옵시디언 파일들이 지워지거나 사용할 수 없는 링크로 변환되니 되도록이면 로컬에서 실행하지 않는 것을 권장한다. 아니면 운영체제가 `Ubuntu` 일때만 실행하도록 위와 같이 코드를 짜면 된다. 실제로 한 번 날려먹었는데, 제목에 `-`나 특수문자를 거의 안 썼다면 역변환할 수 있는 파이썬 스크립트도 만들 수 있으니 한 번 시도해보자.
{: .prompt-danger }

#### Step3. workflow 설정하기
원래라면 `action/setup-python@v5`을 설치하는 과정을 가져야 하는데 `Repository`를 찾을 수 없다는 에러문구가 뜬다. 

그렇기 때문에 `.github/workflow` 내 `yml` 파일에서 `Setup Ruby` 전에 다음 문구를 입력하자.
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
  
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
          # submodules: true
         # If using the 'assets' git submodule from Chirpy Starter, uncomment above
          # (See: https://github.com/cotes2020/chirpy-starter/tree/main/assets)
  
      - name: Setup Pages
        id: pages
        uses: actions/configure-pages@v4

      # 여기 추가
      - name: Run Python Script for link converter
        run: python _plugins/link_converter.py
  
      - name: Setup Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: 3.3
          bundler-cache: true
```

그러면 처음보는 step이 새로 생기면서 문서 변환이 정상적으로 이뤄진다. 
![](/assets/img/res/Pasted%20image%2020240816044932.png)

아마 특수한 문자를 쓰는 거 아니면 정상적으로 동작할 것이다. 추후 새 예외사항이 생기면 본 문서에 추가 작성할 예정이다. 

매우 긴 글이 되었는데 이제 localhost에서 빌드하는 경우를 제외한다면 obsidian 파일링크와 블로그에서의 링크 둘 다 사용할 수 있게 되었다. 다음 시간에 여기서 좀 더 응용해서 `D3-force` 와 막대그래프를 활용한 포트폴리오 페이지를 구성할 예정이다. ■

### 수정사항
#### \[2024-08-16\]
- 정규표현식 변환할 때, 두 번째항 `\2`가 비어있는 경우 현재 파일명을 받도록 수정해야 한다. #issue
	- `\2` 가 비어있으면 자동으로 `localhost:4000/`뒤에 주소가 붙게 되어 있어 build&deploy한 페이지에서는 링크가 정상적으로 작동하지 않는다.
	- [Step2. python 정규표현식 `group` 메소드 활용하기](#Step2.%20python%20정규표현식%20`group`%20메소드%20활용하기) 코드에서 다음 부분을 수정한다.

```python
def regex_rule(match, filename = None) :
	alias = match.group(1)
	other_file = match.group(2)
	heading = match.group(3)

	# 수정 구문
	other_file = filename if other_file is None else other_file 
	
	other_file = other_file.replace("%20", "-").replace(" ","-")
	# 생략
	
# open(파일, "r", encoding = "UTF-8") 직후 구문
content = re.sub(r'정규표현식', lambda x : regex_rule(x, filename), content);
```

- `[]()` "\`" 안 문자도 변환해서 설명하는 문서의 글도 이상하게 변한다. 예외처리해주자. #issue
	- ![](/assets/img/res/Pasted%20image%2020240816130839.png)
	- 정규표현식 수정
	- 앞에 "\`" 또는 `!` 가 온다면 무시한다. 
	- ![](/assets/img/res/Pasted%20image%2020240816131720.png)
```python
def regex_rule(match, filename = None) :
	prefix = match.group(1)
	alias = match.group(2)
	other_file = match.group(3)
	heading = match.group(4)

	if prefix is not None :
		# !, ` 같은 문자가 오면 원문 그대로 반환할 것.
		return prefix + alias + "(" + other_file + heading + ")"
```
- 인코딩 이슈 #issue
	- Github Action에서 정상적으로 변환했음에도 불구하고 한글이 포함된 일부 링크들이 깨진다.
	- 그런데 또, 링크주소 복사를 하면 정상적으로 작동된다.
	- ![](/assets/img/res/Pasted%20image%2020240816145338.png)
	- `regex_rule` 함수 마지막에 `urllib.parse.quote` 함수로 소괄호 안 주소를 변환해줘야 한다.
```python
#4. 날짜를 다음 문자로 치환하기
# urllib.parse.quote()가 `{`, `}`를 %7B, %7D로 바꿔버려 {baseurl}을 블로그 주소로 변환못하게 만든다.
# 따라서 아래 2줄을 아래와 같이 수정한다.
other_file = re.sub(r"\d{4}-\d{2}-\d{2}-", "", other_file)
ret = alias + "(" + "{{baseurl}}/posts/" + urllib.parse.quote(other_file + heading) + ")"
```


## 주의사항

> `[이렇게 텍스트]()` 만 적어놓고 링크 넣는칸을 비워두면 `a tag is missing a reference` 에러가 발생하니 비워두지 않도록 주의하자.
{: .prompt-warning}

> **여전히 해결이 안 되는 부분들**
> - obsidian의 `[[^]]`으로 `image`, `paragraph` 등 컴포넌트 단위로 참조하는 기능을 구현하기 어려워서 여기서는 다루지 않는다.
> - 옵시디언의 경우 제목에 오는 # 문자는 `%20`으로 치환되는데 이건 따로 구분할 방법이 없다. 최대한 Heading에 `#` 외에도 `^, [], |` 등의 특수 문자를 섞어쓰지 않도록 주의한다.
> - ![Pasted image 20240811120604](assets/img/res/Pasted%20image%2020240811120604.png)
> - ![Pasted image 20240811043914](assets/img/res/Pasted%20image%2020240811043914.png)
> - 옵시디언의 문서 임베드 `![]()` 기능은 사용할 수 없다.
{: .prompt-danger}
# Reference

### Ruby
- [Jekyll 커스터마이징 - Plugin(Converter)](https://namhoon.kim/2017/03/27/jekyll/024/index.html)
- [Ruby 정규표현식](https://hanjuren.github.io/2022/01/30/ruby/Ruby-%EC%A0%95%EA%B7%9C%ED%91%9C%ED%98%84%EC%8B%9D/)
- [Ruby sub, gsub 설명](https://jsikim1.tistory.com/291)

### Python
- [정규식 특정단어 제외하기](https://warpgate3.tistory.com/entry/%EC%A0%95%EA%B7%9C%EC%8B%9D-%ED%8A%B9%EC%A0%95-%EB%8B%A8%EC%96%B4-%EC%A0%9C%EC%99%B8%ED%95%98%EA%B3%A0-%EC%84%A0%ED%83%9D%ED%95%98%EA%B8%B0)
- [파이썬 정규표현식](https://wikidocs.net/4308#match)
- [파이썬 정규표현식 패턴으로 변환하기](https://www.squash.io/how-to-replace-regex-in-python/)
- [파이썬 정규표현식 .group method 활용하기](https://stackoverflow.com/questions/12597370/python-replace-string-pattern-with-output-of-function)
- [문자열 변환 메소드 성능 비교](https://dogsavestheworld.tistory.com/entry/python-%EB%AC%B8%EC%9E%90%EC%97%B4-%EC%B9%98%ED%99%98-%EC%B4%9D-%EC%A0%95%EB%A6%AC-%EB%B0%8F-%EC%84%B1%EB%8A%A5-%EB%B9%84%EA%B5%90%ED%95%98%EA%B8%B0strtranslate-strreplace-resub)