# Nataset Tanabodee 6210402411
# Nattapol Kumsang 6210406556

import socket
import threading

PORT = 8080
HOSTNAME = 'localhost'
WIDTH = 7
HEIGHT = 6
PLAYER_ONE = '100'
PLAYER_TWO = '200'
MAX_CLIENTS = 2

shut_down_flag = False
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


def reset():
    global game_turn, player_turn, player_count, players, gamestate, shut_down_flag
    game_turn = 0
    player_turn = PLAYER_ONE
    player_count = 0
    shut_down_flag = False
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
    gamestate = [[0 for x in range(WIDTH)] for y in range(HEIGHT)]


def check_winner(player_on):
    if player_on == PLAYER_ONE:
        check = 1
    elif player_on == PLAYER_TWO:
        check = 2

    for y in range(HEIGHT):
        for x in range(WIDTH - 3):
            if(gamestate[y][x] == check and gamestate[y][x + 1] == check and gamestate[y][x + 2] == check and gamestate[y][x + 3] == check):
                return True

    for x in range(WIDTH):
        for y in range(HEIGHT - 3):
            if(gamestate[y][x] == check and gamestate[y + 1][x] == check and gamestate[y + 2][x] == check and gamestate[y + 3][x] == check):
                return True

    for x in range(WIDTH - 3):
        for y in range(HEIGHT - 3):
            if(gamestate[y][x] == check and gamestate[y + 1][x + 1] == check and gamestate[y + 2][x + 2] == check and gamestate[y + 3][x + 3] == check):
                return True

    for x in range(WIDTH - 3):
        for y in range(HEIGHT):
            if(gamestate[y][x] == check and gamestate[y - 1][x + 1] == check and gamestate[y - 2][x + 2] == check and gamestate[y - 3][x + 3] == check):
                return True

    return False


def insert_token(insert):
    global gamestate
    insert = insert - 1
    y = 0

    if gamestate[0][insert] != 0:
        return False

    while True:
        if y >= HEIGHT - 1 or gamestate[y + 1][insert] != 0:
            gamestate[y][insert] = 1 if player_turn == PLAYER_ONE else 2
            return True
        else:
            y += 1


def conn_handle():
    print('SERVER IS UP')
    while True:
        client_socket, address = server_socket.accept()

        threading.Thread(target=client_handle, args=[
                         client_socket, address]).start()


def client_handle(client_socket, address):
    global players, player_count, shut_down_flag
    if player_count >= MAX_CLIENTS:
        max_clients_handle(client_socket)
        return
    elif player_count == 0:
        shut_down_flag = False
        reset()
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
    player_count = 0
    return


def max_clients_handle(socket):
    print("Maximun number of clients reached")
    socket.send("Maximun number of clients reached".encode())
    socket.close()


def playerone_join_handle(socket, address):
    print(f"Connection from {address}, assign as player ONE")
    send_TCP(PLAYER_ONE, '201')


def playertwo_join_handle(socket, address):
    global game_turn
    print(f"Connection from {address}, assign as player TWO")
    send_TCP(PLAYER_TWO, '202')
    game_turn += 1
    send_TCP(PLAYER_ONE, '301')
    send_TCP(PLAYER_TWO, '301')


def player_one_req_handle():
    global player_count, player_turn, game_turn, shut_down_flag
    print("player_ONE_Thread starting")
    while True:
        if shut_down_flag == True:
            print("player_ONE_Thread is shut down")
            return
        data = players[PLAYER_ONE]['socket'].recv(2048)
        if not data:
            print(f'Lost Connection From {PLAYER_ONE}')
            shut_down_flag = True
            send_TCP(PLAYER_TWO, '501')
            print("player_ONE_Thread is shut down")
            return
        else:
            data = parse_req(data.decode())
            if data[0][1] == '200':
                print("Player ONE Receive Data")
            elif data[0][1] == '401':
                tmp = data[1][0].split(":")
                lastmove = int(tmp[1])
                players[PLAYER_ONE]['lastmove'] = lastmove
                insert_token(lastmove)
                game_turn += 1
                player_turn = PLAYER_TWO
                if check_winner(PLAYER_ONE):
                    print("PLAYER_ONE WIN!!!")
                    send_TCP(PLAYER_ONE, '302')
                    send_TCP(PLAYER_TWO, '302')
                    shut_down_flag = True
                    print("player_ONE_Thread is shut down")
                    return
                else:
                    send_TCP(PLAYER_ONE, '301')
                    send_TCP(PLAYER_TWO, '301')


def player_two_req_handle():
    global player_count, player_turn, game_turn, shut_down_flag
    print("player_TWO_Thread starting")
    while True:
        if shut_down_flag == True:
            print("player_TWO_Thread is shut down")
            return
        data = players[PLAYER_TWO]['socket'].recv(2048)
        if not data:
            print(f'lost connection from {PLAYER_TWO}')
            shut_down_flag = True
            send_TCP(PLAYER_ONE, '502')
            print("player_TWO_Thread is shut down")
            return
        else:
            data = parse_req(data.decode())
            if data[0][1] == '200':
                print("Player TWO Receive Data")
            elif data[0][1] == '402':
                tmp = data[1][0].split(":")
                lastmove = int(tmp[1])
                players[PLAYER_TWO]['lastmove'] = lastmove
                insert_token(lastmove)
                game_turn += 1
                player_turn = PLAYER_ONE
                if check_winner(PLAYER_TWO):
                    print("PLAYER_TWO WIN!!!")
                    send_TCP(PLAYER_ONE, '302')
                    send_TCP(PLAYER_TWO, '302')
                    shut_down_flag = True
                    print("player_TWO_Thread is shut down")
                    return
                else:
                    send_TCP(PLAYER_ONE, '301')
                    send_TCP(PLAYER_TWO, '301')


def send_TCP(player_no, status_code):

    if status_code == '201':
        data = "TNP/1.0 201 OK!_Player_ONE"

    elif status_code == '202':
        data = "TNP/1.0 202 OK!_Player_TWO"

    elif status_code == '301':
        data = f"TNP/1.0 301 Update_Game_State\nGAME_TURN:{str(game_turn)} PLAYER_TURN:{player_turn}\n{array_to_string(gamestate)}"

    elif status_code == '302':
        if player_turn == PLAYER_ONE:
            winner = PLAYER_TWO
        elif player_turn == PLAYER_TWO:
            winner = PLAYER_ONE

        data = f"TNP/1.0 302 Game_End\nGAME_TURN:{str(game_turn)} WINNER:{winner}\n{array_to_string(gamestate)}"

    # elif status_code == '401':
    #     data = f"TNP/1.0 401 Player_ONE_move\nMOVE:{players[PLAYER_ONE]['lastmove']}"

    # elif status_code == '402':
    #     data = f"TNP/1.0 402 Player_TWO_move\nMOVE:{players[PLAYER_TWO]['lastmove']}"

    elif status_code == '501':
        data = f"TNP/1.0 501 Player_ONE_disconnect"

    elif status_code == '502':
        data = f"TNP/1.0 502 Player_TWO_disconnect"

    tmp = data.split('\n')
    log = tmp[0]
    print(f'Sending: {log} TO {player_no}')
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
    print(f"Receive: {tmp[0]}")
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
