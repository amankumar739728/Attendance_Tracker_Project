class Book:
    def __init__(self, title, author, language, year):
        self.title = title
        self.author = author
        self.language = language
        self.year = year

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "language": self.language,
            "year": self.year
        }


class EBook(Book):
    def __init__(self, title, author, language, year, file_format):
        super().__init__(title, author, language, year)
        self.file_format = file_format

    def to_dict(self):
        data = super().to_dict()
        data["format"] = self.file_format
        return data


class Library:
    def __init__(self):
        self.books = []  # List of dictionaries
        self.book_count = 0

    def add_book(self, book):
        self.books.append(book.to_dict())  # Convert object to dict
        self.book_count += 1
        print(f"Book '{book.title}' added successfully.")

    def display_books(self):
        if not self.books:
            print("No books in the library.")
        else:
            print("Available books:")
            print(self.books)
            print(f"\nTotal books in the library: {self.book_count}")

    def remove_book(self, title):
        for book in self.books:
            if book["title"].lower() == title.lower():
                self.books.remove(book)
                self.book_count -= 1
                print(f"Book '{title}' removed successfully.")
                return
        print(f"Book '{title}' not found.")
    
    
    def update_book(self, title, **kwargs):
        for book in self.books:
            if book["title"].lower() == title.lower():
                book.update(kwargs)
                print(f"Book '{title}' updated successfully.")
                print("\nUpdated book data:", book)
                return
        print(f"Book '{title}' not found.")



if __name__ == "__main__":
    
    library = Library()

    # Add books
    b1 = Book("The Alchemist", "Paulo Coelho", "English", "1988")
    b2 = EBook("Digital Fortress", "Dan Brown", "English", "1998", "PDF")
    print("*******Library Management System*******",end="\n\n") # end = "\n" is used to add new line
    library.add_book(b1)
    library.add_book(b2)

    # Display books
    print("\n")
    library.display_books()

    # Update book
    print("\n")
    library.update_book("The Alchemist", year="1993")

    # Remove book
    print("\n")
    library.remove_book("Digital Fortress")

    # Final display
    print("\n")
    library.display_books()
    
    
    
#Sample-Output:

# *******Library Management System*******

# Book 'The Alchemist' added successfully.
# Book 'Digital Fortress' added successfully.


# Available books:
# [{'title': 'The Alchemist', 'author': 'Paulo Coelho', 'language': 'English', 'year': '1988'}, {'title': 'Digital Fortress', 'author': 'Dan Brown', 'language': 'English', 'year': '1998', 'format': 'PDF'}]

# Total books in the library: 2


# Book 'The Alchemist' updated successfully.

# Updated book data: {'title': 'The Alchemist', 'author': 'Paulo Coelho', 'language': 'English', 'year': '1993'}


# Book 'Digital Fortress' removed successfully.


# Available books:
# [{'title': 'The Alchemist', 'author': 'Paulo Coelho', 'language': 'English', 'year': '1993'}]

# Total books in the library: 1