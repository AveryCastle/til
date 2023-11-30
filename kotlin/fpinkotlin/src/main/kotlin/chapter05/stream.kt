package chapter05

import chapter04.None
import chapter04.Option
import chapter04.Some
import chapter05.Stream.Companion.cons
import chapter05.Stream.Companion.empty

sealed class Stream<out A> {

    companion object {

        fun <A> cons(hd: () -> A, tl: () -> Stream<A>): Stream<A> {
            val head: A by lazy(hd)
            val tail: Stream<A> by lazy(tl)
            return Cons({ head }, { tail })
        }

        fun <A> empty(): Stream<A> = Empty

        fun <A> of(vararg xs: A): Stream<A> =
            if (xs.isEmpty()) empty()
            else cons({ xs[0] }, { of(*xs.sliceArray(1..<xs.size)) })
    }

    fun <B> foldRight(z: () -> B, f: (A, () -> B) -> B): B =
        when (this) {
            is Empty -> z()
            is Cons -> f(this.head()) { this.tail().foldRight(z, f) }
        }

    fun exists2(p: (A) -> Boolean): Boolean =
        foldRight({ false }, { a: A, b: () -> Boolean -> p(a) || b() })

    fun find(p: (A) -> Boolean): Option<A> =
        filter(p).headOption()
}

fun <A> Stream<A>.headOption(): Option<A> =
    when (this) {
        is Empty -> None
        is Cons -> Some(this.head())
    }

fun <A> Stream<A>.filter(f: (A) -> Boolean): Stream<A> =
    this.foldRight({ empty() }, { h: A, t: () -> Stream<A> ->
        if (f(h)) cons({ h }, t) else t()
    })

data class Cons<out A>(
    val head: () -> A,
    val tail: () -> Stream<A>
) : Stream<A>()

data object Empty : Stream<Nothing>()

