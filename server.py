import socket
import threading

PORT = 8085
HOSTNAME = 'localhost'
WIDTH = 7
HEIGHT = 6
PLAYER_ONE = '100'
PLAYER_TWO = '200'
MAX_CLIENTS = 2

game_turn = 0
player_count = 0
players = {PLAYER_ONE: '', PLAYER_TWO: ''}


def init():
    global server_socket, gamestate

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOSTNAME, PORT))
    server_socket.listen(5)

    gamestate = [[0 for x in range(WIDTH)] for y in range(HEIGHT)]


def conn_handle():
    while True:
        client_socket, address = server_socket.accept()

        threading.Thread(target=client_handle, args=[
                         client_socket, address]).start()


def max_clients_handle(socket):
    print("Maximun number of clients reached")
    socket.send("Maximun number of clients reached".encode())
    socket.close()


def playerone_join_handle(socket, address):
    print(f"Connection from {address}, assign to player ONE")
    socket.send("Your are player ONE".encode())


def playertwo_join_handle(socket, address):
    print(f"Connection from {address}, assign to player TWO")
    socket.send("Your are player TWO".encode())
    players[0]['socket'].send("start game".encode())
    players[1]['socket'].send("start game".encode())


def client_handle(client_socket, address):
    global players, player_count
    if player_count >= MAX_CLIENTS:
        max_clients_handle(client_socket)
    elif player_count == 0:
        player_count += 1
        players[PLAYER_ONE] = {"socket": socket, "address": address}
        playerone_join_handle(client_socket, address)
        player_req_handle(PLAYER_ONE)

    elif player_count == 1:
        player_count += 1
        players[PLAYER_TWO] = {"socket": client_socket, "address": address}
        playertwo_join_handle(client_socket, address)
        player_req_handle(PLAYER_TWO)


def player_req_handle(player_no):
    if player_no == PLAYER_ONE:
        myplayer = PLAYER_TWO
        player_socket = players[PLAYER_ONE]['socket']
        enamy_socket = players[PLAYER_TWO]['socket']

    elif player_no == PLAYER_TWO:
        myplayer = PLAYER_TWO
        player_socket = players[PLAYER_TWO]['socket']
        enamy_socket = players[PLAYER_ONE]['socket']

    while True:
        data = player_socket.recv(2048)
        if not data:
            print(f'lost connection from {myplayer}')
            break


def send_TCP(player_no, status_code):
    if status_code == '201':
        data = "TNP/1.0 201 OK!_Player_ONE"

    elif status_code == '202':
        data = "TNP/1.0 202 OK!_Player_TWO"

    elif status_code == '300':
        data = "TNP/1.0 300 Start_Game"

    elif status_code == '301':
        data = f"TNP/1.0 301 Update_Game_State\nTURN:{str(game_turn)} PLAYER_TURN:{PLAYER_ONE}\n{array_to_string(gamestate)}"

    players[player_no].send(data.encode())


def array_to_string(array):
    string = []
    for n in array:
        string_ints = [str(int) for int in n]
        s = '-'
        s = s.join(string_ints)
        string.append(s)
    s = ';'
    string = s.join(string)
    return string


def parse_req(message):
    data = []
    tmp = message.split('\n')
    for i in range(len(tmp)):
        ele = tmp[i].split(' ')
        data.append(ele)
    return data


def main():
    init()
    conn_handle()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
