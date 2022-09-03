package com.example.springdocswagger.user.adapter.in.web;

import com.example.springdocswagger.user.application.port.in.UserCreateUseCase;
import com.example.springdocswagger.user.application.port.in.UserResponse;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import java.io.Serializable;

@RestController
@RequestMapping("/v1/users")
@RequiredArgsConstructor
public class UserCreateController {

    private final UserCreateUseCase userCreateUsecase;

    @PostMapping
    public ResponseEntity<UserResponse> create(@RequestBody @Valid UserCreateCommand userCreateCommand) {
        UserResponse userResponse = userCreateUsecase.create(userCreateCommand.getAccount(), userCreateCommand.getEmail(), userCreateCommand.getPhoneNumber());
        return ResponseEntity.ok(userResponse);
    }

    @Data
    public static class UserCreateCommand implements Serializable {

        @NotBlank
        private String account;
        @NotBlank
        private String email;
        @NotBlank
        private String phoneNumber;
    }
}
