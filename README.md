# ASKHY with ARCUS

기존 [MySQL만 쓰던 ASK HY 프로젝트](https://github.com/Prev/askhy/)에서 [NAVER ARCUS](https://naver.github.io/arcus/)를 캐시로 넣어 view 성능을 개선한 어플리케이션입니다.

```bash
docker run -p 8080:80 \
  --link mysql:mysql_host \
  -e DATABASE_HOST=mysql_host \
  -e DATABASE_USER=root \
  -e DATABASE_PASS=root \
  -e DATABASE_NAME=test \
  -e ARCUS_URL=172.17.0.4:2181 \
  -e ARCUS_SERVICE_CODE=ruo91-cloud \
  --name askhy \
  askhy
```

기존 코드에서 
`-e ARCUS_URL=172.17.0.4` 환경변수와 `-e ARCUS_SERVICE_CODE=ruo91-cloud` 환경변수를 추가했습니다.  

이때 `172.17.0.4:2181`은 arcus의 서버 주소와 포트를 써야합니다.


----
> 기존 프로젝트 README


# ASKHY [부탁하냥]

[![Docker Automated build](https://img.shields.io/docker/automated/prev/askhy.svg)](https://hub.docker.com/r/prev/askhy/)

Flask와 MySQL을 이용하고 docker를 이용해서 패키징한 너무너무 간단한 웹 어플리케이션

![Screenshot](https://prev.kr/askhy/screenshot.png)


## How to run

MySQL 컨테이너가 없다면 다음 명령어를 먼저 실행해야 합니다.  
(비밀번호나 컨테이너 이름 등은 취향 껏 수정하되 아래 `askhy` 컨테이너 실행시 알맞게 설정해주어야 합니다)

```bash
docker run -d \
  -e MYSQL_ROOT_PASSWORD=root \
  -e MYSQL_DATABASE=askhy \
  --name mysql \
  mysql:5.7
```

---

그 뒤에 이 명령어를 통해 해당 어플리케이션의 이미지를 다운받고 컨테이너를 실행합니다.

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


## External Libraries

- [Flask](https://github.com/pallets/flask)
- [PyMySQL](https://github.com/PyMySQL/PyMySQL)

