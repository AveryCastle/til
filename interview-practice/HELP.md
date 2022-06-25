# 기본 알고리즘

1. Comparable과 Comparator 인터페이스의 차이는 무엇인가?
   1. Comparable: 자연스러운 순서로 정렬할 때 사용한다.
   2. Comparator: 원하는 대로 정렬 순서를 지정하고 싶을 때 사용한다.

   example:
```java
private static class MyList implements Comparable<MyList> {

        private final String name;
        private final Integer age;

        public MyList(String name, Integer age) {
            this.name = name;
            this.age = age;
        }

        @Override
        public int compareTo(MyList o) {
            return this.age - o.age;
        }

        @Override
        public String toString() {
            return "NaturalOrder{" +
                    "name='" + name + '\'' +
                    ", age=" + age +
                    '}';
        }
    }
```
```java
        MyList[] myList = new MyList[6];
        myList[0] = new MyList("JHope", 28);
        myList[1] = new MyList("JK", 25);
        myList[2] = new MyList("RM", 28);
        myList[3] = new MyList("V", 27);
        myList[4] = new MyList("SUGA", 29);
        myList[5] = new MyList("JIMIN", 27);

        Arrays.sort(myList);

        for (MyList el : myList) {
            System.out.println(el);
        }
```
```shell
NaturalOrder{name='JK', age=25}
NaturalOrder{name='V', age=27}
NaturalOrder{name='JIMIN', age=27}
NaturalOrder{name='JHope', age=28}
NaturalOrder{name='RM', age=28}
NaturalOrder{name='SUGA', age=29}
```
```java
Arrays.sort(myList, ((o1, o2) -> {
   if (o1.name.compareTo(o2.name) <= 0) // 1. 이름 먼저 정렬
       return o1.name.compareTo(o2.name);
   return o1.age - o2.age; // 2. 나이 정렬
}));

System.out.println("=========== 내 맘대로 정렬 ==============");
for (MyList el : myList) {
   System.out.println(el);
}
```
```shell
=========== 내 맘대로 정렬 ==============
NaturalOrder{name='JHope', age=28}
NaturalOrder{name='JIMIN', age=27}
NaturalOrder{name='JK', age=25}
NaturalOrder{name='RM', age=28}
NaturalOrder{name='SUGA', age=29}
NaturalOrder{name='V', age=27}
```

2. 이진 검색(Binary Search)은 어떻게 구현하는가?
- 정렬된 리스트가 있거나 이미 정렬ㄹ이 수행된 상태일 때, 리스트에서 값을 찾을 때는 이진 검색(Binary Search)를 사용하는 것이 효율적이다.

# 자료구조
## 리스트(List)
### 1. 리스트
- 리스트는 특정 타입 값들이 순찿적을로 정렬된 컬렉션(Collection) 이다. Java에서는 LinkedList나 ArrayList 클래스를 일반적으로 사용한다.
- 리스트는 자바의 내장 컬렉션인 배열하고는 다르다. 사실 리스트는 크기 지정에 한계가 없으므로 리스트를 사용하기 전에 크기를 지정할 필요가 없다.

### 2. 배열과 리스트의 관계
- 배열을 정의할 때는 크기를 지정해야 한다.
- 배열의 원소에는 *인덱스* 값을 이용해서 직접 접근할 수 있다. 이를 *랜덤 접근*이라고 한다.

> 1. ArrayList와 LinkedList의 관계는?

**ArrayList**
- 클래스를 생성할 때는 배열의 초기 크기를 지정할 수 있다. 크기를 지정하지 않으면 기본 배열ㄹ 크기는 10이다. 원소로 가득한 배열에 새로운 원소를 추가할 때마다 ArrayList 클래스는 자동으로 더 큰 배열을 재할당한다. 단, 시간이 소요되며 더 큰 메모리 용량을 소모한다.
- 일반적으로 원소에 random access할 수 있어야 하거나 리스트 크기가 클 수록 ArrayList 클래스를 사용하면 좋다.
**LinkedList**
- 리스트의 첫 부분이나 중간에 원소를 삽입/삭제할 일이 많다면 LinkedList 클래스를 사용하는 것이 좋다.
- LinkedList는 ArrayListx 클래스에서 배열 재할당 과정에서 발생하는 손실을ㄹ 막아준다. 그리고 리스트 크기가 작아지면 메모리 용ㄹ량 역시 작아진다는 이점이 있다.
- 혹시 스택처럼 특수한 자료구조를 만들었다면 LinkedList 클래스를 사용하는 것이 좋다. 리스트의 첫 부분에도 원소를 간단하게 넣고 뺄 수 있기 때문이다.

> 2. Queue와 Deque는 무엇인가?

**Queue**
- 선입선출(First in First out) 자료구조를 구현하는 자바 인터페이스이다.

**DeQueue**
- Queue 인터페이스의 확장이며 자료구조의 양끝에 원소를 추가하고 삭제할 수 있다.

### 트리(Tree)
- 이진 검색 트리(Binary Search Tree)에서는 주어진 노드의 값보다 '작은 자식'은 왼쪽에, '큰 원소'는 오른쪽에 위치한다.

### 맵(Map)
- 해쉬(Hash)라고도 하며, 배열이나 사전(Dictionary)과 관련 있는 'Key-Value' 쌍의 저장소다.
- Java Collection API의 일부지만, List 인터페이스와 달리 Collection 인터페이스를 구현하지 않는다.
- Map의 특징은 Key 값은 트리 상에서 한 번만 나타난다는 것이다. 동일한 키를 다시 삽입하면 원래 키에 있던 값을 덮어쒸운다.

**HashTable**
- 동기화할 수 있으며 병렬 처리에 효율적이다.
- 단일 스레드 작업이든 오버헤드 때문에 성능이 상당히 저하된다. 따라서 병렬 환경에서 Map 인터페이스를 사용해야 하면 ConcurrentHashMap을 사용하는 게 좋다.

**HashMap**
- HashTable을 자바로 구현한 것으로, 클래스 구현에는 Key-Value 쌍을 나타내는 Entry라는 내부 클래스가 있다.
- 동기화할 수 없다.

**TreeMap**
- Map 인터페이스를 구현하는데 이진 트리(Binary Tree) 자료구조를 이용한다.
- 키를 정렬 가능한 순서에 따라 저장하기 때문에 hashCode 메소드를 전혀 사용하지 않는다.
- TreeMap 클래스에 포함된 각 원소는 균형을 맞춘 트리 구조로 구성되어 있으므로 검색, 삭제, 삽입 같은 모든 동작은 항상 O(logN)의 처리 성능을 발휘한다.

> 1. TreeMap과 HashMap의 주된 차이점은?
> - TreeMap에서는 컬렉션이 *순서대로 저장*되므로 전체 컬렉션을 반복해서 순회할 때 키의 순서가 보전되는데 반해 HashMap 클래스에서는 순서가 보전되지 않는다는 것이다.

**LinkedHashMap**
- 기본적으로 HashMap 클래스와 같은 방식으로 작동한다.
- 그래서 원소를 찾는데 O(1)의 성능을 발휘한다.
- Key 인덱스를 빠르게 찾을 수 있을 뿐만 아니라 Map 안 원소들의 순서도 보존한다.

**ConcurrentHashMap**
- 많은 스레드에서 공유하고자 할 때 사용할 수 있다.
- Thread Safe 하고, 맵에 값을 쓰는 도중이라도 값을 읽어서 반환할 수 있도록 설계되어 있다. 값을 쓰는 동안에는 테이블의 지정된 줄만 lock되고, 나머지는 읽기 가능한 상탤로 남겨둔다.

### 집합(Set)
- 중복을 허용하지 않는 순서 없는 객체들의 모음이다.

**HashSet**
- HashMap 클래스에 기반을 두고 구현되어 있으므로 값을 Map 키로 저장한다.

**TreeSet**

**LinkedHashSet**

단, ConcurruentHashSet은 없다. 다만, netSetFromMap이라는 정적 메서드가 있는데, ConcurrentHashMap 클래스와 유사한 역할을 한다.

# 디자인 패턴
- 소프트웨어 디자인 패턴은 프로그램을 만들면서 발생할 수 있는 다양한 상황에 효율적으로 적용할 수 있는 해결책이다.
- 보통 하나 이상의 객체를 함께 사용하며 코드 재사용, 확장성에 초점을 두거나 앞으로 개발할 때 필요한 견고한 기반을 제공한다는 점에서 개발하는데 도움이 된다.

**빌더패턴(Builder Pattern)**
- 멤버필드가 많은 객체의 경우, 도메인에 적합한 객체를 생성하는 빌더라는 동반자 객체를 만들 수 있다.

**스트레티지 패턴(Strategy Pattern)**
- 지정된 알고리즘의 세부 구현을 변경할 필요 없이 쉽게 교환할 수 있게 해주는 디자인 패턴이다. 실행 중이ㄹ라도 구현된 알고리즘을 교환할 수 있으므로 의존성 주입(Dependency Injection)에 자주 사용된다.
- 장점은 실행하기 전까지 어떤 구현을 사용할ㄹ지 결정을 미룰 수 있다는 점이다.
- Spring Framework에서 사용되는 예시
  - [ResourceLoader](https://sabarada.tistory.com/32)

**템플릿 메서드 패턴(Template Method Pattern)**
- 알고리즘의 일부 또는 전부를 하위 클래스에서 구현하거나 위임하는데 사용한다.즉, 공통으로 사용하는 안고리즘은 부모 클래스에 정의하고 특정 부분에서 사용하는 알고리즘은 하위 클래스에서 수행하도록 설계하는 것이다.
- Spring Framework에서 사용되는 예시
  - JdbcTemplate, JpaTemplate

**데커레이터 패턴(Decorator Pattern)**
- 특정 객체의 기능을ㄹ 설정하거나 변경할 수 있게 해준다.
- 자바의 기본 입/출력 클래스
  - InputStream, OutputStream, 그리고 하위 클래스들

**플라이웨이 패턴(Flyweight Pattern)**
- 몇 개의 객체에 많은 값을 공유해야 할 때 유용하다.
- Sun에서 구현한 Java 표준 라이브러리 Integer.valueOf()
  - 이전에 캐시된 값이라면 새로운 사본 인스턴스를 만들지 않고, 이전에 생성해둔 인스턴스를 반환한다.
  - 기본 범위는 -128부터 127까지다.
```java
    @HotSpotIntrinsicCandidate
    public static Integer valueOf(int i) {
        if (i >= IntegerCache.low && i <= IntegerCache.high)
            return IntegerCache.cache[i + (-IntegerCache.low)];
        return new Integer(i);
    }
```

**싱글턴 패턴(Singleton Pattern)**
- 오직 하나의 인스턴스만 생성한다는 것을 보장하는 패턴
- Spring Framework에서 사용되는 예시
  - Spring Framework에서 Singleton이 default scope이다.
  - IOC Contanier가 1개의 instance만 생성한다.

**Spring Framework에서 사용되는 예시**
  - [Learn About Design Patterns Used in Spring Framework](https://blog.eduonix.com/java-programming-2/learn-design-patterns-used-spring-framework/)
    - Factory Pattern
      - BeanFactory Container, ApplicationContext Container
    - Proxy Pattern
      - AOP
    - Singleton
      - Spring Framework에서 Singleton이 default scope이다.
      - IOC Contanier가 1개의 instance만 생성한다.
    - Template Method
      - JdbcTemplate, JpaTemplate
    - Model View Controller (MVC)
    - Strategy Pattern
      - [ResourceLoader](https://sabarada.tistory.com/32)

# 자주 묻는 면접 알고리즘 구현하기

FizzBuzz 구현하기

Fibonacci 수열 구현하기

Factorial 수열 구현하기

# Java 기본

> Java에서 객체란 무엇인가?
> - entity와 entity에 관련된 연산을 제공하는 메소드들의 모음이다. 따라서, 객체에는 entity의 상태와 행위가 있다.

> 다형성과 상속이란 무엇인가?
> - *다형성*은 행동의 특정 타입에 대한 정의를 만들 수 있게 하고, 행동을 구현하는 수많은 다른 클래스들을 갖게 한다.
> - *상속*은 부모 클래스에서 클래스의 행동과 정의를 가져다 사용할 수 있게 해준다. 새로운 클래스를 정의할 때, 부모 클래스에서 정의와 상태를 상속할 수 있고 새로운 행동을ㄹ 추가하거나 새로운 타입에 대한 행동을 오버라이드할 수 있다.

> 자바의 예외 처리 구조를 이루는 주요 클래스를 설명하라.
> ![자바 exception hierarchy](src/main/resources/java_exception_hierarchy.png)
> - checked exception은 try/catch/finally로 예외를 적절히 처리해야 한다.

> Java8의 특징을 설명하라.
> - 등장배경: 프로그래밍 언어 생태계에도 변화의 바람이 불기 시작했다.
>   - 하드웨어적 측면: 멀티코어 CPU가 대중화되었다.
>   - 프로그래밍 생태계 변화: 빅데이터를 효율적으로 처리하고자 하는 욕구가 커졌다. 즉, 병렬 플로세싱을 활용해야 하는데 지금까지의 자바로는 충분히 대응하지 못 하는 분야였다.

> Java8에서 제공하는 새로운 기술을 설명하라.
> - Stream API
>   - Stream: 한 번에 한 개씩 만들어지는 연속적인 데이터 항목들의 모임이다.
>   - Stream API의 핵심
>    - 우리가 하려는 작업을 (데이터베이스 질의처럼) 고수준으로 추상화해서 일련의 스트림을로 만들어 처리할 수 있다는 것이다.
>    - 스트림 파이프랄인을 이용해서 입력 부분을 여러 CPU 코어에 쉽게 할당 할 수 있다는 부가적인 이득도 얻을 수 있다. 이로 인해 공짜로 병렬설을 얻을 수 있다.
> - 메서드에 코드를 전달하는 기법
>   - 메서드를 다른 메서드의 인수로 넘겨주는 기능을 제공한다.(동작 팔라미터화)
> - 인터페이스의 디폴트 메서드

> 행위 주도 개발이란 무엇인가?
> - BDD(Behavior-Driven Development)은 가능한한 자연 언어에 가깝게 작성된 테스트 스크립트와 테스트 스크립트 위에서 실행되는 코드라는 두개의 요소로 이뤄져 있다.

# 자바 가상머신 이해하기

**JVM**
- 자바 가상머신(Java Virtual Machine)은 여러분의 플로그램이 실행되는 플랫폼이다. 각각의 운영체제와 아키텍처용으로 만들어져 있고, 운영체제와 애플리케이션 사이에 위칯하면서 애플리케이션이 플랫폼에 상관없이 독립적을로 실행될 수 있도록 만들어준다.
- 자바 프로그램은 javac를 이용해 bytecode로 컴파일된다. 이 byetcode는 JVM에서 명령어들을 아키텍처와 운영체제용으로 해석한다.

> Thread 클래스와 Executor 인터페이스의 차이점은 무엇인가?
> - Java4에서 도입된 동시성 프레임워크는 동시에 동작하는 코드를 위한 클래스의 집합을 제공했으며 자바의 스레드 모델을 이용할 수 있게 도와줬다.
> - Java 에서 실행되는 스레드를 만드는 일은 시스템 자원을 많이 사용하는 연산이므로 운영체제는 애플리케이션에서 한번에 실행되는 스레드 개수를 제한하게 된다. 즉, Thread Pool을 이용함으로써 새로운 스레드를 사용하기보다는 필요할 때 스레드를 가져오게 하거나 이전 코드에서 실행이 완료되었을 때 스레드를 재사용할 수 있게 하는 것이 좋다.
> - 자바의 동시성 프레임워크는 일반적인 경우에 사용할 수 있는 스레드풀들을 제공하며 필요에 따라 확장해서 사용할 수 있다.
> - Executor는 캐시된 Thread Pool을 사용하여 처리할 수 있다.


# HTTP와 REST API 이용하기
> REST 란 무엇인가?
> - REST API(Representational State Transfer)는 URI와 HTTP 메소드를 이용해 Resource에 접근하는 것이다.
> - REST의 요소: 리소스, 메소드(행위), 메세지 3가지 요소로 구성된다.

# 스프링 프레임워크

###Spring Framework
- 등장 배경
  - 2004년에 출시된 스프링 프레임워크 v1.0은 무거운 배포 설명자로 악명 높은 J2EE(Java 2 Platforms, Enterprise Edition)를 대체하여 개발을 더 쉽게 만들겠다는 목적으로 만들어졌다.
  - 의존성 주입(DI: Dependency Injection) 개념을 기반으로 매우 가벼운 개발 모델을 제공하며 J2EE의 배포 설명자와 비교해 훨씬 가벼운 XML 구성 파일을 사용한다.
- 개념
  - Java 엔터프라이즈 애플리케이션 개발의 복잡함을 해소하기 위해 만들어진 오픈 소스 프레임워크이다.
- 기본 임무
  - *Java 개발 간소화*에 초점을 맞춘다.
- Java 복잡도 간소화를 지원하는 Spring의 4가지 주요 전략
  1. POJO를 이용한 가볍고(lightweight) 비침투적(non-invasive)인 개발
  2. DI와 인터페이스 지향(interface orientation)을 통한 느슨한 결합도(loose coupling)
  3. 애스팩트와 공통 규약을 통한 선언적(declarative) 프로그래밍
  4. 애스팩트와 템플릿(template)을 통한 반복적인 코드 제거

**DI(Dependency Injection)**
- Spring Container라는 제 3자가 객체 사이의 관계를 조율하여 생성 시점에 종속객체를 부여해준다.
- 장점
  - 느슨한 결합도(loose coupling): 객체가 종속 객체를 생성하거나 호출하지 않고, 종속 객체를 인터페이스를 통해서만 알고 있으면 되기 때문에 구현체는 쉽게 바꿀 수 있다.

**Spring Container**
- 스프링 컨테이너는 객체를 생성하고, 서로 엮어 주고(wiring), 이들의 전체 생명주기(lifecycle)를 관리한다.
- 구현체
  1. BeanFactory(org.springframework.beans.factory.BeanFactory)
     - DI에 대한 기본적인 지원을 제공하는 가장 단순한 컨테이너이다.
  2. ApplicationContext(org.springframework.context.ApplicationContext)
     - BeanFactory 를 확장해 property 파일에 텍스트 메세지를 읽고, 해당 이벤트 리스너(listener)에 대한 애플리케이션 이벤트 발행 같은 애플리케이션 프레임워크 서비스를 제공하는 컨테이너이다.

**AOP**
- 소프트웨어 시스템 내부의 관심사들을 서로 분리하는 기술이다.
- logging이나 transaction 관리, 보안 등의 횡단 관심사(cross-cutting concern)을 한 곳에 모아 처리를 한다.
- 장점
  - 재사용성을 높임
  

> 스코프란 무엇인가?
> - Singleton scope: ApplicationContext 상의 getBean 메서드를 여러 번 호출할 수 있으며 항상 같은 인스턴스를 반환한다. 기본적으로 스프링 Bean은 애플리케이션 컨텍스트가 초기화될 때 생성되는데, 이를 eager instantiation 이라고 한다. 추가로 지정된 정의에 관한 스프링 빈의 인스턴스는 하나만 생성된다. 이를 싱글턴 스코프(Singleton Scope)라고 한다.
> - Bean scope: ApplicationContext 에서 getBean 메서드를 호출할 때마다 새로운 인스턴스를 반환한다.
> - Request scope: 특정 HTTP 요청이 살아있는 동안 빈이 살아있는 경우
> - Session scope: HTTP 세션이 존재하는 동안 존재하는 경우

> 오토와이어링이란 무엇인가?
> - autowiring 은 애플리케이션 컨텍스트가 클래스 사이의 의존성을 알아내는 과정이다.
> - 의존성을 갖는 빈을 생성하려면 가끔은 의존성에 대한 연결 고리를 직접 명시하지 않아도 된다. 애플리케이션 컨텍스트 내에서 해당 Bean이 1개만 존재할 경우 알아서 자동으로 연결해주기 때문이다.



# 쿠버네티스(Kubernetes)
- Kubernetes는 컨테이너화된 애플리케이션을 효율적으로 배포하고 운영하기 위해 설계된 오픈 소스 플랫폼이다.

**컨테이너 등장 배경**
- 오늘날 애플리케이션이 사용되는 모습을 보면 남녀노소를 불문하고 많은 사람들이 스마트폰을 사용해서 게임, 음악, 쇼핑, SNS 등의 애플리케이션을 이용한다. 일상에서 수시로 사용되고, 경쟁 애플리케이션이 범람하는 가운데 중요성이 점차 높아지는 것이 바로 *지속적 통합(CI)*와 배포(CD)이다. 사용자에게 새로운 기능과 서비스를 빠르고 안정적으로 제공해야 하는 것이다. 컨테이너 기술은 이러한 요구 사항에 효과적인 대안을 제시한다.
- 개발자들은 일반적으로 오픈 소스를 사용해서 짧은 시간에 고품질의 애플리케이션을 개발한다. 그런데 오픈 소스의 경우에는 버전이 계속 바뀌기 때문에 같은 팀의 개발자들 간에도 서로 다른 버전을 사용하는 상황이 벌어지기 일쑤다. 즉,개발자 간에 개발 환경의 차이가 발생하여 개발 생산성과 안정성이 떨어지는 것이다.
- 이러한 상황에서 컨테이너 기술이 빛을 발한다. 컨테이너 기술은 애플리케이션 실행에 필요한 라이브러리나 운영체제 패키지 등을 모두 담아서 불변의 실행 환경(Immutable Infrastructure)을 만든다. 이렇게 하면 개발자들 간에 그리고 테스트와 운영 환경 간의 차이를 없앨 수 있어 개발 생산성을 높이고, 애플리케이션 정식 서비스를 안정적으로 배포할 수 있게 한다.

**쿠버네티스 등장 배경**
- 컨테이너화된 애플리케이션 엔드 유저는 스마트폰을 사용하는 일반 사용자가 될 수도 있으므로, 수십만명에서 수백만명의 규모까지 대응 가능한 *확장성*과 *가용성*이 요구된다.
- 이러한 요구를 만족시킬 수 있는 업계 표준 플랫폼으로 기대를 받는 것이 바로 쿠버네티스(Kubernetes)이다.

**쿠버네티스 기능**
- 배포 계획에 맞춰 애플리케이션을 신속하게 배포할 수 있다.
- 가동 중인 애플리케이션을 스케일 업/다운할 수 있다.
- 새로운 버전의 애플리케이션을 무정지로 업그레이드할 수 있다.
- 하드웨어 가동률을 높여 자원 낭비를 줄인다.
