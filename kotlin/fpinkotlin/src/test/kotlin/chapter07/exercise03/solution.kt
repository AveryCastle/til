package chapter07.exercise03

import chapter07.sec03.Par
import chapter07.sec03.Pars
import io.kotest.assertions.throwables.shouldThrow
import io.kotest.core.spec.style.WordSpec
import io.kotest.matchers.shouldBe
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.util.concurrent.*


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

class Solution3 : WordSpec({

    val es: ExecutorService = ThreadPoolExecutor(
        1,
        1,
        5,
        TimeUnit.SECONDS,
        LinkedBlockingQueue()
    )

    "map2" should {
        "allow two futures to run within a given timeout" {

            val pa = Pars.fork {
                Thread.sleep(400L)
                Pars.unit(1)
            }
            val pb = Pars.fork {
                Thread.sleep(500L)
                Pars.unit("1")
            }
            val pc: Par<Long> =
                map2(pa, pb) { a: Int, b: String ->
                    a + b.toLong()
                }

            withContext(Dispatchers.IO) {
                pc(es).get(1, TimeUnit.SECONDS) shouldBe 2L
            }
        }

        "timeout if first future exceeds timeout" {

            val pa = Pars.fork {
                Thread.sleep(1100L)
                Pars.unit(1)
            }
            val pb = Pars.fork {
                Thread.sleep(500L)
                Pars.unit("1")
            }
            val pc: Par<Long> =
                map2(pa, pb) { a: Int, b: String ->
                    a + b.toLong()
                }

            withContext(Dispatchers.IO) {
                shouldThrow<TimeoutException> {
                    pc(es).get(1, TimeUnit.SECONDS)
                }
            }
        }

        "timeout if second future exceeds timeout" {

            val pa = Pars.fork {
                Thread.sleep(100L)
                Pars.unit(1)
            }
            val pb = Pars.fork {
                Thread.sleep(1000L)
                Pars.unit("1")
            }
            val pc: Par<Long> =
                map2(pa, pb) { a: Int, b: String ->
                    a + b.toLong()
                }

            withContext(Dispatchers.IO) {
                shouldThrow<TimeoutException> {
                    pc(es).get(1, TimeUnit.SECONDS)
                }
            }
        }
    }
})
