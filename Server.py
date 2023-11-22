import socket
import threading
import mysql.connector
import json


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="0227",
    database="name_db"
)
mycursor = mydb.cursor()

HEADER = 64
PORT = 5050

SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if not msg_length:
                connected = False
                break
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))
            
            msg_data = json.loads(msg) 

            if msg_data.get("execution") == 1:
                email = msg_data.get("email")
                first_name = msg_data.get("first_name")
                last_name = msg_data.get("last_name")
                password = msg_data.get("password")
                month = msg_data.get("month")
                day = msg_data.get("day")
                year = msg_data.get("year")
                gender = msg_data.get("gender")
                
                insert_query = "INSERT INTO personal_informations (email, first_name, last_name, user_password, selected_month, selected_day, selected_year, gender) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                values = (email, first_name, last_name, password, month, day, year, gender)
                mycursor.execute(insert_query, values)
                mydb.commit()
            
            elif msg_data.get("execution") == 2:
                user_email = msg_data.get("log")
                user_password = msg_data["password"]

                insert_query = "SELECT COUNT(*) FROM personal_informations WHERE email = %s and user_password = %s;"
                mycursor.execute(insert_query, (user_email, user_password))
                result = mycursor.fetchone()[0]

                if result > 0:
                    print(f"User with email '{user_email}' and password '{user_password}' exists.")
                    
                    conn.send("User exists".encode(FORMAT))
                else:
                    print(f"User with email '{user_email}' and password '{user_password}' does not exist.")
                
                    conn.send("User does not exist".encode(FORMAT))
            elif msg_data.get("execution") == 3:
                print(msg_data)
                email = msg_data.get("email")
                insert_query = "SELECT * FROM personal_informations WHERE email = %s;"
                mycursor.execute(insert_query, (email,))
                results = mycursor.fetchall()
 

                data_list = []  
                id_list = []

                for row in results:
                    data_dict = {
                        "id": row[0],
                        "first_name": row[2],
                        "last_name": row[3],
                        "gender": row[8],
                        "email": row[1],
                        "birthday": row[6],
                        "birthmonth": row[5],
                        "birthyear": row[7]
                    }
                    data_list.append(data_dict)

                req_query = f"select sender from friends where receiver = {data_list[0].get('id')} and friend_status = 0;"
                mycursor.execute(req_query)
                sender = mycursor.fetchall()


                full_name_list = []

                for row in sender:
                    sender_id_0 = row[0]
                    req_name_searcher = f"select full_name from personal_informations where num = {sender_id_0};"
                    mycursor.execute(req_name_searcher)
                    sender_name = mycursor.fetchall()
                    name_data = {
                        "full_name": sender_name[0][0]
                    }
                    full_name_list.append(name_data)
      

                for name_id in sender:
                    sender_id_dict = {
                        "sender_id": name_id[0]
                    }
                    id_list.append(sender_id_dict)

                user_id = results[0][0]
                friends_query = f"SELECT sender, receiver FROM friends WHERE friend_status = 1 AND (sender = '{user_id}' OR receiver = '{user_id}');"
                mycursor.execute(friends_query)
                friends = mycursor.fetchall()
                friend_ids = [friend[0] if friend[0] != user_id else friend[1] for friend in friends]
                friend_ids_str = ', '.join(map(str, friend_ids))

                search_fullnames = "SELECT num, full_name FROM personal_informations;"
                mycursor.execute(search_fullnames)
                full_names = mycursor.fetchall()
                friend_ids_set = set(friend_ids)

                filtered_full_names = [record for record in full_names if record[0] in friend_ids_set]

                friend_id_to_full_name_list = []
                for record in filtered_full_names:
                    friend_id_to_full_name = {
                        "id": record[0],
                        "full_name": record[1]
                    }
                    friend_id_to_full_name_list.append(friend_id_to_full_name)
                list_of_messeges_sent = []
                read_send_user = f"SELECT sender, receiver, messege, messege_date FROM chat WHERE sender = {data_list[0].get('id')};"
                mycursor.execute(read_send_user)
                info_0 = mycursor.fetchall()
                for row in info_0:
                    message_data = {
                        "sender": row[0],
                        "receiver": row[1],
                        "message": row[2],
                        "message_date": row[3].strftime('%Y-%m-%d %H:%M:%S')
                    }
                    list_of_messeges_sent.append(message_data)
               


 
                list_of_messeges_received = [] 
                read_send_user = f"SELECT sender, receiver, messege, messege_date FROM chat WHERE receiver = {data_list[0].get('id')};"
                mycursor.execute(read_send_user)
                info_1 = mycursor.fetchall()
                for row in info_1:
                    message_data = {
                        "sender": row[0],
                        "receiver": row[1],
                        "message": row[2],
                        "message_date": row[3].strftime('%Y-%m-%d %H:%M:%S')
                    }
                    list_of_messeges_received.append(message_data)

                dict_msg = {
                    "sent_messages": list_of_messeges_sent,
                    "received_messages": list_of_messeges_received
                }
                
                
                full_dict = {
                    "user_data": data_list,
                    "sender_id": id_list,
                    "sender_full_name": full_name_list,
                    "my_friends": friend_id_to_full_name_list,
                    "all_messages_i_am_mentioned": dict_msg
                }
                conn.send(json.dumps(full_dict).encode(FORMAT))
            elif msg_data.get("execution") == 4:
                searched_word = msg_data.get("person")
                insert_query = f"SELECT * FROM personal_informations WHERE full_name LIKE '%{searched_word}' OR full_name LIKE '{searched_word}%' OR full_name LIKE '%{searched_word}%'"
                mycursor.execute(insert_query)
                matching_rows = mycursor.fetchall() 
                data_list_2 = []
                
                for row in matching_rows:
                    data_dict_2 = {
                        "receiver_num":row[0],
                        "full_name": row[9]
                    }
                    data_list_2.append(data_dict_2)
                conn.send(json.dumps(data_list_2).encode(FORMAT))
            elif msg_data.get("execution") == 5:
                sender_id = msg_data.get("sender_id")
                receiver_id = msg_data.get("receiver_id")
                friendship_query = f"INSERT INTO friends (sender, receiver, friend_status) VALUES ({sender_id}, {receiver_id}, 0);"
                mycursor.execute(friendship_query)
                mydb.commit()
            elif msg_data.get("execution") == 6:
                sender_other = msg_data.get("sender_other")
                receiver_me = msg_data.get("receiver_me")
                add_friend_query = f"update friends set friend_status = 1 where sender = {sender_other} and receiver = {receiver_me};"
                mycursor.execute(add_friend_query)
                mydb.commit()
            elif msg_data.get("execution") == 7:
                msg_sender_id = msg_data.get("sender_id")
                msg_receiver_id = msg_data.get("receiver_id")
                messege = msg_data.get("messege")
                
                add_messege_query = f"insert into chat (sender, receiver, messege) values ({msg_sender_id}, {msg_receiver_id}, '{messege}');"
                mycursor.execute(add_messege_query)
                mydb.commit()
        except ConnectionResetError:
            connected = False
            print(f"[{addr}] Connection closed by the client.")
        except Exception as e:
            print(f"An error occurred: {e}")
    conn.close()
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
print("[STARTING] Server is starting...")
start()


