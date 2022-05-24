from models import Base, Session, Book, engine


# import models
# main menu - add, search, analysis, exit, view
# add books to the database
# edit books
# delete
# search
# cleaning data
# loop runs program

if __name__ == "__main__":
    Base.metadata.create_all(engine)
