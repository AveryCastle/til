package com.greglturnquist.hackingspringboot.rsocketclient;

import static io.rsocket.metadata.WellKnownMimeType.MESSAGE_RSOCKET_ROUTING;
import java.net.URI;
import java.time.Duration;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.messaging.rsocket.RSocketRequester;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import reactor.util.retry.Retry;

@RestController
public class RSocketController {

    private final RSocketRequester requester;

    public RSocketController(RSocketRequester.Builder builder) {
//        requester = builder.dataMimeType(MediaType.APPLICATION_JSON)
////            .metadataMimeType(parseMediaType(MESSAGE_RSOCKET_ROUTING.toString()))
//            .tcp("localhost", 8000);
        requester = builder.rsocketConnector(connector -> {
            connector.dataMimeType(MediaType.APPLICATION_JSON_VALUE);
            connector.metadataMimeType(MESSAGE_RSOCKET_ROUTING.toString());
            connector.reconnect(Retry.max(5));
        }).tcp("127.0.0.1", 8000);
    }

    @PostMapping("/items/request-response")
    Mono<ResponseEntity<?>> addNeItemUsingRSocketRequestResponse(@RequestBody Item item) {
        return requester
            .route("newItems.request-response")
            .data(item)
            .retrieveMono(Item.class)
            .map(savedItem -> ResponseEntity.created(
                URI.create("/items/request-response")).body(savedItem));
    }

    @GetMapping(value = "/items/request-stream", produces = MediaType.APPLICATION_NDJSON_VALUE)
    Flux<Item> findItemsUsingRSocketRequestStream() {
        return requester
            .route("newItems.request-stream")
            .retrieveFlux(Item.class)
            .delayElements(Duration.ofSeconds(1));
    }

    @PostMapping("/items/fire-and-forget")
    Mono<ResponseEntity<?>> addNewItemUsingRSocketFireAndForget(@RequestBody Item item) {
        return requester
            .route("newItems.fire-and-forget")
            .data(item)
            .send()
            .then(Mono.just(
                ResponseEntity.created(URI.create("/items/fire-and-forget")).build()
            ));
    }

    @GetMapping(value = "/items", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    Flux<Item> liveUpdates() {
        return requester
            .route("newItems.monitor")
            .retrieveFlux(Item.class);
    }

}
