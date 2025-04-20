import pytest

from main import BooksCollector

class TestBooksCollector:
    # Проверяем, что стартовое заполнение объекта соответствует ожиданиям
    # Так как вводных параметров для конструктора у нас нет, в названии вместо входного параметра указываем ОР
    def test_init_books_genre_is_empty_true(self, collector):
        assert len(collector.books_genre) == 0

    def test_init_favorites_is_empty_true(self, collector):
        assert len(collector.favorites) == 0

    def test_init_genre_list_is_expected_true(self, collector):
        expected_genres = ['Фантастика', 'Ужасы', 'Детективы', 'Мультфильмы', 'Комедии']
        assert collector.genre == expected_genres

    def test_init_genre_age_rating_is_expected_true(self, collector):
        expected_age_rating_genres = ['Ужасы', 'Детективы']
        assert collector.genre_age_rating == expected_age_rating_genres

    # Проверяем функции класса BooksCollector
    # при валидной длине названия книга добавляется в словарь
    @pytest.mark.parametrize('name',
                             [
                                '1',
                                'some_valid_len',
                                'max_valid_len_is_40_symbols_000000000000'
                             ])
    def test_add_new_book_valid_len_successfully_added(self, collector, name):
        collector.add_new_book(name)
        assert len(collector.books_genre) == 1 and collector.books_genre[name] == ''

    # при не валидной длине названия книга не добавляется
    @pytest.mark.parametrize('name',
                             [
                                 '',
                                 'min_not_valid_len_is_41_symbols_000000000'
                             ])
    def test_add_new_book_not_valid_len_not_added(self, collector, name):
        collector.add_new_book(name)
        assert len(collector.books_genre) == 0

    # Жанр из списка жанров успешно назначается
    @pytest.mark.parametrize('genre',
                             ['Фантастика',
                              'Ужасы',
                              'Детективы',
                              'Мультфильмы',
                              'Комедии'
                              ])
    def test_set_book_genre_genre_from_genres_list_successfully_added(self, genre, collector):
        book = 'Книга'
        collector.books_genre[book] = '' # добавляем вручную книгу в словарь, чтобы тест был независим
        collector.set_book_genre(book, genre)     # от других методов, в частности, от .add_new_book
        assert collector.books_genre[book] == genre

    # Жанр не из списка жанров не назначается
    def test_set_book_genre_genre_not_in_genres_list_not_added(self, collector):
        book = 'Книга'
        collector.books_genre[book] = ''
        collector.set_book_genre(book, 'Романтика')
        assert collector.books_genre[book] == ''

    # получаем жанр книги по ее имени
    @pytest.mark.parametrize('book, genre',
                             [['Книга Фантастика', 'Фантастика'],
                              ['Книга Ужасы', 'Ужасы'],
                              ['Книга Детективы', 'Детективы'],
                              ['Книга Мультфильмы', 'Мультфильмы'],
                              ['Книга Комедии', 'Комедии']])
    def test_get_book_genre_five_books_all_genres_return_genre(self, collector_with_all_genres_books, book, genre):
        assert collector_with_all_genres_books.get_book_genre(book) == genre

    # Возвращаются книги с выбранным жанром
    @pytest.mark.parametrize('genre',
                             ['Фантастика',
                              'Ужасы',
                              'Детективы',
                              'Мультфильмы',
                              'Комедии'
                              ])
    def test_get_books_with_specific_genre_all_genres_return_one_book(self, collector_with_all_genres_books, genre):
        books_list = collector_with_all_genres_books.get_books_with_specific_genre(genre)
        assert collector_with_all_genres_books.books_genre[books_list[0]] == genre and len(books_list) == 1

    # Возвращается словарь books_genre о всеми добавленными книгами
    def test_get_books_genre_five_books_all_genres_return_all_books(self, collector_with_all_genres_books):
        books_dict = collector_with_all_genres_books.get_books_genre()
        assert len(books_dict) == 5

    # Возвращаются книги, подходящие детям
    def test_get_books_for_children_five_books_all_genres_return_three_books(self, collector_with_all_genres_books):
        books_dict = collector_with_all_genres_books.get_books_for_children()
        assert len(books_dict) == 3 and 'Книга Ужасы' not in books_dict and'Книга Детективы' not in books_dict

    # Книга, которой нет в избранном, но есть в добавленных книгах, добавляется в избранное
    def test_add_book_in_favorites_new_book_from_books_genre_list_successfully_added(self, collector_with_all_genres_books):
        collector_with_all_genres_books.add_book_in_favorites('Книга Ужасы')
    # не используем метод get_list_of_favorites_books, чтобы сохранить независимость теста
        assert (len(collector_with_all_genres_books.favorites) == 1
                and collector_with_all_genres_books.favorites[0] == 'Книга Ужасы')

    # Книга удаляется из избранного
    def test_delete_book_from_favorites_one_book_added_empty_list(self, collector_with_all_genres_books):
        collector_with_all_genres_books.add_book_in_favorites('Книга Детективы')
        collector_with_all_genres_books.delete_book_from_favorites('Книга Детективы')
        assert len(collector_with_all_genres_books.favorites) == 0

    # Возвращается список избранных книг
    def test_get_list_of_favorites_books_three_books_added_three_books_in_list(self, collector_with_all_genres_books):
        favorites_list = ['Книга Мультфильмы', 'Книга Фантастика', 'Книга Комедии']
        for i in favorites_list:
            collector_with_all_genres_books.add_book_in_favorites(i)
        assert len(collector_with_all_genres_books.get_list_of_favorites_books()) == 3