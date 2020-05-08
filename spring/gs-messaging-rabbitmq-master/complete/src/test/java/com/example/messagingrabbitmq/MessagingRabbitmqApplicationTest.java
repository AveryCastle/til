/*
 * Copyright 2012-2015 the original author or authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *	  https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.example.messagingrabbitmq;

import org.junit.jupiter.api.Test;

import org.springframework.amqp.AmqpConnectException;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;

import java.util.Random;

@SpringBootTest
public class MessagingRabbitmqApplicationTest {

//    @MockBean
//    private Producer producer;

    @Autowired
    private RabbitTemplate rabbitTemplate;

    @Autowired
    private Consumer consumer;

    @Test
    public void test() throws Exception {
        try {
            rabbitTemplate.convertAndSend(RabbitConfiguration.queueName1, "Hello from RabbitMQ!");
        } catch (AmqpConnectException e) {
            // ignore - rabbit is not running
        }
    }

    @Test
    public void test2() {
        Random random = new Random();
        int i = random.nextInt(1);
        System.out.println(i);
    }
}
