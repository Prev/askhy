# ASKHY [부탁하냥]

[![Docker Automated build](https://img.shields.io/docker/automated/prev/askhy.svg)](https://hub.docker.com/r/prev/askhy/)

Flask와 MySQL을 이용하고 docker를 이용해서 패키징 한 너무너무 간단한 웹 어플리케이션

![Screenshot](https://prev.kr/askhy/screenshot.png)


## How to run

MySQL 컨테이너가 없다면 다음 명령어를 먼저 실행해야 합니다.  
(비밀번호나 컨테이너 이름 등은 취향껏 수정하되 아래 `askhy` 컨테이너 실행시 알맞게 설정해주어야 합니다)

```bash
docker run -d \
  -e MYSQL_ROOT_PASSWORD=root \
  -e MYSQL_DATABASE=askhy \
  --name mysql \
  mysql:5.7
```

---

그 뒤에 이 명령어를 통해 해당 어플리케이션의 이미지를 다운로드하고 컨테이너를 실행합니다.

```bash
docker run -p 8080:80 \
  --link mysql:mysql_host \
  -e DATABASE_HOST=mysql_host \
  -e DATABASE_USER=root \
  -e DATABASE_PASS=root \
  -e DATABASE_NAME=askhy \
  --name askhy \
  prev/askhy
```
---

다음에 웹 브라우저를 열고 `localhost:8080` 에 접속하면 어플리케이션이 실행됩니다!



## Database Scheme

서비스 컨셉은 기본적인 게시판과 비슷하지만 게시글을 `부탁`이라는 이름으로 쓰며, 댓글을 `응원`이라는 이름을 사용한다. MySQL 스키마는 아래와 같다.

![Screenshot](https://prev.kr/askhy/db_scheme.png)



## Pages

- `GET /`: 메인 화면. 전체 `부탁`과 부탁 별 `응원 수`를 볼 수 있다.
- `GET /ask/{$ask_id}`: 하나의 `부탁`에 대한 자세한 정보가 보여진다. 해당 부탁에 대한 모든 `응원`을 볼 수 있다.
- `POST /ask`: 새로운 `부탁`을 등록하는 페이지다.
- `POST /ask/{$ask_id}/cheer`: 특정 `부탁`에 새로운 `응원`을 등록하는 페이지다.



## Structure

```
.
├── Dockerfile 					이미지 빌드용 스크립트
├── LICENSE 					라이선스
├── README.md
├── app
│   ├── core					앱 내부 코드
│   │   └── dbdriver.py	 			 데이터베이스(MYSQL) 연결 및 초기화용 드라이버
│   ├── main.py					URL route와 템플릿을 렌더링하는 메인 코드
│   ├── static					프론트엔드 정적 파일 
│   │   ├── css
│   │   │   ├── detail.css			'부탁 상세보기'용 CSS
│   │   │   ├── main.css			'메인'용 CSS
│   │   │   └── stylesheet.css			공통 CSS
│   │   ├── favicon.ico
│   │   └── images
│   │       ├── add.png				
│   │       ├── cheer.png
│   │       ├── logo.png
│   │       └── quotation_bg.png
│   └── templates
│       ├── _layout.html			사이트 공통 템플릿
│       ├── detail.html				'부탁 상세보기'용 템플릿
│       └── main.html				'메인'용 CSS
├── docs
└── requirements.txt				Python Pacakage Dependency
```



## Branches

`ASKHY`에 기능을 추가하거나 변형 한 버전들이 존재합니다. 각각은 `branch`를 통해 관리되고 있습니다.

| Branch             | 설명                                       |
| ------------------ | ---------------------------------------- |
| master             | MySQL을 사용하는 기본 웹 어플리케이션                  |
| 1.1                | `부탁` 별 `응원 수`에 추가적으로 하나의 IP 당 하나의 응원으로만 카운팅 한<br />`순수 응원 수`라는 지표도 함께 보여주는 어플리케이션 |
| arcus-combined     | `arcus` 를 이용하여 주요 쿼리를 cache하여 성능 개선을 한 버전 |
| arcus-combined-1.1 | `1.1`의 기능에 `arcus`로 성능 개선을 한 버전          |
| redis-combined     | `redis` 를 이용하여 주요 쿼리를 cache하여 성능 개선을 한 버전 |
| redis-combined-1.1 | `1.1`의 기능에 `redis`로 성능 개선을 한 버전          |




## External Libraries

- [Flask](https://github.com/pallets/flask)
- [PyMySQL](https://github.com/PyMySQL/PyMySQL)

