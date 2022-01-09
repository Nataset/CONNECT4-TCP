import socket


PORT = 8080
HOSTNAME = 'localhost'
PLAYER_ONE = '100'
PLAYER_TWO = '200'

client_player = ''


def string_to_array(string):
    array = []
    tmp = string.split(';')
    for ele in tmp:
        tmp2 = ele.split('-')
        array.append(tmp2)
    print(array)


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOSTNAME, PORT))
while True:
    try:
        data = client_socket.recv(1024)
    except socket.error:
        break
    if not data:
        print(f"Connection Lost")
        break
    else:
        print(f"Recieved: " + data.decode())
        if data.decode() == 'Your are player ONE':
            client_player = PLAYER_ONE
            print("waiting for another player ...")
        elif data.decode() == 'Your are player TWO':
            client_player = PLAYER_ONE
        elif data.decode() == "start game":
            print('gamestart')
