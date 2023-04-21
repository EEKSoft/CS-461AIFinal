from turtle import *
import random
from threading import Timer

#region Game States
def main():
    init()
    draw_screen()
    draw_player_choice()
    mainloop()


def player_chosen():
    global begun
    begun = True
    clear()
    penup()
    draw_grid()
    if player_shape != current_turn:
        Timer(1, ai_turn).start()


def end_game(result):
    clear()
    penup()
    draw_end_screen(result)
#endregion


#region Initialization
def init():
    global begun
    global player_shape
    global current_turn
    global current_state
    global grid_size
    global grid_half
    global grid_third
    global square_dict
    global inv_square_dict
    begun = False
    player_shape = None
    current_turn = "x"
    current_state = "nnnnnnnnn"
    grid_size = 600
    grid_half = grid_size / 2
    grid_third = grid_size / 3
    square_dict = {
        (-grid_third, grid_third): 1, (0, grid_third): 2, (grid_third, grid_third): 3,
        (-grid_third, 0): 4, (0, 0): 5, (grid_third, 0): 6,
        (-grid_third, -grid_third): 7, (0, -grid_third): 8, (grid_third, -grid_third): 9
    }
    inv_square_dict = {}
    for key, value in square_dict.items():
        inv_square_dict[value] = key
    turtle_init()


def turtle_init():
    hideturtle()
    speed('fastest')
    penup()
    onscreenclick(player_click)
    onkey(esc_pressed, "Escape")
    listen()
#endregion


#region Player Inputs
def player_click(x, y):
    global begun
    global player_shape
    nearest = min(square_dict, key=lambda c: distance(c, (x, y)))
    if begun: 
        if player_shape == current_turn and square_dict[nearest] in get_valid_moves(current_state):
            place(nearest[0], nearest[1])
    else:
        if(x < 0):
            player_shape = "x"
        else:
            player_shape = "o"
        player_chosen()


def esc_pressed():
    bye()
#endregion


#region Ai Stuff
def ai_turn():
    moves = get_valid_moves(current_state)
    if len(moves) == 0:
        return
    ai_decision(moves)


def ai_decision(moves):
    potential_moves = []
    for move in moves:
        value = {"move":move, "score":minimax(current_state, move, False)}
        potential_moves.append(value)
    if random.randrange(1, 10) == 1:
        chosen = random_input(moves)
    else:
        chosen = sorted(potential_moves, key=lambda b: b["score"], reverse=True)[0]["move"]
    place(inv_square_dict[chosen][0], inv_square_dict[chosen][1])


def minimax(state, move, maximizing):
    temp = str(state)
    turn = str(current_turn) if not maximizing else player_shape
    temp = update_state(temp, move, turn)
    result = check_conditions(temp)
    if result == None:
        scores = []
        next_moves = get_valid_moves(temp)
        for potential in next_moves:
            scores.append(minimax(temp, potential, not maximizing))
        best = max(scores) if maximizing else min(scores)
        return best
    else:
        if result == "Win":
            return -10
        elif result == "Loss":
            return 10
        else:
            return 0
        

def random_input(valid):
    cur_move = valid[random.randrange(0, len(valid) - 1)] if len(valid) > 1 else valid[0]
    return cur_move
#endregion


#region Drawing
def draw_screen():
    Screen().setup(grid_size, grid_size)
    Screen().cv._rootwindow.resizable(False,False)


def draw_player_choice():
    goto(0, grid_half)
    pendown()
    goto(0, -grid_half)
    penup()
    goto(-grid_half / 2, -42)
    write("X", align="center", font=("Arial", 64, "normal"))
    goto(grid_half / 2, -42)
    write("O", align="center", font=("Arial", 64, "normal"))


def draw_grid():
    points = [
        [-grid_half + grid_third, grid_half], 
        [-grid_half + grid_third, -grid_half], 
        [grid_half - grid_third, grid_half], 
        [grid_half - grid_third, -grid_half], 
        [-grid_half, -grid_half + grid_third], 
        [grid_half, -grid_half + grid_third], 
        [-grid_half, grid_half - grid_third], 
        [grid_half, grid_half - grid_third]
    ]

    for _ in range(4):
        i = _ * 2
        goto(points[i][0], points[i][1])
        pendown()
        goto(points[i + 1][0], points[i + 1][1])
        penup()


def draw_turn(position, side):
    goto(position)
    write(side, align="center", font=("Arial", 64, "normal"))


def draw_end_screen(result):
    if result == "Win":
        bgcolor("#9DF0C0")
    elif result == "Loss":
        bgcolor("#FF4646")
    else:
        bgcolor("#C6C6C6")
    goto(0, grid_half / 3)
    write(result, align="center", font=("Arial", 32, "normal"))
    goto(0, -grid_half / 3)
    write("Press 'ESC' to close!", align="center", font=("Arial", 32, "normal"))
#endregion


#region Helpers
def get_valid_moves(state):
    valid_moves = []
    temp = list(state)
    indx = 1
    for c in temp:
        if c == 'n':
             valid_moves.append(indx)
        indx += 1
    return valid_moves


def potential_next_states(state):
    valid_states = []
    side = "o" if state.count('x') > state.count('o') else "x"
    temp = list(state)
    count = 0
    for c in temp:
        if c == 'n':
            apnd = temp[:]
            apnd[count] = side
            valid_states.append("".join(apnd))
        count += 1
    return valid_states


def place(x, y):
    global current_turn
    global current_state
    prior = str(current_state)
    if current_turn == None:
        return
    draw_turn((x, y - 42), current_turn.upper())
    current_state = update_state(current_state, square_dict[(x, y)], current_turn)
    if current_turn == "x": 
        current_turn = "o"
    else: 
        current_turn = "x"
    result = check_conditions(current_state)
    if result != None:
        current_turn = None
        Timer(1, end_game, [result]).start()
        return
    if current_turn != player_shape: 
        Timer(1, ai_turn).start()


def check_conditions(state):
    global current_turn
    temp = list(state)
    for row in range(3):
        if temp[row * 3] == temp[row * 3 + 1] == temp[row * 3 + 2] != "n": 
            if temp[row * 3] == player_shape: 
                return "Win"
            else:
                return "Loss"
    for col in range(3):
        if temp[col] == temp[col + 3] == temp[col + 6] != "n":
            if temp[col] == player_shape: 
                return "Win"
            else:
                return "Loss"
    if (temp[0] == temp[4] == temp[8] != "n") or (temp[2] == temp[4] == temp[6] != "n"):
        if temp[4] == player_shape: 
            return "Win"
        else:
            return "Loss"
    if "n" not in state:
        return "Draw"


def update_state(state, move, side):
    temp = list(state)
    temp[move - 1] = side
    state = "".join(temp)
    return state


def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
#endregion


if __name__ == '__main__': main()
