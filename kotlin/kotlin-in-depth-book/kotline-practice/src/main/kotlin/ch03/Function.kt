package ch03

import kotlin.math.PI

fun circleArea(radius: Double): Double {
    return PI * radius * radius
}

fun increment(n: Int): Int = n + 1

fun sortItems(vararg items: Int): IntArray {
    items.sort()
    return items
}
