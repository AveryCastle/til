package com.example.hackingspringboot.reactive.ch06;

import com.example.hackingspringboot.reactive.Item;
import com.example.hackingspringboot.reactive.ItemRepository;
import java.net.URI;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@RestController
@RequiredArgsConstructor
public class ApiItemController {

    private final ItemRepository repository;

    @GetMapping("/api/items")
    public Flux<Item> findAll() {
        return repository.findAll();
    }

    @GetMapping("/api/items/{id}")
    public Mono<Item> findOne(@PathVariable String id) {
        return repository.findById(id);
    }

    @PostMapping("/api/items")
    public Mono<ResponseEntity<?>> addNewItem(@RequestBody Mono<Item> item) {
        return item.flatMap(el -> repository.save(el))
            .map(savedItem -> ResponseEntity.created(URI.create("/api/items" + savedItem.getId()))
                .body(savedItem));
    }

    @PutMapping("/api/items/{id}")
    Mono<ResponseEntity<?>> updateItem(@RequestBody Mono<Item> item, @PathVariable String id) {
        return item.map(content -> new Item(id, content.getName(), content.getDescription(), content.getPrice()))
            .flatMap(repository::save)
            .map(ResponseEntity::ok);
    }
}
