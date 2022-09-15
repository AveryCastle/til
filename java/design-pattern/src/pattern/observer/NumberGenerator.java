package pattern.observer;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

abstract class NumberGenerator {

    private List<Observer> observers = new ArrayList<>();

    void addObserver(Observer observer) {
        observers.add(observer);
    }

    void deleteObserver(Observer observer) {
        observers.remove(observer);
    }

    void notifyObserver() {
        Iterator<Observer> iterator = observers.iterator();
        while (iterator.hasNext()) {
            Observer o = iterator.next();
            o.update(this);
        }
    }

    abstract int getNumber();

    abstract void execute();
}
