package com.example.hackingspringboot.reactive.ch05;

import org.springframework.boot.actuate.trace.http.HttpTrace;
import org.springframework.data.annotation.Id;

public class HttpTraceWrapper {

    private @Id String id; // <1>

    private HttpTrace httpTrace; // <2>

    public HttpTraceWrapper(HttpTrace httpTrace) { // <3>
        this.httpTrace = httpTrace;
    }

    public HttpTrace getHttpTrace() { // <4>
        return httpTrace;
    }
}
