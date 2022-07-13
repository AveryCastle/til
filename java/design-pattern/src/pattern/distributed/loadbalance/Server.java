package pattern.distributed.loadbalance;

public class Server {

    private String address;

    public Server(String address) {
        this.address = address;
    }

    public String getAddress() {
        return address;
    }
}
