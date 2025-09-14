---
title: (rust) 동시성, 입출력, 네트워킹, IPC
date: 2025-06-14 16:00:00 +0900
categories: 
tags: 
pin: false
mermaid: "false"
image: 
incomplete: true
math: true
published: true
comments: true
---
보통 I/O 작업은 시간이 오래 걸리기 때문에 스레드를 활용해서 읽고 스레드에서 `panic!`을 처리하자. 

```rust
use std::fs::File;
use std::io::{BufReader, BufRead};
use std::thread;
use std::env;
use std::path::PathBuf;

fn main() {
    let current_dir: PathBuf = env::current_dir().expect("cannot get current directory path");
    println!("{}", current_dir.display());

    let handle = thread::spawn(|| {
        let file = File::open("./src/file.txt").unwrap(); // cmd 상 현재 위치 기준으로 인식함.
        let reader = BufReader::new(file);
        for line in reader.lines() {
            let txt = line.unwrap(); // 
            println!("{}", txt);
        }
    });

    // handle.join().unwrap(); // 스레드가 끝날 때까지 기다린다.
    match handle.join() {
        Ok(_) => {},
        Err(e) => {
            println!("스레드 내부에서 오류가 발생했습니다. {:?}", e);
        }
    };
}
```

채널(**channel**)은 여러 스레드가 안전하게 데이터를 주고 받을 수 있는 방법을 제공한다. 

```rust
use std::thread;
use std::sync::mpsc;

fn main() {
    let (tx, rx) = mpsc::channel();

    thread::spawn(move || {
        let mut sum = 0;
        for i in 1..101 {
            sum = sum+i;
        }
        tx.send(sum).unwrap(); // 이제 부터 해당 tx 변수는 thread가 소유권을 가지게 된다. move 
    });

    let sum = rx.recv().unwrap();
    println!("1부터 100까지의 합: {}", sum);
}
```

```rust
use std::thread;
use std::sync::mpsc;

fn main() {
    let (tx1, rx) = mpsc::channel();
    let tx2 = mpsc::Sender::clone(&tx1); // tx1 복제
    thread::spawn(move || {
        let mut sum = 0;
        for i in 1..51 {
            sum = sum+i;
        }
        tx1.send(sum).unwrap(); 
    });

    thread::spawn(move || {
        let mut sum =0;
        for i in 51..101 {
            sum = sum +i;
        }
        tx2.send(sum).unwrap();
    });

    let mut sum = 0;
    for val in rx {
        println!("수신 : {}", val);
        sum = sum + val;
    }
    println!("1~100 까지의 합 : {}", sum);
}
```

### async/await
러스트가 비동기 프로그래밍하려면 `Cargo.toml`-`[dependency]`에서 `future` 크레이트를 추가해야 한다.

```rust
use futures::executor::block_on;

async fn calc_sum(start: i32, end: i32) -> i32 {
    let mut sum = 0;
    for i in start..=end {
        sum += i;
    }
    sum
}

fn main() {
    let future = calc_sum(1,100);
    let sum = block_on(future);
    println!("1부터 100까지의 합: {}", sum);
}
```

`Async` 사용할 때 `thread`관련 API 호출을 신중하게 해야 한다.

#### tokio 사용하기

```toml
[dependencies]
tokio = {versikon = "1.25.0", features = ["full"]}
```

