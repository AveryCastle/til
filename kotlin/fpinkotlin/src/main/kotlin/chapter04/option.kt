package chapter04

sealed class Option<out A> {

    companion object {
        fun <A> empty(): Option<A> = None
    }

    fun <A, B> Option<A>.map(f: (A) -> B): Option<B> =
        when (this) {
            is None -> None
            is Some -> Some(f(this.get))
        }

    fun <A, B> Option<A>.flatMap(f: (A) -> Option<B>): Option<B> =
        when (this) {
            is None -> None
            is Some -> f(this.get)
        }

    fun <A> Option<A>.getOrElse(default: () -> A): A =
        when (this) {
            is None -> default()
            is Some -> this.get
        }

    fun <A> Option<A>.orElse(ob: () -> Option<A>): Option<A> =
        when (this) {
            is None -> ob()
            is Some -> this
        }

    fun <A> Option<A>.filter(f: (A) -> Boolean): Option<A> =
        when (this) {
            is None -> None
            is Some ->
                if (f(this.get)) this
                else None
        }

    fun isEmpty(): Boolean = this
        .map { false }
        .getOrElse { true }
}

data class Some<out A>(val get: A) : Option<A>()

data object None : Option<Nothing>()
