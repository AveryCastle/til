package chapter07

import arrow.core.extensions.list.foldable.foldLeft

fun sum(ints: List<Int>): Int =
    ints.foldLeft(0) { a, b -> a + b }
