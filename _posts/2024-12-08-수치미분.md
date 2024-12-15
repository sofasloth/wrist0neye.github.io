---
title: (책)딥러닝
date: 2024-12-08 17:07:00 +0900
categories: 
tags: 
pin: false
mermaid: "false"
image: 
incomplete: true
math: true
published: false
comments: true
---
### 수치미분

안 좋은 코드 예시
```python
def numerical_diff(f, x) :
	h = 10e-50 # np.float32(1e-50)은 반올림오차를 발생시킨다.
	return (f(x+h) - f(x))/ h # 전방차분
```
- 위 코드는 `dx`인 `h` 값을 지나치게 잡았다. 이는 **반올림 오차**를 발생시킨다.

개선된 수치미분 함수
```python
def numerical_diff(f, x) :
	h = 1e-4
	return (f(x+h) - f(x-h)/) / (2*h)
```