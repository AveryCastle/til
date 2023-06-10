package com.example.graphqlpractice.graphqlserver;

import java.util.List;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.graphql.data.method.annotation.Argument;
import org.springframework.graphql.data.method.annotation.ContextValue;
import org.springframework.graphql.data.method.annotation.QueryMapping;
import org.springframework.graphql.data.method.annotation.SchemaMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class BookController {

    private final Logger logger = LoggerFactory.getLogger(BookController.class);

    @QueryMapping
    public Book bookByID(@Argument String id, @ContextValue String myAuthorization) {
        logger.info("myAuthorization = {}", myAuthorization);
        return Book.getById(id);
    }

    @QueryMapping
    public Author authorByID(@Argument String id) {
        return Author.getById(id);
    }

    @SchemaMapping
    public Author author(Book book) {
        return Author.getById(book.authorId());
    }

    @SchemaMapping
    public List<Book> book(Author author) {
        return Book.getByAuthorId(author.id());
    }
}
