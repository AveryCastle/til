package com.example.springdocswagger.user.application.port.in;

import java.util.List;

public interface UserSearchUseCase {
    List<UserResponse> searchAll(final String id);
}
