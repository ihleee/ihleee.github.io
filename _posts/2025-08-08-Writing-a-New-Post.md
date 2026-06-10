---
title: Writing a New Post
date: 2025-08-08 16:01:01 +0900
categories: [Blog]
tags: [github,pages,chirpy]     # TAG names should always be lowercase
math: true
mermaid: true
---

새로운 포스트를 작성하는 방법입니다.

이 가이드는 **VS Code에서 Git을 사용해 글을 쓰고 올리는 과정**을 중심으로 설명합니다.

-----

###  1. VS Code에서 Git 연결하기

1.  **VS Code 열기:** `username.github.io` 프로젝트 폴더를 VS Code에서 엽니다.
2.  **소스 제어 탭 열기:** 왼쪽에 있는 소스 제어(Source Control) 아이콘을 클릭합니다. (트리 형태의 아이콘)
3.  **변경 사항 확인:** `_posts` 폴더에 새롭게 추가한 파일이 **'변경 내용'** 목록에 나타나는 것을 확인할 수 있습니다.

###  2. 글 작성 준비

새로운 포스트 파일은 `_posts` 폴더 안에 만들어야 합니다. 파일 이름은 **`YYYY-MM-DD-제목.md`** 형식으로 지정해야 Jekyll이 포스트로 인식합니다.

**파일 이름 예시:**
`2025-08-08-새로운-포스트-작성법.md`



###  3. 포스트 내용 작성

새로 만든 파일에 아래와 같이 **Front Matter**를 먼저 작성하고, 그 아래에 본문 내용을 마크다운으로 작성하세요.

#### **Front Matter (설정)**

```yaml
---
title: 새로운 포스트 작성법
date: 2025-08-08 16:01:01 +0900
categories: [Blog]
tags: [tutorial, jekyll, vscode]
math: true
mermaid: true
---
```

  - **`title`**: 포스트 제목입니다.
  - **`date`**: 작성 날짜와 시간입니다.
  - **`categories`**: 글이 속할 카테고리입니다.
  - **`tags`**: 글의 핵심 키워드입니다.
  - **`math`, `mermaid`**: 필요에 따라 `true`로 설정하면 수학 공식이나 다이어그램을 사용할 수 있습니다.

#### **본문 예시 (마크다운)**

````markdown
## 1. 글 작성 환경 설정

VS Code에서 포스트를 작성하고 Git으로 관리하는 방법을 알아보겠습니다.

### 1-1. VS Code에서 Git 연결하기

VS Code의 '소스 제어' 탭을 통해 변경 사항을 쉽게 관리할 수 있습니다.

## 2. 마크다운 문법 예시

### 헤딩
# 가장 큰 제목
### 중간 제목
#### 작은 제목

### 목록
* 순서 없는 목록
* 순서 없는 목록

### 코드 블록
```markdown
# 코드 블록은 이렇게 작성합니다.
````

## 3\. 업로드 및 배포

### 3-1. 커밋 (Commit)

1.  VS Code 소스 제어 탭에서 변경된 파일 위에 마우스를 올립니다.
2.  '**+**' 버튼을 눌러 스테이지(Staged Changes)에 올립니다.
3.  상단 입력창에 커밋 메시지(예: `feat: 첫 번째 포스트 작성`)를 작성합니다.
4.  '**✔️**' 버튼을 눌러 커밋합니다.

### 3-2. 푸시 (Push)

VS Code 하단의 상태바에 있는 **`↑`** 버튼을 눌러 GitHub 저장소에 변경 내용을 푸시합니다. 잠시 후 GitHub Actions가 블로그를 자동으로 빌드하고 배포합니다.

```
---

###  4. 최종 확인

커밋과 푸시가 완료되면, GitHub 저장소의 **`Actions`** 탭에서 빌드가 성공했는지 확인해 보세요. 초록색 체크 표시가 뜨면 블로그에 새로운 글이 성공적으로 게시된 것입니다.
```



### dummy
How to write a new post,


\begin{equation}
1+x=y
\label{eq:xy}
\end{equation}

위의 공식은 \eqref{eq:xy} 입니다.

\begin{equation}
1+y=x
\label{eq:yx}
\end{equation}


위의 공식은 \eqref{eq:yx} 입니다.

```mermaid
  graph TD;
  A-->B;
  A-->C;
  B-->D;
  C-->D;
```

sdfsd
