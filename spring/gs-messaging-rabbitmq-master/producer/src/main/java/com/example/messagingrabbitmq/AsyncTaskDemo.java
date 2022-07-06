package com.example.messagingrabbitmq;

import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;

import java.util.stream.IntStream;

@Component
public class AsyncTaskDemo {

    @Autowired
    private RabbitTemplate rabbitTemplate;

    @Async
    public void someAsyncMethod() {
        try {
            Thread.sleep(100);  // Let me sleep for 3 sec
            IntStream.range(0, 100).forEach(index -> {
                String message = String.format("%s - %d", "Hello from RabbitMQ!", index);
                rabbitTemplate.convertAndSend(RabbitConfiguration.topicExchangeName, "foo.bar.baz", message);
            });
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        System.out.println("My Name " + Thread.currentThread().getName());
    }
}
