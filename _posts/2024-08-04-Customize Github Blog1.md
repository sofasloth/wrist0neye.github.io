---
title: Github 블로그 꾸며보기
date: 2024-08-04 14:12:00 +0000
categories:
  - Doodle
  - Diary
permalink: 
tags:
  - diary
comments: false
published: true
math: true
incomplete: false
---
## Jekyll Admonition Test
사실 별도의 Admonition은 필요없고 _Chirpy_ template에서 제공하는 방식을 사용하자.

> An example showing the `tip` type prompt.
{: .prompt-tip }

> An example showing the `info` type prompt.
{: .prompt-info }

> An example showing the `warning` type prompt.
{: .prompt-warning }

> An example showing the `danger` type prompt.
>
>이거 할려고 너무 많이 시간을 날림...
{: .prompt-danger }


위 Prompts는 아래와 같이 작성한다. 
```md
> An example showing the `tip` type prompt.
{: .prompt-tip }

> An example showing the `info` type prompt.
{: .prompt-info }

> An example showing the `warning` type prompt.
{: .prompt-warning }

> An example showing the `danger` type prompt.
{: .prompt-danger }
```

## Rich link(linkpreivew) 구현하기
옵시디언에 만든 richlink 기능을 그대로 가져와서 적용하고 싶은데 아직 `ruby + jekyll`이 익숙하지 않아 적용 못하고 있다. 블로그를 오랫동안 작성하게 된다면 언젠가 이 기능도 추가할 예정이다. <span id="Fine">■</span>
![alt text](/assets/img/res/richlink-example.png)


## 댓글 기능 구현하기
- [chirpy 기준 github.io-jekyll 블로그 댓글 만들기](https://www.irgroup.org/posts/utternace-comments-system/)