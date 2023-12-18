package chapter07.exercise13

import java.util.concurrent.ExecutorService
import java.util.concurrent.Future

typealias Par<A> = (ExecutorService) -> Future<A>

// 내가 푼 버전.
fun <A> join(a: Par<Par<A>>): Par<A> = { es: ExecutorService ->
    a(es).get()(es)
}

fun <A, B> map(pa: Par<A>, f: (A) -> B): Par<B> = TODO()

fun <A, B> flatMap(pa: Par<A>, f: (A) -> Par<B>): Par<B> = TODO()

fun <A, B> flatMapViaJoin(pa: Par<A>, f: (A) -> Par<B>): Par<B> =
    join(map(pa, f))

fun <A> joinViaFlatMap(a: Par<Par<A>>): Par<A> =
    flatMap(a) { it }
