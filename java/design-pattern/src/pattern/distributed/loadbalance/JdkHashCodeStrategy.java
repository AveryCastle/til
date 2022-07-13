package pattern.distributed.loadbalance;

public class JdkHashCodeStrategy implements HashStrategy {

    @Override
    public int getHashCode(String key) {
        return key.hashCode();
    }
}
