package consistenthashring;

public interface LoadBalancer {

    MyServer select(String key);
}
