package com.greglturnquist.hackingspringboot.reactive;

import lombok.RequiredArgsConstructor;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Flux;

@RestController
@RequiredArgsConstructor
public class ServerController {

    private final KitchenService kitchen;

    @GetMapping(value = "/server", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<Dish> serveDishes() {
        return kitchen.getDishes();
    }

    @GetMapping(value = "/served-dishes", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    Flux<Dish> deliverDishes() {
        return kitchen.getDishes()
            .map(dish -> Dish.deliver(dish));
    }
}
