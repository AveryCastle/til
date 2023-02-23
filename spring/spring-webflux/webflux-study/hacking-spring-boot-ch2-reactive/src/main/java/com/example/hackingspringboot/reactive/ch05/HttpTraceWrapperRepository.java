package com.example.hackingspringboot.reactive.ch05;

import java.util.stream.Stream;
import org.springframework.data.repository.Repository;

public interface HttpTraceWrapperRepository extends //
    Repository<HttpTraceWrapper, String> {

    Stream<HttpTraceWrapper> findAll(); // <1>

    void save(HttpTraceWrapper trace); // <2>
}
