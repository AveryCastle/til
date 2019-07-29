package strategy;

public class SortAndPrint {

    private Comparable[] data;
    private Sorter sorter;

    public SortAndPrint(Comparable[] data, Sorter sorter) {
        this.data = data;
        this.sorter = sorter;
    }

    public void execute() {
        print();
        sorter.sort(this.data);
        print();
    }

    public void print() {
        for (int i = 0; i < this.data.length; i++) {
            System.out.print(data[i] + ", ");
        }
        System.out.println("");
    }
}
