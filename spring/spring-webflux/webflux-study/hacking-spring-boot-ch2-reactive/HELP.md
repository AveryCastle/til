# Getting Started

### Reference Documentation

For further reference, please consider the following sections:

* [Official Gradle documentation](https://docs.gradle.org)
* [Spring Boot Gradle Plugin Reference Guide](https://docs.spring.io/spring-boot/docs/2.7.8/gradle-plugin/reference/html/)
* [Create an OCI image](https://docs.spring.io/spring-boot/docs/2.7.8/gradle-plugin/reference/html/#build-image)
* [Spring Reactive Web](https://docs.spring.io/spring-boot/docs/2.7.8/reference/htmlsingle/#web.reactive)
* [Thymeleaf](https://docs.spring.io/spring-boot/docs/2.7.8/reference/htmlsingle/#web.servlet.spring-mvc.template-engines)
* [Embedded MongoDB Database](https://docs.spring.io/spring-boot/docs/2.7.8/reference/htmlsingle/#data.nosql.mongodb.embedded)
* [Spring Data Reactive MongoDB](https://docs.spring.io/spring-boot/docs/2.7.8/reference/htmlsingle/#data.nosql.mongodb)

### Guides

The following guides illustrate how to use some features concretely:

* [Building a Reactive RESTful Web Service](https://spring.io/guides/gs/reactive-rest-service/)
* [Handling Form Submission](https://spring.io/guides/gs/handling-form-submission/)
* [Accessing Data with MongoDB](https://spring.io/guides/gs/accessing-data-mongodb/)

### Additional Links

These additional references should also help you:

* [Gradle Build Scans – insights for your project's build](https://scans.gradle.com#gradle)


# Mongo Command

### command line 으로 mongodb 에 접속하기.
```bash
$ docker exec -it local-mongo bash
# root@72ad4ed5bdac:/# mongosh -u root -p root1234 
```

### create database
use('만들 database 이름');

```bash
test> use('springboot');
springboot>
```
