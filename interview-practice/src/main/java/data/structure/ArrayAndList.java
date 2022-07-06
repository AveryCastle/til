package data.structure;

import java.util.ArrayList;

public class ArrayAndList {

    public static void main(String[] args) {
        final int[] integers = new int[3];
        final boolean[] bools = {false, true, true, false};
        final String[] strings = new String[]{"one", "two", "three"};


        String[] new_strings = new String[strings.length * 2];
        System.arraycopy(strings, 0, new_strings, 0, strings.length);
        System.arraycopy(strings, 0, new_strings, strings.length, strings.length);

        for (String el : new_strings) {
            System.out.print(el + " ");
        }
        System.out.println("\n");

        ArrayList arrayList = new ArrayList();
    }
}
