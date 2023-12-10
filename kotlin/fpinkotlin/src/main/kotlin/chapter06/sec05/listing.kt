package chapter06.sec05

import chapter06.sec01.RNG

fun <S, A, B> map(
    sa: (S) -> Pair<A, S>,
    f: (A) -> B
): (S) -> Pair<B, S> = TODO()


data class State<S, out A>(val run: (S) -> Pair<A, S>)

typealias Rand<A> = State<RNG, A>
