# API 명세서

본 API 명세서는 **movies**, **communities**, **accounts** 세 가지 주요 모듈에 대한 엔드포인트를 포함하고 있습니다. 각 엔드포인트는 지원하는 HTTP 메서드, 요청 파라미터, 응답 형식 및 인증 요구 사항에 따라 분류되어 있습니다.

---

## 목차

- [API 명세서](#api-명세서)
  - [목차](#목차)
  - [Movies API](#movies-api)
    - [영화 목록 및 상세 정보](#영화-목록-및-상세-정보)
      - [목록 조회](#목록-조회)
      - [상세 정보 조회](#상세-정보-조회)
    - [영화 선택](#영화-선택)
      - [영화 선택/해제](#영화-선택해제)
    - [엔딩 관리](#엔딩-관리)
      - [엔딩 목록 조회](#엔딩-목록-조회)
      - [엔딩 상세 정보 및 삭제](#엔딩-상세-정보-및-삭제)
    - [댓글 관리](#댓글-관리)
      - [댓글 목록 및 생성](#댓글-목록-및-생성)
      - [댓글 삭제](#댓글-삭제)
    - [좋아요 기능](#좋아요-기능)
      - [엔딩 좋아요/좋아요 취소](#엔딩-좋아요좋아요-취소)
    - [랭킹 조회](#랭킹-조회)
      - [사용자 랭킹 조회](#사용자-랭킹-조회)
      - [엔딩 랭킹 조회](#엔딩-랭킹-조회)
  - [Communities API](#communities-api)
    - [게시글 목록 및 상세 정보](#게시글-목록-및-상세-정보)
      - [게시글 목록 조회](#게시글-목록-조회)
      - [게시글 생성](#게시글-생성)
      - [게시글 상세 정보 조회, 수정 및 삭제](#게시글-상세-정보-조회-수정-및-삭제)
    - [댓글 관리](#댓글-관리-1)
      - [댓글 목록 및 생성](#댓글-목록-및-생성-1)
      - [댓글 삭제](#댓글-삭제-1)
    - [좋아요 기능](#좋아요-기능-1)
      - [게시글 좋아요/좋아요 취소](#게시글-좋아요좋아요-취소)
  - [Accounts API](#accounts-api)
    - [사용자 계정 관리](#사용자-계정-관리)
      - [로그인, 로그아웃, 등록 등](#로그인-로그아웃-등록-등)
    - [사용자 프로필 조회 및 수정](#사용자-프로필-조회-및-수정)
      - [프로필 조회 및 수정](#프로필-조회-및-수정)
  - [공통 사항](#공통-사항)
    - [인증](#인증)
    - [오류 응답](#오류-응답)
    - [응답 형식](#응답-형식)

---

## Movies API

### 영화 목록 및 상세 정보

#### 목록 조회

- **URL:** `/api/v1/movies/`
- **Method:** `GET`
- **Authentication:** 필요 없음
- **설명:** 선택된 모든 영화의 목록을 조회합니다.
- **Response:**
  ```json
  [
    {
      "id": 1,
      "title": "영화 제목",
      "poster": "포스터 URL",
      "plot": "영화 줄거리",
      "is_selected": true
    },
    ...
  ]
  ```

#### 상세 정보 조회

- **URL:** `/api/v1/movies/<int:movie_pk>/`
- **Method:** `GET`
- **Authentication:** 필요 없음
- **설명:** 특정 영화의 상세 정보를 조회합니다.
- **Response:**
  ```json
  {
    "id": 1,
    "title": "영화 제목",
    "poster": "포스터 URL",
    "plot": "영화 줄거리",
    "is_selected": true
  }
  ```

### 영화 선택

#### 영화 선택/해제

- **URL:** `/api/v1/movies/select/`
- **Method:** `PUT`
- **Authentication:** 토큰 기반 인증 필요 (관리자)
- **설명:** 여러 영화를 한 번에 선택 또는 선택 해제합니다.
- **Request Body:**
  ```json
  {
    "selected_movies": [1, 2, 3]
  }
  ```
- **Response:**
  ```json
  {
    "message": "영화 선택이 업데이트되었습니다."
  }
  ```

### 엔딩 관리

#### 엔딩 목록 조회

- **URL:** `/api/v1/movies/altends/`
- **Method:** `GET`
- **Authentication:** 필요 없음
- **설명:** 모든 엔딩의 목록을 조회합니다.
- **Response:**
  ```json
  [
    {
      "id": 1,
      "movie_id": 1,
      "content": "엔딩 내용",
      "user_id": 1,
      "like_count": 10
    },
    ...
  ]
  ```

#### 엔딩 상세 정보 및 삭제

- **URL:** `/api/v1/movies/altends/<int:ending_pk>/`
- **Method:** `GET`, `DELETE`
- **Authentication:** `GET` 필요 없음, `DELETE`는 인증 필요
- **설명:** 특정 엔딩의 상세 정보를 조회하거나 삭제합니다.
- **Response (`GET`):**
  ```json
  {
    "id": 1,
    "movie_id": 1,
    "content": "엔딩 내용",
    "view": 100,
    "user_id": 1
  }
  ```
- **Response (`DELETE`):**
  - 상태 코드: `204 No Content`

### 댓글 관리

#### 댓글 목록 및 생성

- **URL:** `/api/v1/movies/altends/<int:ending_pk>/comments/`
- **Method:** `GET`, `POST`
- **Authentication:** `GET` 필요 없음, `POST`는 인증 필요
- **설명:** 특정 엔딩에 대한 댓글을 조회하거나 생성합니다.
- **Response (`GET`):**
  ```json
  [
    {
      "id": 1,
      "ending_id": 1,
      "user_id": 1,
      "content": "댓글 내용",
      "created_at": "2023-01-01T00:00:00Z"
    },
    ...
  ]
  ```
- **Response (`POST`):**
  ```json
  {
    "id": 2,
    "ending_id": 1,
    "user_id": 1,
    "content": "새로운 댓글 내용",
    "created_at": "2023-01-02T00:00:00Z"
  }
  ```

#### 댓글 삭제

- **URL:** `/api/v1/movies/altends/<int:comment_pk>/comments/delete/`
- **Method:** `DELETE`
- **Authentication:** 인증 필요
- **설명:** 특정 댓글을 삭제합니다.
- **Response:**
  - 상태 코드: `204 No Content`

### 좋아요 기능

#### 엔딩 좋아요/좋아요 취소

- **URL:** `/api/v1/movies/altends/<int:ending_pk>/likes/`
- **Method:** `POST`
- **Authentication:** 인증 필요
- **설명:** 특정 엔딩을 좋아요하거나 좋아요를 취소합니다.
- **Response:**
  ```json
  {
    "is_liked": true
  }
  ```

### 랭킹 조회

#### 사용자 랭킹 조회

- **URL:** `/api/v1/movies/ranking/user/`
- **Method:** `GET`
- **Authentication:** 필요 없음
- **설명:** 좋아요 수 기준 상위 3명의 사용자 랭킹을 조회합니다.
- **Response:**
  ```json
  {
    "1": {
      "user_name": "사용자1",
      "total_likes": 50,
      "user_id": 1
    },
    "2": {
      "user_name": "사용자2",
      "total_likes": 30,
      "user_id": 2
    },
    "3": {
      "user_name": "사용자3",
      "total_likes": 20,
      "user_id": 3
    }
  }
  ```

#### 엔딩 랭킹 조회

- **URL:** `/api/v1/movies/ranking/ending/`
- **Method:** `GET`
- **Authentication:** 필요 없음
- **설명:** 좋아요 수 기준 상위 6개의 엔딩을 조회합니다.
- **Response:**
  ```json
  {
    "1": {
      "movie": "영화1",
      "prompt": "프롬프트 내용",
      "like_count": 100,
      "ending_id": 1
    },
    ...
  }
  ```

---

## Communities API

### 게시글 목록 및 상세 정보

#### 게시글 목록 조회

- **URL:** `/api/v1/communities/`
- **Method:** `GET`
- **Authentication:** 필요 없음
- **설명:** 모든 게시글의 목록을 조회합니다.
- **Response:**
  ```json
  [
    {
      "id": 1,
      "title": "게시글 제목",
      "content": "게시글 내용",
      "user_id": 1,
      "view": 100,
      "like_count": 10
    },
    ...
  ]
  ```

#### 게시글 생성

- **URL:** `/api/v1/communities/`
- **Method:** `POST`
- **Authentication:** 인증 필요
- **설명:** 새로운 게시글을 생성합니다.
- **Request Body:**
  ```json
  {
    "title": "새 게시글 제목",
    "content": "새 게시글 내용"
  }
  ```
- **Response:**
  ```json
  {
    "id": 2,
    "title": "새 게시글 제목",
    "content": "새 게시글 내용",
    "user_id": 1,
    "created_at": "2023-01-02T00:00:00Z"
  }
  ```

#### 게시글 상세 정보 조회, 수정 및 삭제

- **URL:** `/api/v1/communities/<int:article_pk>/`
- **Method:** `GET`, `PUT`, `DELETE`
- **Authentication:** `GET` 필요 없음, `PUT` 및 `DELETE`는 인증 필요
- **설명:** 특정 게시글의 상세 정보를 조회하거나 수정, 삭제합니다.
- **Response (`GET`):**
  ```json
  {
    "id": 1,
    "title": "게시글 제목",
    "content": "게시글 내용",
    "view": 100,
    "user_id": 1
  }
  ```
- **Response (`PUT`):**
  ```json
  {
    "id": 1,
    "title": "수정된 제목",
    "content": "수정된 내용",
    "user_id": 1
  }
  ```
- **Response (`DELETE`):**
  - 상태 코드: `204 No Content`

### 댓글 관리

#### 댓글 목록 및 생성

- **URL:** `/api/v1/communities/<int:article_pk>/comments/`
- **Method:** `GET`, `POST`
- **Authentication:** `GET` 필요 없음, `POST`는 인증 필요
- **설명:** 특정 게시글에 대한 댓글을 조회하거나 생성합니다.
- **Response (`GET`):**
  ```json
  [
    {
      "id": 1,
      "article_id": 1,
      "user_id": 1,
      "content": "댓글 내용",
      "created_at": "2023-01-01T00:00:00Z"
    },
    ...
  ]
  ```
- **Response (`POST`):**
  ```json
  {
    "id": 2,
    "article_id": 1,
    "user_id": 1,
    "content": "새로운 댓글 내용",
    "created_at": "2023-01-02T00:00:00Z"
  }
  ```

#### 댓글 삭제

- **URL:** `/api/v1/communities/<int:comment_pk>/comments/delete/`
- **Method:** `DELETE`
- **Authentication:** 인증 필요
- **설명:** 특정 댓글을 삭제합니다.
- **Response:**
  - 상태 코드: `204 No Content`

### 좋아요 기능

#### 게시글 좋아요/좋아요 취소

- **URL:** `/api/v1/communities/<int:article_pk>/likes/`
- **Method:** `POST`
- **Authentication:** 인증 필요
- **설명:** 특정 게시글을 좋아요하거나 좋아요를 취소합니다.
- **Response:**
  ```json
  {
    "is_liked": true
  }
  ```

---

## Accounts API

### 사용자 계정 관리

#### 로그인, 로그아웃, 등록 등

- **URL:** `/api/v1/accounts/`
- **Method:** `GET`, `POST` 등
- **Authentication:** 필요에 따라 다름
- **설명:** `dj_rest_auth` 패키지를 통해 사용자 인증 및 등록을 관리합니다.

### 사용자 프로필 조회 및 수정

#### 프로필 조회 및 수정

- **URL:** `/api/v1/accounts/<int:user_pk>/`
- **Method:** `GET`, `PUT`
- **Authentication:** `PUT`은 인증 필요
- **설명:** 특정 사용자의 프로필을 조회하거나 수정합니다.
- **Response (`GET`):**
  ```json
  {
    "id": 1,
    "username": "사용자이름",
    "nickname": "닉네임",
    "email": "user@example.com",
    ...
  }
  ```
- **Response (`PUT`):**
  ```json
  {
    "id": 1,
    "username": "사용자이름",
    "nickname": "수정된 닉네임",
    "email": "user@example.com",
    ...
  }
  ```

---

## 공통 사항

### 인증

- 대부분의 `POST`, `PUT`, `DELETE` 메서드는 **토큰 기반 인증**이 필요합니다.
- `GET` 메서드는 일부 엔드포인트에서 인증 없이 접근할 수 있습니다.

### 오류 응답

- **400 Bad Request:** 잘못된 요청 데이터
- **401 Unauthorized:** 인증 실패 또는 누락
- **403 Forbidden:** 권한 없음
- **404 Not Found:** 리소스 존재하지 않음
- **500 Internal Server Error:** 서버 내부 오류

### 응답 형식

- 모든 응답은 JSON 형식으로 반환됩니다.
- 성공 시 데이터와 함께 적절한 상태 코드가 반환됩니다.
- 실패 시 오류 메시지와 상태 코드가 반환됩니다.

---

이상으로 API 명세서를 마칩니다. 각 엔드포인트의 세부 사항은 실제 구현에 따라 달라질 수 있으므로, 최신 코드를 참고하여 사용하시기 바랍니다.