---
title: Rust의 String에 대해서 알아보기
date: 2024-08-27 01:23:00 +0900
categories:
  - Programming
  - Rust
tags:
  - Rust
  - cpp
  - string
  - python
pin: false
mermaid: "false"
image: 
incomplete: true
math: true
published: false
comments: true
---
- 이전 글 : [2024-08-14-Rust_comparison_with_other_lang](2024-08-14-Rust_comparison_with_other_lang.md)
- 공식문서 : [8. 컬렉션 > 8.2 스트링](https://rinthel.github.io/rust-lang-book-ko/ch08-02-strings.html)

---

## 공식문서?

>`String` 타입의 특징
>- rust의 표준 라이브러리를 통해 제공되는 타입
>- 커질 수 있고, 가변적이다.
>- 소유권을 가지고 있고
>- **UTF-8**로 인코딩된 스트링 타입이다. 
>- rust의 표준 라이브러리는 `&str`, `String` 외에 추가적인 몇 가지 타입을 제공한다.
>	- `OsString`, `OsStr` : 경로 관련 스트링, **Non UTF-8** 문자열 필요할 때 사용.
>	- `CString`, `CStr`
{: .prompt-info}

### 새로운 스트링 생성하기
- 비어있는 새로운 `String` 생성하기
```rust
let mut s = String::new();
```

- 문자열을 통해 `String` 타입 받는 세 가지 방법
```rust
// 1. 문자열 -> 변수 -> to_string
let data = "initial contents";
let s1 = data.to_string();

// 2. 문자열.to_string()
let s2 = "initial contents".to_string();

// 3. String::from()
let s3 = String::from("initial contents");
```

이 글을 쓰게 된 가장 큰 이유는 `"initial contents"`와 `String::from("initial contents")`, `&str` 의 차이점이 아직도 잘 몰라서다. Rust는 왜 문자열을 다루는 타입만 최소 3가지를 요구할까?

- `"initial contents"` : 문자열 [리터럴](2024-08-18-Discipline%20for%20Flexible%20Programming1.md#Reference)
	- **Literal** : 값 자체를 말한다.
- `String::from("initial contents")` : `String` 타입
- `str` : `String slice` 타입
	- 일반적으로 슬라이싱을 위해 borrowed 형태인 `&str`로 많이 쓰인다.

이를 *VSC + rust-analyzer* 로 확인해봤다. 

![](/assets/img/res/Pasted%20image%2020240827015633.png)

그랬더니 1번 문자열을 보면 *rust-analyzer* 는 `&str` 타입으로 인식하고 있다.
그리고 이해가 안 되는 부분이 2가지 정도 있는데
- `String` 타입은 보통 소유권을 가지고 있어 다른 변수로 소유권이 넘어가면 이전 변수는 사용할 수 없다. 
	- 그런데, `let s1`에서 `data.clone().to_string()`이 아닌 `data.to_string()`으로 값을 가져오는데 `data` 변수를 사용할 수 있다.
- 문자열 리터럴과 `&str`은 진짜로 같은 타입인지? 
	- 아래 코드와 실행 결과문을 확인해보자.

```rust
use std::any::type_name;

fn type_of<T>(_: T) -> &'static str {
    type_name::<T>()
}

fn main() {
    // 1. 문자열 -> 변수 -> to_String
    let data = "initial contents";
    let hello_in_korean = "안녕하세요.";
    let s1 = data.to_string();

    println!("type of data : {}, {}", type_of(data), type_of(&data));
    println!("type of literal Korean : {}, {}", type_of(hello_in_korean), type_of(&hello_in_korean));
    println!("type of s1 : {}, {}", type_of(s1.clone()), type_of(&s1));
    // 이하 생략
```

![](/assets/img/res/Pasted%20image%2020240827020005.png)

- `UTF-8` 로 치환할 때마다 문자 하나당 3 bytes로 쪼갠다. 
- [ ] 디버깅시 데이터 형태 비교
	- [ ] cpp
	- [ ] python
- [ ] 리터럴과 String 비교하기
	- [ ] 메모리 static과 heap 관점
	- [ ] `mutable`과 `immutable`한 관점
	- [ ] Stack overflow에서 물어본 `io::stdin()::read_line(&mut )`일 경우 메모리 어디에 저장되는지? (이건 런타임에서 결정되니까)
- [ ] 
>`&str`과 `&String`은 다르다.
>{: .prompt-warning}
### C++, Python과 비교하기


## Reference 
- [How to check type of variable in Rust](https://users.rust-lang.org/t/how-check-type-of-variable/33845)
- [(Stack overflow)String literal 메모리 위치?](https://stackoverflow.com/questions/77591134/are-rust-string-literal-values-stored-on-the-heap)
- 