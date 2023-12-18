package chapter07.exercise10

import chapter07.sec03.map
import java.util.concurrent.ExecutorService
import java.util.concurrent.Future

typealias Par<A> = (ExecutorService) -> Future<A>

fun <A> choiceN(n: Par<Int>, choices: List<Par<A>>): Par<A> = { es: ExecutorService ->
    choices[n(es).get()].invoke(es)
}

fun <A> choice(cond: Par<Boolean>, t: Par<A>, f: Par<A>): Par<A> = { es: ExecutorService ->
    choiceN(
        map(cond) { if (it) 1 else 0 },
        listOf(t, f)
    )(es)
}
