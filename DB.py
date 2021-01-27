import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host="",
        user="",
        password="",
        database=""
    )
    return connection

#work with competition
def add_table_in_database(table_name):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE {} (id_Captain VARCHAR (255), Captain VARCHAR (255) , Team_name VARCHAR (255),"
                   " Confirmation INTEGER(10), PRIMARY KEY(id_Captain, Captain, Team_name, "
                   "Confirmation))".format(table_name))
    cursor.execute("SHOW TABLES")

    for tb in cursor:
        print(tb)

def add_to_table(table_name, id_captain_read, captain_read, team_name_read):
    connection = get_connection()
    cursor = connection.cursor()

    sqlInsert = "INSERT INTO {} (id_Captain, Captain, Team_name, Confirmation) VALUES (%s, %s, %s, %s) " \
                "ON DUPLICATE KEY UPDATE Captain = %s, Team_name = %s".format(table_name)
    participant = (id_captain_read, captain_read, team_name_read, 0, captain_read, team_name_read)

    cursor.execute(sqlInsert, participant)
    connection.commit()

    connection.close()

def update_status(table_name_read, id_captain_read, team_name_read, confirmation):
    connection = get_connection()
    cursor = connection.cursor()

    sqlUpd = "UPDATE {} SET Confirmation = %s WHERE id_Captain = %s AND Team_name = %s".format(table_name_read)
    temp = (confirmation, id_captain_read, team_name_read)

    cursor.execute(sqlUpd,temp)
    connection.commit()

    connection.close()

#verification by captain's name and team name
#you can insert it in add_to_table() to verify registration
def return_data_from_database(table_name_read, captain_read, team_name_read):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT Captain, Team_name FROM {} WHERE Captain = %s".format(table_name_read),
                   (captain_read, team_name_read,))

    rows = cursor.fetchone()
    arr_result = []
    i = 0;

    for row in rows:
        arr_result.insert(i, rows[i])
        i += 1

    cursor.close()
    connection.close()

    #arr_result[0] - Captain name
    #arr_result[1] - Team name
    return(arr_result)

#verification by dint of captain's_id
def return_data_from_database_by_id(table_name_read, captain_id_read):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT Captain, Team_name FROM {} WHERE id_Captain = %s".format(table_name_read),
                   (captain_id_read,))

    rows = cursor.fetchone()
    arr_result = []
    i = 0

    for row in rows:
        arr_result.insert(i, rows[i])
        i += 1

    cursor.close()
    connection.close()

    #arr_result[0] - Captain name
    #arr_result[1] - Team name
    return(arr_result)

#if the number of participants exceeds the specified limit, the function returns false
#limit seat = 50;
def seat_check(table_name_read):
    limit_seat = 3
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT Confirmation FROM {} WHERE Confirmation = 0".format(table_name_read))

    rows = cursor.fetchall()

    result = len(rows) #number of participants who have confirmed their participation
    print(result)

    cursor.close()
    connection.close()

    if(result < limit_seat):
        return True
    else:
        return False

def delete_table(table_name):
    connection = get_connection()
    cursor = connection.cursor()

    sqlDel = "DROP TABLE {} ".format(table_name)

    cursor.execute(sqlDel)
    connection.commit()
    connection.close()

#work with distribution
#operation performed 1 time
def add_idTable_in_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE id_table (id VARCHAR (255) PRIMARY KEY )")


def add_to_id_table(id_read):
    connection = get_connection()
    cursor = connection.cursor()

    sqlInsert = "INSERT IGNORE INTO id_table (id) VALUES (%s)"
    participant = (id_read,)

    cursor.execute(sqlInsert, participant)
    connection.commit()

    connection.close()


def delete_from_idTable(del_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM id_table WHERE id = %s", (del_id,))
    connection.commit()

    connection.close()

#data
def extract_data():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM id_table")

    rows = cursor.fetchall()
    id_arr = []
    i = 0
# here you can do the distribution for each individual id using row[0],
# given an example of how it displays all the elements of the tuple
    for row in rows:
        id_arr.insert(i,row[0])
        i += 1

    cursor.close()
    connection.close()

    return id_arr


#print("Enter captain id")
#captain_id = "id56783"
#print("Enter team name")
#team = "hyruijm"
#table_name = "teams_new"
#update_status(table_name, captain_id, team, 1)
#update_status(table_name, captain_id, team, 1)
#update_status(table_name, captain_id, team, 1)

#print(seat_check(table_name))

#extract_data()

#add_table_in_database("Teams_new")
#delete_table("teams_new")


#data = input().split()
#add_to_table(data[0], data[1])
#update_status(data[0], data[1])

#print("Enter captain id")
#captain_id = input()
#print("Enter captain")
#captain = input()
#print("Enter team name")
#team = input()
#table_name = "teams_new"
#add_to_table(table_name, captain_id, captain, team)

#delete_table("id_table")
#add_idTable_in_database()
#add_to_id_table("id6789")
#add_to_id_table("id7869")
#add_to_id_table("id9067")
#add_to_id_table("id5576")
#add_to_id_table("id9706")
#add_to_id_table("id3434")

#delete_from_idTable("id6758")
