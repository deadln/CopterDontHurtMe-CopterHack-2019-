# coding=utf-8
from Tkinter import *
import Tkinter as tk
import tkFont as font
import ttk as ttk
import time
import subprocess
import sys
import paramiko

host = "192.168.11.1"
user = "pi"
pas = "raspberry"

class Point:
    def __init__(self,x=0,y=0,z=0):
        self.x = x
        self.y = y
        self.z = z

        def __str__(self):
                s = "Point(" + self.x + " " + self.y + " " + self.z + ")"
                return s

class App:
    def __init__(self):

        self.host = "192.168.11.1"
        self.user = "pi"
        self.pas = "raspberry"
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(hostname=self.host, username=self.user, password=self.pas)
	stdin, stdout, stderr = self.client.exec_command("source catkin_ws/devel/setup.bash")
	data = stdout.read() + stderr.read()

        self.window = Tk()
        self.window.title("Copter don't hurt me")
        self.window.geometry("600x500")
        self.button_passed = 0

        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(size=20)
        self.window.option_add("*Font", self.default_font)
        self.tab_control = ttk.Notebook(self.window)

        self.square_arr = []

    def start(self):
        self.main_menu()
        self.window.mainloop()

    def square_fly(self):
        def close():
            self.button_passed = 0
            win.destroy()
        def ok():
            #point = Point(p_arr[0], p_arr[1], p_arr[2])
            circles = int(text_circle.get())
            p = text_start.get().split()

            res = ""
            res += "python square_f.py "
            for i in p:
                res += i + " "
            res+=text_side.get() + " "
            res+=text_ang.get() + " "
            res+=text_circle.get()
            print res
            stdin, stdout, stderr = self.client.exec_command(res)
            data = stdout.read() + stderr.read()
            print data
            ################
            #subprocess.call(data)
            #time.sleep(3)
            ################
            self.button_passed = 0

            win.destroy()

        win = tk.Toplevel(self.window)
        win.geometry("600x320")
        win.title("Облёт квадрата")
        label = Label(win, text="Введите данные:", font="georgia 15")
        label.grid(column=0, row=0, sticky=N, padx=10, pady=10)

        label_start = Label(win, text="Введите точку старта:", font="georgia 12")
        label_start.grid(column=0, row=1, sticky=E, padx=10, pady=10)

        text_start = Entry(win, width=20, font="georgia 12")
        text_start.grid(column=1, row=1, sticky=W, padx=10, pady=10)

        label_side = Label(win, text="Введите длину стороны:", font="georgia 12")
        label_side.grid(column=0, row=2, sticky=E, padx=10, pady=10)

        text_side = Entry(win, width=20, font="georgia 12")
        text_side.grid(column=1, row=2, sticky=W, padx=10, pady=10)

        label_circle = Label(win, text="Введите количество кругов:", font="georgia 12")
        label_circle.grid(column=0, row=3, sticky=E, padx=10, pady=10)

        text_circle = Entry(win, width=20, font="georgia 12")
        text_circle.grid(column=1, row=3, sticky=W, padx=10, pady=10)

        label_ang = Label(win, text="Введите угол наклона: ", font="georgia 12")
        label_ang.grid(column=0, row=4, sticky=E, padx=10, pady=10)

        text_ang = Entry(win, width=20, font="georgia 12")
        text_ang.grid(column=1, row=4, sticky=W, padx=10, pady=10)

        button_cancel = Button(win, text="Отмена", font="georgia 12", command = close)
        button_ok = Button(win, text="Подтвердить", font="georgia 12", command = ok)
        button_cancel.grid(column=2, row=5)

        button_ok.grid(column=1, row=5, sticky=E, padx=10)

        win.protocol("WM_DELETE_WINDOW", close)
        win.mainloop()

    def points_fly(self):
        data = []
        str_data = "Добавленные точки: "

        dat = [str_data]

        def add():

            dst = ""

            p = text_start.get().split()
            if len(p)==3:
                dst += text_start.get() + ", "
                dat[0] += dst

                show_data.configure(text=dat[0])
                text_start.delete(0, END)
                for i in p:
                    data.append(int(i))


        def close():
            self.button_passed = 0
            win.destroy()

        def ok():
            data.append("c")
            data.append(int(text_circle.get()))
            ############
            self.button_passed = 0
            win.destroy()
            print data
            res = ""
            res += "python bypoints.py "
            for i in range(len(data) - 1):
                res+=str(data[i]) + " "
            res+=str(data[-1])
            print res

            stdin, stdout, stderr = self.client.exec_command(res)
            dat = stdout.read() + stderr.read()
            print dat
            ################
            #subprocess.call(data)

            ################


        win = tk.Toplevel(self.window)
        win.geometry("600x300")
        win.title("Полёт по точкам")
        label = Label(win, text="Введите данные:", font="georgia 15")
        label.grid(column=0, row=0, sticky=N, padx=10, pady=10)

        label_start = Label(win, text="Введите точку:", font="georgia 12")
        label_start.grid(column=0, row=1, sticky=E, padx=10, pady=10)

        button_add = Button(win, text="Добавить", font="georgia 12", command=add)
        button_add.grid(column=2, row=1, sticky=E, padx=10, pady=10)

        text_start = Entry(win, width=20, font="georgia 12")
        text_start.grid(column=1, row=1, sticky=W, padx=10, pady=10)

        label_circle = Label(win, text="Введите количество кругов:", font="georgia 12")
        label_circle.grid(column=0, row=3, sticky=E, padx=10, pady=10)

        text_circle = Entry(win, width=20, font="georgia 12")
        text_circle.grid(column=1, row=3, sticky=W, padx=10, pady=10)

        button_cancel = Button(win, text="Отмена", font="georgia 12", command=close)
        button_ok = Button(win, text="Подтвердить", font="georgia 12", command=ok)
        button_cancel.grid(column=2, row=4)
        button_ok.grid(column=1, row=4, sticky=E, padx=10)

        show_data = Message(win, text=str_data, padx=5, pady=5, width=480, font="georgia 12")
        show_data.grid(column=0, row=4)

        show_data.place(x=4, y=249)

        win.protocol("WM_DELETE_WINDOW", close)
        win.mainloop()

    def circle_fly(self):
        stdin, stdout, stderr = self.client.exec_command("python spi.py")
        dat = stdout.read() + stderr.read()
        print dat

    def main_menu(self):
        def square_fly():
            if not self.button_passed:
                self.button_passed = 1
                self.square_fly()

        def points_fly():
            if not self.button_passed:
                self.button_passed = 1
                self.points_fly()
            pass

        def circle_fly():
            if not self.button_passed:
                self.button_passed = 1
                self.circle_fly()
            pass

        label = Label(self.window, text="Выберите режим полёта:", font="georgia 30")
        label.grid(column=0, row=0, sticky=N, padx=60, pady=20)

        square_button = Button(self.window, text="Облёт квадрата", command=square_fly, height = 1, width=30)
        square_button.grid(column=0, row=1, padx=10, pady=10, sticky=N)

        points_button = Button(self.window, text="Полёт по точкам", command=points_fly, height = 1, width=30)
        points_button.grid(column=0, row=2, padx=10, pady=10, sticky=N)

        circle_button = Button(self.window, text="Полёт по спирали", command=circle_fly, height = 1, width=30)
        circle_button.grid(column=0, row=3, padx=10, pady=10, sticky=N)
