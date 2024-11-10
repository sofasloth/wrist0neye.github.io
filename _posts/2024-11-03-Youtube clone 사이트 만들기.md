---
title: Youtube clone 사이트 만들기
date: 2024-11-03 17:44:00 +0900
categories:
  - Programming
  - Web
tags:
  - MongoDB
  - React
  - frontend
  - nodejs
  - Web
pin: false
mermaid: "false"
image: 
incomplete: true
math: true
published: true
comments: true
---
> 이번 블로그 글은 John Ahn 님의 [따라하며 배우는 노드, 리액트 시리즈 - 유튜브 만들기](https://www.inflearn.com/course/%EB%94%B0%EB%9D%BC%ED%95%98%EB%A9%B0-%EB%B0%B0%EC%9A%B0%EB%8A%94-%EB%85%B8%EB%93%9C-%EB%A6%AC%EC%95%A1%ED%8A%B8-%EC%9C%A0%ED%8A%9C%EB%B8%8C-%EB%A7%8C%EB%93%A4%EA%B8%B0/dashboard) 강의를 보고 필기한 파일입니다. 
{: .prompt-info }

우선 저분의 github 주소에 들어가서 파일을 열어보면 아래와 같은 구조를 취하고 있다.


---
### Mongo DB
mongoDB 가입 후 *Cluster* 를 생성한다. AWS EC2 같은 서버를 생성한다고 생각하면 된다. 무료 계정으로 가입해두자. 

![](/assets/img/res/Pasted%20image%2020241103180606.png)

사용할 서버 사양은 다음과 같이 한다. (해외 사용자면 지역 변경하고)

![](/assets/img/res/Pasted%20image%2020241103180650.png)

접속할 계정의 아이디와 비밀번호를 설정했다면 다음 단계로 넘어가게 될 것인데, Driver와 그 버전을 선택한다.

![](/assets/img/res/Pasted%20image%2020241103180945.png)

생성되고 나서 약간의 시간이 지나면 다시 Driver 설정으로 들어가 어떻게 앱에서 이 서버로 연결할 지 확인하면 된다.

![](/assets/img/res/Pasted%20image%2020241103181256.png)

Database Access로 들어가면 새 계정을 생성할 수 있다. 필요하면 추가하자.
![](/assets/img/res/Pasted%20image%2020241103181421.png)

