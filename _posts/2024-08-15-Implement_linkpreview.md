---
title: (blog)linkpreview를 github.io 블로그에 적용하기
date: 2024-08-15 22:53:00 +0900
categories:
  - Doodle
  - Diary
permalink: 
tags:
  - diary
  - blog
  - obsidian
  - Web
comments: true
published: true
math: true
image: 
incomplete: false
---
> \[2024-08-15\] [2024-08-08-Customize Github Blog2](2024-08-08-Customize%20Github%20Blog2.md) 파일이 지나치게 길어져 별도의 파일로 분리합니다.
# [Linkpreview 설치하기](https://github.com/ysk24ok/jekyll-linkpreview)

```ruby
gem install jekyll-gist jekyll-coffeescript jekyll-remote-theme some-other-jekyll-plugin jekyll-linkpreview
```

그리고 `/assets/css` 폴더 내에 `linkpreview.css` 파일을 생성한다. 내용은 [여기 페이지 코드](https://github.com/ysk24ok/jekyll-linkpreview/blob/master/assets/css/linkpreview.css)대로 채우면 된다.

[이전 블로그 꾸미기 포스트](2024-08-04-Customize%20Github%20Blog1.md#Rich%20link(linkpreivew)%20구현하기)에서 rich link 구현을 실패했었는데, 위 플러그인을 설치하고 아래와 같은 문법으로 작성하면 linkpreview 링크를 만들 수 있다. 

{% raw %}
```liquid
{% linkpreview "url" %}
```
{% endraw %}

Linkpreview의 기본 css 스타일과 Chirpy 스타일과 조금 잘 안 어울린다. 그에 맞게 약간의 수정이 필요하다. 개발자 도구를 열어보면 `_layouts/home.html`를 열어보면 이 테마의 preview는 `bootstrap`의 `card`인 걸 확인할 수 있다. 

그리고 `.row` 코드와 같이 특정 폭 크기에 따라 형태가 바뀌는 `@media`도 적용되어 있다. `home.html`의 일부 코드는 아래와 같다.
{% raw %}
```html
<!--home.html-->
<div id="post-list" class="flex-grow-1 px-xl-1">
  {% for post in posts %}
    <article class="card-wrapper card">
      <a href="{{ post.url | relative_url }}" class="post-preview row g-0 flex-md-row-reverse">
        {% assign card_body_col = '12' %}
        
        {% if post.image %}
          {% assign src = post.image.path | default: post.image %}
          {% unless src contains '//' %}
            {% assign src = post.media_subpath | append: '/' | append: src | replace: '//', '/' %}
          {% endunless %}
  
          {% assign alt = post.image.alt | xml_escape | default: 'Preview Image' %}
  
          {% assign lqip = null %}
  
          {% if post.image.lqip %}
            {% capture lqip %}lqip="{{ post.image.lqip }}"{% endcapture %}
          {% endif %}
  
          <div class="col-md-5">
            <img src="{{ src }}" alt="{{ alt }}" {{ lqip }}>
          </div>
  
          {% assign card_body_col = '7' %}
        {% endif %}
  
        <div class="col-md-{{ card_body_col }}">
          <div class="card-body d-flex flex-column">
            <h1 class="card-title my-2 mt-md-0">{{ post.title }}</h1>
  
            <div class="card-text content mt-0 mb-3">
              <p>{% include post-description.html %}</p>
            </div>
  
            <div class="post-meta flex-grow-1 d-flex align-items-end">
              <div class="me-auto">
                <!-- posted date -->
                <i class="far fa-calendar fa-fw me-1"></i>
                {% include datetime.html date=post.date lang=lang %}
  
                <!-- categories -->
                {% if post.categories.size > 0 %}
                  <i class="far fa-folder-open fa-fw me-1"></i>
                  <span class="categories">
                    {% for category in post.categories %}
                      {{ category }}
                      {%- unless forloop.last -%},{%- endunless -%}
                    {% endfor %}
                  </span>
                {% endif %}
              </div>
  
              {% if post.pin %}
                <div class="pin ms-1">
                  <i class="fas fa-thumbtack fa-fw"></i>
                  <span>{{ site.data.locales[lang].post.pin_prompt }}</span>
                </div>
              {% endif %}
            </div>
            <!-- .post-meta -->
          </div>
          <!-- .card-body -->
        </div>
      </a>
    </article>
  {% endfor %}
</div>
<!-- #post-list -->
```
{% endraw %}


![bootstrap_card](assets/img/res/bootstrap_card.gif)

그리고 아래 사진과 같이 `naver`, `google` 같이 *Open Graph protocol metadata* (줄여서 `og`) 가 없는 경우도 있으니 이 때 사용하는 `linkpreview_nog.html`도 별도로 만들어두자.

> `linkpreview_nog.html` 없을 경우 나오는 화면
>![linkpreview_nog.html을 만들어두지 않은 경우](/assets/img/res/Pasted%20image%2020240811032023.png)
{: .prompt-warning }

![](assets/img/res/Pasted%20image%2020240811114936.png)

#### 1. linkpreview.html 
- path : `/_includes/linkpreview.html`
- 이상하게도 `<a>` 태그 안에 `<div>` 태그들을 집어넣을 수 없어 위의 `home.html` 처럼 짜기가 어려웠다.
	- [여기 블로그 글](https://velog.io/@jongk91/%EA%B0%84%EB%8B%A8-a%ED%83%9C%EA%B7%B8-%EC%A0%84%EC%B2%B4%EC%A0%81%EC%9A%A9)을 참고하여 `<a>` 태그가 `div.card` 전체를 차지하도록 만드는 방식으로 구현했다.

{% raw %}

```html
<!--linkpreview.html-->
<link rel="stylesheet" type = "text/css" href="/assets/css/linkpreview.css" media="screen">
  
<div class="card bg-transparent jekyll-linkpreview-wrapper">
  <a href="{{url}}" class="post-preview jekyll-linkpreview-linkbox"></a>
    <div class ="post-preview row g-0 flex-md-row-reverse jekyll-linkpreview-inner">
        {% assign card_body_col = '12' %}
  
        {% if image %}
          {% assign src = image.path | default: image %}
          {% unless src contains '//' %}
            {% assign src = post.media_subpath | append: '/' | append: src | replace: '//', '/' %}
          {% endunless %}
  
          {% assign alt = image.alt | xml_escape | default: 'Preview Image' %}
  
          {% assign lqip = null %}
  
          {% if image.lqip %}
            {% capture lqip %}lqip="{{ image.lqip }}"{% endcapture %}
          {% endif %}
  
          <div class="col-md-5">
            <div class="preview-img jekyll-linkpreview-img-wrapper">
              <img src="{{src}}" alt="{{alt}}" {{lqip}}>
            </div>
          </div>
  
          {% assign card_body_col = '7' %}
        {% endif %}
  
        <div class="col-md-7">
            <div class="card-body d-flex flex-column">
                <h1 class="card-title my-2 mt-md-0 jekyll-linkpreview-title">{{ title }}</h1>
                <div class="card-text mt-0">
                    <p class = "jekyll-linkpreview-description">{{ description }}</p>
                </div>
                <span class="jekyll-linkpreview-domain">
                  {{ domain }}
                </span>
            </div>
        </div>
    </div>
</div>
```
{% endraw %}
#### 2. linkpreview_nog.html
- path : `/_includes/linkpreview_nog.html`

```html
<link rel="stylesheet" type = "text/css" href="/assets/css/linkpreview.css" media="screen">

<div class="card bg-transparent jekyll-linkpreview-wrapper">
  <a href="{{url}}" class="post-preview jekyll-linkpreview-linkbox"></a>
    <div class ="post-preview row g-0 flex-md-row-reverse jekyll-linkpreview-inner">
        <div class="col-md-12">
            <div class="card-body d-flex flex-column">
                <h1 class="card-title my-2 mt-md-0 jekyll-linkpreview-title">{{ title }}</h1>
                <div class="card-text mt-0">
                    <p class = "jekyll-linkpreview-description">{{ description }}</p>
                </div>
                <span class="jekyll-linkpreview-domain">
                  {{ domain }}
                </span>
            </div>
        </div>
    </div>
</div>
```

#### 3. linkpreview.css 
- path : `/assets/css/linkpreview.css`
- `card`, `post-preview` 같은 class는 *Chirpy* 블로그에 내장되어 있는 css를 재활용한 것이다.

```css
.jekyll-linkpreview-wrapper{
  margin-bottom:1.2rem;
}
  
.jekyll-linkpreview-inner {
  cursor: pointer;
}
  
.jekyll-linkpreview-linkbox{
  position: absolute;
  width: 100%;
  height: 100%;
  z-index:2;
  border:none !important;
  border-radius: 0.375rem;
  background-color: transparent;
}
  
.jekyll-linkpreview-img-wrapper{
  height:100%;
  display:flex;
  flex-direction: column;
  justify-content: center;
  padding-right:0;
}
  
.jekyll-linkpreview-title{
  font-size:1.25rem;
  font-weight: 400;
  color: var(--heading-color);
}
  
.jekyll-linkpreview-description{
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
  overflow: hidden;
  color:var(--text-color);
  
  margin: 0;
}
  
.jekyll-linkpreview-domain{
  color:var(--text-muted-color);
  text-decoration: underline;
  text-underline-offset: 0.2rem;
}
```


#### linkpreview 결과물
아직 그림파일 크기 조절이 내맘대로 안 되서 아쉬운데 추후에 시간되면 추가 보완해볼 예정이다.

{% linkpreview "https://github.com/ysk24ok/jekyll-linkpreview" %}

{% linkpreview "https://www.google.com" %}

{% linkpreview "https://www.naver.com" %}

{% linkpreview "https://www.github.com" %}

#### `a tag is missing a reference` Failure 해결방안
`2024-08-11` localhost에서는 빌드가 되지만 github Action에서는 빌드가 안되는 문제가 발생했다. 이는 local에서는 `bundle exec jekyll serve`로 빌드하지만 Action에서는 `htmlproofer`를 동작시키는데 여기서 `a tag is missing a reference`라는 문제가 발생한다.
![](/assets/img/res/Pasted%20image%2020240811163621.png)

![](/assets/img/res/Pasted%20image%2020240811170723.png)
예를 들어, `404.html` 파일에 보면  `<a href =""` 과 같이 비어있는 코드를 보면 failure를 띄운다. 
그렇기 때문에 아래와 같이 코드를 수정해 `url`이  비어 있는 경우 `"\"`로 빌드할 수 있게 만든다.

{% raw %}
```html
<!--linkpreview.html-->
<!--linkpreview_nog.html-->
<link rel="stylesheet" type = "text/css" href="/assets/css/linkpreview.css" media="screen">
  
<div class="card bg-transparent jekyll-linkpreview-wrapper">
  {% assign og_url = "/" %}
  {% if url and url != ""%}
    {% assign og_url = url%}
  {% endif %}
  <a href="{{og_url}}" class="post-preview jekyll-linkpreview-linkbox"></a>
    <!-- 생략 -->
```

liquid syntax로 `{% if page.linkpreview %} ~ {% endif %}` 설정해보려고 했지만 잘 인식이 안 되었다(다른 `page.comments`, `page.title`은 잘만 인식되었다). 시간되면 이부분도 손 볼 예정이다. <span id="Fine">■</span>

{% endraw %}

> `[이렇게 텍스트]()` 만 적어놓고 링크 넣는칸을 비워두면 `a tag is missing a reference` 에러가 발생하니 비워두지 않도록 주의하자.
{: .prompt-warning }

---
### 사용 후 이슈 모음
#### 2024-08-21
- 항상 모든 사이트의 `og:img`를 정상적으로 가져오지 못한다.
	- 그 중 redirect하는 사이트가 있으면 github action - **`htmlproof` 단계에서 `fail`**을 일으킬 수 있다.
- 그리고 `linkpreview`를 사용할 수록 `/_cache` 폴더 내 `json` 파일이 쌓인다.
	- 이 파일들을 삭제하고 처음 localbuild할 때 걸리는 시간은 `linkpreview` 불러올 횟수만큼 추가적으로 걸린다.
	- 용량은 1 KB 내외로 작으나 vsc로 블로그 편집할 때 explorer에 공간 차지해서 살짝 귀찮다. 

>**따라서 아무 레퍼런스에 대해서 linkpreview를 적용하지 말고 강조하고 싶은 외부링크에 대해서만 linkpreview를 적용하자.** 
{: .prompt-tip}

# Reference
1. **[Linkpreview plugin github 주소](https://github.com/ysk24ok/jekyll-linkpreview)**
2. [a태그 안에 div 안 들어갈 경우..](https://velog.io/@jongk91/%EA%B0%84%EB%8B%A8-a%ED%83%9C%EA%B7%B8-%EC%A0%84%EC%B2%B4%EC%A0%81%EC%9A%A9)
3. [`a` tag is missing a reference](https://talk.jekyllrb.com/t/chirpy-theme-a-tag-is-missing-a-reference/8731/2)