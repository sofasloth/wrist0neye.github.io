---
title: (Svelte)vite 경로 세팅 방법
date: 2025-03-15 19:51:00 +0900
categories:
  - Design
  - Web
tags:
  - Web
  - Svelte
  - Vite
pin: false
mermaid: "false"
image: 
incomplete: true
math: true
published: true
comments: true
---
꼭 svelte만 아니더라도 vite 경로를 세팅하는 방법을 알아두면 상대경로를 쓸 필요없이 자주 접근하는 경로를 프로젝트 전역에 사용할 수 있다.

npm으로 패키지 설치할 때 svelte, electron, tauri에서 자동으로 vite를 설치해준다.
만약에 vite가 안 깔려있는 곳이라면 다음과 같은 커맨드로 시작하여 원하는 프론트엔드를 선택하여 시작해도 된다.^[1]

```shell
npm create vite@latest
```

그러고 나서 새로 생성된 하위 디렉토리로 접근하여 `npm i`로 `package.json` 내 라이브러리를 설치한다. 

이제 본론으로 들어가자. 필자의 경우 `tauri`를 설치했기 때문에 폴더 내부가 다음과 같이 생겼다.

![](/assets/img/res/Pasted%20image%2020250315200040.png)

`/src` 디렉토리와 그 하위파일/디렉토리에 자유롭게 접근하고 싶어서 `$root`로 등록해서 사용하고 싶다. 그러면 `vite.config.js`, `tsconfig.json` 파일에서 다음 부분을 추가하자.

![](/assets/img/res/Pasted%20image%2020250315200346.png)

```json
//vite.config.js

// https://vitejs.dev/config/

export default defineConfig(async () => ({
  plugins: [sveltekit()],

  // 아래 코드만 추가
  resolve:{
    alias : {
      $root: path.resolve('./src'),
    },
  },

```

```json
//tsconfig.json
{
	"extends":"./.svelte-kit/tsconfig.json",
	"compilerOptions" : {
		"baseUrl" : ".",
		"paths" : {
			"$root/*" : ["./src/*"]
		}
	}
}
```

두 파일을 수정 후 저장한 뒤에 다음과 같이 코드를 사용하면 된다. <span id="Fine">■</span>

![](/assets/img/res/Pasted%20image%2020250315200748.png)

# Reference
[^1] : [vite 홈페이지](https://ko.vite.dev/guide/)