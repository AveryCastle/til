package pattern.unique.id;

import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.IntStream;

public class IntToBit {

    private static final AtomicInteger atomicInteger = new AtomicInteger();
    private static final long BASIS_TIME = LocalDateTime.of(2022, 1, 1, 0, 0, 0, 0).toEpochSecond(ZoneOffset.UTC);

    public static void main(String[] args) {
        System.out.println(UUID.randomUUID());
//        IntStream.rangeClosed(0, 100000).parallel().forEach(el -> {
//            long now = System.currentTimeMillis() - BASIS_TIME;
//
//            String signStr = Long.toBinaryString(0);
//            String timeStr = String.format("%41s", Long.toBinaryString(now)).replaceAll(" ", "0");
//            String datacenter = String.format("%5s", Long.toBinaryString(1)).replaceAll(" ", "0");
//            String serverIndex = String.format("%5s", Long.toBinaryString(1)).replaceAll(" ", "0");
//            if (System.currentTimeMillis() - BASIS_TIME - now > 0) {
//                atomicInteger.set(0);
//            }
//            String serial = String.format("%12s", Integer.toBinaryString(atomicInteger.getAndIncrement())).replaceAll(" ", "0");
//
//            String uniqueIdString = signStr + timeStr + datacenter + serverIndex + serial;
//            System.out.println(uniqueIdString);
//
//            long uniqueId = Long.parseLong(uniqueIdString, 2);
//            System.out.println(uniqueId);
//        });


//        for (int i = 0; i < 5; i++) {
//            String binaryString = Integer.toBinaryString(i);
//            System.out.println(String.format("%32s", binaryString).replaceAll(" ", "0"));
//        }
    }
}
