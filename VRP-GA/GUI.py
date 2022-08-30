from tkinter import *
from main import Main
from numpy import double

d = 0
v = 0
c = 0
p = 0
x = 0
y = 0
depots = []
customers = []


def get():
    global d
    d = int(e1.get())
    global v
    v = int(e2.get())
    global c
    c = int(e3.get())
    global p
    p = int(e4.get())
    call_back(d, c)

def call_back(d, c):
    Label(master, text='x and y coordinates of depots', font='Bold').grid(row=6, column=2)

    def get_d():
        x = double(e.get())
        y = double(h.get())
        depots.append((x, y))
        if len(depots) == d:
            customer(c)
        print(depots)
        print(len(depots))

    Label(master, text='XCOORD').grid(row=8, column=0)
    Label(master, text='YCOORD').grid(row=8, column=2)
    e = Spinbox(master, from_=0, to=10)
    h = Spinbox(master, from_=0, to=10)
    e.grid(row=8, column=1)
    h.grid(row=8, column=3)
    bu = Button(master, text="send ", font='Bold', command=get_d).grid(row=8, column=4)


def customer(c):
    Label(master, text='x and y coordinates of customer', font='Bold').grid(row=9, column=2)

    def get_c():
        x = double(e.get())
        y = double(h.get())
        customers.append((x, y))
        if len(customers) == c:
            Label(master, text='thank you', font='Bold').grid(row=11, column=2)
        print(customers)
        print(c)
        print(len(customers))

    Label(master, text='XCOORD').grid(row=10, column=0)
    Label(master, text='YCOORD').grid(row=10, column=2)
    e = Spinbox(master, from_=0, to=10)
    h = Spinbox(master, from_=0, to=10)
    e.grid(row=10, column=1)
    h.grid(row=10, column=3)
    bu = Button(master, text="send ", font='Bold', command=get_c).grid(row=10, column=4)


if __name__ == '__main__':
    master = Tk()
    Label(master, text=' "Vehicle Routing Problem" ', font='Bold').grid(row=0, column=1)
    Label(master, text='Depots number').grid(row=1, column=0)
    Label(master, text='vehicle number').grid(row=1, column=2)
    Label(master, text='customer number').grid(row=2, column=0)
    Label(master, text='population size').grid(row=2, column=2)

    e1 = Spinbox(master, from_=0, to=10)
    e2 = Spinbox(master, from_=0, to=10)
    e3 = Spinbox(master, from_=0, to=10)
    e4 = Spinbox(master, from_=0, to=10)

    e1.grid(row=1, column=1)
    e2.grid(row=1, column=3)
    e3.grid(row=2, column=1)
    e4.grid(row=2, column=3)

    B = Button(master, text="get ", font='Bold', command=get).grid(row=5, column=2)

    mainloop()

    df = open('pr10.txt', 'r')
    data = df.readline().split()

    customers = []
    for j in range(c):
        info = df.readline().split()
        x = double(info[1])
        y = double(info[2])
        customers.append((x, y))

    depots = []
    for j in range(d):
        info = df.readline().split()
        x = double(info[1])
        y = double(info[2])
        depots.append((x, y))

    o = Main(depots, customers, v, d, c, p)
    o.run()

