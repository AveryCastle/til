package mastermind

data class Evaluation(val rightPosition: Int, val wrongPosition: Int)

fun evaluateGuess(secret: String, guess: String): Evaluation {
    var (rightPosition, wrongPosition) = 0 to 0
    val secretHash: HashMap<Char, Int> = HashMap()
    val guessHash: HashMap<Char, Int> = HashMap()
    val wrongPositionSet: HashSet<Char> = HashSet()

    for (ch in secret) {
        if (ch in secretHash.keys) secretHash[ch] = secretHash[ch]!!.plus(1) else secretHash[ch] = 1
    }

    for (ch in guess) {
        if (ch in guessHash.keys) guessHash[ch] = guessHash[ch]!!.plus(1) else guessHash[ch] = 1
    }

    for ((index, value) in guess.withIndex()) {
        when {
            index < secret.length && value == secret[index] -> {
                rightPosition++
                if (wrongPositionSet.contains(value)) wrongPositionSet.remove(value)
            }
            value in secretHash.keys && secretHash[value]!! > 0 -> {
                wrongPosition++
                wrongPositionSet.add(value)

                calculateHash(secretHash, value)

                calculateHash(guessHash, value)
            }
        }
    }

    return Evaluation(rightPosition, wrongPositionSet.size)
}

private fun calculateHash(hashMap: HashMap<Char, Int>, value: Char) {
    if (hashMap[value]!! > 1) {
        hashMap[value] = hashMap[value]!!.minus(1)
    } else {
        hashMap.remove(value)
    }
}
