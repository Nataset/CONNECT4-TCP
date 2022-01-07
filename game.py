import os

WIDTH = 7
HEIGHT = 6
PLAYER_ONE = 100
PLAYER_TWO = 200


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


def start_scene():
    welcomeText = '''
    #####################################################################################
    #####################################################################################
    

                                                                                ####
    ########  ########  #     #  #     #  ########  ########  ########         ## ##
    #         #      #  ##    #  ##    #  #         #            ##           ##  ##
    #         #      #  # #   #  # #   #  #         #            ##          ##   ##
    #         #      #  #  #  #  #  #  #  ######    #            ##         ##    ##
    #         #      #  #   # #  #   # #  #         #            ##        ##     ##
    #         #      #  #    ##  #    ##  #         #            ##       ##      ##
    ########  ########  #     #  #     #  ########  ########     ##      ###############
                                                                                  ##
                                                                                  ##

                    #*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*#
                    # A simple command line connect 4 game in Python. #
                    #*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*#                                                       

                                 Press Enter to Continue
                                =========================
                            
    #####################################################################################
    #####################################################################################
    '''

    clearConsole()
    input(welcomeText)


def init():
    global gamestate, current_player

    clearConsole()
    current_player = PLAYER_ONE
    gamestate = [[0 for x in range(WIDTH)] for y in range(HEIGHT)]


def d_print():
    for i in gamestate:
        print(i)


def insert_token(insert):
    insert = insert - 1
    y = 0

    if gamestate[0][insert] != 0:
        return False

    while True:
        if y >= HEIGHT - 1 or gamestate[y + 1][insert] != 0:
            gamestate[y][insert] = 1 if current_player == PLAYER_ONE else 2
            return True
        else:
            y += 1


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
            color = bcolors.OKCYAN
            color_end = bcolors.ENDC

        else:
            ch = ' '
            color = ''
            color_end = ''

        print('# ' + color + ch * 3 + bcolors.ENDC + ' #', end="")


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


def check_winner():
    check = 1 if current_player == PLAYER_ONE else 2
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


def display():
    print('    ##  1  ##  2  ##  3  ##  4  ##  5  ##  6  ##  7  ##\n    ###################################################')
    for x in range(HEIGHT):

        print(' ' * 4 + '#', end='')

        display_color_token(x)

        print('#\n'+' ' * 4 + '#', end='')

        display_color_token(x)

        print('#\n' + ' ' * 4 + '###################################################')


def update():
    global current_player
    while True:
        display()
        if (current_player == PLAYER_ONE):
            input_text = '\n' + ' ' * 15 + \
                '!---- PLAYER ONE TURN ----!\n    Please select number between 1-7 to insert token: '
        else:
            input_text = '\n' + ' ' * 15 + \
                '!---- PLAYER TWO TURN ----!\n    Please select number between 1-7 to insert token: '

        insert_index = input(input_text)

        if not check_input(insert_index):
            continue

        if not insert_token(int(insert_index)):
            clearConsole()
            print("!---- Fail to insert token ----!")
            continue

        if check_winner():
            clearConsole()
            display()
            if current_player == PLAYER_ONE:
                print('\n' + ' ' * 17 + '!---- PLAYER ONE WON ----!')
            else:
                print('\n' + ' ' * 17 + '!---- PLAYER TWO WON ----!')
            break

        clearConsole()
        current_player = PLAYER_TWO if current_player == PLAYER_ONE else PLAYER_ONE


def main():
    start_scene()
    init()
    update()


if __name__ == "__main__":
    main()
