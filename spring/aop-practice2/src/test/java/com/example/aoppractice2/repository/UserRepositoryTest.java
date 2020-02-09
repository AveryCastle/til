package com.example.aoppractice2.repository;

import com.example.aoppractice2.domain.User;
import org.junit.Test;
import org.junit.runner.RunWith;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.orm.jpa.TestEntityManager;
import org.springframework.test.context.junit4.SpringRunner;

import static org.assertj.core.api.Assertions.assertThat;

@RunWith(SpringRunner.class)
@DataJpaTest
public class UserRepositoryTest {
    @Autowired
    private TestEntityManager entityManager;

    @Autowired
    private UserRepository repository;

    @Test
    public void login() {
        this.entityManager.persist(User.create("test", "test1234", "테스터"));
        User user = this.repository.findByLoginId("test");

        assertThat(user.getName()).isEqualTo("테스터");
        assertThat(user.getPassword()).isEqualTo("test1234");
    }
}
