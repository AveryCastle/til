package com.example.springdocswagger;

import com.example.springdocswagger.user.adapter.in.web.UserCreateController;
import com.example.springdocswagger.user.adapter.in.web.UserSearchController;
import org.junit.jupiter.api.Disabled;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.test.web.servlet.MockMvc;

@Disabled
@WebMvcTest({
        UserCreateController.class,
        UserSearchController.class
})
public abstract class ControllerTest {

    @Autowired
    protected MockMvc mockMvc;
}
