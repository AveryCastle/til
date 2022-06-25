package algorithm;

import java.util.Arrays;

public class ComparableAndComparator {

    public static void main(String[] args) {
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

        Arrays.sort(myList, ((o1, o2) -> {
            if (o1.name.compareTo(o2.name) <= 0)
                return o1.name.compareTo(o2.name);
            return o1.age - o2.age;
        }));

        System.out.println("=========== 내 맘대로 정렬 ==============");
        for (MyList el : myList) {
            System.out.println(el);
        }
    }

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
}
