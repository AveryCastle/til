package chapter05.exercise05


import chapter03.List
import chapter05.Stream
import chapter05.toList
import io.kotest.core.spec.style.WordSpec
import io.kotest.matchers.shouldBe


class Solution5 : WordSpec({
    
    fun <A> Stream<A>.takeWhile(p: (A) -> Boolean): Stream<A> =
        foldRight({ Stream.empty() }) { a: A, f: () -> Stream<A> ->
            if (p(a)) Stream.cons({ a }, f)
            else Stream.empty()
        }

    "Stream.takeWhile using foldRight" should {
        "return elements while the predicate evaluates true" {
            val s = Stream.of(1, 2, 3, 4, 5)
            s.takeWhile { it < 4 }.toList() shouldBe
                    List.of(1, 2, 3)
        }
        "stop returning once predicate evaluates false" {
            val s = Stream.of(1, 2, 3, 4, 5, 4, 3, 2, 1)
            s.takeWhile { it < 4 }.toList() shouldBe
                    List.of(1, 2, 3)
        }
        "return all elements if predicate always evaluates true" {
            val s = Stream.of(1, 2, 3, 4, 5)
            s.takeWhile { true }.toList() shouldBe
                    List.of(1, 2, 3, 4, 5)
        }
        "return empty if predicate always evaluates false" {
            val s = Stream.of(1, 2, 3, 4, 5)
            s.takeWhile { false }.toList() shouldBe
                    List.empty()
        }
    }
})
