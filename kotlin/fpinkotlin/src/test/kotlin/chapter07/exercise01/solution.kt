package chapter07.exercise01

import io.kotest.core.spec.style.WordSpec

class Par<A>(val get: A)

fun <A> unit(a: () -> A): Par<A> = Par(a())

fun <A, B, C> map2(l: Par<A>, r: Par<B>, fn: (A, B) -> C): Par<C> =
    Par(fn(l.get, r.get))


class Solution1 : WordSpec({

    "Par.map2" should {
        """declare a valid signature that combines two Pars by
            applying another function""" {
            map2(unit { 1 }, unit { 2 }) { i, j -> i + j }
        }
    }
})
