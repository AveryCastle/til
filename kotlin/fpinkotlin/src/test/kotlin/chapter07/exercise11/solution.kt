package chapter07.exercise11

import java.util.concurrent.ExecutorService
import java.util.concurrent.Future

typealias Par<A> = (ExecutorService) -> Future<A>

// 내가 푼 버전
//fun <K, V> choiceMap(
//    key: Par<K>,
//    choices: Map<K, Par<V>>,
//): Par<V> = { es: ExecutorService ->
//    val k: K = key(es).get()
//    choices.getValue(k).invoke(es)
//}

// 해답지
fun <K, V> choiceMap(
    key: Par<K>,
    choices: Map<K, Par<V>>,
): Par<V> = { es: ExecutorService ->
    choices[key(es).get()]!!.invoke(es)
}
