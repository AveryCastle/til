package chapter04.exercise.ex03

import chapter04.None
import chapter04.None.flatMap
import chapter04.None.map
import chapter04.Option
import chapter04.Some
import io.kotest.core.spec.style.WordSpec
import io.kotest.matchers.shouldBe

// 내가 푼 방식
//fun <A, B, C> map2(a: Option<A>, b: Option<B>, f: (A, B) -> C): Option<C> =
//    when (a) {
//        is None -> None
//        is Some -> when (b) {
//            is None -> None
//            is Some -> Some(f(a.get, b.get))
//        }
//    }

// 해답지
fun <A, B, C> map2(oa: Option<A>, ob: Option<B>, f: (A, B) -> C): Option<C> =
    oa.flatMap { a ->
        ob.map { b ->
            f(a, b)
        }
    }

class Solution3 : WordSpec({
    "map2" should {

        val a: Option<Int> = Some(5)
        val b: Option<Int> = Some(10)
        val none: Option<Int> = None

        "combine two option values using a binary function" {
            map2(a, b) { aa, bb ->
                aa * bb
            } shouldBe Some(50)
        }

        "return none if either option is not defined" {
            map2(a, none) { aa, bb ->
                aa * bb
            } shouldBe None
            map2(none, b) { aa, bb ->
                aa * bb
            } shouldBe None
        }
    }
})
