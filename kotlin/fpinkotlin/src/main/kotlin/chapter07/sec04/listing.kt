package chapter07.sec04

import chapter07.sec03.Par
import chapter07.sec03.Pars.fork
import chapter07.sec03.Pars.lazyUnit
import java.util.concurrent.ExecutorService
import java.util.concurrent.Executors

//typealias Par<A> = (ExecutorService) -> Future<A>

infix fun <A> Par<A>.shouldBe(other: Par<A>) = { es: ExecutorService ->
    if (this(es).get() != other(es).get())
        throw AssertionError("Par instances not equal")
}

val es = Executors.newFixedThreadPool(1)

val a: Par<Int> = lazyUnit { 42 + 1 }
val b: Par<Int> = fork { a }
//(a shouldBe b)(es)

