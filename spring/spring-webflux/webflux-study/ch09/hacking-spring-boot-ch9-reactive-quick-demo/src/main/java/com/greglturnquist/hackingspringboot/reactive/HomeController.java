package com.greglturnquist.hackingspringboot.reactive;

import lombok.RequiredArgsConstructor;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.reactive.result.view.Rendering;
import reactor.core.publisher.Mono;

@Controller
@RequiredArgsConstructor
public class HomeController {

    private final InventoryService inventoryService;

    // tag::user-cart[]
    @GetMapping
    Mono<Rendering> home(Authentication auth) { // <1>
        return Mono.just(Rendering.view("home.html") //
            .modelAttribute("items", this.inventoryService.getInventory()) //
            .modelAttribute("cart", this.inventoryService.getCart(cartName(auth)) // <2>
                .defaultIfEmpty(new Cart(cartName(auth)))) //
            .modelAttribute("auth", auth) // <3>
            .build());
    }
    // end::user-cart[]

    // tag::adjust-cart[]
    @PostMapping("/add/{id}")
    Mono<String> addToCart(Authentication auth, @PathVariable String id) {
        return this.inventoryService.addItemToCart(cartName(auth), id) //
            .thenReturn("redirect:/");
    }

    @DeleteMapping("/remove/{id}")
    Mono<String> removeFromCart(Authentication auth, @PathVariable String id) {
        return this.inventoryService.removeOneFromCart(cartName(auth), id) //
            .thenReturn("redirect:/");
    }
    // end::adjust-cart[]

    // tag::inventory[]
    @PostMapping
    @ResponseBody
    Mono<Item> createItem(@RequestBody Item newItem) {
        return this.inventoryService.saveItem(newItem);
    }

    @DeleteMapping("/{id}")
    @ResponseBody
    Mono<Void> deleteItem(@PathVariable String id) {
        return this.inventoryService.deleteItem(id);
    }
    // end::inventory[]

    // tag::cartName[]
    private static String cartName(Authentication auth) {
        return auth.getName() + "'s Cart";
    }
}
