package trietree;

import org.junit.jupiter.api.Test;

class TrieTreeTest {

    @Test
    void test() {
        TrieTree trieTree = new TrieTree();
        TrieTree.Node root = new TrieTree.Node('\u0000');
        trieTree.insert("aac", root);
        trieTree.insert("aab", root);
    }
}
