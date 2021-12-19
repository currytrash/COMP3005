from tabulate import tabulate
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import pandas as pd
from psycopg2 import errors
from datetime import datetime
import random
import string
UniqueViolation = errors.lookup('23505')
ForeignKeyViolation = errors.lookup('23503')
CheckViolation = errors.lookup('23514')
global run
global currUser
global currResult
global isLoggedIn
global isAdmin

queryHeaders = [
    'ISBN', 'TITLE', 'AUTHORS', 'PUBLISHER', 'YEAR', 'GENRE', 'PAGES', 'PRICE', 'STOCK']


def executeScriptsFromFile(filename):
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    # Execute every command from the input file
    for command in sqlCommands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        try:
            cursor.execute(command)
        except psycopg2.ProgrammingError as e:
            print("Command skipped: ", command, e)


def makeQuery(*args):
    query = "("
    for arg in args:
        if (arg == args[-1]):
            query += "'" + arg + "')"
        else:
            query += "'" + arg + "',"
    return query


def searchByQuery(searchBy, searchArg):
    global currResult
    print("")
    cursor.execute(searchQuery.format(searchBy, searchArg))
    currResult = cursor.fetchall()
    print(tabulate(currResult, headers=queryHeaders))
    print("")


def searchByAuthor(searchBy, searchType, searchArg):
    global currResult
    print("")
    cursor.execute(searchQueryAuthor.format(
        searchBy, searchType, searchArg))
    currResult = cursor.fetchall()
    print(tabulate(currResult, headers=queryHeaders))
    print("")


# Connect to PostgreSQL DBMS

con = psycopg2.connect(database='lookinnabook',
                       user='postgres',
                       password='doublelift9')

con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)


# Obtain a DB Cursor
global cursor
cursor = con.cursor()

name_Database = "LookInnaBook"
name_Schema = "bookstore"

viewQuery = (
    """
        Select isbn,title, string_agg(full_name, ',') as author,pub_name,pub_year,genre,pages,price,stock from (
SELECT isbn,title,
trim(concat(writes.author_first, ' ',writes.author_last)) as full_name,
	   genre,pages,price,stock,pub_name,pub_year
FROM bookstore.book natural join bookstore.writes natural join bookstore.publisher natural join bookstore.publishes
Group by isbn,title,genre,pages,price,stock,writes.author_first,writes.author_last,publisher.pub_name,publishes.pub_year
)src
group by src.isbn,src.title,src.price,src.stock,src.pages,src.genre,src.pub_name,src.pub_year

""")


searchQuery = (
    """
        Select isbn,title, string_agg(full_name, ',') as author,pub_name,pub_year,genre,pages,price,stock from (
SELECT isbn,title,
trim(concat(writes.author_first, ' ',writes.author_last)) as full_name,
	   genre,pages,price,stock,pub_name,pub_year
FROM bookstore.book natural join bookstore.writes natural join bookstore.publisher natural join bookstore.publishes
Group by isbn,title,genre,pages,price,stock,writes.author_first,writes.author_last,publisher.pub_name,publishes.pub_year
)src
where src.{}='{}'

group by src.isbn,src.title,src.price,src.stock,src.pages,src.genre,src.pub_name,src.pub_year

""")

searchQueryAuthor = (
    """
       Select isbn,title, string_agg(full_name, ',') as author,pub_name,pub_year,genre,pages,price,stock from (
SELECT isbn,title,
trim(concat(writes.author_first, ' ',writes.author_last)) as full_name,
	   genre,pages,price,stock,pub_name,pub_year,author_first,author_last

FROM bookstore.book natural join bookstore.writes natural join bookstore.publisher natural join bookstore.publishes
Group by isbn,title,genre,pages,price,stock,writes.author_first,writes.author_last,publisher.pub_name,publishes.pub_year
)src
where src.author_first ='{}' {} src.author_last='{}'

group by src.isbn,src.title,src.price,src.stock,src.pages,src.genre,src.pub_name,src.pub_year,src.author_first,src.author_last


""")

# Create table statement

sqlCreateDatabase = "create database " + name_Database + ";"


# Create a table in PostgreSQL database

# cursor.execute(sqlCreateDatabase)


# executeScriptsFromFile("Comp3005Project.txt")
# executeScriptsFromFile("insertions.txt")

run = True
isLoggedIn = False
isAdmin = False

while (run):
    userInput = input("Enter your command ('h' for help): ")
    #
    commands = [
        #
        ["help", "prints help command"],
        ["add user", "register new user"],
        ["add admin", "register new admin"],
        ["login", "login to account"],
        ["add cc", "add credit card"],
        ["add addr", "add address"],
        ["browse", "browse books"],
        ["search", "search for books"],
        ["add basket", "add basket"],
        ["view basket", "view basket"],
        ["add book", "add book to basket"],
        ["del book", "del book from store"],
        ["checkout", "checkout basket"],
        ["submit", "submit order"],
        ["track", "track order"]





    ]

################################################################################################################################
    if (userInput == 'h'):

        print(tabulate(commands, headers=["Command", "Description"]))
################################################################################################################################

    if (userInput == "add user" or userInput == "add admin"):
        isAdmin = "f"
        Newusername = input("Enter new UserName: ")
        Newpassword = input("Enter Password: ")
        Newfn = input("Enter First Name: ")
        Newln = input("Enter Last Name: ")
        Newemail = input("Enter Email: ")

        if (userInput == "add admin"):
            isAdmin = "t"
        query = makeQuery(Newusername, Newpassword,
                          Newfn, Newln, Newemail, isAdmin)
        cursor.execute("insert into bookstore.user values" + query)
################################################################################################################################
    if (userInput == "login"):

        userlgn = input("Enter Username:")
        cursor.execute(
            "select * from bookstore.user where username = '" + userlgn + "';")
        if(cursor.rowcount):
            pwlgn = input("Enter Password:")
            cursor.execute(
                "select first_name, last_name, isAdmin from bookstore.user where username = '" + userlgn + "' and password = '" + pwlgn + "';")
            if (cursor.rowcount):
                isLoggedIn = True
                currUser = userlgn

                result = cursor.fetchall()
                query = (
                    """select count(*) from bookstore.user_basket where username = '{}'""").format(currUser)
                cursor.execute(query)
                baskresults = cursor.fetchall()
                if baskresults[0][0] == 0:
                    cursor.execute(
                        "insert into bookstore.basket values(Default)")
                    cursor.execute("select * from bookstore.basket")
                    baskidresult = cursor.fetchall()
                    query = makeQuery(str(baskidresult[-1][0]), currUser)
                    cursor.execute(
                        "insert into bookstore.user_basket values" + query)

                if result[0][2] == True:
                    isAdmin = True
                    print("Welcome ADMIN " +
                          result[0][0] + " " + result[0][1] + "!")
                else:
                    print("Welcome USER " +
                          result[0][0] + " " + result[0][1] + "!")
            else:
                print("Login Failed! Incorrect Password...")
                continue
        else:
            print("Login Failed! Invalid Username...")
            continue

################################################################################################################################
    if (userInput == "browse" and isLoggedIn):
        cursor.execute(viewQuery)

        print("")
        print("")
        print(tabulate(cursor.fetchall(), headers=queryHeaders))
        print("")
        continue
################################################################################################################################
    if (userInput == "search"):

        searchCommands = [


            ["title", "Search by Title"],
            ["author", "Search by Author Full Name"],
            ["author fn", "Search by Author First Name"],
            ["author ln", "Search by Author Last Name"],
            ["genre", "Search by Genre"],
            ["publisher", "Search by Publisher"],
            ["isbn", "Search by isbn-10"],
            ["pub_year", "Search by Year Published"],
            ["", ""],
            ["", ""]

        ]

        print(tabulate(searchCommands, headers=[
              'Search Command', 'Description']))
        searchBy = input("What parameter would you to search by?: ")

        if (searchBy == 'title'):
            searchArg = input("Enter Book Title: ")
            searchByQuery(searchBy, searchArg)
        if (searchBy == 'author'):
            searchArg = input("Enter Author's Full Name: ")
            searchInput = searchArg.split(' ')
            searchByAuthor(searchInput[0], 'and', searchInput[1])
        if (searchBy == 'author fn'):
            searchBy = input("Enter Author's First Name: ")
            searchByAuthor(searchBy, 'or', '')
        if (searchBy == 'author ln'):
            searchBy = input("Enter Author's Last Name: ")
            searchByAuthor('', 'or', searchBy)
        if (searchBy == 'genre'):
            searchArg = input("Enter Book Genre: ")
            searchByQuery(searchBy, searchArg)
        if (searchBy == 'publisher'):
            searchArg = input("Enter Publisher's Name: ")
            searchByQuery(searchBy, searchArg)
        if (searchBy == 'isbn'):
            searchArg = input("Enter ISBN-10: ")
            searchByQuery(searchBy, searchArg)
        if (searchBy == 'pub_year'):
            searchArg = input("Enter Year Published: ")
            searchByQuery(searchBy, searchArg)

    if (userInput == "add cc" and isLoggedIn):

        Newcc = input("Enter 16 digit Credit Card Number (no spaces): ")
        query = (
            """select count(*) from bookstore.user_cc where cc_number= '{}' and username = '{}'""").format(Newcc, currUser)
        cursor.execute(query)
        results = cursor.fetchall()
        if results[0][0] == 1:
            print("User Already Has This CC Linked...")
            continue

        Newfn = input("Enter First Name: ")
        Newln = input("Enter Last Name: ")
        Newmonth = input("Enter Month Expiry: ")
        Newyear = input("Enter year Expiry: ")
        Newcvv = input("Enter 3 digitCVV: ")

        query = makeQuery(Newcc, Newfn, Newln, Newmonth, Newyear, Newcvv)
        cursor.execute("insert into bookstore.cc values" + query)
        query = makeQuery(Newcc, currUser)
        cursor.execute("insert into bookstore.user_cc values" + query)
        print("...CC Added")
    if (userInput == "add basket" and isLoggedIn):
        cursor.execute("insert into bookstore.basket values(Default)")
        cursor.execute("select * from bookstore.basket")
        result = cursor.fetchall()
        query = makeQuery(str(result[-1][0]), currUser)
        cursor.execute("insert into bookstore.user_basket values" + query)
        print("...Added Basket")

    if (userInput == "add addr" and isLoggedIn):

        addrname = input("Enter Address Name: ")
        addrnum = input("Enter Address Number: ")
        city = input("Enter City: ")
        province = input("Enter Province: ")
        postal = input("Enter Postal Code: ")

        query = ("""insert into bookstore.address values(Default,'{}','{}','{}','{}','{}')""").format(
            addrname, addrnum, city, province, postal)
        cursor.execute(query)
        cursor.execute("select * from bookstore.address")
        result = cursor.fetchall()
        query = makeQuery(str(result[-1][0]), currUser)
        cursor.execute("insert into bookstore.user_addr values" + query)
        print("...Added Address")

    if (userInput == "del book" and isLoggedIn):
        if (not isAdmin):
            print("Must be Admin to Delete a Book")
            continue
        ISBN = input("Enter ISBN-10 of Book to be Deleted: ")
        query = (
            """select count(*) from bookstore.book where isbn ='{}'""").format(ISBN)
        cursor.execute(query)
        results = cursor.fetchall()
        if results[0][0] == 0:
            print("Book does not exist...Aborting")
            continue
        query = (
            """select title from bookstore.book where isbn='{}'""").format(ISBN)
        cursor.execute(query)
        results = cursor.fetchall()
        title = results[0][0]
        print("Deleting...")
        query = ("""delete from bookstore.book where isbn='{}'""").format(ISBN)
        cursor.execute(query)
        print("..." + title + "was Deleted ")

    if (userInput == "add book" and isLoggedIn and isAdmin):
        ISBN = input('Enter ISBN-10: ')
        query = (
            """select count(*) from bookstore.book where isbn ='{}'""").format(ISBN)
        cursor.execute(query)
        results = cursor.fetchall()
        if results[0][0] == 1:
            print("Book already exists in store...Aborting")
            continue

        Title = input("Enter Book Title: ")
        Genre = input("Enter Book Genre: ")
        Pages = input("Enter Number of Pages: ")
        Price = input("Enter Book Price: ")
        Royalty = input("Enter Publisher Royalty %: ")
        Stock = input("Enter Stock: ")

        query = makeQuery(ISBN, Title, Genre, Pages, Price, Royalty, Stock)
        cursor.execute("insert into bookstore.book values" + query)

        numAuthor = int(input("Number of Authors? :"))

        for i in range(numAuthor):
            AuthorFN = input("Enter Author First Name:  ")
            AuthorLN = input("Enter Author Last Name: ")

            query = (
                """select count(*) from bookstore.author where author_first = '{}' and author_last = '{}'""").format(AuthorFN, AuthorLN)
            cursor.execute(query)
            results = cursor.fetchall()
            if results[0][0] == 0:
                print("Author not found in DataBase...")
                query = makeQuery(AuthorFN, AuthorLN)
                cursor.execute("insert into bookstore.author values" + query)
                print("...Author Added")
            query = makeQuery(AuthorFN, AuthorLN, ISBN)
            cursor.execute("insert into bookstore.writes values " + query)

        Publisher = input("Enter Book Publisher Name: ")
        PubMonth = input("Enter Month of Publish MM: ")
        PubDay = input("Enter Day of Publish DD: ")
        PubYear = input("Enter Year of Publish YYYY: ")

        query = (
            """select count(*) from bookstore.publisher where pub_name = '{}'""").format(Publisher)
        cursor.execute(query)
        results = cursor.fetchall()
        if results[0][0] == 0:
            print("Publisher Not Found...")
            print("Adding new Publisher")
            pubmail = input("Enter Publisher Email")
            pubnumber = input("Enter Publisher phonenumber (no '-'):")

            query = ("""insert into bookstore.publisher values ('{}','{}',{},0)""".format(
                Publisher, pubmail, pubnumber))
            cursor.execute(query)
            print("...Publisher Added")
        query = makeQuery(Publisher, ISBN, PubMonth, PubDay, PubYear)
        cursor.execute("insert into bookstore.publishes values" + query)
        continue

    if (userInput == "add book" and isLoggedIn):
        ISBN = input('Select ISBN-10:')
        Quantity = input('Quantity? (Max 99):')
        cursor.execute(
            "select basket_id from bookstore.user_basket where username='" + currUser + "';")
        print(tabulate(cursor.fetchall(), headers=["Basket"]))
        basketID = input("Select Basket: ")

        query = """('{}','{}','{}')""".format(basketID, ISBN, Quantity)
        try:
            cursor.execute(
                "insert into bookstore.book_basket values" + query)
        except ForeignKeyViolation as e:
            print("Invalid ISBN")
            continue
        except UniqueViolation as e:
            cursor.execute("update bookstore.book_basket set quantity = quantity + "
                           + Quantity + "WHERE isbn = '" + ISBN + "' AND basket_id = '" + basketID + "';")

    if (userInput == "view basket" and isLoggedIn):
        cursor.execute(
            "select basket_id from bookstore.user_basket where username='" + currUser + "';")
        print(tabulate(cursor.fetchall(), headers=["Basket"]))
        basketID = input("Select Basket: ")
        query = ("""
        select title,isbn,quantity,price,quantity*price as TOTAL from bookstore.book
        natural join bookstore.user_basket natural join bookstore.book_basket
        where username = '{}' and basket_id ='{}'
        group by title,book.isbn,user_basket.basket_id,book_basket.quantity   """)
        cursor.execute(query.format(currUser, basketID))
        results = cursor.fetchall()
        print("")
        print(tabulate(results, headers=[
              'Title', 'ISBN', 'Quantity', 'PRICE', 'TOTAL']))
        total = 0
        for row in results:
            total += row[4]
        print("")
        print("BASKET TOTAL:   " + str(total))

    if (userInput == "checkout" and isLoggedIn):
        cursor.execute(
            "select basket_id from bookstore.user_basket where username='" + currUser + "';")
        print(tabulate(cursor.fetchall(), headers=["Basket"]))
        basketID = input("Select Basket: ")

        query = ("""
        select title,isbn,quantity,price,quantity*price as TOTAL from bookstore.book
        natural join bookstore.user_basket natural join bookstore.book_basket
        where username = '{}' and basket_id ='{}'
        group by title,book.isbn,user_basket.basket_id,book_basket.quantity   """)
        cursor.execute(query.format(currUser, basketID))
        basketresults = cursor.fetchall()
        print("")
        print(tabulate(basketresults, headers=[
            'Title', 'ISBN', 'Quantity', 'PRICE', 'TOTAL']))
        total = 0
        for row in basketresults:
            total += row[4]
        print("")
        print("BASKET TOTAL:   " + str(total))
        print("")
        print("")
        print("")
        query = ("""select  ROW_NUMBER () OVER (ORDER BY cc_number),cc_number,cc_first_name,cc_last_name from bookstore.cc natural join bookstore.user_cc
        where username = '{}'""").format(currUser)
        cursor.execute(query)
        results = cursor.fetchall()
        print(tabulate(results, headers=[
              'Index', 'CC NUMBER', 'FIRST NAME', 'LAST NAME']))
        index = int(input("Select CC by Index Number: "))
        selectedCC = results[index - 1][1]

        query = """
        select
        address_id,
        address_name,
        address_num,
        city,
        province,
        postal_code

        from bookstore.user_addr natural join bookstore.address where
        bookstore.user_addr.address_id = bookstore.address.address_id and username ='{}'""".format(currUser)
        cursor.execute(query)
        results = cursor.fetchall()
        print(tabulate((results), headers=[
              'ADDRESS ID', 'ADDRESS NAME', 'NUMBER', 'CITY', 'PROVINCE', 'POSTAL CODE']))
        print("")
        shippingAddress = input("Select Shipping Address by ID : ")
        billingAddress = input("Select Billing Address: by ID : ")

        date = datetime.today().strftime('%Y-%m-%d')
        status = "Packing"
        trackingNum = ''.join(random.choice('0123456789ABCDEF')
                              for i in range(16))
        print("")
        query = ("(Default,'{}','{}','{}')".format(
            str(trackingNum), date, status))
        cursor.execute("insert into bookstore.order values" + query)
        cursor.execute("select * from bookstore.order")
        result = cursor.fetchall()

        query = """('{}','{}','{}')""".format(
            str(result[-1][0]), shippingAddress, 'f')
        cursor.execute("insert into bookstore.order_address values" + query)

        query = """('{}','{}','{}')""".format(
            str(result[-1][0]), billingAddress, 't')
        cursor.execute("insert into bookstore.order_address values" + query)

        query = """('{}','{}')""".format(str(result[-1][0]), currUser)
        cursor.execute("insert into bookstore.user_order values" + query)

        query = """('{}','{}')""".format(str(result[-1][0]), selectedCC)
        cursor.execute("insert into bookstore.paid_with values" + query)

        print("Please Record Tracking Number : {}".format(trackingNum))
        query = ("delete from bookstore.basket where basket_id = '{}'").format(
            basketID)
        total = str(total)
        print("$" + total + " Charged to CC : " + str(selectedCC))

        print("...")
        for row in basketresults:

            query = ("""select royalty,pub_name from bookstore.publisher natural join bookstore.publishes natural join bookstore.book
where isbn = '{}'""").format(row[1])

            cursor.execute(query)
            results = cursor.fetchall()
            royaltyfee = results[0][0] * (row[4] / 100)
            pubroy = results[0][1]

            query = (
                """update bookstore.publisher set acc_balance = acc_balance + {} WHERE pub_name =  '{}';""").format(royaltyfee, pubroy)
            cursor.execute(query)

            printstr = ("""Royalties:${:.2f} Added to publisher account {}""").format(
                royaltyfee, pubroy)
            print(printstr)
            query = ("""select stock from bookstore.book where isbn = '{}'""").format(
                row[1])
            cursor.execute(query)
            res = cursor.fetchall()
            currstock = res[0][0]
            print(currstock)
            query = (
                """update bookstore.book set stock = stock - {} where isbn = '{}'""").format(row[2], row[1])
            try:
                cursor.execute(query)
            except CheckViolation as e:

                newstock = row[2] - currstock
                if newstock == 0:
                    print("Damn you finessed all the " + row[0] + " books!")
                    print("...Ordering 99 more for future customers!")
                    query = (
                        """update bookstore.book set stock = 99  where isbn = '{}'""").format(row[1])
                    cursor.execute(query)
                    continue

                printstr = ("""Not Enough {} Books ...Ordering {} more to acomodate this order!""").format(
                    row[0], newstock)
                print(printstr)
                query = (
                    """update bookstore.book set stock = stock + {}  where isbn = '{}'""").format(newstock, row[1])
                cursor.execute(query)

    if (userInput == "track"):
        track = input("Enter Tracking Number:")
        query = (
            """select shipping_status from bookstore.order where tracking_num = '{}'""").format(track)
        cursor.execute(query)
        result = cursor.fetchall()

        print("Order is Currently : " + result[0][0])
