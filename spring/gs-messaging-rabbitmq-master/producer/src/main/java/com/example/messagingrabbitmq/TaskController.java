package com.example.messagingrabbitmq;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;

@RestController
public class TaskController {

    @Autowired
    private AsyncTaskDemo asyncDemo;

    @GetMapping("/hello")
    public Map<String, String> callAsyncMethod() {
        asyncDemo.someAsyncMethod();
        return new HashMap<String, String>();  // returns empty braces
    }
}
