from models import Base, session, Book, engine
import datetime
import csv
import time


def menu():
    while True:
        print("""Programming Books:
        1. Add a book
        2. View all books
        3. Search a book
        4. Book analysis
        5. Exit
        """)
        choice = input("What do you want to do? ")
        if choice in ("1", "2", "3", "4", "5"):
            return choice
        else:
            input("Invalid choice. Please choose one of the number from 1-5. Press enter to try again.")


def sub_menu():
    while True:
        print("""Sub menu to choose:
        1. Edit 
        2. Delete a book
        3. Return to main menu
        """)
        choice = input("What do you want to do? ")
        if choice in ("1", "2", "3"):
            return choice
        else:
            input("Invalid choice. Please choose one of the number from 1-3. Press enter to try again.")


# main menu - add, search, analysis, exit, view
# add books to the database
# edit books
# delete
# search


def clean_date(date_str):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']
    split_date = date_str.split(' ')
    try:
        month = int(months.index(split_date[0]) + 1)
        day = int(split_date[1].split(',')[0])
        year = int(split_date[2])
        return_date = datetime.date(year, month, day)
    except ValueError:
        input("Date error. Valid date format should be like this (Ex: January 23, 2001). Press enter to try again. ")
        return
    else:
        return return_date


def clean_price(price_str):
    try:
        price = float(price_str)
    except ValueError:
        input("Price error. Valid price format should be like this (Ex: 5.99). Press enter to try again. ")
        return
    else:
        return int(price * 100)


def clean_id(id_str, options):
    try:
        book_id = int(id_str)
    except ValueError:
        input("Id error. Id should be a number. Press enter to try again. ")
        return
    else:
        if book_id in options:
            return book_id
        else:
            print(f"Your input id is out of options. Please try again. Options: {options}")
            return


def edit_check(column_name, current_value):
    print(f'\nEDIT {column_name} ')
    if column_name == 'Price':
        print(f"Current value: {current_value/100}")
    elif column_name == 'Published':
        print(f"Current value: {current_value.strftime('%B %d, %Y')}")
    else:
        print(f"Current value: {current_value}")

    if column_name == 'Price' or column_name == 'Published':
        while True:
            changes = input('What would you like change the value to? ')
            if column_name == 'Published':
                changes = clean_date(changes)
                if type(changes) == datetime.date:
                    return changes
            elif column_name == 'Price':
                changes = clean_price(changes)
                if type(changes) == int:
                    return changes
    else:
        return input('What would you like to change the value to? ')


def add_csv():
    with open('suggested_book.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            book_in_db = session.query(Book).filter(Book.title == row[0]).one_or_none()
            if book_in_db == None:
                title = row[0]
                author = row[1]
                date = clean_date(row[2])
                price = clean_price(row[3])
                new_book = Book(title=title, author=author, published_date=date, price=price)
                session.add(new_book)
        session.commit()


def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == '1':
            title = input("Title: ")
            author = input("Author: ")
            date_error = True
            while date_error:
                date = input("Published date (Ex: October 25, 2017): ")
                date = clean_date(date)
                if type(date) == datetime.date:
                    date_error = False

            price_error = True
            while price_error:
                price = input("Price (Ex: 29.99): ")
                price = clean_price(price)
                if type(price) == int:
                    price_error = False

            new_book = Book(title=title, author=author, published_date=date, price=price)
            session.add(new_book)
            session.commit()
            print("Book added! ")
            time.sleep(1.5)
        elif choice == '2':
            for book in session.query(Book):
                print(f"{book.id} -> {book.title} -> {book.author} -> {book.published_date} -> {book.price}")
        elif choice == '3':
            id_options = []
            for book in session.query(Book):
                id_options.append(book.id)
            id_error = True
            while id_error:
                id_choice = input(f"ID options: {id_options} \nBook id: ")
                id_choice = clean_id(id_choice, id_options)
                if type(id_choice) == int:
                    id_error = False
            the_book = session.query(Book).filter(Book.id == id_choice).first()
            print(f"{the_book.title} by {the_book.author} is published in {the_book.published_date} "
                  f"and price is {the_book.price/100}")
            sub_choice = sub_menu()
            if sub_choice == '1':
                the_book.title = edit_check("Title", the_book.title)
                the_book.author = edit_check("Author", the_book.author)
                the_book.published_date = edit_check("Published", the_book.published_date)
                the_book.price = edit_check("Price", the_book.price)
                session.commit()
                print("Book updated! ")
                time.sleep(1.5)
            elif sub_choice == '2':
                session.delete(the_book)
                session.commit()
                print("Book deleted! ")
                time.sleep(1.5)
        elif choice == '4':
            oldest_book = session.query(Book).order_by(Book.published_date).first()
            newest_book = session.query(Book).order_by(Book.published_date.desc()).first()
            total_books = session.query(Book).count()
            python_books = session.query(Book).filter(Book.title.like("%Python%")).count()
            print(f"_____Book Analysis_____"
                  f"\nOldest book: {oldest_book}"
                  f"\nNewest book: {newest_book}"
                  f"\nTotal number of books: {total_books}"
                  f"\nTotal number of python books: {python_books}\n")
            input("Press enter to return to main menu. ")
        else:
            print("Goodbye!")
            app_running = False


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    add_csv()
    app()
