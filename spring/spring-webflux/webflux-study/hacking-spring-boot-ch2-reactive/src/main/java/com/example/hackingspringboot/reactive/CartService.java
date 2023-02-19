package com.example.hackingspringboot.reactive;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

@Service
@RequiredArgsConstructor
public class CartService {

    private final ItemRepository itemRepository;
    private final CartRepository cartRepository;

    Mono<Cart> addToCart(String cartId, String id) {
        return cartRepository.findById(cartId) //
            .defaultIfEmpty(new Cart(cartId)) // <3>
            .flatMap(cart -> cart.getCartItems().stream() // <4>
                .filter(cartItem -> cartItem.getItem() //
                    .getId().equals(id)) //
                .findAny() //
                .map(cartItem -> {
                    cartItem.increment();
                    return Mono.just(cart);
                }) //
                .orElseGet(() -> { // <5>
                    return itemRepository.findById(id) //
                        .map(item -> new CartItem(item)) //
                        .map(cartItem -> {
                            cart.getCartItems().add(cartItem);
                            return cart;
                        });
                }))
            .flatMap(cart -> cartRepository.save(cart)); // <6>
    }

    public Mono<Cart> search(String id) {
        return cartRepository.findById(id)
            .defaultIfEmpty(new Cart(id));
    }
}
