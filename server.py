import socket

TCP_IP = '0.0.0.0'
TCP_PORT = 5005

P1 = 'X'
P2 = 'O'
EMPTY = '-'
allowed = [P1, P2, EMPTY]
INITIAL_BOARD = EMPTY * 9

BUFFER_SIZE = len(INITIAL_BOARD) + 1


def check_valid(prev_state, cur_state, symbol) -> bool:
    if len(cur_state) < 9:
        print("Length: {:d}".format(len(cur_state)))
        return False
    matching = 0
    for i in range(0, 9):
        if prev_state[i] == cur_state[i]:
            matching += 1
            # print("{:s} == {:s} at {:d}".format(prev_state[i], cur_state[i], i))
            continue
        # else:
        # print("!!!{:s} != {:s} at {:d}".format(prev_state[i], cur_state[i], i))
        if prev_state[i] != EMPTY:
            print("{:s} was not empty at {:d}".format(prev_state[i], i))
            return False
        if cur_state[i] != symbol:
            print("{:s} is not allowed symbol {:s} at {:d}".format(cur_state[i], symbol, i))
            return False

    return matching == 8


def end(winner: int):
    print("Player {:d} has won the game!".format(winner + 1))
    players[winner].send("You have won!".encode('utf-8'))
    loser = (winner + 1) % 2
    players[loser].send("You have lost!".encode('utf-8'))


def check_win(msg: str, symbol: str) -> bool:
    win_combinations = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]
    for combo in win_combinations:
        matching_count = 0
        for pos in combo:
            if msg[pos] == symbol:
                matching_count += 1
            else:
                break
        if matching_count == 3:
            return True
    return False


def print_board():
    row = ''
    for i in range(0, 9):
        row += msg[i] + ' '
        if i % 3 == 2:
            print(row)
            row = ''


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

while 1:
    print("============================\nNew Game")
    state = INITIAL_BOARD

    conn1, addr1 = s.accept()
    print('Connection address 1:', addr1)
    conn2, addr2 = s.accept()
    print('Connection address 2:', addr2)

    players = [conn1, conn2]
    actual = 0
    players[actual].send(state.encode('utf-8'))
    while 1:
        next = (actual + 1) % 2
        msg = players[actual].recv(BUFFER_SIZE).decode('utf-8')
        if not msg:
            end(next)
            break
        if not check_valid(state, msg, allowed[actual]):
            print("received from player {:d}: {:s}".format(actual + 1, msg))
            end(next)
            break
        print("Player {:d}:".format(actual + 1))
        print_board()

        if check_win(msg, allowed[actual]):
            end(actual)
            break

        state = msg
        players[next].send(state.encode('utf-8'))
        actual = (actual + 1) % 2
    conn1.close()
    conn2.close()
