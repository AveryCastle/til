package chapter07.sec03

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

    fun <A, B, C> map2(
        a: Par<A>,
        b: Par<B>,
        f: (A, B) -> C,
    ): Par<C> =
        { es: ExecutorService ->
            val af: Future<A> = a(es)
            val bf: Future<B> = b(es)
            UnitFuture(f(af.get(), bf.get()))
        }

    fun <A> fork(
        a: () -> Par<A>,
    ): Par<A> =
        { es: ExecutorService ->
            es.submit(Callable<A> { a()(es).get() })
        }
}
