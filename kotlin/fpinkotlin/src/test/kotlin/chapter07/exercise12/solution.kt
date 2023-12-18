package chapter07.exercise12

import java.util.concurrent.ExecutorService
import java.util.concurrent.Future

typealias Par<A> = (ExecutorService) -> Future<A>

fun <A, B> chooser(pa: Par<A>, choices: (A) -> Par<B>): Par<B> = { es: ExecutorService ->
    val a: A = pa(es).get()
    // choices(a).invoke(es)와 구분 일치.
    choices(a)(es)
}

fun <A> choice(cond: Par<Boolean>, t: Par<A>, f: Par<A>): Par<A> = { es: ExecutorService ->
    chooser(cond) { if (it) t else f }(es)
}

fun <A> choiceN(n: Par<Int>, choices: List<Par<A>>): Par<A> = { es: ExecutorService ->
    chooser(n) { choices[it] }(es)
}

fun <K, V> choiceMap(
    key: Par<K>,
    choices: Map<K, Par<V>>,
): Par<V> = { es: ExecutorService ->
    chooser(key) { k -> choices[k]!! }(es)
}
