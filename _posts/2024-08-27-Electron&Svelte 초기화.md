---
title: (Electron)Electron with Svelte 초기화
date: 2024-08-27 23:00:00 +0900
categories:
  - Programming
  - Web_desktop
tags:
  - Svelte
  - Web
  - Electron
pin: false
mermaid: "false"
image:
  path: /assets/img/thumbnail/Electron_20.0.3_screenshot.png
incomplete: true
math: true
published: false
comments: true
---
- 관련 글 : [2024-08-12-Multi Browser 만들기](2024-08-12-Multi%20Browser%20만들기.md)
## 방법 1. Github 블로그 그대로 가져오기

예전에 `npm i svelte@latest` 후 `npm i electron`으로 설치 했는데 `svlete` 화면을 `electron` 에 띄우는 방법을 못 찾아 아래 깃허브 주소대로 설치하려고 한다.

{% linkpreview "https://github.com/soulehshaikh99/create-svelte-electron-app" %}

`git clone` 하고 `yarn`으로 실행하면 편하다.
```shell
yarn install # 현재 패키지 전부 설치
yarn run electron
```

`npm`은 잘 안 되고 `yarn`으로 실행하면 잘 된다.

나중에 시간이 되면 *typescript* 로 코드 짤 방법을 알아봐야겠다.

---

## Reference
- [방법 1은 여기 블로그 참고해서 작성했습니다.](https://seorenn.github.io/note/electron-svelte-app.html)
- [Electron with svelte 초기 세팅하기](https://hokeydokey.tistory.com/159)
- 