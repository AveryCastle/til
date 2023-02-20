package com.example.hackingspringboot.reactive;

import java.util.logging.Level;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;
import reactor.core.publisher.SignalType;

@Service
@RequiredArgsConstructor
public class CartService {

    private final ItemRepository itemRepository;
    private final CartRepository cartRepository;

    Mono<Cart> addToCart(String cartId, String id) {
        return cartRepository.findById(cartId)
            .log("foundCart", Level.ALL, SignalType.ON_COMPLETE)
            .defaultIfEmpty(new Cart(cartId))
            .log("emptyCart", Level.ALL, SignalType.CURRENT_CONTEXT)
            .flatMap(cart -> cart.getCartItems().stream() // <4>
                .filter(cartItem -> cartItem.getItem() //
                    .getId().equals(id)) //
                .findAny() //
                .map(cartItem -> {
                    cartItem.increment();
                    return Mono.just(cart).log("newCartItem");
                }) //
                .orElseGet(() -> { // <5>
                    return itemRepository.findById(id)
                        .log("fetchedItem")
                        .map(item -> new CartItem(item))
                        .map(cartItem -> {
                            cart.getCartItems().add(cartItem);
                            return cart;
                        }).log("addedCartItem");
                }))
            .flatMap(cart -> cartRepository.save(cart))
            .log("savedCart");
    }

    public Mono<Cart> search(String id) {
        return cartRepository.findById(id)
            .defaultIfEmpty(new Cart(id));
    }
}
