package pattern.distributed.loadbalance;

import java.util.List;
import java.util.Map;
import java.util.TreeMap;

public class ConsistentHashLoadBalancer implements LoadBalancer {

    private static final int VIRTUAL_NODE_SIZE = 5;

    private final static String VIRTUAL_NODE_SUFFIX = "-";

    private final HashStrategy hashStrategy;

    private final HashStrategyFactory hashStrategyFactory = new HashStrategyFactory();

    public ConsistentHashLoadBalancer() {
        HashStrategy hashStrategy = hashStrategyFactory.create(null);
        this.hashStrategy = hashStrategy;
    }

    public ConsistentHashLoadBalancer(HashAlgorithm algorithm) {
        HashStrategy hashStrategy = hashStrategyFactory.create(algorithm);
        this.hashStrategy = hashStrategy;
    }

    @Override
    public Server select(List<Server> servers, Invocation invocation) {
        int invocationHashCode = hashStrategy.getHashCode(invocation.getHashKey());
        TreeMap<Integer, Server> ring = buildConsistentHashRing(servers);
        Server server = findLocate(ring, invocationHashCode);
        return server;
    }

    private TreeMap<Integer, Server> buildConsistentHashRing(List<Server> servers) {
        TreeMap<Integer, Server> virtualNodeRing = new TreeMap<>();
        for (Server server : servers) {
            for (int i = 0; i < VIRTUAL_NODE_SIZE; i++) {
                // 가상 노드를 추가하는 방법이 영향을 미치는 경우 물리적 노드에서 가상 노드를 확장하는 클래스를 추상화할 수도 있습니다.
                int hashKey = hashStrategy.getHashCode(server.getAddress() + VIRTUAL_NODE_SUFFIX + i);
                virtualNodeRing.put(hashKey, server);
            }
        }
        return virtualNodeRing;
    }

    private Server findLocate(TreeMap<Integer, Server> ring, int invocationHashCode) {
//        if (!ring.containsKey(invocationHashCode)) {
//            SortedMap<Integer, Server> tailMap = ring.tailMap(invocationHashCode);
//            int tailHashCode = tailMap.isEmpty() ? ring.firstKey() : tailMap.firstKey();
//            return ring.get(tailHashCode);
//        }
//
//        return ring.get(invocationHashCode);
        // key: 오른쪽에서 첫번째를 찾는다.
        Map.Entry<Integer, Server> locateEntry = ring.ceilingEntry(invocationHashCode);
        if (locateEntry == null) {
            // Ring이라고 생각할 때, 꼬리 지나서 처음 찾는 key
            locateEntry = ring.firstEntry();
        }
        return locateEntry.getValue();
    }
}
