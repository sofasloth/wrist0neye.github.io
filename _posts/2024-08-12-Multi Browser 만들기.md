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
  - Electron
comments: 
published: false
math: true
pin: "false"
mermaid: "false"
image:
  path: /assets/img/res/tauri_banner.png
linkpreview: false
incomplete: true
---
이번에 만들 어플리케이션은 VSC, Pycharm과 같이 문서를 여러 개 열 수 있는 어플리케이션이다.

이 브라우저를 만들기 위해서는 다음 기능에 대해서 어느 정도 이해도가 있어야 한다.
- html/css/js `[Ref](#html/css/js)`
	- [ ] drag & drop 기능에 대한 이해
		-  [ ] (선택) `DropZone` 패키지 활용하기
	- [ ] 웹을 html component 안에서 열어보기
- Tauri `[Ref](#Tauri)`
	- [ ] Session 및 Cookie 활용하기
- 기타 `[Ref](#기타)`
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

![](/assets/img/res/Pasted%20image%2020240812011724.png)

![](/assets/img/res/Pasted%20image%2020240812011825.png)

이것만으로 페이지 여는 걸 어떻게 여는지 확인할 수 없다..

![](/assets/img/res/Pasted%20image%2020240812012620.png)

하지만 위 사진처럼 문제가 생겼는데`https://www.electron.org`, `https:/tauri.app`은 `<iframe>`으로 그대로 가져올 수 있었는데, `goolge`, `naver`, `github` 등은 위와 같이 `X-frame-options` to `sameorigin`이라는 Warning창을 띄우며 액세스를 거부한다.

![](/assets/img/res/Pasted%20image%2020240814001728.png)

이는 [mdn X-Frame-Options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options)를 봤는데 이해가 잘 안 되서 google에 `X-Frame-Options`와 `frame-ancestors` 검색했는데 *click jacking* 이라고 `iframe` 위에 `z-index` 높은 이상한 링크를 숨겨놓아서 사용자가 클릭 시 이상한 사이트로 옮겨버리는 방식 때문에 생긴 보안 장치라고 보면 된다. 

electron의 경우 iframe을 안 쓰고 `<webview>` 라는 태그를 대신 사용하는데, [Tauri 공식 문서](https://tauri.app/)에서 비슷한 기능이 없는지 찾아봤지만 이에 대해서 설명한 내용이 없었는지 확인해본 결과 window.ts 에서 비슷한 기능을 하는 WebViewWindow 라는 클래스를 찾을 수 있다. 그 클래스 내용은 다음과 같다. 
```ts
declare class WebviewWindow extends WindowManager {
    /**
     * Creates a new WebviewWindow.
     * @example
     * ```typescript
     * import { WebviewWindow } from '@tauri-apps/api/window';
     * const webview = new WebviewWindow('my-label', {
     *   url: 'https://github.com/tauri-apps/tauri'
     * });
     * webview.once('tauri://created', function () {
     *  // webview window successfully created
     * });
     * webview.once('tauri://error', function (e) {
     *  // an error happened creating the webview window
     * });
     * ```
     *
     * * @param label The unique webview window label. Must be alphanumeric: `a-zA-Z-/:_`.
     * @returns The WebviewWindow instance to communicate with the webview.
     */

    constructor(label: WindowLabel, options?: WindowOptions);
    /**
     * Gets the WebviewWindow for the webview associated with the given label.
     * @example
     * ```typescript
     * import { WebviewWindow } from '@tauri-apps/api/window';
     * const mainWindow = WebviewWindow.getByLabel('main');
     * ```
     *
     * @param label The webview window label.
     * @returns The WebviewWindow instance to communicate with the webview or null if the webview doesn't exist.
     */

    static getByLabel(label: string): WebviewWindow | null;
    /**
     *  Gets the focused window.
     * @example
     * ```typescript
     * import { WebviewWindow } from '@tauri-apps/api/window';
     * const focusedWindow = WebviewWindow.getFocusedWindow();
     * ```
     *
     * @returns The WebviewWindow instance to communicate with the webview or `undefined` if there is not any focused window.
     *
     * @since 1.4
     */
    static getFocusedWindow(): Promise<WebviewWindow | null>;
}
```

위에서 가이드라인 대로 한 번 코드를 짜보자.




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
- [iframe 와 click jacking](https://lucas-owner.tistory.com/69)

{% linkpreview "https://wikidocs.net/86838" %}
{% linkpreview "https://tauri.app/v1/references/webview-versions/" %}


### Tauri
#### Session & Cookie 설명

{% linkpreview "https://hahahoho5915.tistory.com/32" %}

{% linkpreview "https://nesoy.github.io/articles/2017-03/Session-Cookie" %}

### 기타

#### 브라우저 메모리 확인

{% linkpreview "https://blog.eunsukim.me/posts/debugging-javascript-memory-leak-with-chrome-devtools" %}
