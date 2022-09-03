package com.example.springdocswagger.user.adapter.in.web;

import com.example.springdocswagger.RestDocsTestSupport;
import com.example.springdocswagger.user.application.port.in.UserResponse;
import com.example.springdocswagger.user.application.port.in.UserSearchUseCase;
import com.example.springdocswagger.user.domain.User;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.restdocs.payload.FieldDescriptor;

import java.time.LocalDateTime;
import java.util.List;

import static org.hamcrest.Matchers.containsString;
import static org.mockito.Mockito.when;
import static org.springframework.restdocs.payload.PayloadDocumentation.fieldWithPath;
import static org.springframework.restdocs.payload.PayloadDocumentation.responseFields;
import static org.springframework.restdocs.request.RequestDocumentation.parameterWithName;
import static org.springframework.restdocs.request.RequestDocumentation.requestParameters;
import static org.springframework.restdocs.snippet.Attributes.attributes;
import static org.springframework.restdocs.snippet.Attributes.key;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(UserSearchController.class)
class UserSearchControllerTest extends RestDocsTestSupport {

    @MockBean
    private UserSearchUseCase userSearchUseCase;

    @Test
    void searchAllUsers() throws Exception {
        when(userSearchUseCase.searchAll("account")).thenReturn(List.of(UserResponse.of(new User(1L, "SUGA", "suga@bts.com", "010-333-3333", LocalDateTime.now(), null))));

        mockMvc.perform(get("/v1/users")
                        .queryParam("ordering", "account")
                        .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(content().string(containsString("SUGA")))
                .andDo(restDocs.document(
                        requestParameters(
                                attributes(key("title").value("Fields for user searching")),
                                parameterWithName("ordering")
                                        .optional()
                                        .description("Ordering 할 Property 명칭"))
                        , responseFields(
                                fieldWithPath("[]")
                                        .description("Array of Users"))
                                .andWithPrefix("[].", usersResponseFiled())
                ));
    }

    private FieldDescriptor[] usersResponseFiled() {
        return new FieldDescriptor[]{
                fieldWithPath("id").description("ID"),
                fieldWithPath("account").description("Account"),
                fieldWithPath("email").description("email"),
                fieldWithPath("phoneNumber").description("phoneNumber"),
                fieldWithPath("createdAt").description("생성일자")
        };
    }
}