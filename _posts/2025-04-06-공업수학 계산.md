---
title: 파이썬으로 수치해석 해보기
date: 2025-04-06 00:22:00 +0900
categories:
  - Programming
tags:
  - python
  - Rust
  - Javascript
  - mathematics
  - engineering
  - excel
pin: false
mermaid: "false"
image:
  path: /assets/img/thumbnail/engineering_math.png
incomplete: true
math: true
published: true
comments: true
---
이 글 시작하기 전에 먼저 말해두고 싶은게 있다.
> 엑셀은 신이다.

엑셀의 장점은 다음과 같다.
- 내가 코딩을 잘 몰라도 대부분의 계산을 해낼 수 있다.
- `scipy` 등 수치해석을 활용해야 하는 경우에도 해찾기 기능으로 해결이 가능하다.
- 간단한 데이터는 테이블로 표현하고 차트로 나타낼 수 있다.
- 회사에서 공유하기 좋다. 
- 빠르게 계산 양식을 만들어낼 수 있다.
- 신경만 쓴다면 GUI 짤 필요 없이 예쁜 디자인으로 만들어낼 수 있다.

time-dependent한 계산을 할 거 아니면 대부분의 계산은 해찾기 등을 활용해서 해결할 수 있다. 하지만 엑셀을 사용하면서 다음 부분이 아쉬우면 프로그래밍을 고려해보자.
- 공용파일로 쓰는 데 누군가 자꾸 수식을 한 두 개씩 수정할 경우
	- 필자의 경우 셀 잠금을 걸어놔도 풀어달라는 요청이 들어옴.
	- 예를 들어, 100행 x 23열의 인풋 데이터+계산 데이터 중 한 두 개씩 수식 `+1`, `x2` 혹은 정수만 넣었을 때 찾아내기 쉽지 않다.
- (해찾기 사용할 경우) 입력값만 수정해서 수백 수천 건 이상의 계산을 수행해야 할 경우
	- 매크로 + 해찾기 기능을 활용하는 경우 되돌리기(`ctrl`+`z`) 기능으로 값 복원이 안 된다. 잘못된 계산/매크로 실행 시 되돌릴 수 없는 치명적인 단점이 있다.
	- **매크로 실행 도중에는 모든 엑셀 파일을 제어할 수 없다.** 실행 중단이 되면 다행이지만 잘못 건들이면 프리징 발생한다.
		- 수식 업데이트, 스크린 업데이트 등을 끄고 마지막에 다시 켜두면[^1] 조금 낫지만 프로그램이 중단되면 직접 켜야하는 순간이 온다.
	- 런타임 에러 발생하면 당연히 켜져 있는 엑셀파일 전부 날아간다.

이 글에서는 Matlab은 안 다룬다. matlab은 유료이기도 하고, 회사에서 라이센스 수량이 한정되어 사용 못하는 경우도 가끔 발생해서 python 위주로 사용했다. 

## 수치해석 계산방법
다음 항목들을 체크하자.
- [ ] Time-independent 한지, time-dependent 한지
- [ ] 몇 차원의 공간 데이터 계산할 것인지
- [ ] 

## Python
파이썬으로 할 수 있는 계산을 다음과 같다.
- sklearn : Machine Learning 다룰 때 설명할 예정
	- 엑셀 : 차트-추세선 기능이나 선형회귀처럼 사용
	- 분류/회귀/차원축소/군집화 등을 수행할 수 있다.
- `tensorflow / pytorch` : Deep Learning할 때 사용하는 라이브러리
- `scipy` : 엑셀의 해찾기와 유사한 편
- `sympy` : scipy와 비슷하게 공학 계산이 가능하고 변수명을 지정할 수 있다는 게 특징이다. 다만, nonlinear 계산 등을 수행할 때 `sympy`만의 자료형(예를 들어  `FinteSet` 등 집합체) 을 사용해서 결과값 추출하기가 번거롭다.

이 중 `scipy`를 추천한다. `latex` 등을 활용한 수학 공식에 익숙하다면 `sympy`보다 직관적이지는 못하지만 엑셀의 해찾기에 익숙하다면 오히려 이 라이브러리의 방식이 친숙할 것이다.

아직까진 데이터 분석 업무에 익숙하지만 필자는 대용량 연산을 할 때 다음 라이브러리를 활용한다. 
- 데이터 저장 형식 : `csv` or `.db`(sqlite3 활용)
- 자료형 : `numpy` or `pandas.DataFrame`
- 머신러닝 : [`scikit-learn`](https://scikit-learn.org/stable/)
- 계산라이브러리 : [`scipy`](https://scipy.org/)
- 비동기 실행 : [`concurrent.futures.ThreadPoolExecutor`](https://docs.python.org/ko/3.13/library/concurrent.futures.html#concurrent.futures.ProcessPoolExecutor) (파이썬 기본 내장)
- 그래프 툴
	- 정적형 : `matplotlib.pyplot` + `seaborn`
	- 인터랙티브 : [`pyqtgraph`](2024-09-03-PyQt6%20pyqtgraph%20소개하기.md) (pyqt5/pyside2 이상의 버전을 사용을 권장)

%% 추후 svg 파일로 2x3 grid로 a>img + span 구성할 것.%%


### Scipy
> Scipy로 할 수 있는 것들을 확인해보자.

양이 방대해서 대충 아래와 같이 다이어그램으로 정리했다.

#### 미적분
가끔 미적분을 지원하는 라이브러리가 없는 언어들이 있는데 파이썬은 scipy에서 지원한다. 

```python
from scipy.integrate import solve_ivp # 미적분 식
```

#### 통계분석
통계에 관해서 다음 부분을 제공한다. 자세한 건 [2025-04-08-STEM 통계 튜토리얼](2025-04-08-STEM%20통계%20튜토리얼.md) 참고 바람.
- 정규분포
- t분포
- chi제곱 분포
- 지수함수 분포

#### 연립방정식
- 선형이든 비선형이든 상관 없다.
- 초기값 세팅할 것
- 해/정의역 조건 세팅하는 방법
- 경우에 따라 solution space가 1 이상인 경우가 있을 수 있는데 이 때 목표 변수의 최소, 최대가 되도록 세팅하면 된다.
- 이 방식은 수치해석 방법 : ??? 에 준거한다.

#### ODE 계산하기


#### PDE 계산하기


##### example : spring-damper system

##### example : basic LCR system 

##### example :


---
다음 시간에 다룰 것들
## Rust
- `nalgebra` : 
- `ndarray` : 

## C/C++

## Javascript / Typescript



## Reference
- [Thumbnail Image Reference](https://engineering-sciences.uniroma2.it/news/engineering-math-pre-courses-a-y-2022-23-2/)
- [수치해석 블로그](https://m.blog.naver.com/hodong32/223030787366)
- [PDE calculation with rust](https://nodiscard.tistory.com/217)

[^1]: [엑셀 매크로 속도 향상 4가지 방법](https://han8849.tistory.com/102)
[^2]: [Integrals 300X Faster in Python (DON'T use Scipy)](https://www.youtube.com/watch?v=GOiTF11umMo)