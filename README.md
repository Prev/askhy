# ASKHY [부탁하냥]

[![Docker Automated build](https://img.shields.io/docker/automated/prev/askhy.svg)](https://hub.docker.com/r/prev/askhy/)
[![Docker Build Status](https://img.shields.io/docker/build/prev/askhy.svg)](https://hub.docker.com/r/prev/askhy/)

Very very simple web application made with flask connected with MySQL and packaged with docker  
Flask와 MySQL을 이용하고 docker를 이용해서 패키징한 너무너무 간단한 웹 어플리케이션

![Screenshot](https://prev.kr/askhy/screenshot.png)


## How to run

MySQL컨테이너가 없다면 다음 명령어를 먼저 실행하고 위 명령어를 실행해야 합니다.

```bash
docker run -d -p 3307:3306 \
  -e MYSQL_ROOT_PASSWORD=root \
  -e MYSQL_DATABASE=test \
  --name mysql \
  mysql:5.7
```

---

그 뒤에 이 명령어를 통해 해당 어플리케이션의 이미지를 다운받고 실행합니다.

```bash
docker run -p 8080:80 \
  --link mysql:mysql_host \
  -e DATABASE_HOST=mysql_host \
  -e DATABASE_USER=root \
  -e DATABASE_PASS=root \
  -e DATABASE_NAME=test \
  --name askhy \
  prev/askhy
```
---

다음에 웹 브라우저를 열고 `localhost:8080` 에 접속하면 어플리케이션이 실행됩니다!


## External Libraries

- [Flask](https://github.com/pallets/flask)
- [PyMySQL](https://github.com/PyMySQL/PyMySQL)

