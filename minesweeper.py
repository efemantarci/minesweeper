#minesweeper
import random
import tkinter
import time
WIDTH = 9
HEIGHT = 9
unopened = WIDTH * HEIGHT
BOMB_COUNT = 10
UNKNOWN = " "
BOMB = "#"
seed = 124
finished = False
first_press = True
#Initialize arrays
bomb_grid = [[0 for i in range(WIDTH)] for i in range(HEIGHT)]
visited = [[False for i in range(WIDTH)] for i in range(HEIGHT)]
table = [[None for i in range(WIDTH)] for i in range(HEIGHT)]
player = [[None for i in range(WIDTH)] for i in range(HEIGHT)]
delta = [[1,-1],[1,0],[1,1],
         [0,-1],      [0,1],
         [-1,-1],[-1,0],[-1,1],
        ]
buttons = [[None for i in range(WIDTH)] for i in range(HEIGHT)]

labels = [] #0 : minecount 1 : timecount 2: seed
bombs = 0
seconds = 0
root = tkinter.Tk()
seed_entry = tkinter.Entry()
seed_entry.grid(row=0,column=0)
seed_entry.insert(0,"Enter seed...")

def main():
    prepare_bombs()
    #Draw the array
    draw(bomb_grid)
    #Table'ı tamamla
    initialize_table()
    root.title("Minesweeper")
    info_frame = tkinter.Frame(root)
    main_frame = tkinter.Frame(root)
    info_frame.pack()
    main_frame.pack()
    mine_count = tkinter.Label(info_frame,text = f"Bombs left : {bombs}")
    time_count = tkinter.Label(info_frame,text = f"Time : {seconds}")
    seed_label = tkinter.Label(info_frame,text = f"Seed : {seed}")
    labels.append(mine_count)
    labels.append(time_count)
    labels.append(seed_label)
    mine_count.grid(row = 0,column = 0)
    time_count.grid(row = 0,column = 1)
    seed_label.grid(row = 0,column = 2)
    for y in range(HEIGHT):
            for x in range(WIDTH):
                button = tkinter.Button(main_frame,text = UNKNOWN,image=images[11])
                button.grid(row = y,column = x)
                buttons[y][x] = button
                button.bind("<Button-1>",left_click)
                button.bind("<Button-2>",right_click)
                button.bind("<Button-3>",right_click)
    update_clock()

def seed_onclick():
    global seed
    seed = int(seed_entry.get())
    random.seed(seed)
    hide_buttons()
    main()
seed_entry.bind("<Button-1>", lambda e: seed_entry.delete(0, tkinter.END))
seed_button = tkinter.Button(text = "Start",command=seed_onclick)
seed_button.grid(row=0,column=1)
def hide_buttons():
    seed_entry.grid_forget()
    seed_button.grid_forget()
#To avoid no root window error I initialize it here
images = [None for i in range(13)]
# 0 to 8 numbers 9 bomb 10 flag 11 unknown 12 bomb pressed
for i in range(13):
    images[i] = tkinter.PhotoImage(file=f"images/{i}.png")

def clear():
    for y in range(HEIGHT):
        for x in range(WIDTH):
            buttons[y][x].configure(text = UNKNOWN)
        
def open(y,x):
    global first_press
    if(visited[y][x]):
        return
    #Nedense global yapmam lazım
    global unopened
    unopened -= 1
    visited[y][x] = True
    player[y][x] = True
    # Resim koyma kodunu iki kez kullanıyorum sonra düzelticem
    if(bomb_grid[y][x] == 1):
        if not first_press:
            buttons[y][x].configure(text=table[y][x],image=images[12])
            print("Patladın mal")
            finish()
        else:
            prepare_bombs()
            first_press = False
            #Draw the array
            draw(bomb_grid)
            #Table'ı tamamla
            initialize_table()
            clear()
            visited[y][x] = False
            open(y,x)
    else:
        buttons[y][x].configure(text=table[y][x],image=images[table[y][x]])
        if table[y][x] == 0:
            for item in delta:
                dy = y + item[0]
                dx = x + item[1]
                if 0 <= dy < HEIGHT and 0 <= dx < WIDTH:
                    open(dy,dx)
    #oyun bitirme
    if unopened - bombs <= 0 and bombs == 0:
            finish()
    first_press = False
def finish():
    for y in range(HEIGHT):
        for x in range(WIDTH):
            buttons[y][x].configure(state=tkinter.DISABLED)
            buttons[y][x].unbind("<Button-1>")
            buttons[y][x].unbind("<Button-2>")
            buttons[y][x].unbind("<Button-3>")
    global finished
    finished = True

def update_clock():
    global seconds
    labels[1].configure(text = f"Time : {seconds}")
    seconds += 1
    if not finished:
        root.after(1000,update_clock)
def initialize_table():
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if bomb_grid[y][x] == 1:
                table[y][x] = BOMB
            else:
                bombcount = 0
                for item in delta:
                    dy = y + item[0]
                    dx = x + item[1]
                    if 0 <= dy < HEIGHT and 0 <= dx < WIDTH:
                        if bomb_grid[dy][dx] == 1:
                            bombcount += 1
                table[y][x] = bombcount
def draw(table):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            print(table[y][x],end = " ")
        print()

def havalı_check(y,x):
    bomb_count = 0
    for item in delta:
        dy = y + item[0]
        dx = x + item[1]
        if 0 <= dy < HEIGHT and 0 <= dx < WIDTH:
            if buttons[dy][dx]["text"] == BOMB:
                bomb_count += 1
    if bomb_count == table[y][x]:
        for item in delta:
            dy = y + item[0]
            dx = x + item[1]
            if 0 <= dy < HEIGHT and 0 <= dx < WIDTH:
                open(dy,dx)

def prepare_bombs():
    global bombs
    bombs = 0
    #Initialize the array
    for y in range(HEIGHT):
        for x in range(WIDTH):
            bomb_grid[y][x] = 0
    #Place the bombs
    while(bombs < BOMB_COUNT):
        y = random.randint(0,HEIGHT - 1)
        x = random.randint(0,WIDTH - 1)
        if(bomb_grid[y][x] == 1):
            continue
        bombs += 1
        bomb_grid[y][x] = 1

def left_click(event):
    button = event.widget
    col = button.grid_info()["column"]
    row = button.grid_info()["row"]
    print(f"col : {col} row : {row}")
    #oyun bitirme
    if unopened - bombs <= 0 and bombs == 0:
        finish()
    if visited[row][col]:
        havalı_check(row,col)
    else:
        open(row,col)
    first_press = False

def right_click(event):
    button = event.widget
    col = button.grid_info()["column"]
    row = button.grid_info()["row"]
    print(f"col : {col} row : {row}")
    global unopened
    global bombs
    if not visited[row][col]:
        button.configure(text = BOMB,image=images[10])
        unopened -= 1
        bombs -= 1
        labels[0].configure(text = f"Bombs left : {bombs}")
        #oyun bitirme
        if unopened - bombs <= 0 and bombs >= 0:
            finish()
        visited[row][col] = True
    elif button["text"] == BOMB:
        button.configure(text = UNKNOWN,image=images[0])
        unopened += 1
        bombs += 1
        labels[0].configure(text = f"Bombs left : {bombs}")
        visited[row][col] = False


root.mainloop()

