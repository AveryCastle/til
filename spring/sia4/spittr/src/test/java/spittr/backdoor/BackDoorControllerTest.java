package spittr.backdoor;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.iterableWithSize;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import spittr.SpittrApplication;
import spittr.domain.Spittle;
import spittr.repository.SpittleRepository;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.SpringApplicationConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import java.util.List;

/**
 * BackDoorControllerTest.
 */
@RunWith(SpringJUnit4ClassRunner.class)
@SpringApplicationConfiguration(SpittrApplication.class)
public class BackDoorControllerTest {

    @Autowired
    private BackDoorController controller;

    @Autowired
    private SpittleRepository spittleReposiitory;

    private MockMvc mockMvc;

    @Before
    public void setUp() {
        mockMvc = MockMvcBuilders.standaloneSetup(controller).build();
    }

    @Test
    public void createSpittles() throws Exception {
        mockMvc.perform(get("/_backdoor/create-spittles"))
                .andExpect(status().isOk())
                .andExpect(content().string("create success"));

        List<Spittle> spittles = spittleReposiitory.findAll();
        assertThat(spittles, iterableWithSize(100));
    }
}
