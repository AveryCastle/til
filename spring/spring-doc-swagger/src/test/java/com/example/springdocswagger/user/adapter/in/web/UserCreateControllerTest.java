package com.example.springdocswagger.user.adapter.in.web;

import com.example.springdocswagger.RestDocsTestSupport;
import com.example.springdocswagger.user.application.port.in.UserCreateUseCase;
import com.example.springdocswagger.user.application.port.in.UserResponse;
import com.example.springdocswagger.user.domain.User;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.restdocs.payload.JsonFieldType;

import java.time.LocalDateTime;

import static org.hamcrest.Matchers.containsString;
import static org.mockito.Mockito.when;
import static org.springframework.restdocs.mockmvc.MockMvcRestDocumentation.document;
import static org.springframework.restdocs.payload.PayloadDocumentation.*;
import static org.springframework.restdocs.snippet.Attributes.attributes;
import static org.springframework.restdocs.snippet.Attributes.key;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

/**
 * 참고
 * - https://spring.io/guides/gs/testing-web/
 * - https://docs.spring.io/spring-restdocs/docs/current/reference/html5/#getting-started-build-configuration
 */
@WebMvcTest(UserCreateController.class)
class UserCreateControllerTest extends RestDocsTestSupport {

    @MockBean
    private UserCreateUseCase userCreateUseCase;

    @Test
    public void shouldCreateUser() throws Exception {
        when(userCreateUseCase.create("SUGA", "suga@bts.com", "010-333-3333"))
                .thenReturn(UserResponse.of(new User(1L, "SUGA", "suga@bts.com", "010-333-3333", LocalDateTime.now(), null)));

        this.mockMvc.perform(post("/v1/users")
                        .contentType(MediaType.APPLICATION_JSON)
                        .accept(MediaType.APPLICATION_JSON)
                        .content("{\"account\": \"SUGA\",\n" +
                                "    \"email\": \"suga@bts.com\",\n" +
                                "    \"phoneNumber\": \"010-333-3333\"}"))
                .andExpect(status().isOk())
                .andExpect(content().string(containsString("SUGA")))
                .andDo(restDocs.document(
                        requestFields(
                                attributes(key("title").value("Fields for user creation")),
                                fieldWithPath("account").description("The user's account")
                                        .attributes(key("constraints").value("Must not be null. Must not be empty")),
                                fieldWithPath("email").description("The user's email")
                                        .attributes(key("constraints").value("Must not be null. Must not be empty")),
                                fieldWithPath("phoneNumber").description("The user's phone number")
                                        .attributes(key("constraints").value("Must not be null. Must not be empty"))
                        ),
                        responseFields(
                                fieldWithPath("id").type(JsonFieldType.NUMBER).description("사용자 ID"),
                                fieldWithPath("account").type(JsonFieldType.STRING).description("사용자 계정"),
                                fieldWithPath("email").type(JsonFieldType.STRING).description("이메일"),
                                fieldWithPath("phoneNumber").type(JsonFieldType.STRING).description("전화번호"),
                                fieldWithPath("createdAt").type(JsonFieldType.STRING).description("생성일자")
                        )));
    }
}