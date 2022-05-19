#minesweeper
import random
import tkinter
import time

class Minesweeper:
    def __init__(self,width,height,bomb_count,seed):
        self.width = width
        self.height = height
        self.bomb_count = bomb_count
        self.seed = seed
        self.unopened = width * height
        self.finished = False
        self.first_press = True
        #İlk başta text-based di oradan kaldı
        #Bunlara sonra dokunurum
        self.UNKNOWN = " "
        self.BOMB = "#"
        #Arrayleri baslat
        self.bomb_grid = [[0 for i in range(self.width)] for i in range(self.height)]
        self.visited = [[False for i in range(self.width)] for i in range(self.height)]
        self.table = [[None for i in range(self.width)] for i in range(self.height)]
        self.delta = [[1,-1],[1,0],[1,1],
                 [0,-1],      [0,1],
                 [-1,-1],[-1,0],[-1,1],
                ]
        self.buttons = [[None for i in range(self.width)] for i in range(self.height)]
        self.labels = [] #0 : minecount 1 : timecount 2: seed
        self.seconds = 0
        self.root = tkinter.Tk()
        #13 tane ile başlatıyorum hardcodeladık biraz
        self.images = [None for i in range(14)]
        # 0 dan 8 numara 9 mayın 10 bayrak 11 unknown 12 bomb pressed 13 wrong_flag
        #13 tane şu an
        for i in range(14):
            self.images[i] = tkinter.PhotoImage(file=f"images/{i}.png")
        self.seed_entry = tkinter.Entry()
        self.seed_entry.grid(row=0,column=0)
        self.seed_entry.insert(0,"Enter seed...")
            
        self.seed_entry.bind("<Button-1>", lambda e: self.seed_entry.delete(0, tkinter.END))
        self.seed_button = tkinter.Button(text = "Start",command=self.seed_onclick)
        self.seed_button.grid(row=0,column=1)

        self.root.mainloop()

    def seed_onclick(self):
            seed = int(self.seed_entry.get())
            random.seed(seed)
            self.seed = seed
            self.hide_buttons()
            self.main()

    def hide_buttons(self):
        self.seed_entry.grid_forget()
        self.seed_button.grid_forget()
        
    def prepare_bombs(self):
        self.bombs = 0
        #Initialize the array
        for y in range(self.height):
            for x in range(self.width):
                self.bomb_grid[y][x] = 0
        #Place the bombs
        while(self.bombs < self.bomb_count):
            y = random.randint(0,self.height - 1)
            x = random.randint(0,self.height - 1)
            if(self.bomb_grid[y][x] == 1):
                continue
            self.bombs += 1
            self.bomb_grid[y][x] = 1
    def draw(self,table):
        for y in range(self.height):
            for x in range(self.width):
                print(table[y][x],end = " ")
            print()

    def initialize_table(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.bomb_grid[y][x] == 1:
                    self.table[y][x] = self.BOMB
                else:
                    self.bombcount = 0
                    for item in self.delta:
                        dy = y + item[0]
                        dx = x + item[1]
                        if 0 <= dy < self.height and 0 <= dx < self.width:
                            if self.bomb_grid[dy][dx] == 1:
                                self.bombcount += 1
                    self.table[y][x] = self.bombcount

    def left_click(self,event):
        button = event.widget
        col = button.grid_info()["column"]
        row = button.grid_info()["row"]
        print(f"col : {col} row : {row}")
        #oyun bitirme
        if self.unopened - self.bombs <= 0 and self.bombs >= 0:
            self.finish()
        if self.visited[row][col]:
            self.havalı_check(row,col)
        else:
            self.open(row,col)
        self.first_press = False

    def right_click(self,event):
        button = event.widget
        col = button.grid_info()["column"]
        row = button.grid_info()["row"]
        print(f"col : {col} row : {row}")
        if not self.visited[row][col]:
            button.configure(text = self.BOMB,image=self.images[10])
            self.unopened -= 1
            self.bombs -= 1
            self.labels[0].configure(text = f"Bombs left : {self.bombs}")
            #oyun bitirme
            if self.unopened - self.bombs <= 0 and self.bombs >= 0:
                self.finish()
            self.visited[row][col] = True
        elif button["text"] == self.BOMB:
            button.configure(text = self.UNKNOWN,image=self.images[0])
            self.unopened += 1
            self.bombs += 1
            self.labels[0].configure(text = f"Bombs left : {self.bombs}")
            self.visited[row][col] = False

    def update_clock(self):
        self.labels[1].configure(text = f"Time : {self.seconds}")
        self.seconds += 1
        if not self.finished:
            #Sonsuz döngü
            self.root.after(1000,self.update_clock)

    def clear(self):
        for y in range(self.height):
            for x in range(self.width):
                self.buttons[y][x].configure(text = UNKNOWN)

    def finish(self):
        for y in range(self.height):
            for x in range(self.width):
                #Yanlış flag varsa
                if self.buttons[y][x]["text"] == self.BOMB and not self.bomb_grid[y][x]:
                    self.buttons[y][x].configure(image=self.images[13])
                self.buttons[y][x].configure(state=tkinter.DISABLED)
                self.buttons[y][x].unbind("<Button-1>")
                self.buttons[y][x].unbind("<Button-2>")
                self.buttons[y][x].unbind("<Button-3>")
        self.finished = True

    def havalı_check(self,y,x):
        bomb_count = 0
        for item in self.delta:
            dy = y + item[0]
            dx = x + item[1]
            if 0 <= dy < self.height and 0 <= dx < self.width:
                if self.buttons[dy][dx]["text"] == self.BOMB:
                    bomb_count += 1
        if bomb_count == self.table[y][x]:
            for item in self.delta:
                dy = y + item[0]
                dx = x + item[1]
                if 0 <= dy < self.height and 0 <= dx < self.width:
                    self.open(dy,dx)

    def open(self,y,x):
        #DFS?
        if(self.visited[y][x]):
            return
        self.unopened -= 1
        self.visited[y][x] = True
        # Resim koyma kodunu iki kez kullanıyorum sonra düzelticem
        if(self.bomb_grid[y][x] == 1):
            if not self.first_press:
                self.buttons[y][x].configure(text=self.table[y][x],image=self.images[12])
                print("Patladın mal")
                self.finish()
            else:
                self.prepare_bombs()
                self.first_press = False
                #Draw the array
                self.draw(self.bomb_grid)
                #Table'ı tamamla
                self.initialize_table()
                self.clear()
                self.visited[y][x] = False
                self.open(y,x)
        else:
            self.buttons[y][x].configure(text=self.table[y][x],image=self.images[self.table[y][x]])
            if self.table[y][x] == 0:
                for item in self.delta:
                    dy = y + item[0]
                    dx = x + item[1]
                    if 0 <= dy < self.height and 0 <= dx < self.width:
                        self.open(dy,dx)
        #oyun bitirme
        if self.unopened - self.bombs <= 0 and self.bombs == 0:
                self.finish()
        self.first_press = False

    def main(self):
        self.prepare_bombs()
        #Draw the array
        self.draw(self.bomb_grid)
        #Table'ı tamamla
        self.initialize_table()
        self.root.title("Eda bittin sen")
        self.info_frame = tkinter.Frame(self.root)
        self.main_frame = tkinter.Frame(self.root)
        self.info_frame.pack()
        self.main_frame.pack()
        self.mine_count = tkinter.Label(self.info_frame,text = f"Bombs left : {self.bombs}")
        self.time_count = tkinter.Label(self.info_frame,text = f"Time : {self.seconds}")
        self.seed_label = tkinter.Label(self.info_frame,text = f"Seed : {self.seed}")
        self.labels.append(self.mine_count)
        self.labels.append(self.time_count)
        self.labels.append(self.seed_label)
        self.mine_count.grid(row = 0,column = 0)
        self.time_count.grid(row = 0,column = 1)
        self.seed_label.grid(row = 0,column = 2)
        for y in range(self.height):
            for x in range(self.width):
                button = tkinter.Button(self.main_frame,text = self.UNKNOWN,image=self.images[11])
                button.grid(row = y,column = x)
                self.buttons[y][x] = button
                button.bind("<Button-1>",self.left_click)
                button.bind("<Button-2>",self.right_click)
                button.bind("<Button-3>",self.right_click)
        self.update_clock()

main = Minesweeper(9,9,10,124)
