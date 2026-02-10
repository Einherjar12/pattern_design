# Задание 3. Создайте приложение для работы в библиотеке. Оно должно оперировать следующими
# сущностями: Книга, Библиотекарь, Читатель. Приложение должно позволять вводить, удалять,
# изменять, сохранять вфайл, загружать из файла, логгировать действия, искать информацию
# (результаты поиска выводятся на экран или файл) о сущностях. При реализации используйте
# максимально возможное количество паттернов проектирования.

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
import json
import logging
from enum import Enum

# ==================== Настройка логирования ====================
logging.basicConfig(
    filename='library.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

def log(message: str):
    logging.info(message)
    print(f"[LOG] {message}")

# ==================== ПАТТЕРН: COMMAND ====================
class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

# ==================== ПАТТЕРН: OBSERVER ====================
class Observer(ABC):
    @abstractmethod
    def update(self, message: str) -> None:
        pass

class ConsoleLogger(Observer):
    def update(self, message: str) -> None:
        print(f"[OBS] {message}")

# ==================== СУЩНОСТИ ====================
class BookStatus(Enum):
    AVAILABLE = "available"
    BORROWED = "borrowed"

@dataclass
class Book:
    id: int
    title: str
    author: str
    year: int
    isbn: str
    status: BookStatus = BookStatus.AVAILABLE
    borrower_id: Optional[int] = None

@dataclass
class Librarian:
    id: int
    name: str
    email: str
    phone: str
    position: str

@dataclass
class Reader:
    id: int
    name: str
    email: str
    phone: str
    books_borrowed: List[int]

# ==================== ПАТТЕРН: REPOSITORY ====================
class Repository(ABC):
    @abstractmethod
    def add(self, entity): ...
    @abstractmethod
    def get(self, entity_id): ...
    @abstractmethod
    def get_all(self): ...
    @abstractmethod
    def update(self, entity): ...
    @abstractmethod
    def delete(self, entity_id): ...
    @abstractmethod
    def search(self, **kwargs): ...

class BookRepository(Repository):
    def __init__(self):
        self.books: Dict[int, Book] = {}
        self.next_id = 1
    def add(self, book: Book):
        book.id = self.next_id
        self.books[self.next_id] = book
        self.next_id += 1
    def get(self, entity_id): return self.books.get(entity_id)
    def get_all(self): return list(self.books.values())
    def update(self, book: Book):
        if book.id in self.books: self.books[book.id] = book
    def delete(self, entity_id):
        if entity_id in self.books: del self.books[entity_id]
    def search(self, **kwargs):
        results = self.get_all()
        for key, value in kwargs.items():
            if value is not None:
                results = [b for b in results if getattr(b, key, None) == value]
        return results

class LibrarianRepository(Repository):
    def __init__(self):
        self.librarians: Dict[int, Librarian] = {}
        self.next_id = 1
    def add(self, librarian: Librarian):
        librarian.id = self.next_id
        self.librarians[self.next_id] = librarian
        self.next_id += 1
    def get(self, entity_id): return self.librarians.get(entity_id)
    def get_all(self): return list(self.librarians.values())
    def update(self, librarian: Librarian):
        if librarian.id in self.librarians: self.librarians[librarian.id] = librarian
    def delete(self, entity_id):
        if entity_id in self.librarians: del self.librarians[entity_id]
    def search(self, **kwargs):
        results = self.get_all()
        for key, value in kwargs.items():
            if value is not None:
                results = [l for l in results if getattr(l, key, None) == value]
        return results

class ReaderRepository(Repository):
    def __init__(self):
        self.readers: Dict[int, Reader] = {}
        self.next_id = 1
    def add(self, reader: Reader):
        reader.id = self.next_id
        self.readers[self.next_id] = reader
        self.next_id += 1
    def get(self, entity_id): return self.readers.get(entity_id)
    def get_all(self): return list(self.readers.values())
    def update(self, reader: Reader):
        if reader.id in self.readers: self.readers[reader.id] = reader
    def delete(self, entity_id):
        if entity_id in self.readers: del self.readers[entity_id]
    def search(self, **kwargs):
        results = self.get_all()
        for key, value in kwargs.items():
            if value is not None:
                results = [r for r in results if getattr(r, key, None) == value]
        return results

# ==================== ФАСАД ====================
class LibraryFacade:
    def __init__(self):
        self.books = BookRepository()
        self.librarians = LibrarianRepository()
        self.readers = ReaderRepository()
        self.observers: List[Observer] = []

    def add_observer(self, observer: Observer):
        self.observers.append(observer)

    def notify(self, message: str):
        log(message)
        for obs in self.observers:
            obs.update(message)

    # ----------------- BOOK -----------------
    def add_book(self, title, author, year, isbn) -> Book:
        book = Book(0, title, author, year, isbn)
        self.books.add(book)
        self.notify(f"Book added: {book.title}")
        return book

    def update_book(self, book: Book):
        self.books.update(book)
        self.notify(f"Book updated: {book.title}")

    def delete_book(self, book_id: int):
        book = self.books.get(book_id)
        if book:
            self.books.delete(book_id)
            self.notify(f"Book deleted: {book.title}")

    def borrow_book(self, reader_id, book_id):
        book = self.books.get(book_id)
        reader = self.readers.get(reader_id)
        if book and reader and book.status == BookStatus.AVAILABLE:
            book.status = BookStatus.BORROWED
            book.borrower_id = reader_id
            reader.books_borrowed.append(book_id)
            self.books.update(book)
            self.readers.update(reader)
            self.notify(f"Book '{book.title}' borrowed by {reader.name}")
            return True
        return False

    def return_book(self, book_id):
        book = self.books.get(book_id)
        if book and book.status == BookStatus.BORROWED:
            reader = self.readers.get(book.borrower_id)
            if reader and book_id in reader.books_borrowed:
                reader.books_borrowed.remove(book_id)
                self.readers.update(reader)
            book.status = BookStatus.AVAILABLE
            book.borrower_id = None
            self.books.update(book)
            self.notify(f"Book '{book.title}' returned")
            return True
        return False

    # ----------------- LIBRARIAN -----------------
    def add_librarian(self, name, email, phone, position):
        librarian = Librarian(0, name, email, phone, position)
        self.librarians.add(librarian)
        self.notify(f"Librarian added: {name}")
        return librarian

    def update_librarian(self, librarian: Librarian):
        self.librarians.update(librarian)
        self.notify(f"Librarian updated: {librarian.name}")

    def delete_librarian(self, librarian_id: int):
        librarian = self.librarians.get(librarian_id)
        if librarian:
            self.librarians.delete(librarian_id)
            self.notify(f"Librarian deleted: {librarian.name}")

    # ----------------- READER -----------------
    def add_reader(self, name, email, phone):
        reader = Reader(0, name, email, phone, [])
        self.readers.add(reader)
        self.notify(f"Reader added: {name}")
        return reader

    def update_reader(self, reader: Reader):
        self.readers.update(reader)
        self.notify(f"Reader updated: {reader.name}")

    def delete_reader(self, reader_id: int):
        reader = self.readers.get(reader_id)
        if reader:
            self.readers.delete(reader_id)
            self.notify(f"Reader deleted: {reader.name}")

    # ----------------- STATE -----------------
    def save_state(self, filename='library_state.json'):
        state = {
            'books': [
                {**b.__dict__, 'status': b.status.value} for b in self.books.get_all()
            ],
            'librarians': [l.__dict__ for l in self.librarians.get_all()],
            'readers': [r.__dict__ for r in self.readers.get_all()]
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        self.notify("Library state saved")

    def load_state(self, filename='library_state.json'):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                state = json.load(f)
                # Load books
                self.books = BookRepository()
                for item in state['books']:
                    item['status'] = BookStatus(item['status'])
                    book = Book(**item)
                    self.books.add(book)
                    self.books.next_id = max(self.books.next_id, book.id + 1)
                # Load librarians
                self.librarians = LibrarianRepository()
                for item in state['librarians']:
                    librarian = Librarian(**item)
                    self.librarians.add(librarian)
                    self.librarians.next_id = max(self.librarians.next_id, librarian.id + 1)
                # Load readers
                self.readers = ReaderRepository()
                for item in state['readers']:
                    reader = Reader(**item)
                    self.readers.add(reader)
                    self.readers.next_id = max(self.readers.next_id, reader.id + 1)
            self.notify("Library state loaded")
        except FileNotFoundError:
            self.notify("No saved state found")

# ==================== КОМАНДЫ ====================
class AddBookCommand(Command):
    def __init__(self, facade: LibraryFacade, title, author, year, isbn):
        self.facade = facade
        self.title = title
        self.author = author
        self.year = year
        self.isbn = isbn
    def execute(self): self.facade.add_book(self.title, self.author, self.year, self.isbn)

class BorrowBookCommand(Command):
    def __init__(self, facade: LibraryFacade, reader_id, book_id):
        self.facade = facade
        self.reader_id = reader_id
        self.book_id = book_id
    def execute(self): self.facade.borrow_book(self.reader_id, self.book_id)

class ReturnBookCommand(Command):
    def __init__(self, facade: LibraryFacade, book_id):
        self.facade = facade
        self.book_id = book_id
    def execute(self): self.facade.return_book(self.book_id)

# ==================== ДЕМО ====================
if __name__ == "__main__":
    facade = LibraryFacade()
    facade.add_observer(ConsoleLogger())

    print("=== Демонстрация библиотеки ===")

    # Добавление книг через Command
    add_cmd1 = AddBookCommand(facade, "Новая жизнь", "Иван Иванов", 2021, "111-AAA")
    add_cmd2 = AddBookCommand(facade, "Программирование на Python", "Мария Петрова", 2022, "222-BBB")
    add_cmd1.execute()
    add_cmd2.execute()

    # Добавление читателя
    reader = facade.add_reader("Сергей Кузнецов", "sergey@mail.com", "+7-999-123-45-67")

    # Выдача книги через Command
    borrow_cmd = BorrowBookCommand(facade, reader.id, 1)
    borrow_cmd.execute()

    # Возврат книги через Command
    return_cmd = ReturnBookCommand(facade, 1)
    return_cmd.execute()

    # Состояние библиотеки
    facade.save_state()


