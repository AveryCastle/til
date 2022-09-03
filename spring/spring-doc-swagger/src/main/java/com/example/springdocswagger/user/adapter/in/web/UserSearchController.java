package com.example.springdocswagger.user.adapter.in.web;

import com.example.springdocswagger.user.application.port.in.UserResponse;
import com.example.springdocswagger.user.application.port.in.UserSearchUseCase;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import javax.websocket.server.PathParam;
import java.util.List;

@RestController
@RequestMapping("/v1/users")
@RequiredArgsConstructor
public class UserSearchController {
    private final UserSearchUseCase userSearchUseCase;

    @GetMapping()
    public List<UserResponse> getAll(@RequestParam(name = "ordering", defaultValue = "id") String ordering) {
        List<UserResponse> allUsers = userSearchUseCase.searchAll(ordering);
        return allUsers;
    }
}
