package com.example.springdocswagger.user.application.port.in;

import com.example.springdocswagger.user.domain.User;
import lombok.AllArgsConstructor;
import lombok.Data;

import java.io.Serializable;
import java.time.LocalDateTime;

@Data
@AllArgsConstructor
public class UserResponse implements Serializable {

    private Long id;
    private String account;
    private String email;
    private String phoneNumber;
    private LocalDateTime createdAt;

    public static UserResponse of(User user) {
        return new UserResponse(user.getId(), user.getAccount(), user.getEmail(), user.getPhoneNumber(), user.getCreatedAt());
    }
}
