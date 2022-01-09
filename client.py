import socket
import os

from game import check_winner


PORT = 8080
HOSTNAME = 'localhost'
WIDTH = 7
HEIGHT = 6
PLAYER_ONE = '100'
PLAYER_TWO = '200'

client_player = ''
lastmove = ''
gamestate = ''


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)


def display_color_token(x):
    for y in range(WIDTH):
        ch = ' '
        color = ''
        color_end = ''
        if gamestate[x][y] == 1:
            ch = 'X'
            color = bcolors.FAIL
            color_end = bcolors.ENDC

        elif gamestate[x][y] == 2:
            ch = 'O'
            color = bcolors.WARNING
            color_end = bcolors.ENDC

        else:
            ch = ' '
            color = ''
            color_end = ''

        print('# ' + color + ch * 3 + bcolors.ENDC + ' #', end="")


def display():
    print('    ##  1  ##  2  ##  3  ##  4  ##  5  ##  6  ##  7  ##\n    ###################################################')
    for x in range(HEIGHT):

        print(' ' * 4 + '#', end='')

        display_color_token(x)

        print('#\n'+' ' * 4 + '#', end='')

        display_color_token(x)

        print('#\n' + ' ' * 4 + '###################################################')


def string_to_array(string):
    array = []
    tmp = string.split(';')
    for ele in tmp:
        tmp2 = ele.split('-')
        for i in range(len(tmp2)):
            tmp2[i] = int(tmp2[i])
        array.append(tmp2)
    return array


def insert_token(insert):
    insert = insert - 1
    y = 0

    if gamestate[0][insert] != 0:
        clearConsole()
        text = '''
  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  !------- Fail to insert token please try again -------!
  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                                '''
        print(text)
        return False

    while True:
        if y >= HEIGHT - 1 or gamestate[y + 1][insert] != 0:
            gamestate[y][insert] = 1 if client_player == PLAYER_ONE else 2
            return True
        else:
            y += 1


def check_input(game_input):
    try:
        val = int(game_input)
    except ValueError:
        clearConsole()
        text = '''
  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  !---------------- Please Enter Number ----------------!
  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
        '''
        print(text)
        return False

    game_input = int(game_input)

    if (game_input < 1 or game_input > 7):
        clearConsole()
        text = '''
  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  !--- Wrong number, Please Enter number between 1-7 ---!
  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        '''
        print(text)
        return False

    return True


def parse_req(message):
    data = []
    tmp = message.split('\n')
    for i in range(len(tmp)):
        ele = tmp[i].split(' ')
        data.append(ele)
    return data


def send_TCP(status_code):
    print(status_code == '400', client_player == PLAYER_ONE)
    if status_code == '200':
        data = "TNP/1.0 200 OK!_server"

    elif status_code == '201':
        data = "TNP/1.0 201 OK!_Player_ONE"

    elif status_code == '202':
        data = "TNP/1.0 202 OK!_Player_TWO"

    elif status_code == '300':
        data = "TNP/1.0 300 Start_Game"

    elif status_code == '400' and client_player == PLAYER_ONE:
        data = f"TNP/1.0 401 Player_ONE_move\nMOVE:{lastmove}"

    elif status_code == '400' and client_player == PLAYER_TWO:
        data = f"TNP/1.0 401 Player_TWO_move\nMOVE:{lastmove}"

    elif status_code == '500':
        data = f"TNP/1.0 500 UNKNOWN_ERROR"

    elif status_code == '501':
        data = f"TNP/1.0 501 Player_ONE_disconnect"

    elif status_code == '502':
        data = f"TNP/1.0 501 Player_TWO_disconnect"

    client_socket.send(data.encode())


def main():
    global gamestate, client_socket, lastmove, client_player

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOSTNAME, PORT))

    while True:
        try:
            data = client_socket.recv(2048)
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
                client_player = PLAYER_TWO
            elif data.decode() == "start game":
                send_TCP('200')
            else:
                data = parse_req(data.decode())
                if data[0][1] == '301':
                    clearConsole()
                    gamestate = string_to_array(data[2][0])
                    display()
                    tmp = data[1][1].split(':')
                    player_turn = tmp[1]
                    if client_player == player_turn:
                        while True:
                            input_text = '\n' + ' ' * 18 + \
                                '!---- YOUR TURN ----!\n    Please select number between 1-7 to insert token: '
                            insert_index = input(input_text)
                            if not check_input(insert_index) or not insert_token(int(insert_index)):
                                display()
                                continue

                            lastmove = insert_index
                            break
                        send_TCP('400')
                    else:
                        output_text = '\n' + ' ' * 15 + \
                            '!---- OPPONENT TURN ----!'
                        print(output_text)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
