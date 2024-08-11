---
title: (Tauri) Multi Browser App 만들기
date: 2024-08-11 21:57:00 +0900
categories:
  - Programming
  - Web_desktop
permalink: 
tags:
  - FE
  - GUI
  - programming
  - Tauri
comments: 
published: true
math: true
pin: "false"
mermaid: "false"
image:
  path: /assets/img/res/tauri_banner.png
linkpreview: false
---
이번에 만들 어플리케이션은 VSC, Pycharm과 같이 문서를 여러 개 열 수 있는 어플리케이션이다.

이 브라우저를 만들기 위해서는 다음 기능에 대해서 어느 정도 이해도가 있어야 한다.
- html/css/js [Ref](#html/css/js)
	- [ ] drag & drop 기능에 대한 이해
		-  [ ] (선택) `DropZone` 패키지 활용하기
	- [ ] 웹을 html component 안에서 열어보기
- Tauri [Ref](#Tauri)
	- [ ] Session 및 Cookie 활용하기
- 기타 [Ref](#기타)
	- [ ] 브라우저 메모리 (누수) 확인하기

## 개발 단계
### Step 1_기본 기능 점검하기
다음 기능들을 사용할 수 있는지 검토 해보자.
![](/assets/img/res/Pasted%20image%2020240811223716.png)
- [ ] drag & drop을 테스트할 수 있는 `<div>`
- [ ] browser를 `<div>` 태그 안에서 열어보기.




---
# Reference
## 기반지식 모음
### html/css/js

#### Drag & Drop 기능 활용하기

{% linkpreview "https://inpa.tistory.com/entry/%EB%93%9C%EB%9E%98%EA%B7%B8-%EC%95%A4-%EB%93%9C%EB%A1%AD-Drag-Drop-%EA%B8%B0%EB%8A%A5" %}

#### iframe vs webview

{% linkpreview "https://www.electronjs.org/docs/latest/tutorial/web-embeds" %}

### Tauri
#### Session & Cookie 설명

{% linkpreview "https://hahahoho5915.tistory.com/32" %}

{% linkpreview "https://nesoy.github.io/articles/2017-03/Session-Cookie" %}
5
### 기타

#### 브라우저 메모리 확인

{% linkpreview "https://blog.eunsukim.me/posts/debugging-javascript-memory-leak-with-chrome-devtools" %}
