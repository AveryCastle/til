package pattern.distributed.loadbalance;

public interface HashStrategy {

    int getHashCode(String key);
}
