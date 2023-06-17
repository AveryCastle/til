package ch03

import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Test

internal class ConditionsKtTest {

    @Test
    fun max() {
        assertEquals(100, max(10, 100))
    }

    @Test
    fun test1() {
        assertEquals("13717", divide("1234567890", 7))
    }

    @Test
    fun hexDigit() {
        assertEquals('9', hexDigit(9))
        assertEquals('A', hexDigit(10))
        assertEquals('B', hexDigit(11))
        assertEquals('?', hexDigit(20))
    }

    @Test
    fun length() {
        assertEquals(5, ch03.length("hello"))
        assertEquals(null, ch03.length(null))
    }

    @Test
    fun strictLength() {
        assertEquals(5, ch03.strictLength("hello"))
        assertEquals(0, ch03.strictLength(null))
    }
}
