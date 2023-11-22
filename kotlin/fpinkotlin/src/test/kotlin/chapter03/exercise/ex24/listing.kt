package chapter03.exercise.ex24

import chapter03.Branch
import chapter03.Leaf
import chapter03.Tree
import io.kotest.core.spec.style.WordSpec
import io.kotest.matchers.shouldBe

fun <A> size(tree: Tree<A>): Int =
    when (tree) {
        is Leaf -> 1
        is Branch -> size(tree.left) + size(tree.right) + 1
    }

class Exercise24 : WordSpec({
    "tree size" should {
        "determine the total size of a tree" {
            val tree =
                Branch(
                    Branch(Leaf(1), Leaf(2)),
                    Branch(Leaf(3), Leaf(4))
                )
            size(tree) shouldBe 7
        }
    }
})
