package chapter06.sec06

//import arrow.core.Id
//import arrow.core.Tuple2
//import arrow.core.extensions.id.monad.monad
//import arrow.mtl.State
//import arrow.mtl.extensions.fx

interface RNG {
    fun nextInt(): Pair<Int, RNG>
}

//val int: State<RNG, Int> = TODO()
//
//fun ints(x: Int): State<RNG, List<Int>> = TODO()
//
//fun <A, B> flatMap(
//    s: State<RNG, A>,
//    f: (A) -> State<RNG, B>
//): State<RNG, B> = TODO()
//
//fun <A, B> map(
//    s: State<RNG, A>,
//    f: (A) -> B
//): State<RNG, B> = TODO()
//
//val ns: State<RNG, List<Int>> =
//    flatMap(int) { x: Int ->
//        flatMap(int) { y: Int ->
//            map(ints(x)) { xs ->
//                xs.map { it % y }
//            }
//
//        }
//    }
//
//val ns2: State<RNG, List<Int>> =
//    State.fx(Id.monad()) {
//        val x: Int = int.bind()
//        val y: Int = int.bind()
//        val xs: List<Int> = ints(x).bind()
//        xs.map { it % y }
//    }
//
//fun <S> get(): State<S, S> =
//    State { s -> Pair(s, s) }
//
//fun <S> set(s: S): State<S, Unit> =
//    State { s -> Tuple2(s, Unit) }
