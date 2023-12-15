package chapter07.sec03

import chapter07.sec03.Pars.map2
import chapter07.sec03.Pars.unit
import java.util.concurrent.Callable
import java.util.concurrent.ExecutorService
import java.util.concurrent.Future
import java.util.concurrent.TimeUnit

typealias Par<A> = (ExecutorService) -> Future<A>

object Pars {
    fun <A> unit(a: A): Par<A> =
        { es: ExecutorService -> UnitFuture(a) }

    data class UnitFuture<A>(val a: A) : Future<A> {
        override fun cancel(mayInterruptIfRunning: Boolean): Boolean {
            TODO("Not yet implemented")
        }

        override fun isCancelled(): Boolean {
            TODO("Not yet implemented")
        }

        override fun isDone(): Boolean {
            TODO("Not yet implemented")
        }

        override fun get(): A {
            TODO("Not yet implemented")
        }

        override fun get(timeout: Long, unit: TimeUnit): A {
            TODO("Not yet implemented")
        }
    }

//    fun <A, B, C> map2(
//        a: Par<A>,
//        b: Par<B>,
//        f: (A, B) -> C,
//    ): Par<C> =
//        { es: ExecutorService ->
//            val af: Future<A> = a(es)
//            val bf: Future<B> = b(es)
//            UnitFuture(f(af.get(), bf.get()))
//        }

    fun <A, B, C> map2(
        a: Par<A>,
        b: Par<B>,
        f: (A, B) -> C,
    ): Par<C> =
        { es: ExecutorService ->
            val af: Future<A> = a(es)
            val bf: Future<B> = b(es)
            TimeMap2Future(af, bf, f)
        }

    data class TimeMap2Future<A, B, C>(
        val pa: Future<A>,
        val pb: Future<B>,
        val f: (A, B) -> C,
    ) : Future<C> {

        override fun get(): C {
            TODO("Not yet implemented")
        }

        override fun get(timeout: Long, timeUnit: TimeUnit): C {
            val timeoutMillis = TimeUnit.MILLISECONDS.convert(timeout, timeUnit)

            val start = System.currentTimeMillis()
            // TODO: src/chapter07.sec03.Pars 에서 구현하지 않은 get() 을 호출하고 있다. 이유를 모르겠다.
            val a = pa.get(timeout, timeUnit)
            val duration = System.currentTimeMillis() - start

            val remainder = timeoutMillis - duration
            val b = pb.get(remainder, timeUnit)
            return f(a, b)
        }

        override fun cancel(evenIfRunning: Boolean): Boolean {
            TODO("Not yet implemented")
        }

        override fun isDone(): Boolean {
            TODO("Not yet implemented")
        }

        override fun isCancelled(): Boolean {
            TODO("Not yet implemented")
        }
    }

    fun <A> fork(
        a: () -> Par<A>,
    ): Par<A> =
        { es: ExecutorService ->
            es.submit(Callable<A> { a()(es).get() })
        }
}

//fun sortPar(parList: Par<List<Int>>): Par<List<Int>> =
//    map3(parList, unit(Unit)) { a: List<Int>, _ -> a.sorted() }

fun <A, B> map(pa: Par<A>, f: (A) -> B): Par<B> =
    map2(pa, unit(Unit)) { a: A, _: Unit -> f(a) }

fun sortPar(parList: Par<List<Int>>): Par<List<Int>> =
    map(parList) { it.sorted() }

val step6 = {
    fun <A, B> asyncF(f: (A) -> B): (A) -> Par<B> = TODO()

    fun <A, B> parMap(
        ps: List<A>,
        f: (A) -> B,
    ): Par<List<B>> {
        val fbs: List<Par<B>> = ps.map(asyncF(f))
        TODO()
    }
}
