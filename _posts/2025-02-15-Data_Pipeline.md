---
title: (Python)Pipeline tutorial
date: 2025-02-15 16:37:00 +0900
categories:
  - Programming
  - Data_Science
tags:
  - python
  - machine_learning
  - database
pin: false
mermaid: "false"
image: 
incomplete: true
math: true
published: true
comments: true
---
## [Pipeline](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html)
Pipeline은 `scikit-learn` 라이브러리에서 제공하는 기능 중 하나다.
Jupyter notebook이 있어서 코드블럭별로 실행 및 검정을 편리하게 할 수 있다. 하지만 코드 셀 실행 순서를 뒤죽박죽으로 진행하거나 코드 길이가 지나치게 길어지면 불편한 점이 생긴다.
1. 어떤 변수명이 있는지 찾으려면 코드 셀 전체를 전체를 뒤져봐야 한다. 
2. 동일한 전처리 ~ 모델학습을 진행하는데,

첫 번째 문제는 그래도 여러 에디터에서 **조사식** 기능을 제공한다. 유형(Type)보고 원하는 변수를 찾으면 된다.

![](/assets/img/res/Pasted%20image%2020250215172335.png)

![](/assets/img/res/Pasted%20image%2020250215172352.png)

문제는 두 번째 케이스인데, 파일을 읽고 전처리 ~ 모델 학습하는 과정을 여러 번 반복해야 하는 경우다. 

반복문이나 `os.listdir`로 파일을 여러 개 학습하는 방법도 있지만, 일을 하거나 시간이 경과되면서 데이터셋이 추가될 수도 있다. 그럴 때마다 셀을 복사해서 일일이 변수명을 수정해야 한다. 거기에 한 술 더 떠서 모델 성능을 개선하기 위해 전처리 과정, 모델 hyperparameter 값을 바꿀 때마다 모든 셀에 대해서 일일이 수정해야 하는데.. 그건 비효율적이다.


---
### Pipeline 구성에 대해서 살펴보기


---
### Ensemble Learning

- `Voting`
- `Bagging`
- `Boosting`
	- `Bagging`, `Boosting` 대부분은 `RandomForestClassifier`로 처리된다.
- `Stacking`

---
