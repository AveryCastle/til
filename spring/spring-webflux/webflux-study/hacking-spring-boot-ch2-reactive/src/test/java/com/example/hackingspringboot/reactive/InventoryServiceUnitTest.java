package com.example.hackingspringboot.reactive;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.when;
import java.util.Collections;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.data.mongodb.core.ReactiveFluentMongoOperations;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

@ExtendWith(SpringExtension.class)
class InventoryServiceUnitTest {

    InventoryService inventoryService;

    @MockBean
    private ItemRepository itemRepository;

    @MockBean
    private CartRepository cartRepository;

    @MockBean
    private ReactiveFluentMongoOperations fluentOperations;

    @BeforeEach
        // <1>
    void setUp() {
        // Define test data <2>
        Item sampleItem = new Item("item1", "TV tray", "Alf TV tray", 19.99);
        CartItem sampleCartItem = new CartItem(sampleItem);
        Cart sampleCart = new Cart("My Cart", Collections.singletonList(sampleCartItem));

        // Define mock interactions provided
        // by your collaborators <3>
        when(cartRepository.findById(anyString())).thenReturn(Mono.empty());
        when(itemRepository.findById(anyString())).thenReturn(Mono.just(sampleItem));
        when(cartRepository.save(any(Cart.class))).thenReturn(Mono.just(sampleCart));

        inventoryService = new InventoryService(itemRepository, cartRepository); // <4>
    }

    @Test
    void addItemToEmptyCartShouldProduceOneCartItem() {
        inventoryService.addItemToCart("My Cart", "item1")
            .as(StepVerifier::create)
            .expectNextMatches(cart -> {
                assertThat(cart.getCartItems()).extracting(CartItem::getQuantity)
                    .containsExactlyInAnyOrder(1);

                assertThat(cart.getCartItems()).extracting(CartItem::getItem)
                    .containsExactly(new Item("item1", "TV tray", "Alf TV tray", 19.99));

                return true;
            })
            .verifyComplete();
    }

    @Test
    void alternativeWayToTest() {
        StepVerifier.create(
                inventoryService.addItemToCart("My Cart", "item1"))
            .expectNextMatches(cart -> {
                assertThat(cart.getCartItems()).extracting(CartItem::getQuantity)
                    .containsExactlyInAnyOrder(1);

                assertThat(cart.getCartItems()).extracting(CartItem::getItem)
                    .containsExactly(new Item("item1", "TV tray", "Alf TV tray", 19.99));

                return true;
            })
            .verifyComplete();
    }
}
