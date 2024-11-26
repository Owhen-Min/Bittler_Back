---

---
# BackEnd
---
## 0. INDEX
---
1. 기술 스택
2. 설치 및 실행 방법
3. 구성 요소 설명
4. 환경 변수 설정
5. 기타 참고 사항

## 1. 기술 스택
---
이 Django 프로젝트는 다음과 같은 기술 스택과 라이브러리를 사용합니다:

#### **1) 프레임워크 및 언어**

- Python 3
- Django 4.2.16 (웹 프레임워크)
- Django REST Framework (API 설계 및 관리)
- SQLite3 (기본 데이터베이스)

#### **2)인증 및 권한 관리**

- `dj-rest-auth`: RESTful 인증 및 권한 처리
- `django-allauth`: 소셜 인증 및 사용자 관리
- `rest_framework.authtoken`: 토큰 기반 인증

#### **3) 환경 변수 관리**

- `python-decouple`: `.env` 파일을 통한 환경 변수 관리

#### **4) CORS 설정**

- `django-cors-headers`: 프론트엔드와의 CORS 정책 처리

#### **5) 이미지 및 파일 관리**

- `Pillow`: 이미지 처리 및 업로드 지원

#### **6) 기타 사용한 라이브러리**

- `openai`: OpenAI API 연동 (대체 결말 생성 기능)
- `django-environ`: 환경 설정 파일 관리

## 2. 설치 및 실행 방법
---
이 프로젝트를 로컬 환경에서 실행하려면 다음 단계를 따르세요:

#### **1. 프로젝트 클론**

GitHub 또는 프로젝트 저장소에서 코드를 클론합니다:

```bash
git clone <your-repository-url>
cd <project-directory>
```

#### **2. 가상환경 설정**

Python 가상환경을 생성하고 활성화합니다:

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
source venv\Scripts\activate     # Windows
```

#### **3. 의존성 설치**

`requirements.txt` 파일을 통해 필요한 패키지를 설치합니다:

```bash
pip install -r requirements.txt
```

#### **4. 환경 변수 설정**

`.env` 파일을 생성하고 다음과 같은 내용을 추가하세요:

```.env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

#### **5. 데이터베이스 설정**

데이터베이스를 마이그레이션합니다:

```bash
python manage.py makemigrations
python manage.py migrate
```

#### **6. 로컬 서버 실행**

개발 서버를 실행합니다:

```bash
python manage.py runserver
```

서버가 실행되면 http://127.0.0.1:8000에서 프로젝트를 확인할 수 있습니다.

## 3. API Endpoints 구성 요소 설명
---
## 1) `accounts/views.py`

### 1. `GetProfile` 함수
- **기능**: 특정 사용자의 프로필 정보를 조회하거나 수정하는 API 엔드포인트입니다.
- **사용 경로**: `GET /api/v1/accounts/<int:user_pk>/` (사용자 프로필 조회)  
  `PUT /api/v1/accounts/<int:user_pk>/` (사용자 프로필 수정)



| **Domain**  | **Method** | **Feature**           | **URL**                                                      |
| ----------- | ---------- | --------------------- | ------------------------------------------------------------ |
| Movies      | GET        | 목록 조회                 | /api/v1/movies/                                              |
| Movies      | GET        | 상세 정보 조회              | /api/v1/movies/<int:movie_pk>/                               |
| Movies      | PUT        | 영화 선택/해제              | /api/v1/movies/select/                                       |
| Movies      | GET        | 엔딩 목록 조회              | /api/v1/movies/altends/                                      |
| Movies      | GET        | 엔딩 상세 정보 <br>및 삭제     | /api/v1/movies/altends/<int:ending_pk>/                      |
| Movies      | DELETE     | 엔딩 상세 정보 <br>및 삭제     | /api/v1/movies/altends/<int:ending_pk>/                      |
| Movies      | GET        | 댓글 목록 및 생성            | /api/v1/movies/altends<br>/<int:ending_pk>/comments/         |
| Movies      | POST       | 댓글 목록 및 생성            | /api/v1/movies/altends<br>/<int:ending_pk>/comments/         |
| Movies      | DELETE     | 댓글 삭제                 | /api/v1/movies/altends/<br><int:comment_pk>/comments/delete/ |
| Movies      | POST       | 엔딩 좋아요<br>/좋아요 취소     | /api/v1/movies/altends/<int:ending_pk>/likes/                |
| Movies      | GET        | 사용자 랭킹 조회             | /api/v1/movies/ranking/user/                                 |
| Movies      | GET        | 엔딩 랭킹 조회              | /api/v1/movies/ranking/ending/                               |
| Communities | GET        | 게시글 목록 조회             | /api/v1/communities/                                         |
| Communities | POST       | 게시글 생성                | /api/v1/communities/                                         |
| Communities | GET        | 게시글 상세 정보 조회, 수정 및 삭제 | /api/v1/communities/<int:article_pk>/                        |
| Communities | PUT        | 게시글 상세 정보 조회, 수정 및 삭제 | /api/v1/communities/<int:article_pk>/                        |
| Communities | DELETE     | 게시글 상세 정보 조회, 수정 및 삭제 | /api/v1/communities/<int:article_pk>/                        |
| Communities | GET        | 댓글 목록 및 생성            | /api/v1/communities/<int:article_pk>/comments/               |
| Communities | POST       | 댓글 목록 및 생성            | /api/v1/communities/<int:article_pk>/comments/               |
| Communities | DELETE     | 댓글 삭제                 | /api/v1/communities/<int:comment_pk><br>/comments/delete/    |
| Communities | POST       | 게시글 좋아요/좋아요 취소        | /api/v1/communities/<int:article_pk>/likes/                  |
| Accounts    | GET        | 로그인, 로그아웃, 등록 등       | /api/v1/accounts/                                            |
| Accounts    | POST       | 로그인, 로그아웃, 등록 등       | /api/v1/accounts/                                            |
| Accounts    | GET        | 프로필 조회 및 수정           | /api/v1/accounts/<int:user_pk>/                              |
| Accounts    | PUT        | 프로필 조회 및 수정           | /api/v1/accounts/<int:user_pk>/                              |

## 4. 기타 참고 사항
---
