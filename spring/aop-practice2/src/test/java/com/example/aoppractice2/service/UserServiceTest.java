package com.example.aoppractice2.service;

import com.example.aoppractice2.domain.History;
import com.example.aoppractice2.domain.User;
import com.example.aoppractice2.repository.HistoryRepository;
import com.example.aoppractice2.repository.UserRepository;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.junit4.SpringRunner;

import static junit.framework.TestCase.assertFalse;
import static junit.framework.TestCase.assertTrue;
import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.BDDMockito.given;

@RunWith(SpringRunner.class)
@SpringBootTest
public class UserServiceTest {

    public static final String LOGIN_ID = "test";
    @Autowired
    private UserService userService;

    @MockBean
    private UserRepository userRepository;

    @Autowired
    private HistoryRepository historyRepository;

    private static User USER;

    @Before
    public void setUp() {
        USER = User.create(LOGIN_ID, "test1234", "테스터");

        given(userRepository.findByLoginId(LOGIN_ID)).willReturn(USER);
    }

    @Test
    public void shouldSuccess() throws Exception {
        User foundOne = userService.login(LOGIN_ID, "test1234");

        assertThat(foundOne.getId()).isEqualTo(USER.getId());
        assertThat(foundOne.getName()).isEqualTo("테스터");

        History history = historyRepository.findByLoginId(LOGIN_ID);
        assertTrue(history.isSuccess());
        assertThat(history.getReason()).isEqualTo("SUCCESS");
    }

    @Test
    public void shouldFail() {
        final String NOT_FOUND = "NOT-FOUND";
        try {
            userService.login(NOT_FOUND, "WRONG-PASSWORD");
        } catch (Exception e) {
            History history = historyRepository.findByLoginId(NOT_FOUND);
            assertFalse(history.isSuccess());
            assertThat(history.getReason()).isEqualTo("FAIL");
        }
    }
}
