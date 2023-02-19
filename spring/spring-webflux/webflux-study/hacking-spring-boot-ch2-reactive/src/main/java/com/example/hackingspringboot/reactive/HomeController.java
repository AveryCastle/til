package com.example.hackingspringboot.reactive;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.reactive.result.view.Rendering;
import reactor.core.publisher.Mono;

@Controller
@RequiredArgsConstructor
public class HomeController {

    private final InventoryService inventoryService;
    private final CartService cartService;

    @GetMapping()
    Mono<Rendering> home() {
        return Mono.just(Rendering.view("home.html")
            .modelAttribute("items", inventoryService.getItems())
            .modelAttribute("cart", cartService.search("My Cart"))
            .build()
        );
    }

    // tag::3[]
    @PostMapping("/add/{id}")
    Mono<String> addToCart(@PathVariable String id) {
        return cartService.addToCart("My Cart", id)
            .thenReturn("redirect:/");
    }
    // end::3[]

    @GetMapping("/search")
    Mono<Rendering> search(@RequestParam(required = false) String name,
        @RequestParam(required = false) String description,
        @RequestParam(required = false) boolean useAnd) {
        return Mono.just(Rendering.view("home.html")
//            .modelAttribute("items", inventoryService.searchByExample(name, description, useAnd))
                .modelAttribute("items", inventoryService.searchByFluentExample(name, description, useAnd))
                .modelAttribute("cart", cartService.search("My Cart"))
                .build()
        );
    }
}
