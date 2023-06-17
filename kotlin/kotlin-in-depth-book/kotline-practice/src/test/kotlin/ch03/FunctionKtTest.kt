package ch03

import org.junit.jupiter.api.Assertions.assertArrayEquals
import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Test
import kotlin.math.PI

internal class FunctionKtTest {

    @Test
    fun circleArea() {
        assertEquals(circleArea(3.1), PI * 3.1 * 3.1)
    }

    @Test
    fun increment() {
        assertEquals(increment(10), 11)
    }

    @Test
    fun printSorted() {
        assertArrayEquals(sortItems(10, 1, 6, 2), intArrayOf(1, 2, 6, 10))
    }
}
