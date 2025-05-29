---
title: Electron과 VITE 같이 사용해보기
date: 2025-04-13 13:01:00 +0900
categories:
  - Programming
  - Web_desktop
tags:
  - Electron
  - Javascript
  - Vite
pin: false
mermaid: "false"
image: 
incomplete: false
math: true
published: true
comments: true
---
>회사에서 가벼운 프로그램을 제작하려고 *tauri* 를 설치하려고 했다. 회사 프록시와 인증서 난관을 뚫고 `cargo new && cargo check` 했지만 보안프로그램으로 인해 `EXCEPTION_ACCESS_ERROR`가 발생해서 포기하고 *electron* 으로 전환하고 사용하려고 한다. 하지만 *tauri* 와 다르게 *electron*은 초기 세팅이 달라 최대한 유사하게 만들어보려고 한다.*claude*나 *chatGPT*한테 물어봤는데 제대로 알려주지 않아서 금요일 하루 꼬박 소비해가며 겨우 찾아낸 방법이라 정확하지 않다.

## 1. 초기 세팅하기
다음 순서에 맞게 초기세팅하면 된다.
1. `npm create vite@latest` : *vite* + 웹 프레임워크 초기화
2. *electron* 및 *concurrently* 등 설치

### 1-1. vite 설치하기
- `--template ${template name}` 옵션을 통해 바로 선택지 없이 설치를 진행할 수 있다.
- 하위 디렉토리를 생성하여 프로젝트 시작
```shell
npm create vite@latest
cd {project_name}
```

- 현재 디렉토리에서 프로젝트 시작
```shell
npm create vite@latest ./
```

필자는 `svelte`만 사용하므로 가장 익숙한 `sveltekit`으로 설치한다.

### 1-2 패키지 설치하기

- [electron](https://www.electronjs.org/docs/latest/tutorial/tutorial-first-app) : 윈도우 웹 어플리케이션 만들기 위해 
- `concurrently` : 해당 패키지는 프론트엔드와 백엔드 동시에 시작할 수 있게 만든다.
- `electron-builder` : 필수는 아닌데, `.exe` 파일로 빌드하고 싶을 때 필요하다.
- `cross-env` : 노드 서비스 개발/배포할 때 `env` 값을 세팅해서 상황에 맞게 빌드해주는 패키지다. [^1]
```shell
npm install electron concurrently electron-builder cross-env --save-dev
```

## 2. 프로젝트 구조 소개
위 과정을 수행하고 나면 아래와 같이 프로젝트가 구성될 것이다. (build 폴더는 원래 생성 안 되니 무시할 것) 

![](/assets/img/res/Pasted%20image%2020250413133356.png)

1. 필요한 파일 생성하기
2. `package.json` 값 수정하기

### 2-1 electron 파일 생성
하단과 같이 `./electron/main.cjs`와 `./electron/preload.cjs` 파일을 생성한다.
```md
my-project/
├── .sveltekit/
├── src/
├── static/
├── electron/
│   ├── main.cjs
│   └── preload.cjs
├── .gitignore
├── package.json
├── package-lock.json
├── README.md 등등
└── vite.config.ts
```


```js
// main.cjs
const {app, BrowserWindow, ipcMain} = require('electron');
const path = require('path');

let mainWindow;

function createWindow() {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences :  {
      nodeIntegration: true,
      preload: path.join(__dirname, 'preload.js')
    },
    //icon: path.join(__dirnmae, 'public/favicon.png)
  });
  win.loadURL('http://localhost:5173'); // port 번호에 따라 바꿔 쓰면 된다.
}

  

app.once('ready', createWindow);
app.on('activate', () => {
  if (!mainWindow) {
    createMainWindow();
  }
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
```

`preload.cjs`는 **IPC communication**할 때마다 코드를 추가해서 사용하면 된다.


### 2-2 package.json 수정하기
`"scripts"` 내부에 다음 코드를 추가하면 된다.
```json
{
	"name": "my-project",
	"version": "0.0.1",
	"type": "module",
	"scripts": {
		"dev" : "vite dev",
		"electron" : "electron ./electron/main.cjs",
		"dev:electron" : "concurrently \"npm run dev\" \"npm run electron\""
	},
	/*중략*/
```

`dev:electron` script처럼 코드를 짜면 프론트에는 `vite dev`, 백엔드에는 `electron`이 실행된다. <span id="Fine">■</span>


## 3. 실행파일로 배포하기
보통 *electron* 은 `electron-builder`를 사용해서 빌드하는데 아래와 같이 `package.json`을 구성해도 프론트엔드는 빌드가 되지 않아 빈 화면만 보여준다.
```json
{
	"name": "my-project",
	"version": "0.0.1",
	"type": "module",
	"scripts": {
		"dev" : "vite dev",
		"electron" : "electron ./electron/main.cjs",
		"dev:electron" : "concurrently \"npm run dev\" \"npm run electron\"",
		"deploy:osx" : "electron-builder --mac",
		"deploy:win32" : "electron-builder --win --x32",
		"deploy:win64" : "electron-builder --win --x64",
	},
	"build" : {
		"productName" : "build_test",
		"appId" : "net.example.my_project"
	}
	/*중략*/
```

*Tauri* 를 빌드하면 다음 라이브러리 사용한 것을 확인할 수 있다.

![](/assets/img/res/Pasted%20image%2020250413201848.png)

확인해보니 *SvelteKit* 은 기본적으로 **SSR** 으로 처리되기 때문에 정적 빌드 결과물을 Electron이 읽도록 구성해야 한다.

1. `@sveltejs/adapter-static` 설치
2. `svelte.config.js` 라이브러리 `@sveltejs/adapter-static`를 `import` 한다.

```shell
npm install -D @sveltejs/adapter-static
```

```js
import adapter from '@sveltejs/adapter-static'; // 라이브러리 교체
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
  // Consult https://svelte.dev/docs/kit/integrations
  // for more information about preprocessors
  preprocess: vitePreprocess(),

  kit: {
    adapter: adapter({
      pages: 'build',
      assets: 'build',
      fallback: 'index.html',
      precompress: false
    }),
    paths: {
      base: '',
    }
  }
};

export default config;
```

위와 같이 페이지 구성 안 하면 아래처럼 `.svelte-kit` 경로 내에 파일이 흩어져서 찾기 힘들다. (`index.html` 파일이 생성이 안 된다.)

![](/assets/img/res/Pasted%20image%2020250413211012.png)

그럼에도 잘 빌드가 되지 않는다.. React나 그냥 svelte로 빌드를 시도해봐야할 거 같다.

## Reference
- [Electron 시작하기 : 배포하기](https://jetalog.net/106)
- [Packaging an electron-react-vite app using electron-builder](https://youtu.be/n18d1vQsPFM?si=iwpZkswydBqIUs6K)

[^1]: [\[NODE\] cross-env 모듈 사용법](https://inpa.tistory.com/entry/NODE-%F0%9F%93%9A-cross-env-%EB%AA%A8%EB%93%88-%EC%82%AC%EC%9A%A9%EB%B2%95)
