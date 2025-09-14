---
title: Rust 동적메모리 할당
date: 2024-12-01 19:56:00 +0900
categories:
  - Programming
  - Rust
tags:
  - Rust
  - 자료구조
  - DP
pin: false
mermaid: "false"
image:
  path: /assets/img/thumbnail/rust_banner.png
incomplete: true
math: true
published: true
comments: true
---
## 목차
- [ ] Rust 동적 메모리
	- [ ] `Box`
	- [ ] `Rc`
	- [ ] `RefCell`
- [ ] 자료구조 구현하기

## Rust 동적메모리
런타임에 프로그램이 필요한 메모리를 할당하려면 동적메모리를 할댕하야 한다. 이는 컴파일 타임에 프로그램의 메모리 사용을 정확히 예측하기 어려울 때 사용된다.

### `Box`
`Box`를 사용하면 `Heap` 영역에 동적으로 메모리 할당을 받으며 스마트 포인터 역할을 한다.


![](/assets/img/res/Pasted%20image%2020241201195928.png)

![](/assets/img/res/Pasted%20image%2020241201195953.png)

### `Rc`
`Rc`는 reference-counting pointer인데, `Rc`로 관리되는 데이터는 공유가 가능해서 여러 변수가 동일한 값을 참조할 수 있도록 한다.

`Box`는 빌림 방식 외에는 공유가 불가능한데, `Rc`는 공유가 가능해서 여러 변수에 값을 공유해야 할 때 유연하게 사용할 수 있다.

![](/assets/img/res/Pasted%20image%2020241201204631.png)

![](/assets/img/res/Pasted%20image%2020241201204613.png)

20~26번 줄 사이에 있는 `p3`가 소멸되면서 참조횟수가 하나 줄어들었다.

#### `box`를 이용한 연결리스트
`ref` 개념과 `Option<>` enum을 활용해서 만들어야 한다.
```rust
struct Node {
	value: i32, // 노드의 값을 저장하는 i32 타입의 필드
	next: Option<Box<Node>>, // 다음 노드를 가리키는 필드, Option을 사용해 노드가 없을 수 있는 상황을 처리
}
```

```rust
impl Node{
	fn append(&mut self, elem: i32) {
		match self.next{
			Some(ref mut next) => { // 값이 존재하는 경우
				next.append(elem);
			}
			None=> {
				let node = Node{
					value: elem,
					next: None,
				};
				self.next = Some(Box::new(node));
			}
		}
	}
	fn list(&self) {
		print!("{},", self.value);
		match self.next{
			Some(ref 23anext) => next.list(),
			None => {}
		}
	}
}
```

```rust
// test code
fn main() {
	let mut head = Node {
		value : 1,
		next: None,
	};

	for i in 2..10 {
		head.append(i);
	}
	head.list();
}
```

![](/assets/img/res/Pasted%20image%2020241201205934.png)

#### 자료를 `head` 앞에 추가하는 연결리스트 만들기
`Rc`를 활용하면 [`box`를 이용한 연결리스트](#`box`를%20이용한%20연결리스트) 보다 쉽게 만들 수 있다. `Rc`를 이용하면 데이터 공유가 가능하기 때문에 더 유연하고 강력한 기능을 가진 연결리스트를 만들 수 있게 된다.

```rust
use std::rc::Rc;

struct Person{
	name: String,
	age: i32,
	next: Option<Rc<Person>>,
}

fn main() {
	// p1 노드 생성
	let p1 = Rc::new(Person {
		name: String::from("Luna"),
		age: 30,
		next: None,
	});

	let p2 = Rc::new(Person{
		name: String::from("Rust"),
		age:28,
		next: Some(p1.clone()), // Rust의 다음 노드를 Luna로 설정
		//Rc::clone을 사용해 참조 카운트를 증가시킴
	});

	print!("{} -> ", p2.name); // p2 이름 출력

	match &p2.next{
		Some(p) => {
			println!("{}", p.name);
		}
		None => {}
	};
}
```

![](/assets/img/res/Pasted%20image%2020241201210852.png)

```rust
// 새로운 노드를 head 앞에 추가
fn push_front(head:Rc<Person>, name:String, age:i32) -> Rc<Person> {
	//새로운 Person 노드를 생성합니다.
	// name과 age는 함수의 인자로 주어지며, next 필드는 기존 연결 리스트의 head를 가리키게 된다.

	let p = Rc::next(Person {
		name : name,
		age : age,
		next: Some(head.clone()), // 기존 head를 clone해 새 노드의 next로 설정한다.
	});

	p.clone() // 새로 생성된 노드의 Rc를 클론해 반환한다. 이제 p노드가 head가 된다.
}
```


```rust
// 테스트 코드
fn main() {
	let head = Rc::new(Person {
		name: String::from("Luna"),
		age: 30,
		next: None,
	});

	let head = push_front(head, String::from("Rust"), 10);
	let head = push_front(head, String::from("Wikidocs"), 20);

	let mut current = head.clone();

	loop {
		print("{} -> ", current.name);
		current = match &current.next{
			Some(p) => p,
			None => break,
		}.clone();
	}
}
```

![](/assets/img/res/Pasted%20image%2020241201212317.png)

### `RefCell`
`Rc`는 범용성이 높지만 **불변성(immutable)**을 가진 참조형이기 때문에 데이터를 변경할 수 없다.
그렇기 때문에 위에서 구현한 연결 리스트 노드를 수정하려고 해도 수정할 수 없다. `RefCell`은 변경 불가능한 변수를 임시로 변경 가능하게 해 주는 기능을 제공한다. 그래서 `Rc`와 함께 쓰는 경우가 많다.

```rust
use std::rc::Rc;
use std::cell::RefCell;

struct Person {
	name: String,
	age: i32,
	next: RefCell<Option<Rc<Person>>>, // RefCell로 감싸기
}

fn main() {
	let p1 = Rc::new(Person {
		name: String::from("Luna"),
		age: 30,
		next: RefCell::new(None),
	});
	let p2 = Rc::new(Person{
		name: String::from("Rust"),
		age:28,
		next: RefCell::new(None), // 처음에는 다음 노드가 없음.
		//Rc::clone을 사용해 참조 카운트를 증가시킴
	});

	// p1의 next 필드에 대한 가변 참조를 얻음.
	let mut next = p1.next.borrow_mut();
	*next = Some(p2.clone());
}
```

#### 자료 `tail` 뒤에 추가하는 연결 리스트 만들기
```rust
fn push_back(head:Rc<Person>, name:String, age: i32) -> Rc<Person> {
	let p = Rc::new(Person {
		name : name,
		age : age,
		next: RefCell::new(None),
	});

	// tail의 next 필드에 대한 가변 참조를 얻는다.
	// tail은 기존 리스트의 마지막 노드
	let mut next = head.next.borrow_mut();
	*next = Some(p.clone());

	p
}

fn main() {
	let mut head = Rc::new(Person {
		name: String::from("Luna"),
		age: 30,
		next: RefCell::new(None),
	});

	let tail = push_back(head.clone(), String::from("Rust"), 10);
	let tail = push_back(head.clone(), String::from("Wikidocs"), 20);

	let mut current = head.clone();
	loop {
		print("{} -> ", current.name);
		let t = current.clone();
		current = match &(*(t.next.borrow_mut())) {
			Some(p) => p,
			None => break,
		}.clone();
	}
}
```