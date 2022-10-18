# Docker Machine

https://www.docker.com/docker-machine

```
$ brew update
$ brew install docker docker-machine
$ brew cask install virtualbox
```

```
$ docker -v
$ docker-machine -v
$ docker-machine create --driver virtualbox dev
$ docker-machine ls
$ eval "$(docker-machine env dev)"
$ docker -v
```

에러가 발생하면... `Error response from daemon: client is newer than server (client API version: 1.21, server API version: 1.20)`

```
$ docker-machine upgrade dev
```


# 강의 정리
- [Docker 따라 배우기 정리](./LEARNING.md)
