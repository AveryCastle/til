package com.example.graphqlpractice.graphqlserver;

import java.util.List;

import org.springframework.graphql.data.method.annotation.Argument;
import org.springframework.graphql.data.method.annotation.QueryMapping;
import org.springframework.graphql.data.method.annotation.SchemaMapping;
import org.springframework.stereotype.Controller;

@Controller
public class BookController {

	@QueryMapping
	public Book bookByID(@Argument String id) {
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
