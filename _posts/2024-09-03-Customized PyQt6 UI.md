---
title: (PyQt6)3. PyQt6 UI 간단히 꾸며보기
date: 2024-09-03 01:05:00 +0900
categories:
  - Programming
  - Python
tags:
  - python
  - pyQt6
  - GUI
pin: false
mermaid: "false"
image:
  path: /assets/img/thumbnail/pyqt++.png
incomplete: false
math: true
published: true
comments: true
---
- 목차 글 : [2024-08-06-pyQt6 Index](2024-08-06-pyQt6%20Index.md)
- 이전 글 : [PyQt6_2. 기본 위젯 소개](2024-09-03-PyQt6_Basic_Widgets.md)

### 작성할 내용들
- [x] `.setStyleSheet()`로 꾸미기
- [x] `.setStyleSheet`로 안 되는 것들
	- [x] `dropshadow`
	- [ ] `animation`은 구현 안 할 예정..
- [ ] 다른 컴퓨터에도 돌려보기
	- [ ] raspberrypi
	- [ ] macOS (m1)

> 이 글부터는 `pyside6-uic.exe`로 UI를 만들지 않고 코드만으로 UI를 짤 예정이다. 그 이유는 나중에 `sqlite3`나 `json/csv` 등을 활용해 UI를 동적으로 만들어지도록 하기 위해서다. 
{: .prompt-info}

이번 시간에는 pyqt를 그나마 html처럼 꾸미는 방법에 대해서 알아볼 예정이다.

## `.setStyleSheet()`로 UI꾸미기

다음과 같은 UI를 구현해보려고 한다. 

![](/assets/img/res/Pasted%20image%2020240906135547.png)

```python정
{: .prompt-danger }

Window11에서는 기본 디자인이 깔끔해서 잘 나왔지만, 10 혹은 raspberry pi에서 돌려보자. 실행파일을 `.exe` 파일로 변환하고 옮겨서 테스트해보려고 한다.
```shell
pip install pyinstaller==5.13.2 # 최신 버전은 윈도우 보안에 걸려서 빌드가 안 된다.
pyinstaller -F --noconsole main.py # --onefile --noconsole
```

성공적으로 빌드되면 `/dist` 폴더 내에 `main.exe`파일이 정상적으로 생성된다.

```shell
pip install PyQt6 --break-system-package
```

개발자는 이 앱이 어떻게 구성되어있는지 알지만 사용자나 의뢰자는 구린 UI를 보고 한 번에 이해하기 어려울 수도 있다. 웹 페이지처럼 반응형으로 꾸미긴 어렵더라도 간단하게라도 가독성을 높이는 방법이 있다.

### 그냥 `.setStyleSheet()` 적용했을 경우
`.setStyleSheet()`는 `QWidget`의 스타일을 적용하는 메소드로 웹 페이지의 `css` 방식대로 작성하면 된다. 대신 **스타일 적용한 위젯 내부에 포함된 위젯까지 모두 적용**되니 이 점 유의해야 한다. 예를 들어, 위 위젯창의 *property* 를 포함하는 container의 border만 추가해보자. 

```python
# property 구현  
self.propertycontainer = QWidget()  
# 아래 코드 한 줄만 추가함.
self.propertycontainer.setStyleSheet("border:2px solid gray;")  
self.bglayout.addWidget(self.propertycontainer)
```

![](/assets/img/res/Pasted%20image%2020241007000045.png)

![](/assets/img/res/Pasted%20image%2020241007000420.png)

이를 방지하기 위해서는 저 *propertycontainer* 에 포함된 위젯 전부 다 `.setStyleSheet`을 적용해주거나 `ObjectName`을 정의해서 저 container만 스타일 적용하게 할 수 있다.

### ObjectName 설정하기
1. `.setObjectName()`으로 위젯 이름을 부여한다. 이 `ObjectName`은 `css`의 `id` 같은거라고 생각하면 된다.
2. `.setStyleSheet(위젯타입#ObjectName {css})`으로 해당 `Object`에만 적용하겠다고 명시하면 된다.

```python
# property 구현  
self.propertycontainer = QWidget()  
# self.propertycontainer.setStyleSheet("border:2px solid gray;")

# 아래 2줄만 추가하면 된다.
self.propertycontainer.setObjectName("propertycontainer") # css ID 같은 역할  
self.propertycontainer.setStyleSheet("QWidget#propertycontainer {border:2px dashed yellow}")
self.bglayout.addWidget(self.propertycontainer)
```

![](/assets/img/res/Pasted%20image%2020241007001103.png)

조금 더 번거롭긴 한데 프로그램 GUI 구조가 복잡하다면 스타일이 꼬여서 적용되는 걸 방지할 수 있다.

### `box-shadow` 구현하기
- `.setStyleSheet()`으로 CSS 일부 기능을 그대로 따라 구현이 가능하지만 이 메소드로 적용할 수 없는 스타일이 있다.
	- 대표적으로 `.box-shadow`와 `transition` 같은 애니메이션 기능이다.
- 이 스타일들은 Qt 모듈에서 별도의 기능으로 구현되어 있다.

애니메이션은 생략하고 그림자를 어떻게 적용하는지만 소개할 예정이다.

```python
# Drop Shadow  
SHADOW_COLOR = "#C0C0C0"  
SHADOW_OFFSET = 3  
SHADOW_BLUR = 12  
def applyShadow(target:QWidget) :  
    effect = QGraphicsDropShadowEffect() # PyQt6.QtWidget 안에 포함.
    effect.setColor(QColor(SHADOW_COLOR))  
    effect.setOffset(SHADOW_OFFSET)  
    effect.setBlurRadius(SHADOW_BLUR)  
    target.setGraphicsEffect(effect)
```

### QDoubleSpinbox 지수표기법
property3을 보면 지수로 표기가 안 되어있다. 만약에 다루는 숫자의 범위가 $10^{-8} \sim 10^{8}$ 과 같이 미소~극대 범위를 다룰 경우 지수 표기가 더 편할 수 있다. 그럴 때  `QDoubleSpinBox`를 상속하는 위젯을 만들어서 사용하면 된다.

아래 코드에서 `textFromValue`, `valueFromtText`, `validate`는 `QDoubleSpinBox`에서 사용하는 메소드라 아래처럼 오버라이딩했는데 이 중 **`textFromValue`**에서 본인이 원하는 스타일로 적용하면 된다.

```python
class ScientificDoubleSpinBox(QDoubleSpinBox) :  
    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)  
        self.setDecimals(8)  
        self.setStyleSheet(DOUBLESPINBOXSTYLE) # "{border: ;margin:;}" 처럼 미리 스타일 저장해서 적용
        self.setFixedWidth(14*10 + 12*2 + 2* 2)
  
    def textFromValue(self,value) :
	    # 숫자가 10^-3보다 작거나 10^8보다 크면 지수표기한다.
        if float(abs(value)) < 0.001 or len(str(value))>9 :  
            return f"{value:.3e}" # 과학적 표기법으로 변환  
        else :  
	        # 10^-3과 10^8 이내의 숫자는 그대로 표기한다.
            return f"{value}"  
  
    def valueFromText(self, text) :  
        return float(text) # 텍스트를 실수로 변환  
  
    def validate(self, text, pos) :  
        try :            
	        float(text)  
            return (QValidator.State.Acceptable, text, pos)  
        except ValueError:  
            return (QValidator.State.Intermediate, text, pos)
```

#### 파일관리하기
위와 같은 Style 종류들은 기능의 메인이 아니기 때문에 `main.py` 안에 작성하면 코드 관리하기만 불편해진다. 따라서 `style.py` 이라는 파일을 따로 만들어 관리하는 것을 추천한다.

예를 들어 다음 기능을 구현한다고 하자.
- *Title* 의 폰트는 `inter`, 크기는 20 px, 볼트체(black)로 한다.
- *propertycontainer* 
	- 테두리는 노란 실선 2px로 한다.
	- 바탕화면 색을 blue로 지정한다.
	- dropshadow를 적용한다.
- *property3* 은 소수점 여섯자리까지 다루며, $10^{-3}$ 미만, $10^{3}$이상의 실수가 들어가면 지수로 표기한다.

##### style.py
```python
from PyQt6.QtWidgets import QDoubleSpinBox, QGraphicsDropShadowEffect  
from PyQt6.QtGui import QValidator, QFont, QColor  
  
FONTS = "Inter"  
  
TITLEFONT = QFont(FONTS, 16, QFont.Weight.Black, False)  
TITLEFONT.setFamilies(["Inter", "NanumSquareNeo"]) # 한글 폰트는 Inter 대응이 안 됨  
  
CONTAINER = "{background-color:blue;border:2px solid yellow;}"  
  
SHADOW_COLOR = "#C0C0C0"  
SHADOW_OFFSET = 3  
SHADOW_BLUR = 12  
  
def applyShadow(target) :  
    effect = QGraphicsDropShadowEffect()  # PyQt6.QtWidget 안에 포함.  
    effect.setColor(QColor(SHADOW_COLOR))  
    effect.setOffset(SHADOW_OFFSET)  
    effect.setBlurRadius(SHADOW_BLUR)  
    target.setGraphicsEffect(effect)  
  
  
class ScientificDoubleSpinBox(QDoubleSpinBox):  
    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)  
        self.setDecimals(6)  
    def textFromValue(self, value):  
        # 숫자가 10^-3보다 작거나 10^8보다 크면 지수표기한다.  
        if float(abs(value)) < 10**(-3) or float(abs(value)) > 10**3:  
            return f"{value:.3e}"  # 과학적 표기법으로 변환  
        else:  
            # 10^-3과 10^8 이내의 숫자는 그대로 표기한다.  
            return f"{value}"  
  
    def valueFromText(self, text):  
        return float(text)  # 텍스트를 실수로 변환  
  
    def validate(self, text, pos):  
        try:            float(text)  
            return (QValidator.State.Acceptable, text, pos)  
        except ValueError:  
            return (QValidator.State.Intermediate, text, pos)
```

##### main.py 수정점

총 4군데 수정하면 된다. 
```python
# 아래 4줄 추가
try :  
    from style import *  
except ImportError :  
    from .style import * # 같은 파일 경로상 파일 불러오기
```

```python
# title QLabel 스타일 적용(.setFont)
self.title = QLabel("Class 1")  
self.title.setFont(TITLEFONT)  
self.title_hspacer = QWidget()  
self.title_hspacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
```

```python
# propertycontainer 수정
# property 구현  
self.propertycontainer = QWidget()  
# self.propertycontainer.setStyleSheet("border:2px solid gray;")  
self.propertycontainer.setObjectName("propertycontainer") # css ID 같은 역할  
self.propertycontainer.setStyleSheet("QWidget#propertycontainer" + CONTAINER)  
applyShadow(self.propertycontainer)  
self.bglayout.addWidget(self.propertycontainer)
```

```python
# property3 코드 변경
self.prop3_value = ScientificDoubleSpinBox()  
self.prop3_value.setMaximum(10**10)  
self.prop3_value.setMinimum(-(10**10))  
self.propertylayout.addWidget(self.prop3_value,1,1)
```

결과물은 아래와 같다.

![](/assets/img/res/Pasted%20image%2020241007010203.png)

- 다음 글 : [2024-09-03-PyQt6+Sqlite3](2024-09-03-PyQt6+Sqlite3.md)
## Reference
- **[(stackoverflow) pyinstaller :: win32ctypes.pywin32 에러 해결](https://stackoverflow.com/questions/77239487/win32ctypes-pywin32-pywintypes-error-when-using-pyinstaller-in-vs-code-possib)**
- [(stackoverflow) raspberrypi pip install 시 발생하는 externally-managed-environment 에러 해결 방법](https://stackoverflow.com/questions/75608323/how-do-i-solve-error-externally-managed-environment-every-time-i-use-pip-3)