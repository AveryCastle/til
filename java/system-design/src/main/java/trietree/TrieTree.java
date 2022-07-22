package trietree;

public class TrieTree {

    public void insert(String string, Node root) {
        if (string.isEmpty()) {
            root.last = true;
            return;
        }

        if (string.length() == 1 && root.isLast()) {
            root.last = false;
        }

        char key = string.charAt(0);
        Node nextNode = root.getEdge(key);
        if (nextNode == null) {
            nextNode = new Node(key);
            root.put(key, nextNode);
        }

        insert(string.substring(1), nextNode);
    }

    public static class Node {
        private static final int ALPHABET_SIZE = 26;
        private final char key;
        private boolean last;
        private final Node[] edges;

        public Node(char key) {
            this.key = key;
            this.last = false;
            this.edges = new Node[ALPHABET_SIZE];
        }

        public Node getEdge(char ch) {
            return edges[ch - 'a'];
        }

        public char getKey() {
            return key;
        }

        public boolean isLast() {
            return last;
        }

        public Node[] getEdges() {
            return edges;
        }

        public void put(char ch, Node node) {
            edges[ch - 'a'] = node;
        }
    }
}
