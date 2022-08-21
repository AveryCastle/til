package intro

class Person(val name: String, var age: Int)

fun main() {
//    val jimin = Person("Jimin", 27)
//    val square10 = Rectangle(10, 10)
//    square10.isSquare eq true

    // lambda result is calculated only once when we assign it.
//    println("$foo1 $foo1")
//    println("$foo2 $foo2")

//    StateLogger().state = true

//    val counter = LengthCounter()
//    println("before call addWord - counter: ${counter.counter}")
//    counter.addWord("Jimin is Cute and Sexy and Lovely.")
//    println("after call addWord - counter: ${counter.counter}")

    val sb = StringBuilder("Jimin?")
    sb.lastChar = '!'
    println(sb)
}

class Rectangle(private val height: Int, private val width: Int) {
    val isSquare: Boolean
        get() {
            return height == width
        }
}

val foo1 = run {
    println("calculating...foo1")
    27
}

val foo2: Int
    get() {
        println("calculating...foo2")
        return 29
    }

class StateLogger {
    var state = false
        set(value) {
            println("state has changed: from $field to $value")
            field = value
        }
}

class LengthCounter {
    var counter: Int = 0
        private set

    fun addWord(word: String) {
        counter += word.length
    }
}

interface User {
    val nickname: String
}

class FacebookUser(private val accountId: Int) : User {
    override val nickname: String = getFacebookName(accountId)

    private fun getFacebookName(accountId: Int): String {
        return "Anonymous"
    }
}

class SubscribeUser(private val email: String) : User {
    override val nickname: String
        get() = email.substringBefore("@")
}

var StringBuilder.lastChar: Char
    get() = get(length - 1)
    set(value: Char) {
        this.setCharAt(length - 1, value)
    }