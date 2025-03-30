import pytest
from main import BooksCollector
from random import randint as r

@pytest.fixture
def collector():
    collector = BooksCollector()
    return collector

@pytest.fixture
def collector_with_all_genres_books():
    collector = BooksCollector()
    for genre in collector.genre:
        book_name = 'Книга ' + genre
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
    return collector