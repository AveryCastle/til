package chapter04.sec02

import chapter04.None
import chapter04.Option
import chapter04.Some

fun mean(xs: List<Double>): Option<Double> =
    if (xs.isEmpty()) None
    else Some(xs.sum() / xs.size)
