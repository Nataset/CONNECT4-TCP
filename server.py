import socket
import threading

PORT = 8080
HOSTNAME = 'localhost'
WIDTH = 7
HEIGHT = 6
PLAYER_ONE = '100'
PLAYER_TWO = '200'
MAX_CLIENTS = 2

game_turn = 0
player_turn = PLAYER_ONE
player_count = 0
players = {
    PLAYER_ONE: {
        'socket': '',
        'address': '',
        'lastmove': '',
    }, PLAYER_TWO: {
        'socket': '',
        'address': '',
        'lastmove': '',
    }}


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
    print(f"Connection from {address}, assign as player ONE")
    socket.send("Your are player ONE".encode())


def playertwo_join_handle(socket, address):
    global game_turn
    print(f"Connection from {address}, assign as player TWO")
    socket.send("Your are player TWO".encode())
    players[PLAYER_ONE]['socket'].send("start game".encode())
    players[PLAYER_TWO]['socket'].send("start game".encode())
    game_turn += 1
    send_TCP(PLAYER_ONE, '301')
    send_TCP(PLAYER_TWO, '301')


def player_one_req_handle():
    global player_count
    while True:
        data = players[PLAYER_ONE]['socket'].recv(2048)
        if not data:
            print(f'lost connection from {PLAYER_ONE}')
            player_count -= 1
            break
        else:
            data = parse_req(data.decode())
            if data[0][1] == '200':
                print("Player ONE Receive Data")
            elif data[0][1] == '401':
                tmp = data[1][0].split(":")
                print(tmp)


def player_two_req_handle():
    global player_count
    while True:
        data = players[PLAYER_TWO]['socket'].recv(2048)
        if not data:
            print(f'lost connection from {PLAYER_TWO}')
            player_count -= 1
            break
        else:
            data = parse_req(data.decode())
            if data[0][1] == '200':
                print("Player TWO Receive Data")


def client_handle(client_socket, address):
    global players, player_count
    if player_count >= MAX_CLIENTS:
        max_clients_handle(client_socket)
    elif player_count == 0:
        player_count += 1
        players[PLAYER_ONE]['socket'] = client_socket
        players[PLAYER_ONE]['address'] = address
        playerone_join_handle(client_socket, address)
        player_one_req_handle()

    elif player_count == 1:
        player_count += 1
        players[PLAYER_TWO]['socket'] = client_socket
        players[PLAYER_TWO]['address'] = address
        playertwo_join_handle(client_socket, address)
        player_two_req_handle()


def send_TCP(player_no, status_code):

    if status_code == '200':
        data = "TNP/1.0 200 OK!_server"

    elif status_code == '201':
        data = "TNP/1.0 201 OK!_Player_ONE"

    elif status_code == '202':
        data = "TNP/1.0 202 OK!_Player_TWO"

    elif status_code == '300':
        data = "TNP/1.0 300 Start_Game"

    elif status_code == '301':
        data = f"TNP/1.0 301 Update_Game_State\nGAME_TURN:{str(game_turn)} PLAYER_TURN:{player_turn}\n{array_to_string(gamestate)}"

    elif status_code == '401':
        data = f"TNP/1.0 401 Player_ONE_move\nMOVE:{players[PLAYER_ONE]['lastmove']}"

    elif status_code == '401':
        data = f"TNP/1.0 401 Player_TWO_move\nMOVE:{players[PLAYER_TWO]['lastmove']}"

    elif status_code == '500':
        data = f"TNP/1.0 500 UNKNOWN_ERROR"

    elif status_code == '501':
        data = f"TNP/1.0 501 Player_ONE_disconnect"

    elif status_code == '502':
        data = f"TNP/1.0 501 Player_TWO_disconnect"

    players[player_no]['socket'].send(data.encode())


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
