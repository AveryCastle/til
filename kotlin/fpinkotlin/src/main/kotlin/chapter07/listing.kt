package chapter07

import arrow.core.Option
import arrow.core.getOrElse

fun sum(ints: List<Int>): Int =
    ints.fold(0) { acc: Int, i: Int -> acc + i }

fun sum2(ints: List<Int>): Int =
    if (ints.size <= 1)
        Option.fromNullable(ints.first).getOrElse { 0 }
    else {
        val l = ints.subList(0, ints.size / 2)
        val r = ints.subList(ints.size / 2, ints.size)
        sum2(l) + sum2(r)
    }

fun sum3(ints: List<Int>): Int =
    if (ints.size <= 1)
        Option.fromNullable(ints.first).getOrElse { 0 }
    else {
        val l = ints.subList(0, ints.size / 2)
        val r = ints.subList(ints.size / 2, ints.size)
        val sumL = unit { sum2(l) }
        val sumR = unit { sum2(r) }
        sumL.get + sumR.get
    }

fun sum4(ints: List<Int>): Par<Int> =
    if (ints.size <= 1)
        unit { Option.fromNullable(ints.first).getOrElse { 0 } }
    else {
        val l = ints.subList(0, ints.size / 2)
        val r = ints.subList(ints.size / 2, ints.size)
        map2(sum4(l), sum4(r)) { lx: Int, rx: Int -> lx + rx }
    }

fun <A> map2(l: Par<A>, r: Par<A>, fn: (A, A) -> A): Par<A> =
    Par(fn(l.get, r.get))

class Par<A>(val get: A)

fun <A> unit(a: () -> A): Par<A> = Par(a())

fun <A> get(a: Par<A>): A = a.get

fun main() {
    val list = listOf(1, 2, 3, 4, 5, 6, 7)
    println("${sum(list)}")
    println("${sum2(list)}")
    println("${sum3(list)}")
}
