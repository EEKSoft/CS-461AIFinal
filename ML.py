from turtle import *


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


#region Initialization
def init():
    global begun
    global player_shape
    global current_turn
    global start_state 
    global current_state
    global grid_size
    global grid_half
    global grid_third
    global square_dict
    begun = False
    player_shape = None
    current_turn = "x"
    start_state = "nnnnnnnnn"
    current_state = "nnnnnnnnn"
    grid_size = 600
    grid_half = grid_size / 2
    grid_third = grid_size / 3
    square_dict = {
        (-grid_third, grid_third): 1, (0, grid_third): 2, (grid_third, grid_third): 3,
        (-grid_third, 0): 4, (0, 0): 5, (grid_third, 0): 6,
        (-grid_third, -grid_third): 7, (0, -grid_third): 8, (grid_third, -grid_third): 9

    }
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
    if begun: 
        if player_shape == current_turn:
            player_place(x, y)
    else:
        if(x < 0):
            player_shape = "x"
        else:
            player_shape = "o"
        player_chosen()


def esc_pressed():
    bye()


def player_place(x, y):
    print(x, y)
    nearest = min(square_dict, key=lambda c: distance(c, (x, y)))
    print(nearest)
#endregion


#region Initialization Drawing
def draw_screen():
    Screen().setup(grid_size, grid_size)


def draw_player_choice():
    goto(0, grid_half)
    pendown()
    goto(0, -grid_half)
    penup()
    goto(-grid_half / 2, 0)
    write("X", align="center", font=("Arial", 64, "normal"))
    goto(grid_half / 2, 0)
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
#endregion


#region Helpers
def get_valid_states(state, side):
    valid_states = []
    temp = list(state)
    count = 0
    for c in temp:
        if c == 'n':
            apnd = temp[:]
            apnd[count] = side
            valid_states.append("".join(apnd))
        count += 1
    return valid_states


def state_to_dict(state):
    state_dict = {}
    state_list = list(state)
    for _ in range(9):
        state_dict[_ + 1] = "".join(state_list[_])
    return state_dict    
    

def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
#endregion

if __name__ == '__main__': main()