
print("============================== start TableEls.py file content ===========================")

import psycopg2

def connect():
    #  First connect the code to postgress
    con=psycopg2.connect("dbname='suryabhan' user='surya' password='Pandeyji@9' host='localhost' port='5432' ")
    cur=con.cursor()
    #  after connected succefully to postgress; create a table
    cur.execute("CREATE TABLE if not exists ElsObj(address_id INT, address TEXT NOT NULL, " 
     "al1 TEXT NOT NULL, al2 TEXT NOT NULL, al3 TEXT NOT NULL, sortcode TEXT NOT NULL, keyword TEXT NOT NULL, pincode INT)")
    # commit the changes to the database
    con.commit()
    con.close()

def insert(address_id, address, al1, al2, al3, sortcode,  keyword, pincode):
    #  First connect the code to postgress
    con=psycopg2.connect("dbname='suryabhan' user='surya' password='Pandeyji@9' host='localhost' port='5432' ")
    cur=con.cursor()
    #  after connected succefully to postgress; insert in to table
    cur.execute("INSERT INTO ElsObj(address_id, address, al1, al2, al3, sortcode, keyword, pincode)"
       "VALUES(%s, %s, %s, %s, %s, %s, %s, %s) returning address_id", (address_id, address, al1, al2, al3, sortcode, keyword, pincode))
    # commit the changes to the database
    con.commit()
    con.close()

def selectAll(address_id):
    #  First connect the code to postgress
    con=psycopg2.connect("dbname='suryabhan' user='surya' password='Pandeyji@9' host='localhost' port='5432' ")
    cur=con.cursor()
    #  after connected succefully to postgress; select data from table
    cur.execute(f'''SELECT * from ElsObj where address_id = {address_id}''')

    #  after execute the command of  select data from table; export the dat and store it;
    # Note: without execute the command for selecet the data; you cann't export directly using result = cur.fetchall()
    # use cur.fetchone() to print the top 1st row and cur.fetchall() to print all rows
    result = cur.fetchone()
    print("ElsObj result = ", result, cur)

    try:
      for obj in result:
       print("inside selectAll function ", obj, sep=' ')
       print("result = ", result)
    except:
     return ["address_id does not exist"]

    print("==============================  End  TableEls.py file content ===========================")

    # commit the changes to the database
    con.commit()
    con.close()
    
    # return tha stored data show that we can store the data again in any varible;
    return result



# connect()

# insert(1, "Bihar, Kaimur(Bhabhua), Manihari", "Bihar", "Kaimur", "Manijari", "sort1", "BKM", 821105)
# insert(2, "Bihar, Kaimur(Bhabhua), Naraw", "Bihar", "Kaimur", "Naraw", "sort2",  "BKN") #pincode ->null
# insert(3, "Bihar, Kaimur(Bhabhua), Khanaw", "Bihar", "Kaimur", "", "sort1",  "BKNP")    #pincode, al3 ->null
# insert(4, "Bihar, Kaimur(Bhabhua), Morwa", "Bihar", "", "", "sort3", "BNN", 821106)         #al2, al3 ->null
# insert(5, "Bihar, Kaimur(Bhabhua), Khanaw", "", "", "", "sort2", "BKM", 821107)             #al1, al2, al3 ->null
# insert(6, "Bihar, Kaimur(Bhabhua), Khanaw", "Bihar", "Kaimur", "Manihari", "", "", 821108) #sortcode ->null
# insert(7, "", "", "", "", "", "ALLLN", 821108) #sortcode ->null
# insert(8, "Bihar, Kaimur(Bhabhua), khanaw", "", "", "", "", "BKMM", 821105)
# insert(9, "Bihar, Kaimur(Bhabhua), khanaw", "", "", "", "", "", 821105)



