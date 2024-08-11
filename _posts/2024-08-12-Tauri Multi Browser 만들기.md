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

#### Step 1.1 drag & drop 기능 모음
우리가 구현할 기능은 VSC의 창 기능과 같다.
![vsc-docking](/assets/img/res/vsc-docking.gif)
- widget의 제목창만 미리 표시한다.
- widget의 내부에 상하좌우, 가운데에 `drag`하면 미리 놓을 장소를 표시하고 `drop`시 표시한 위치로 이동하게 만든다.

drag & drop에 관한 이벤트 종류는 아래와 같다. 
- `dragstart`
- `drag`
- `dragenter`
- `dragover`
- `drop`
- `dragleave`
- `dragend`

파일 drag & drop 의 경우 `dataTransfer`를 활용해야 하는데 이번 프로젝트에서는 사용 안 하니 넘어가자.


#### Step 1.2 `<iframe>` 활용하기
`<iframe>`은 상당히 간단하다. 아래 내용만 만족시켜주면 되기 때문이다.
```xml
<iframe src="삽입하는 웹페이지 URL" title="내용"></iframe>
```

이것만으로 구현하면 허전하니 Browser의 기본기능들을 구현해보자.
![](/assets/img/res/Pasted%20image%2020240812003438.png)


#### Step 1.3 구현하기



---
# Reference
## 기반지식 모음
### html/css/js

#### Drag & Drop 기능 활용하기

{% linkpreview "https://inpa.tistory.com/entry/%EB%93%9C%EB%9E%98%EA%B7%B8-%EC%95%A4-%EB%93%9C%EB%A1%AD-Drag-Drop-%EA%B8%B0%EB%8A%A5" %}

{% linkpreview "https://svelte.dev/repl/b225504c9fea44b189ed5bfb566df6e6?version=4.2.18" %}

{% linkpreview "https://svelte.dev/repl/adf5a97b91164c239cc1e6d0c76c2abe?version=3.14.1" %}
#### iframe vs webview
- [Electron : Web Embeds](https://www.electronjs.org/docs/latest/tutorial/web-embeds)
- [웹페이지 뒤로가기 및 앞으로 가기](https://codingbroker.tistory.com/73)
- [웹페이지 새로고침](https://bba-jin.tistory.com/30)

{% linkpreview "https://wikidocs.net/86838" %}
{% linkpreview "https://tauri.app/v1/references/webview-versions/" %}

### Tauri
#### Session & Cookie 설명

{% linkpreview "https://hahahoho5915.tistory.com/32" %}

{% linkpreview "https://nesoy.github.io/articles/2017-03/Session-Cookie" %}

### 기타

#### 브라우저 메모리 확인

{% linkpreview "https://blog.eunsukim.me/posts/debugging-javascript-memory-leak-with-chrome-devtools" %}
