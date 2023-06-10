package com.example.graphqlpractice.graphqlserver;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.graphql.GraphQlTest;
import org.springframework.graphql.test.tester.GraphQlTester;

@GraphQlTest(BookController.class)
class BookControllerTest {

    @Autowired
    private GraphQlTester graphQlTester;

    @Test
    void shouldGetFirstBook() {
        this.graphQlTester
            .documentName("bookDetails")
            .variable("id", "book-1")
            .execute()
            .path("bookByID")
            .matchesJson("""
                    {
                        "id": "book-1",
                        "name": "Effective Java",
                        "pageCount": 416,
                        "author": {
                          "firstName": "Joshua",
                          "lastName": "Bloch"
                        }
                    }
                """);
    }

    @Test
    void shouldGetFirstAuthor() {
        this.graphQlTester
            .documentName("authorDetails")
            .variable("id", "author-2")
            .execute()
            .path("authorByID")
            .matchesJson("""
                    {
                        "id": "author-2",
                        "firstName": "Douglas",
                        "lastName": "Adams",
                        "book": [
                            {
                              "id" : "book-2",
                              "name": "Hitchhiker's Guide to the Galaxy"
                            },
                            {
                              "id": "book-4",
                              "name": "Jimin"
                            },
                            {
                              "id": "book-5",
                              "name": "VVV"
                            }
                        ]
                    }
                """);
    }
}
