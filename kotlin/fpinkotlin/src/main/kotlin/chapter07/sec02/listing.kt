package chapter07.sec02

import chapter07.sec01.Par
import java.util.concurrent.TimeUnit

fun interface Callable<A> {
    fun call(): A
}

interface Future<A> {
    fun get(): A
    fun get(timeout: Long, timeUnit: TimeUnit): A
    fun cancel(evenIfRunning: Boolean): Boolean
    fun isDone(): Boolean
    fun isCancelled(): Boolean
}

interface ExecutorService {
    fun <A> submit(a: Callable<A>): Future<A>
}

fun <A> run(ex: ExecutorService, a: Par<A>): A = TODO()

typealias Par<A> = (ExecutorService) -> Future<A>
