package chapter05.exercise13

import chapter03.List
import chapter03.Nil
import chapter04.None
import chapter04.Option
import chapter04.Some
import chapter05.Cons
import chapter05.Empty
import chapter05.Stream
import chapter05.exercise11.unfold
import chapter05.toList
import io.kotest.core.spec.style.WordSpec
import io.kotest.matchers.shouldBe

class Solution13 : WordSpec({

    // 못 풀었음.
    fun <A, B> Stream<A>.map(f: (A) -> B): Stream<B> =
        unfold(this) { it: Stream<A> ->
            when (it) {
                is Empty -> None
                is Cons -> Some(Pair(f(it.head()), it.tail()))
            }
        }

    // 못 풀었음.
    fun <A> Stream<A>.take(n: Int): Stream<A> =
        unfold(this) { it: Stream<A> ->
            when (it) {
                is Empty -> None
                is Cons -> if (n > 0) Some(Pair(it.head(), it.tail().take(n - 1)))
                else None
            }

        }

    // 못 풀었음.
    fun <A> Stream<A>.takeWhile(p: (A) -> Boolean): Stream<A> =
        unfold(this) { it: Stream<A> ->
            when (it) {
                is Empty -> None
                is Cons ->
                    if (p(it.head())) Some(Pair(it.head(), it.tail()))
                    else None
            }
        }

//    fun <A, S> unfold(z: S, f: (S) -> Option<Pair<A, S>>): Stream<A> =
//        f(z).map { pair ->
//            Stream.cons({ pair.first }, { unfold(pair.second, f) })
//        }.getOrElse { Stream.empty() }

    // 못 풀었음.
    fun <A, B, C> Stream<A>.zipWith(that: Stream<B>, f: (A, B) -> C): Stream<C> =
        unfold(this to that) { (ths: Stream<A>, tht: Stream<B>) ->
            when (ths) {
                is Cons -> when (tht) {
                    is Cons ->
                        Some(
                            Pair(
                                f(ths.head(), tht.head()),
                                ths.tail() to tht.tail()
                            )
                        )

                    else -> None
                }

                else -> None
            }
        }

    fun <A, B> Stream<A>.zipAll(that: Stream<B>): Stream<Pair<Option<A>, Option<B>>> = TODO()


    "Stream.map" should {
        "apply a function to each evaluated element in a stream" {
            val s = Stream.of(1, 2, 3, 4, 5)
            s.map { (it * 2).toString() }.toList() shouldBe
                    List.of("2", "4", "6", "8", "10")
        }
        "return an empty stream if no elements are found" {
            Stream.empty<Int>().map { (it * 2).toString() } shouldBe Stream.empty()
        }
    }

    "Stream.take(n)" should {
        "return the first n elements of a stream" {
            val s = Stream.of(1, 2, 3, 4, 5)
            s.take(3).toList() shouldBe List.of(1, 2, 3)
        }

        "return all the elements if the stream is exhausted" {
            val s = Stream.of(1, 2, 3)
            s.take(5).toList() shouldBe List.of(1, 2, 3)
        }

        "return an empty stream if the stream is empty" {
            val s = Stream.empty<Int>()
            s.take(3).toList() shouldBe Nil
        }
    }

    "Stream.takeWhile" should {
        "return elements while the predicate evaluates true" {
            val s = Stream.of(1, 2, 3, 4, 5)
            s.takeWhile { it < 4 }.toList() shouldBe List.of(1, 2, 3)
        }
        "return all elements if predicate always evaluates true" {
            val s = Stream.of(1, 2, 3, 4, 5)
            s.takeWhile { true }.toList() shouldBe
                    List.of(1, 2, 3, 4, 5)
        }
        "return empty if predicate always evaluates false" {
            val s = Stream.of(1, 2, 3, 4, 5)
            s.takeWhile { false }.toList() shouldBe List.empty()
        }
    }

    "Stream.zipWith" should {
        "apply a function to elements of two corresponding lists" {
            Stream.of(1, 2, 3).zipWith(
                Stream.of(4, 5, 6)
            ) { x, y ->
                x + y
            }.toList() shouldBe List.of(5, 7, 9)
        }
    }
})
