package pattern.observer;

import java.util.Random;

class RandomNumberGenerator extends NumberGenerator {

    private Random random = new Random();
    private int number;

    @Override
    int getNumber() {
        return number;
    }

    @Override
    void execute() {
        number = random.nextInt(50);
        notifyObserver();
    }
}
