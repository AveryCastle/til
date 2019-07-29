package strategy;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

class SortAndPrintTest {

    @Test
    public void test() {
        String[] data = {"Dumpty", "Bown", "Carrol", "Elfland", "Alice"};
        SortAndPrint sortAndPrint = new SortAndPrint(data, new SelectionSorter());
        sortAndPrint.execute();
    }
}
