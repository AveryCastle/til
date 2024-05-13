package chapter08.sec01


fun main() {
    val listGen: Gen<List<Int>> = Gen.forLists(Gen.choose(0, 100))
    val generatedList: List<Int> = listGen.random().first()
    println(generatedList)
}
