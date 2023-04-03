package com.example.hackingspringboot.reactive;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.reactive.result.view.Rendering;
import reactor.core.publisher.Mono;

@Slf4j
@Controller
@RequiredArgsConstructor
public class HomeController {

    private final InventoryService inventoryService;
    private final CartService cartService;

    @GetMapping()
    Mono<Rendering> home() {
        return Mono.just(Rendering.view("home.html")
//            .modelAttribute("items", inventoryService.getItems().doOnNext(item -> log.info("{}", item))) // with logging
                .modelAttribute("items", inventoryService.getInventory())
                .modelAttribute("cart", inventoryService.getCart("My Cart")
                    .defaultIfEmpty(new Cart("My Cart")))
                .build()
        );
    }

    @PostMapping("/add/{id}")
    Mono<String> addToCart(@PathVariable String id) {
        return this.inventoryService.addItemToCart("My Cart", id)
            .thenReturn("redirect:/");
    }

    @DeleteMapping("/remove/{id}")
    Mono<String> removeFromCart(@PathVariable String id) {
        return this.inventoryService.removeOneFromCart("My Cart", id)
            .thenReturn("redirect:/");
    }

    @PostMapping
    Mono<String> createItem(@ModelAttribute Item newItem) {
        return this.inventoryService.saveItem(newItem) //
            .thenReturn("redirect:/");
    }

    @DeleteMapping("/delete/{id}")
    Mono<String> deleteItem(@PathVariable String id) {
        return this.inventoryService.deleteItem(id) //
            .thenReturn("redirect:/");
    }

//    @GetMapping("/search")
//    Mono<Rendering> search(@RequestParam(required = false) String name,
//        @RequestParam(required = false) String description,
//        @RequestParam(required = false) boolean useAnd) {
//        return Mono.just(Rendering.view("home.html")
////            .modelAttribute("items", inventoryService.searchByExample(name, description, useAnd))
//                .modelAttribute("items", inventoryService.searchByFluentExample(name, description, useAnd))
//                .modelAttribute("cart", cartService.search("My Cart"))
//                .build()
//        );
//    }
}
