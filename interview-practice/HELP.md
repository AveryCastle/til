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

**HashMap**
- HashTable을 자바로 구현한 것으로, 클래스 구현에는 Key-Value 쌍을 나타내는 Entry라는 내부 클래스가 있다.

**TreeMap**
- Map 인터페이스를 구현하는데 이진 트리(Binary Tree) 자료구조를 이용한다.
- 키를 정렬 가능한 순서에 따라 저장하기 때문에 hashCode 메소드를 전혀 사용하지 않는다.
- TreeMap 클래스에 포함된 각 원소는 균형을 맞춘 트리 구조로 구성되어 있으므로 검색, 삭제, 삽입 같은 모든 동작은 항상 O(logN)의 처리 성능을 발휘한다.

> 1. TreeMap과 HashMap의 주된 차이점은?
> - TreeMap에서는 컬렉션이 *순서대로 저장*되므로 전체 컬렉션을 반복해서 순회할 때 키의 순서가 보전되는데 반해 HashMap 클래스에서는 순서가 보전되지 않는다는 것이다.

**LinkedHashMap**
- 기본적으로 HashMap 클래스와 같은 방식으로 작동한다.
- 그래서 원소를 찾는데 O(1)의 성능을 발휘한다.

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
