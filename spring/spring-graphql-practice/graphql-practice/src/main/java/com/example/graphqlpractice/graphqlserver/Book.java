package com.example.graphqlpractice.graphqlserver;

import static java.util.stream.Collectors.*;

import java.util.Arrays;
import java.util.List;

public record Book(String id, String name, int pageCount, String authorId) {

	private static List<Book> books = Arrays.asList(
		new Book("book-1", "Effective Java", 416, "author-1"),
		new Book("book-2", "Hitchhiker's Guide to the Galaxy", 208, "author-2"),
		new Book("book-3", "Down Under", 436, "author-3"),
		new Book("book-4", "Jimin", 406, "author-2"),
		new Book("book-5", "VVV", 736, "author-2"),
		new Book("book-6", "SUGA", 306, "author-3")
	);

	public static Book getById(String id) {
		return books.stream()
					.filter(book -> book.id().equals(id))
					.findFirst()
					.orElse(null);
	}

	public static List<Book> getByAuthorId(String authorId) {
		return books.stream()
					.filter(book -> book.authorId.equals(authorId))
					.collect(toList());
	}
}
