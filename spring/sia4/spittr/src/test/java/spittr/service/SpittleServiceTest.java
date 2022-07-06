package spittr.service;

import static java.time.temporal.ChronoUnit.MILLIS;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.equalTo;
import static org.hamcrest.Matchers.hasItems;
import static org.hamcrest.Matchers.iterableWithSize;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;

import spittr.SpittrApplication;
import spittr.domain.Spittle;
import spittr.repository.SpittleRepository;

import org.junit.Test;
import org.junit.runner.RunWith;

import org.springframework.boot.test.SpringApplicationConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * SpittleServiceTest.
 */
@RunWith(SpringJUnit4ClassRunner.class)
@SpringApplicationConfiguration(SpittrApplication.class)
public class SpittleServiceTest {

    private static final int COUNT_OF_SPITTLES = 20;

    @Test
    public void shouldShowRecentSpittles() throws Exception {
        // Given:

        List<Spittle> expectedSpittles = createSpittles(COUNT_OF_SPITTLES);

        SpittleRepository mockRepository = mock(SpittleRepository.class);
        when(mockRepository.findTop20ByOrderByDateTimeDesc())
                .thenReturn(expectedSpittles);

        SpittleService service = new SpittleService(mockRepository);

        // When:

        List<Spittle> spittles = service.findTop20();

        // Then:

        assertThat(spittles, iterableWithSize(COUNT_OF_SPITTLES));

        for (int i = 0; i < COUNT_OF_SPITTLES; i++) {
            assertThat(spittles.get(i).getMessage(),
                    equalTo(expectedSpittles.get(i).getMessage()));
        }
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
