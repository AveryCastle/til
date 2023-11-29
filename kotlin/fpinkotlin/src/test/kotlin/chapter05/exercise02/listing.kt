package chapter05.exercise02

import chapter03.List
import chapter03.Nil
import chapter05.Cons
import chapter05.Empty
import chapter05.Stream
import chapter05.exercise01.toList
import io.kotest.core.spec.style.WordSpec
import io.kotest.matchers.shouldBe

tailrec fun <A, B> Stream<A>.foldLeft(xs: Stream<A>, z: Stream<B>, f: (Stream<B>, A) -> Stream<B>): Stream<B> =
    when (xs) {
        is Empty -> z
        is Cons -> foldLeft(xs.tail(), f(z, xs.head()), f)
    }

fun <A> Stream<A>.reverse(xs: Stream<A>): Stream<A> =
    foldLeft(xs, Stream.empty()) { t: Stream<A>, h: A -> Cons({ h }, { t }) }


fun <A> Stream<A>.take(n: Int): Stream<A> {
    tailrec fun go(xs: Stream<A>, n: Int, acc: Stream<A>): Stream<A> = when (xs) {
        is Empty -> acc
        is Cons ->
            if (n == 0) acc
            else go(xs.tail(), n - 1, Stream.cons(xs.head) { acc })
    }
    return reverse(go(this, n, Stream.empty()))
}

fun <A> Stream<A>.drop(n: Int): Stream<A> {
    tailrec fun go(xs: Stream<A>, n: Int): Stream<A> = when (xs) {
        is Empty -> xs
        is Cons ->
            if (n == 0) xs
            else go(xs.tail(), n - 1)
    }
    return go(this, n)
}

class Solution2 : WordSpec({

    "Stream.take(n)" should {
        "return the first n elements of a stream" {
            val bts = Stream.of("JIN", "J-HOPE", "SUGA", "RM", "V", "JIMIN", "JK")
            bts.take(3).toList() shouldBe List.of("JIN", "J-HOPE", "SUGA")
        }

        "return all the elements if the stream is exhausted" {
            val bts = Stream.of("JIN", "J-HOPE", "SUGA")
            bts.take(5).toList() shouldBe List.of("JIN", "J-HOPE", "SUGA")
        }

        "return an empty stream if the stream is empty" {
            val s = Stream.empty<String>()
            s.take(3).toList() shouldBe Nil
        }
    }

    "Stream.drop(n)" should {
        "return the remaining elements of a stream" {
            val bts = Stream.of("JIN", "J-HOPE", "SUGA", "RM", "V", "JIMIN", "JK")
            bts.drop(3).toList() shouldBe List.of("RM", "V", "JIMIN", "JK")
        }

        "return empty if the stream is exhausted" {
            val bts = Stream.of("JIN", "J-HOPE", "SUGA")
            bts.drop(7).toList() shouldBe Nil
        }

        "return empty if the stream is empty" {
            val s = Stream.empty<String>()
            s.drop(3).toList() shouldBe Nil
        }
    }
})
