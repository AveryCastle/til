package com.example.hackingspringboot.reactive.ch05;

import java.util.List;
import java.util.stream.Collectors;
import lombok.RequiredArgsConstructor;
import org.springframework.boot.actuate.trace.http.HttpTrace;
import org.springframework.boot.actuate.trace.http.HttpTraceRepository;

@RequiredArgsConstructor
public class SpringDataHttpTraceRepository implements HttpTraceRepository {

    private final HttpTraceWrapperRepository repository;

    @Override
    public List<HttpTrace> findAll() {
        return repository.findAll()
            .map(HttpTraceWrapper::getHttpTrace)
            .collect(Collectors.toList());
    }

    @Override
    public void add(HttpTrace trace) {
        repository.save(new HttpTraceWrapper(trace));
    }
}
