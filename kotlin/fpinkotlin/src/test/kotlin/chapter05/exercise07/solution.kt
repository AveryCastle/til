package chapter05.exercise07

import chapter03.List
import chapter05.Stream
import chapter05.Stream.Companion.cons
import chapter05.Stream.Companion.empty
import chapter05.toList
import io.kotest.core.spec.style.WordSpec
import io.kotest.matchers.shouldBe


class Solution6 : WordSpec({

    // 방법1.
//fun <A, B> Stream<A>.map(f: (A) -> B): Stream<B> = when (this) {
//    is Empty -> empty()
//    is Cons -> cons({ f(this.head()) }) { this.tail().map(f) }
//}
    fun <A, B> Stream<A>.map(f: (A) -> B): Stream<B> =
        this.foldRight(
            { empty() },
            { h: A, t: () -> Stream<B> -> cons({ f(h) }, t) }
        )

    //// 방법1.
//fun <A> Stream<A>.filter(f: (A) -> Boolean): Stream<A> = when (this) {
//    is Empty -> empty()
//    is Cons ->
//        if (f(this.head())) cons(this.head) { this.tail().filter(f) }
//        else this.tail().filter(f)
//}
    fun <A> Stream<A>.filter(f: (A) -> Boolean): Stream<A> =
        this.foldRight({ empty() }, { h: A, t: () -> Stream<A> ->
            if (f(h)) cons({ h }, t) else t()
        })

    // 방법1.
//fun <A> Stream<A>.append(a: () -> Stream<A>): Stream<A> = when (this) {
//    is Empty -> a()
//    is Cons -> cons(this.head) { this.tail().append(a) }
//}
    fun <A> Stream<A>.append(a: () -> Stream<A>): Stream<A> =
        this.foldRight(a) { h: A, t: () -> Stream<A> -> cons({ h }, t) }

    "Stream.map" should {
        "apply a function to each evaluated element in a stream" {
            val s = Stream.of(1, 2, 3, 4, 5)
            s.map { (it * 2).toString() }.toList() shouldBe
                    List.of("2", "4", "6", "8", "10")
        }
        "return an empty stream if no elements are found" {
            empty<Int>().map { (it * 2).toString() } shouldBe empty()
        }
    }

    "Stream.filter" should {
        "return all elements of a stream that conform to a predicate" {
            val s = Stream.of(1, 2, 3, 4, 5)
            s.filter { it % 2 == 0 }.toList() shouldBe
                    List.of(2, 4)
        }
        "return no elements of an empty stream" {
            empty<Int>().filter { it % 2 == 0 }
                .toList() shouldBe List.empty()
        }
    }

    "Stream.append" should {
        "append two streams to each other" {
            val s1 = Stream.of(1, 2, 3)
            val s2 = Stream.of(4, 5, 6)
            s1.append { s2 }.toList() shouldBe
                    List.of(1, 2, 3, 4, 5, 6)
        }
        "append a stream to an empty stream" {
            val s1 = empty<Int>()
            val s2 = Stream.of(1, 2, 3)
            s1.append { s2 }.toList() shouldBe List.of(1, 2, 3)
        }
        "append an empty stream to a stream" {
            val s1 = Stream.of(1, 2, 3)
            val s2 = empty<Int>()
            s1.append { s2 }.toList() shouldBe List.of(1, 2, 3)
        }
    }
})
