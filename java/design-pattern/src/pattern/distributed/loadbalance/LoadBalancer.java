package pattern.distributed.loadbalance;

import java.util.List;

public interface LoadBalancer {

    Server select(List<Server> server, Invocation invocation);
}
