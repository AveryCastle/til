package chapter04.sec03

import chapter04.None.map
import chapter04.Option

fun <A, B> lift(f: (A) -> B): (Option<A>) -> Option<B> = { it.map(f) }

val abs0: (Option<Double>) -> Option<Double> =
    lift { kotlin.math.abs(it) }
