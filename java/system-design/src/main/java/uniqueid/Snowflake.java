package uniqueid;

import java.time.Instant;
import java.time.Year;
import java.time.ZoneOffset;
import java.util.concurrent.atomic.AtomicLong;

/**
 * 참고: https://github.com/callicoder/java-snowflake/blob/master/src/main/java/com/callicoder/snowflake/Snowflake.java
 */
public class Snowflake {

    private static final int UNUSED_BITS = 1; // Sign bit, Unused (always set to 0)
    private static final int TIMESTAMP_BITS = 41;
    private static final int DATACENTER_BITS = 5;
    private static final int SERVER_BITS = 5;
    private static final int SEQUENCE_BITS = 12;
    private static final long BASIS_EPOCH = Year.of(2022).atMonth(1).atDay(1).atTime(0, 0, 0).atZone(ZoneOffset.UTC).toInstant().toEpochMilli();
    private static AtomicLong sequence = new AtomicLong(0l);
    private static final long maxSequence = (1L << SEQUENCE_BITS) - 1;
    private static AtomicLong lastTimestamp = new AtomicLong(-1l);

    public synchronized static long nextValue(int dataCenter, int server) {
        long currentTimeMillis = timestamp();
        lastTimestamp.set(currentTimeMillis);

        if (currentTimeMillis == lastTimestamp.get()) {
            sequence.set((sequence.get() + 1) & maxSequence);
            if (sequence.get() == 0) {
                // Sequence Exhausted, wait till next millisecond.
                currentTimeMillis = waitNextMillis(currentTimeMillis);
            }
        } else {
            // reset sequence to start with zero for the next millisecond
            sequence.set(0);
        }

        lastTimestamp.set(currentTimeMillis);

        long uniqueId = currentTimeMillis << (DATACENTER_BITS + SERVER_BITS + SEQUENCE_BITS)
                | (dataCenter << (SERVER_BITS + SEQUENCE_BITS))
                | (server << SEQUENCE_BITS)
                | sequence.get();
        return uniqueId;
    }

    public static long[] parse(long id) {
        long maskDatacenter = ((1L << (DATACENTER_BITS + SERVER_BITS)) - 1) << SEQUENCE_BITS;
        long maskServer = ((1L << SERVER_BITS) - 1) << SEQUENCE_BITS;
        long maskSequence = (1L << SEQUENCE_BITS) - 1;

        long timestamp = (id >> (DATACENTER_BITS + SERVER_BITS + SEQUENCE_BITS)) + BASIS_EPOCH;
        long datacenterId = (id & maskDatacenter) >> (SERVER_BITS + SEQUENCE_BITS);
        long serverId = (id & maskServer) >> SEQUENCE_BITS;
        long sequence = id & maskSequence;

        return new long[]{timestamp, datacenterId, serverId, sequence};
    }

    // Get current timestamp in milliseconds, adjust for the custom epoch.
    private static long timestamp() {
        return Instant.now().toEpochMilli() - BASIS_EPOCH;
    }

    // Block and wait till next millisecond
    private static long waitNextMillis(long currentTimestamp) {
        while (currentTimestamp == lastTimestamp.get()) {
            currentTimestamp = timestamp();
        }
        return currentTimestamp;
    }
}
