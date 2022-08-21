package intro

val lazyProperty: String by lazy {
    println("computed!!")
    "Hello"
}

fun main() {
    println(lazyProperty)
    println(lazyProperty)
    println(lazyProperty)

    val myclass = MyClass()
    myclass.initializationLogic()
}

class MyClass {
    lateinit var lateInitializeVar: String

    fun initializationLogic() {
        println(this::lateInitializeVar.isInitialized)
        lateInitializeVar = "initialized!"
        println(this::lateInitializeVar.isInitialized)
    }
}