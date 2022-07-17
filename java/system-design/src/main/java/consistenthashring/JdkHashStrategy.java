package consistenthashring;

public class JdkHashStrategy implements HashStrategy {

    @Override
    public Integer hashCode(String key) {
        return key.hashCode();
    }
}
