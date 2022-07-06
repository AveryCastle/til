package spittr.repository;

import static java.time.temporal.ChronoUnit.MILLIS;
import static org.hamcrest.Matchers.equalTo;
import static org.hamcrest.Matchers.iterableWithSize;
import static org.junit.Assert.assertThat;

import spittr.SpittrApplication;
import spittr.domain.Spittle;

import org.junit.Test;
import org.junit.runner.RunWith;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.SpringApplicationConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import org.springframework.test.context.transaction.BeforeTransaction;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * SpittleRepositoryTest.
 */
@RunWith(SpringJUnit4ClassRunner.class)
@SpringApplicationConfiguration(SpittrApplication.class)
@Transactional
public class SpittleRepositoryTest {

    private static final int MAX_COUNT = 20;

    private List<Spittle> spittles;

    @Autowired
    private SpittleRepository repository;

    @BeforeTransaction
    public void givenAndWhen() {
        spittles = createSpittles(MAX_COUNT);
        repository.save(spittles);
    }

    @Test
    public void testFindRecentTwentySpittles() {
        List<Spittle> foundSpittles =
                repository.findTop20ByOrderByDateTimeDesc();

        assertThat(foundSpittles, iterableWithSize(MAX_COUNT));

        for (int i = 0; i < MAX_COUNT; i++) {
            assertThat(foundSpittles.get(i).getMessage(),
                    equalTo(spittles.get(i).getMessage()));
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
