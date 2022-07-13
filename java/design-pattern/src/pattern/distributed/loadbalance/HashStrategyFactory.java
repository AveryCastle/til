package pattern.distributed.loadbalance;

public class HashStrategyFactory {

    public HashStrategy create(HashAlgorithm algorithm) {
        switch (algorithm) {
            case JDK_HASHCODE:
                return new JdkHashCodeStrategy();
            case MD5:
                return new MD5HashStrategy();
            default:
                return new FnvHashStrategy();
        }
    }
}
