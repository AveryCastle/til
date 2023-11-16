package chapter03.sec4

sealed class List<out A> {
    companion object {
        fun <A> of(vararg aa: A): List<A> {
            val tail = aa.sliceArray(1..<aa.size)
            return if (aa.isEmpty()) Nil else Cons(aa[0], of(*tail))
        }

        fun sum(ints: List<Int>): Int =
            foldRight(ints, 0) { a, b -> a + b }

        // 연습문제 3.6
        fun product(doubles: List<Double>): Double =
            foldRight(doubles, 1.0) { a, b ->
                when {
                    a == 0.0 || b == 0.0 -> 0.0
                    else -> a * b
                }
            }

        fun <A> empty(): List<A> = Nil

        fun <A, B> foldRight(xs: List<A>, z: B, f: (A, B) -> B): B =
            when (xs) {
                is Nil -> z
                is Cons -> f(xs.head, foldRight(xs.tail, z, f))
            }

        // 연슴문제3.8
        fun <A> length(xs: List<A>): Int = foldRight(xs, 0) { _, z -> z + 1 }
    }
}

data object Nil : List<Nothing>()

data class Cons<out A>(val head: A, val tail: List<A>) : List<A>()

fun main() {
    println("sum = ${List.sum(List.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10))}")
    println("product = ${List.product(List.of(1.0, 2.0, 3.0, 0.0, 4.0, 5.0))}")

    println(
        List.foldRight(
            Cons(1, Cons(2, Cons(3, Nil))),
            Nil as List<Int>
        ) { x, y -> Cons(x, y) }
    )

    val members = List.of("RM", "JIN", "SUGA", "J-HOPE", "JIMIN", "V", "JK")
    println("length = ${List.length(members)}")
}

