package chapter04.exercise.ex04

import chapter03.Cons
import chapter03.List
import chapter04.None
import chapter04.Option
import chapter04.Some
import chapter04.exercise.ex03.map2
import io.kotest.core.spec.style.WordSpec
import io.kotest.matchers.shouldBe

// 내 풀이
//fun <A> sequence(xs: List<Option<A>>): Option<List<A>> =
//    xs.foldRight(xs, Some(List.empty())) { a: Option<A>, b: Option<List<A>> ->
//        a.flatMap { ita: A ->
//            b.map { itb ->
//                Cons(ita, itb)
//            }
//        }
//    }

fun <A> sequence(xs: List<Option<A>>): Option<List<A>> =
    xs.foldRight(xs, Some(List.empty())) { oa: Option<A>, ob: Option<List<A>> ->
        map2(oa, ob) { a: A, list: List<A> ->
            Cons(a, list)
        }
    }

class Solution4 : WordSpec({

    "sequence" should {
        "turn a list of some options into an option of list" {
            val lo = List.of(Some(10), Some(20), Some(30))
            sequence(lo) shouldBe Some(List.of(10, 20, 30))
        }
        "turn a list of options containing none into a none" {
            val lo = List.of(Some(10), None, Some(30))
            sequence(lo) shouldBe None
        }
    }
})
