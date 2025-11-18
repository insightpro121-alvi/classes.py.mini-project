import os

# in this  program we use inheritance ,encapsulation and polimorphism 


# ============================
#       INHERITANCE BASE CLASS
# ============================
class Person:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    # POLYMORPHISM METHOD
    def show_details(self):
        print("Person:", self.name)


# ============================
#            USER CLASS
# ============================
class User(Person):   # INHERITANCE
    def __init__(self, user_id, name, email):
        super().__init__(name, email)     # inherit parent attributes
        self.user_id = user_id
        self.borrowed_books = []

    # POLYMORPHISM (same method, different output)
    def show_details(self):
        print(f"[User] {self.user_id} | {self.name} | {self.email}")

    def borrow_book(self, book_id):
        self.borrowed_books.append(book_id)

    def return_book(self, book_id):
        if book_id in self.borrowed_books:
            self.borrowed_books.remove(book_id)

    def to_line(self):
        borrowed = ";".join(self.borrowed_books) if self.borrowed_books else "None"
        return f"{self.user_id},{self.name},{self.email},{borrowed}"

    @staticmethod
    def from_line(line):
        parts = line.split(",")
        if len(parts) < 4:
            return None
        borrowed_list = parts[3].split(";") if parts[3] != "None" else []
        u = User(parts[0], parts[1], parts[2])
        u.borrowed_books = borrowed_list
        return u


# ============================
#             BOOK CLASS
# ============================
class Book:
    def __init__(self, book_id, title, author, year, total_copies):
        self.book_id = book_id

        # ENCAPSULATION (private attributes)
        self.__title = title
        self.__author = author
        self.__year = year
        self.__total_copies = total_copies
        self.__available_copies = total_copies
        self.borrowed_by = "None"

    # Encapsulation (getter)
    def get_title(self):
        return self.__title

    # Borrow book
    def borrow(self, user_id):
        if self.__available_copies > 0:
            self.__available_copies -= 1
            self.borrowed_by = user_id
            return True
        return False

    # Return book
    def return_book(self):
        self.__available_copies += 1
        if self.__available_copies == self.__total_copies:
            self.borrowed_by = "None"

    def to_line(self):
        return f"{self.book_id},{self.__title},{self.__author},{self.__year},{self.__total_copies},{self.__available_copies},{self.borrowed_by}"

    @staticmethod
    def from_line(line):
        parts = line.split(",")
        if len(parts) < 7:
            return None
        b = Book(parts[0], parts[1], parts[2], parts[3], int(parts[4]))
        b.__available_copies = int(parts[5])
        b.borrowed_by = parts[6]
        return b


#  now library class
#         LIBRARY CLASS

class Library:
    def __init__(self, filename):
        self.filename = filename
        self.books = {}
        self.users = {}
        self.load_data()

    # ----------------  data save function  ----------------
    def save_data(self):
        try:
            with open(self.filename, "w") as f:
                f.write("#BOOKS\n")
                for b in self.books.values():
                    f.write(b.to_line() + "\n")

                f.write("#USERS\n")
                for u in self.users.values():
                    f.write(u.to_line() + "\n")

            print("Data saved successfully!")

        except Exception as e:
            print("Error saving:", e)

    # ----------------  now data load finction ----------------
    def load_data(self):
        if not os.path.exists(self.filename):
            print("No file found — starting fresh.")
            return

        try:
            section = None
            with open(self.filename, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    if line == "#BOOKS":
                        section = "books"
                        continue
                    elif line == "#USERS":
                        section = "users"
                        continue

                    if section == "books":
                        b = Book.from_line(line)
                        if b:
                            self.books[b.book_id] = b

                    elif section == "users":
                        u = User.from_line(line)
                        if u:
                            self.users[u.user_id] = u

            print("Data loaded successfully!")

        except Exception as e:
            print("Error loading:", e)

    # ---------------- DASHBOARD ka function  ----------------
    def show_dashboard(self):
        total_books = len(self.books)
        total_users = len(self.users)
        available = sum(b._Book__available_copies for b in self.books.values())
        borrowed = sum((b._Book__total_copies - b._Book__available_copies for b in self.books.values()))

        print("\n==== LIBRARY DASHBOARD ====")
        print("Total Books:", total_books)
        print("Available Copies:", available)
        print("Borrowed Copies:", borrowed)
        print("Total Users:", total_users)
        print("============================\n")

#------------------- USER LOGIN section  ----------------
    def user_login(self):
        user_id = input("Enter User ID: ")

        if user_id in self.users:
            print(f"Welcome {self.users[user_id].name}!")
        else:
            print("New user — registration required.")
            name = input("Enter name: ")
            email = input("Enter email: ")
            self.users[user_id] = User(user_id, name, email)
            self.save_data()

        return user_id
#---------------------- DISPLAY  ALL USERS ----------------
    def display_users(self):
        print("\n=== USERS LIST ===")
        for u in self.users.values():
            u.show_details()
        print("===================")

    # ---------------- ADD BOOK ----------------
    def add_book(self):
        book_id = input("Enter Book ID: ")

        if book_id in self.books:
            print("Book exists — adding more copies.")
            extra = int(input("How many copies to add? "))
            self.books[book_id]._Book__total_copies += extra
            self.books[book_id]._Book__available_copies += extra
        else:
            title = input("Enter title: ")
            author = input("Enter author: ")
            year = input("Enter year: ")
            copies = int(input("Enter no. of copies: "))

            self.books[book_id] = Book(book_id, title, author, year, copies)

        self.save_data()

    # ---------------- SHOW BOOKS ----------------
    def show_available_books(self):
        print("\n=== AVAILABLE BOOKS ===")
        for b in self.books.values():
            if b._Book__available_copies > 0:
                print(f"{b.get_title()} ({b._Book__available_copies} available)")
        print("========================")

    def display_all_books(self):
        print("\n=== ALL BOOKS ===")
        for b in self.books.values():
            print(f"[{b.book_id}] {b.get_title()} | Borrowed by: {b.borrowed_by}")
        print("=================")

    # ---------------- BORROW ----------------
    def borrow_book(self, user_id):
        book_id = input("Enter Book ID to borrow: ")

        if book_id not in self.books:
            print("Book not found.")
            return

        user = self.users[user_id]
        book = self.books[book_id]

        if book.borrow(user_id):
            user.borrow_book(book_id)
            self.save_data()
            print("Book borrowed!")
        else:
            print("No copies available.")
#--------------------- RETURN BOOK FUNCTION ----------------
    def return_book(self, user_id):
        book_id = input("Enter Book ID to return: ")
        user = self.users[user_id]

        if book_id not in user.borrowed_books:
            print("You did not borrow this book.")
            return

        user.return_book(book_id)
        self.books[book_id].return_book()
        self.save_data()
        print("Book returned!")

#----- ---------------- MAIN MENU  OF THE PROGRAM  ----------------
    def run(self):
        current_user = self.user_login()

        while True:
            self.show_dashboard()

            print("1. Add Book")
            print("2. Show Available Books")
            print("3. Display ALL Books")
            print("4. Borrow Book")
            print("5. Return Book")
            print("6. Display Users")
            print("7. Exit")

            choice = input("Enter choice: ")

            if choice == "1":
                self.add_book()
            elif choice == "2":
                self.show_available_books()
            elif choice == "3":
                self.display_all_books()
            elif choice == "4":
                self.borrow_book(current_user)
            elif choice == "5":
                self.return_book(current_user)
            elif choice == "6":
                self.display_users()
            elif choice == "7":
                self.save_data()
                print("Goodbye!")
                break
            else:
                print("Invalid choice!")


# ========================= MAIN ========================= JANGO MANGO
if __name__ == "__main__":
    filename = "library.txt"
    lib = Library(filename)
    lib.run()
