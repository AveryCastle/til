package com.example.hackingspringboot.reactive.ch06;

import com.example.hackingspringboot.reactive.Item;
import com.example.hackingspringboot.reactive.ItemRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.hateoas.CollectionModel;
import org.springframework.hateoas.EntityModel;
import org.springframework.hateoas.IanaLinkRelations;
import org.springframework.hateoas.Link;
import org.springframework.hateoas.Links;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Mono;
import static org.springframework.hateoas.server.reactive.WebFluxLinkBuilder.linkTo;
import static org.springframework.hateoas.server.reactive.WebFluxLinkBuilder.methodOn;

@RestController
@RequiredArgsConstructor
public class AffordancesItemController {

    private final ItemRepository repository;

    @GetMapping("/affordances/items/{id}") // <1>
    Mono<EntityModel<Item>> findOne(@PathVariable String id) {
        AffordancesItemController controller = methodOn(AffordancesItemController.class); // <2>

        Mono<Link> selfLink = linkTo(controller.findOne(id)) //
            .withSelfRel() //
            .andAffordance(controller.updateItem(null, id)) // <3>
            .toMono();

        Mono<Link> aggregateLink = linkTo(controller.findAll()) //
            .withRel(IanaLinkRelations.ITEM) //
            .toMono();

        return Mono.zip(repository.findById(id), selfLink, aggregateLink) //
            .map(o -> EntityModel.of(o.getT1(), Links.of(o.getT2(), o.getT3())));
    }

    @GetMapping("/affordances/items")
    Mono<CollectionModel<EntityModel<Item>>> findAll() {
        AffordancesItemController controller = methodOn(AffordancesItemController.class);

        Mono<Link> aggregateRoot = linkTo(controller.findAll()) //
            .withSelfRel() //
            .andAffordance(controller.addNewItem(null)) // <1>
            .toMono();

        return this.repository.findAll() // <2>
            .flatMap(item -> findOne(item.getId())) // <3>
            .collectList() // <4>
            .flatMap(models -> aggregateRoot //
                .map(selfLink -> CollectionModel.of( //
                    models, selfLink))); // <5>
    }

    @PostMapping("/affordances/items") // <1>
    Mono<ResponseEntity<?>> addNewItem(@RequestBody Mono<EntityModel<Item>> item) { // <2>
        return item //
            .map(EntityModel::getContent) // <3>
            .flatMap(this.repository::save) // <4>
            .map(Item::getId) // <5>
            .flatMap(this::findOne) // <6>
            .map(newModel -> ResponseEntity.created(newModel // <7>
                .getRequiredLink(IanaLinkRelations.SELF) //
                .toUri()).body(newModel.getContent()));
    }

    @PutMapping("/affordances/items/{id}") // <1>
    public Mono<ResponseEntity<?>> updateItem(@RequestBody Mono<EntityModel<Item>> item, // <2>
        @PathVariable String id) {
        return item //
            .map(EntityModel::getContent) //
            .map(content -> new Item(id, content.getName(), // <3>
                content.getDescription(), content.getPrice())) //
            .flatMap(this.repository::save) // <4>
            .then(findOne(id)) // <5>
            .map(model -> ResponseEntity.noContent() // <6>
                .location(model.getRequiredLink(IanaLinkRelations.SELF).toUri()).build());
    }
}
