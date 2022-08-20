package intro

fun main() {

    // error: function can't not be assigned to variable.
//    val predicate = isEven
    val predicate = ::isEven // same as: val predicate = { i: Int -> isEven(i) }

    val action1 = { age: Int, name: String ->
        createPeople(age, name)
    }
    val action2 = ::createPeople // member reference: parameter가 동일할 때는 reference 호출로 간단하게 할 수 있다.

    // Bound Reference: object를 저장함. object의 멤버 호출을 delay할 수 있음.
}

fun isEven(i: Int): Boolean = i % 2 == 0

fun createPeople(age: Int, name: String) {

}