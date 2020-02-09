package com.example.messagingrabbitmq;

import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.stereotype.Service;

import java.util.stream.IntStream;

@Service
public class Producer {

    private final RabbitTemplate rabbitTemplate;

    public Producer(RabbitTemplate rabbitTemplate) {
        this.rabbitTemplate = rabbitTemplate;
    }

    //    @Scheduled(fixedRate = 10 * 1000)
    public void sendMessage() {
        for (int i = 0; i < 5; i++) {
            new Thread(() -> {
                IntStream.range(0, 100).forEach(index -> {
                    String message = String.format("%s - %d", "Hello from RabbitMQ!", index);
                    rabbitTemplate.convertAndSend(RabbitConfiguration.topicExchangeName, "foo.bar.baz", message);
                });
            }).start();
        }
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
