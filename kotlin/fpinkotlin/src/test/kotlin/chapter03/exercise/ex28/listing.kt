package chapter03.exercise.ex28

import chapter03.Branch
import chapter03.Leaf
import chapter03.Tree
import io.kotest.core.spec.style.WordSpec
import io.kotest.matchers.shouldBe

fun <A, B> fold(ta: Tree<A>, l: (A) -> B, b: (B, B) -> B): B =
    when (ta) {
        is Leaf -> l(ta.value)
        is Branch -> b(fold(ta.left, l, b), fold(ta.right, l, b))
    }

fun <A> sizeF(t: Tree<A>): Int =
//    fold(t, { _: A -> 1 }, { a: Int, b: Int -> a + b + 1 })
    fold(t, { 1 }, { a: Int, b: Int -> a + b + 1 })

fun maximumF(t: Tree<Int>): Int =
    fold(t, { a: Int -> a }, { b, c -> if (b >= c) b else c })

fun <A> depthF(ta: Tree<A>): Int =
//    fold(ta, { _: A -> 0 }, { a, b -> maxOf(a, b) + 1 })
    fold(ta, { 0 }, { a, b -> maxOf(a, b) + 1 })

fun <A, B> mapF(ta: Tree<A>, f: (A) -> B): Tree<B> =
    fold(ta, { a: A -> Leaf(f(a)) })
    { b1: Tree<B>, b2: Tree<B> -> Branch(b1, b2) }

class Exercise28 : WordSpec({
    "tree fold" should {

        val tree = Branch(
            Branch(Leaf(1), Leaf(2)),
            Branch(
                Leaf(3),
                Branch(
                    Branch(Leaf(4), Leaf(5)),
                    Branch(
                        Leaf(21),
                        Branch(Leaf(7), Leaf(8))
                    )
                )
            )
        )

        "generalise size" {
            sizeF(tree) shouldBe 15
        }

        "generalise maximum" {
            maximumF(tree) shouldBe 21
        }

        "generalise depth" {
            depthF(tree) shouldBe 5
        }

        "generalise map" {
            mapF(tree) { it * 10 } shouldBe
                    Branch(
                        Branch(Leaf(10), Leaf(20)),
                        Branch(
                            Leaf(30),
                            Branch(
                                Branch(Leaf(40), Leaf(50)),
                                Branch(
                                    Leaf(210),
                                    Branch(Leaf(70), Leaf(80))
                                )
                            )
                        )
                    )
        }
    }
})
