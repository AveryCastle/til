package pattern.observer;

class ObserverMain {

    public static void main(String[] args) {
        NumberGenerator numberGenerator = new RandomNumberGenerator();
        numberGenerator.addObserver(new DigitObserver());
        numberGenerator.addObserver(new GraphObserver());
        numberGenerator.execute();
    }
}
