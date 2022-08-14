package intro

import java.io.IOException


@Throws(IOException::class)
fun fnBar() {
    throw IOException("foo exception!!!")
}

fun fnFoo() {
    throw IOException("foo exception!!!")
}
