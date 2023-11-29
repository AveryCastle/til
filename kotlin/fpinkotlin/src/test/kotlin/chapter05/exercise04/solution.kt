package chapter05.exercise04

import chapter05.Stream
import io.kotest.core.spec.style.WordSpec
import io.kotest.matchers.shouldBe

// 버전1. 그냥 내가 혼자서 푼 버전
//fun <A> Stream<A>.forAll(p: (A) -> Boolean): Boolean = when (this) {
//    is Empty -> true
//    is Cons -> p(this.head()) && this.tail().forAll(p)
//}

// 버전2. 답지 foldRight 으로 푸는 힌트 보고 푼 버전
fun <A> Stream<A>.forAll(p: (A) -> Boolean): Boolean =
    foldRight({ true }) { a: A, f: () -> Boolean -> p(a) && f() }

class Solution4 : WordSpec({

    "Stream.forAll" should {
        "ensure that all elements match the predicate" {
            val s = Stream.of(1, 2, 3, 4, 5)
            s.forAll { it < 6 } shouldBe true
        }
        """stop evaluating if one element does not satisfy
            the predicate""" {
            val s = Stream.of(1, 2, 3, 4, 5)
            s.forAll { it != 3 } shouldBe false
        }
    }
})
