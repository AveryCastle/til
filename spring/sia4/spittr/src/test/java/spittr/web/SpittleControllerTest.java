package spittr.web;

import static java.time.temporal.ChronoUnit.MILLIS;
import static org.hamcrest.Matchers.hasItems;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.model;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.view;
import static org.springframework.test.web.servlet.setup.MockMvcBuilders.standaloneSetup;

import spittr.SpittrApplication;
import spittr.domain.Spittle;
import spittr.repository.SpittleRepository;
import spittr.service.SpittleService;

import org.junit.Test;
import org.junit.runner.RunWith;

import org.springframework.boot.test.SpringApplicationConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * SpittleController Test.
 */
@RunWith(SpringJUnit4ClassRunner.class)
@SpringApplicationConfiguration(SpittrApplication.class)
public class SpittleControllerTest {

    private static final int COUNT_OF_SPITTLES = 20;

    @Test
    public void shouldShowRecentSpittles() throws Exception {
        // Given:

        List<Spittle> expectedSpittles = createSpittles(COUNT_OF_SPITTLES);

        SpittleService mockService = mock(SpittleService.class);
        when(mockService.findTop20()).thenReturn(expectedSpittles);

        SpittleController spittleController =
                new SpittleController(mockService);

        MockMvc mockMvc =
                MockMvcBuilders.standaloneSetup(spittleController).build();

        // When and Then

        mockMvc.perform(get("/spittles"))
                .andExpect(view().name("spittr/home"))
                .andExpect(model().attributeExists("spittles"))
                .andExpect(model().attribute("spittles",
                        hasItems(expectedSpittles.toArray())));
    }

    private List<Spittle> createSpittles(int count) {
        List<Spittle> spittles = new ArrayList<Spittle>();

        for (int i = 0; i < count; i++) {
            spittles.add(new Spittle("Spittle_" + i,
                    LocalDateTime.now().plus(i, MILLIS)));
        }

        Collections.reverse(spittles);

        return spittles;
    }
}
