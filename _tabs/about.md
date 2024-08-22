---
# the default layout is 'page'
icon: fas fa-info-circle
order: 4
---
<script src="https://cdn.jsdelivr.net/npm/d3@7.9.0/dist/d3.min.js"></script>

<h1>Hello World!</h1>
<div id="chart"></div>

<script defer type="application/json" id="about-data">
{
	
}
</script>
<script defer src="/assets/js/about_node.js"></script>

> 비개발자의 유사 개발블로그 겸 일기장입니다.


# 기술 스택
%%`D3` 라이브러리를 활용해서 추가할려고 하는 내용%%

- Python : PyQt + `numpy/pandas/scipy` + 시각화
- Rust
- Web : Svelte + JS
	- JS 라이브러리를 활용한 각종 프로젝트
- Flutter(TBD)
	- Mobile cross platform
- Web + Gui Application
	- Electron
	- Tauri
- Excel, PPT, AI
- 그 외 기타 공유하고 싶은 내용 위주로 작성


### 블로그 앞으로 업데이트 할 내용
D3 라이브러리 위주로 작성. 모바일 화면(768px 이하)와 데스크톱 모드 모두 고려하자.
- about 전체 보기 : D3-force
	- [Force-directed tree](https://observablehq.com/@d3/force-directed-tree?intent=fork)
	- [Force-directed tree2](https://observablehq.com/@d3/force-directed-graph/2?intent=fork)
	- [Disjoint force-directed graph](https://observablehq.com/@d3/disjoint-force-directed-graph/2?intent=fork)
- categories : (cascaded / zoomable)treemap
	- [Sequences Sunburst](https://observablehq.com/@kerryrodden/sequences-sunburst)
	- [zoomable treemap](https://observablehq.com/@d3/zoomable-treemap?intent=fork)
	- [cascaded treemap](https://observablehq.com/@d3/cascaded-treemap?intent=fork)
	- [tree of life](https://observablehq.com/@d3/tree-of-life?intent=fork)
- tag, 조회수, 댓글 등등.
	- [Bubble Chart](https://observablehq.com/@d3/bubble-chart/2?intent=fork)
- 활동내역 : heatmap(문서 종류, push)
	- [Calendar](https://observablehq.com/@d3/calendar/2?intent=fork)
	- [Calendar + category](https://observablehq.com/@d3/the-impact-of-vaccines?intent=fork)
애니메이션 기능은 잘못 넣으면 웹 전체가 느려지니 규모가 엄청 커졌을 때만 고려하자. 나만 그런지 모르겠지만 [이 예제](https://observablehq.com/@d3/animated-treemap?intent=fork)는 이상하게도 다른 애니메이션 예제와 다르게 웹 브라우저 전체를 버벅이게 만든다.
