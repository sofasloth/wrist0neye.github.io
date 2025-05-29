---
title: 데이터, SQL 공부용 데이터셋 모음
date: 2025-02-11 22:54:00 +0900
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
published: false
comments: true
---
## 데이터 사이언스
> Scikit-learn 내장

머신러닝 공부용 태그
#평가 #분류 #회귀 #차원축소 #군집화

데이터 분석용
- `sns.hist(data:1차원 ndarray,bins:히스토그램 막대 수)`
	- `plt.hist(data, bins)`도 정상적으로 동작함.
- 

### [Scikit-learn 내장 데이터셋](https://scikit-learn.org/stable/api/sklearn.datasets.html)
```python
# 불러올 데이터셋은 load_... 로 시작.
from sklearn.datasets import load_iris, load_diabests, #...

# 분류모델은 아래와 같이 dataframe에 담기
iris_raw = load_iris()
df=pd.DataFrame(iris_raw.data, columns = iris_raw.feature_names)
df['Species'] = iris_raw.target_names[iris_raw.target] #분류 

# 회귀모델은 아래와 같이 dataframe에 담기
diabetes_raw = load_diabetes()
df = pd.DataFrame(diabetes_raw.data, columns = diabetes_raw.feature_names)
df['target'] = diabetes_raw.target
```
- ⭐ **`load_iris` : 붓꽃 품종 비교용 데이터셋** #분류
- `load_diabetes` : 당뇨병 데이터셋 #회귀
- `load_breast_cancer` : #분류 
- `load_digits` : #분류 
- `load_wine` : #분류 

### kaggle 데이터 셋

#### [1. 피마 인디언 당뇨병](https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database?select=diabetes.csv)
- 태그 : #평가 #분류

```python
import kagglehub

# Download latest version
path = kagglehub.dataset_download("uciml/pima-indians-diabetes-database")

print("Path to dataset files:", path)
```

#### [2. Human Acitivty Recognition Using Smartphones Data Sets](https://archive.ics.uci.edu/dataset/240/human+activity+recognition+using+smartphones)
> 사람에게 스마트폰 센서를 장착하여 사람의 동작과 관련된 여러 가지 피처를 수집한 데이터다.

이 데이터셋에 대해서 다음 책[^1][^2]에서 설명을 자세히 해주니 참고하자. 여기서는 이 데이터셋 dataframe 구성하는 데까지만 소개할 예정이다.
- 태그 : #분류 
	- `DecisionTreeClassifier`
	- `RandomForestClassifier`
- `UCI HAR Dataset/features.txt` : 피처명
- `UCI HAR Dataset/train/X_train.txt, y_train.txt` : 학습용 데이터셋

### [3. Titanic](https://www.kaggle.com/competitions/titanic)


### [4. Bike](https://www.kaggle.com/competitions/bike-sharing-demand)


## 데이터 분석할 때 사용하는 기능들

#### `DataFrame.corr()`
`.corr()` 메소드는 각 피처들 간의 상관계수를 `DataFrame`으로 반환하는 메서드다. 

- `pearson` :  두 변수가 **선형** 상관계수를 구합니다. 값의 범위는 $[-1, 1]$입니다.
- `kendal` : 
- `spearman` : 

#### `DataFrame.crosstab()`
`.`


---
## SQL 연습용 데이터 베이스

# Reference
[^1]:⭐ **[데이터 머신러닝 완벽 가이드](https://product.kyobobook.co.kr/detail/S000001766511)** 
[^2]: ⭐**[데이터 머신러닝 완벽 가이드_github](https://github.com/wikibook/pymlrev2)**