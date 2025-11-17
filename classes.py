#classes topic
#library managment system 
#creating library mangment syastem using oop 
#----------------------------------------------

import os
#-----------------classes----------------------
class book:
   def __init__(self,book_id,author,total_copies,year,title):
    self.book_id=book_id
    self.author=author
    self.title=title
    self.total_copies=total_copies
    self.available_copies=total_copies
    self.year=year
    self.borrow_by="None"

   def borrow(self,user_id):
    if self.available_copies>0:
       self.available_copies-=1
       self.borrowed_by=user_id

   def return_book(self):
    self.available_copies+=1
    if self.available_copies==self.total_copeis:
        self.borrowed_by="None"


   def to_line(self):
        return f"{self.book_id},{self.title},{self.author},{self.year},{self.total_copies},{self.available_copies},{self.borrowed_by}"
   @staticmethod
   def from_line(line):
        parts = line.split(",")
        if len(parts) < 7:
            return None
        book =book(parts[0], parts[1], parts[2], parts[3], int(parts[4]))
        book.available_copies = int(parts[5])
        book.borrowed_by = parts[6]
        return book
   
class user:
   def __init__(self,user_id,name,email):
      self.user_id=user_id
      self.name=name
      self.email=email
      self.borrowed_books=[]

   def borrow_book(self, book_id):
        self.borrowed_books.append(book_id)
 
   def return_book (self, book_id):
      if book_id in self.borrowed_books:
       self.borrowed_books.remove(book_id)

   def to_line(self):
     borrowed = ";".join(self.borrowed_books) if self.borrowed_books else "None"
     return f"{self.user_id},{self.name},{self.email},{borrowed}"
   
   @staticmethod
   def from_line(line):
      parts=line.split(",")
      if len(parts) < 4:
            return None
      borrowed_list = parts[3].split(";") if parts[3] != "None" else []
      user = user(parts[0], parts[1], parts[2])
      user.borrowed_books = borrowed_list
      return user 


class library:

  def __init__(self,filename):
     self.filename=filename
     self.books = {}
     self.users = {}
     self.load_data()


     #file handling -------------------
  
def save_data(self):
    try:
        with open(self.filename,"w")as f:
           f.write("#BOOKS\n")
           for b in self.books.values():
                    f.write(b.to_line() + "\n")
                    f.write("#USERS\n")
           for u in self.users.values():
                    f.write(u.to_line() + "\n")
                    print(" All data saved successfully!")
    except Exception as e:
            print(f" Error saving data: {e}") 

def load_data(self):
    if not os.path.exists(self.filename):  # <-- use exists (not exist)
        print("No existing file found! Refresh again.")
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
                    book = book.from_line(line)
                    if book:
                        self.books[book.book_id] = book

                elif section == "users":
                    user = user.from_line(line)
                    if user:
                        self.users[user.user_id] = user

        print("Data loaded successfully!")

    except Exception as e:
        print(f"Error loading data: {e}")


#-------------------dashboard-------------------------
def show_dashboard(self):  #creating dashboard ! jango mango 
  total_books=len(self.books) 
  total_users=len(self.users )
  available=sum(b.available_copies for b in self.books.values())
  borrowed=sum((b.total_copies - b.available_copies for b in self.books.values()))
  print("\n" + "="*60)
  print("📚 LIBRARY DASHBOARD")
  print("="*60)
  print(f" Total Books: {total_books}")
  print(f" Available Copies: {available}")
  print(f" Borrowed Copies: {borrowed}")
  print(f" Total Users: {total_users}")
  print("="*60)


#------------------user managment ka section---------------


def user_login(self):
        user_id = input("Enter your User ID: ")
        if user_id in self.users:
            print(f"Welcome back, {self.users[user_id].name}!")
        else:
            print("New user detected — please register.")
            name = input("Enter your Name: ")
            email = input("Enter your Email: ")
            self.users[user_id] = user(user_id, name, email)
            self.save_data()
            print(" User registered successfully!")
        return user_id

def display_users(self):
        print("\n ALL USERS")
        print("="*60)
        for u in self.users.values():
            borrowed = ", ".join(u.borrowed_books) if u.borrowed_books else "None"
            print(f"[{u.user_id}] {u.name} ({u.email}) | Borrowed: {borrowed}")
        print("="*60)

    # ------------------ BOOK MANAGEMENT ------------------
def add_book(self):
        while True:
            book_id = input("Enter Book ID: ")
            if book_id in self.books:
                print("Book already exists — adding more copies.")
                extra = int(input("How many extra copies to add? "))
                self.books[book_id].total_copies += extra
                self.books[book_id].available_copies += extra
            else:
                title = input("Enter Book Title: ")
                author = input("Enter Author Name: ")
                year = input("Enter Published Year: ")
                copies = int(input("Enter Number of Copies: "))
                self.books[book_id] = book(book_id, title, author, year, copies)
            self.save_data()
            print(" Book record updated successfully!")
            if input("Add another book? (y/n): ").lower() != 'y':
                break

def show_available_books(self):
        print("\n AVAILABLE BOOKS")
        print("="*60)
        found = False
        for b in self.books.values():
            if b.available_copies > 0:
                found = True
                print(f"{b.title} by {b.author} ({b.year}) — {b.available_copies} copies available")
        if not found:
            print(" No books currently available.")
        print("="*60)

def display_all_books(self):
        print("="*60)
        if not self.books:
            print("No books found.")
            return
        for b in self.books.values():
            print(f"[{b.book_id}] {b.title} by {b.author} ({b.year})")
            print(f"   Total: {b.total_copies} | Available: {b.available_copies} | Borrowed by: {b.borrowed_by}")
        print("="*60)

    # ------------------ TRANSACTIONS ------------------
def borrow_book(self, user_id):
        book_id = input("Enter Book ID to borrow: ")
        if book_id not in self.books:
            print(" Book not found.")
            return
        book = self.books[book_id]
        user = self.users[user_id]

        if book.borrow(user_id):
            user.borrow_book(book_id)
            self.save_data()
            print(f" You borrowed '{book.title}' successfully!")
        else:
            print(" No copies available right now.")

def return_book(self, user_id):
        book_id = input("Enter Book ID to return: ")
        user = self.users[user_id]
        if book_id not in user.borrowed_books:
            print(" You haven’t borrowed this book.")
            return
        user.return_book(book_id)
        self.books[book_id].return_book()
        self.save_data()
        print(f" You returned '{self.books[book_id].title}' successfully!")

#----------------main menu ______________________________
## This code is so good, it practically writes itself.
# I'm not saying I'm lazy, but I prefer to call it "efficient."
# Warning: May spontaneously generate unicorns.
# If this code works, I'm a genius. If not, blame the coffee.
# This comment is intentionally left blank.
# My therapist told me to embrace my inner child, so I wrote this.
# TODO: Replace magic with actual code.
# I spent 3 hours debugging this for a typo. You're welcome.
# This function is a work of art, if art were made of bugs.
# Future me will thank me for this comment. Or curse me. Probably curse me.
# Don't try this at home, kids. Or do. I'm not your parent.



def run(self):
    current_user=self.user_login()
    while True:
        self.show_dashboard()
        print("main menu:")
        print("="*60)
        print("1 add book")
        print("2 show available books")
        print("3 display all books ")
        print("4 borrow books")
        print("5 return book")
        print("6 display all users  ")
        print("7 exit")
        print("="*60)

        
        choice = input("Enter choice: ")
        if choice == '1':
                self.add_book()
        elif choice == '2':
                self.display_all_books()
        elif choice == '3':
                self.show_available_books()
        elif choice == '4':
                self.borrow_book(current_user)
        elif choice == '5':
                self.return_book(current_user)
        elif choice == '6':
                self.display_users()
        elif choice == '7':
                self.save_data()
                print("💾Data saved. Exiting... Goodbye! tata seeyou")
            
                break
        else:
                print(" Invalid choice!")

# ------------------ MAIN ------------------
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(script_dir, "library.txt")
    library = library(filename)
    library.run()










