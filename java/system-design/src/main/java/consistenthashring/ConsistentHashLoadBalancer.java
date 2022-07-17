package consistenthashring;

import java.util.List;
import java.util.Map;
import java.util.TreeMap;

public class ConsistentHashLoadBalancer implements LoadBalancer {

    private final HashStrategy hashStrategy;
    private final static int VIRTUAL_NODE_COUNT = 5;
    private final TreeMap<Integer, MyServer> hashRing;

    public ConsistentHashLoadBalancer(List<MyServer> servers, HashStrategy hashStrategy) {
        this.hashStrategy = hashStrategy;
        this.hashRing = buildConsistentHashRing(servers);
    }

    private TreeMap<Integer, MyServer> buildConsistentHashRing(List<MyServer> servers) {
        TreeMap<Integer, MyServer> consistentHashRing = new TreeMap<>();
        for (MyServer server : servers) {
            for (int index = 0; index < VIRTUAL_NODE_COUNT; index++) {
                Integer hashCode = hashStrategy.hashCode(server.getIp() + "-" + index);
                consistentHashRing.put(hashCode, server);
            }
        }
        return consistentHashRing;
    }

    @Override
    public MyServer select(String key) {
        Integer hashKey = hashStrategy.hashCode(key);
        MyServer found = findLocation(hashKey);
        return found;
    }

    private MyServer findLocation(Integer hashKey) {
        Map.Entry<Integer, MyServer> locationEntry = hashRing.ceilingEntry(hashKey);
        if (locationEntry == null) {
            locationEntry = hashRing.firstEntry();
        }

        return locationEntry.getValue();
    }
}
