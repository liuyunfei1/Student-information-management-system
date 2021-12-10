from tkinter import messagebox
from PIL import Image, ImageTk
import csv
import tkinter as tk
import redis
import json

stu_dict2 = {"schoolnumber": "", "name": "", "chinese": -1, "math": -1, "english": -1, "total": -1}
stu_dict0 = {"schoolnumber": "", "name": "", "chinese": -1, "math": -1, "english": -1, "total": -1}

class Studentonly(object):
    def __init__(self, master=None, key=None):
        self.root = master
        self.root.title('学生信息管理系统-学生端')
        self.root.geometry('800x400')
        self.root.geometry('+300+200')
        self.data = {}
        self.db2 = redis.Redis(host='127.0.0.1', port=6379, db=3, decode_responses=True)
        self.db0 = redis.Redis(host='127.0.0.1', port=6379, db=1, decode_responses=True)
        self.db1 = redis.Redis(host='127.0.0.1', port=6379, db=2, decode_responses=True)
        self.data2 = eval(self.db2.hget('student', key))
        self.data0 = eval(self.db0.hget('student', key))
        stu_dict2.update(self.data2)
        stu_dict0.update(self.data0)
        pic1 = Image.open('img/background2.jpg').resize((800, 500))
        pic = ImageTk.PhotoImage(pic1)
        render = tk.Label(self.root, image=pic, compound=tk.CENTER, justify=tk.LEFT)
        render.place(x=0, y=0)

        label = tk.Label(self.root, text='输入内容', font=('微软雅黑', 15), fg='black', bg='#FFD700')
        label.place(x=0, y=10, width=100, height=40)

        self.entry1 = tk.Entry(self.root, font=('宋体', 15), width=15, bg='#F5DEB3')
        self.entry1.place(x=480, y=10, width=120, height=40)

        queren_button = tk.Button(self.root, text='信息确认', font=('微软雅黑', 15), bg='#00BFFF', command=self.queren_data)
        queren_button.place(x=690, y=10, width=100, height=40)

        start_button = tk.Button(self.root, text='启动系统', font=('微软雅黑', 15), bg='#DC143C', command=self.get_next1)
        start_button.place(x=0, y=60, width=100, height=40)

        meizhao_label = tk.Label(self.root, text='美照专栏', font=('微软雅黑', 15), bg='#EE82EE', fg='#9400D3')
        meizhao_label.place(x=5, y=120, width=150, height=40)

        self.studentdata = tk.Text(self.root, bg='#87CEFA', fg='#1E90FF', font=('微软雅黑', 15))
        self.studentdata.place(x=170, y=120, width=600, height=250)

        acquire_button1 = tk.Button(self.root, text='查询期中信息', font=('微软雅黑', 15), bg='#7FFF00', command=self.cha_data0)
        acquire_button1.place(x=160, y=60, width=150, height=40)

        acquire_button2 = tk.Button(self.root, text='查询期末信息', font=('微软雅黑', 15), bg='#32CD32', command=self.cha_data2)
        acquire_button2.place(x=320, y=60, width=150, height=40)

        mi_button = tk.Button(self.root, text='修改登录密码', font=('微软雅黑', 15), bg='#22BB22', command=self.get_next2)
        mi_button.place(x=480, y=60, width=150, height=40)

        quit_button = tk.Button(self.root, text='退出学生系统', font=('微软雅黑', 15), bg='#008000', command=self.quit)
        quit_button.place(x=640, y=60, width=150, height=40)
        self.root.mainloop()

    def queren_data(self):
        new_mi = self.entry1.get()
        if new_mi:
            self.db1.set(stu_dict0['schoolnumber'], new_mi)
            messagebox.showinfo('提示', '新密码修改成功')

    def get_next1(self):
        self.studentdata.delete('1.0', 'end')
        self.str1 = """
        ****************************
        欢迎使用【学生信息管理系统】V1.0
        本系统是学生端，只能对本人信息操作
        ****************************
            请选择你想要进行的操作
              查询期中，期末信息
                退出学生系统
        ****************************
        """
        self.studentdata.insert(tk.END, self.str1)

    def get_next2(self):
        self.studentdata.delete('1.0', 'end')
        self.str1 = """
        ****************************
                修改密码功能
        ****************************
                输入新的密码
             再点击右上角的信息确认
        ****************************
        """
        self.studentdata.insert(tk.END, self.str1)

    def check(self):
        messagebox.showinfo('提示', '一定要合法输入，否则文件保存会出错哦')

    def cha_data0(self):
        self.studentdata.delete('0.0', 'end')
        self.studentdata.insert(tk.END, '*************************期中成绩展示************************\n')
        self.studentdata.insert(tk.END, 'schoolnumber   \tname  \tchinese \tmath\t english\t total\n')
        self.studentdata.insert(tk.END, stu_dict0['schoolnumber'])
        self.studentdata.insert(tk.END, '\t ')
        self.studentdata.insert(tk.END, stu_dict0['name'])
        self.studentdata.insert(tk.END, '\t    ')
        if int(stu_dict0['chinese']) >= 0:
            self.studentdata.insert(tk.END, stu_dict0['chinese'])
        else:
            self.studentdata.insert(tk.END, 'NA')
        self.studentdata.insert(tk.END, '\t     ')
        if int(stu_dict0['math']) >= 0:
            self.studentdata.insert(tk.END, stu_dict0['math'])
        else:
            self.studentdata.insert(tk.END, 'NA')
        self.studentdata.insert(tk.END, '\t   ')
        if int(stu_dict0['english']) >= 0:
            self.studentdata.insert(tk.END, stu_dict0['english'])
        else:
            self.studentdata.insert(tk.END, 'NA')
        self.studentdata.insert(tk.END, '\t  ')
        if int(stu_dict0['total']) >= 0:
            self.studentdata.insert(tk.END, stu_dict0['total'])
        else:
            self.studentdata.insert(tk.END, 'NA')
        self.studentdata.insert(tk.END, '\n')
        img_ = Image.open('img/1.png').resize((150, 180))
        img1 = ImageTk.PhotoImage(img_)
        meizhao_label = tk.Label(self.root, image=img1, bg='pink')
        meizhao_label.place(x=5, y=170, width=150, height=180)
        def pic_change(name):
            if name:
                name_pic = 'img/' + name + '.png'
            else:
                name_pic = 'img/1.png'
            try:
                img__ = Image.open(name_pic).resize((150, 180))
                img = ImageTk.PhotoImage(img__)
                meizhao_label.configure(image=img)
                meizhao_label.image = img
            except Exception as e:
                img__ = Image.open('img/1.png').resize((150, 180))
                img = ImageTk.PhotoImage(img__)
                meizhao_label.configure(image=img)
                meizhao_label.image = img
        pic_change(stu_dict0['schoolnumber'])
        if stu_dict0['schoolnumber']:
            messagebox.showinfo('提示', '该同学数据查询成功')

    def cha_data2(self):
        self.studentdata.delete('0.0', 'end')
        self.studentdata.insert(tk.END, '*************************期末成绩展示************************\n')
        self.studentdata.insert(tk.END, 'schoolnumber   \tname  \tchinese \tmath\t english\t total\n')
        self.studentdata.insert(tk.END, stu_dict2['schoolnumber'])
        self.studentdata.insert(tk.END, '\t ')
        self.studentdata.insert(tk.END, stu_dict2['name'])
        self.studentdata.insert(tk.END, '\t    ')
        if int(stu_dict2['chinese']) >= 0:
            self.studentdata.insert(tk.END, stu_dict2['chinese'])
        else:
            self.studentdata.insert(tk.END, 'NA')
        self.studentdata.insert(tk.END, '\t     ')
        if int(stu_dict2['math']) >= 0:
            self.studentdata.insert(tk.END, stu_dict2['math'])
        else:
            self.studentdata.insert(tk.END, 'NA')
        self.studentdata.insert(tk.END, '\t   ')
        if int(stu_dict2['english']) >= 0:
            self.studentdata.insert(tk.END, stu_dict2['english'])
        else:
            self.studentdata.insert(tk.END, 'NA')
        self.studentdata.insert(tk.END, '\t  ')
        if int(stu_dict2['total']) >= 0:
            self.studentdata.insert(tk.END, stu_dict2['total'])
        else:
            self.studentdata.insert(tk.END, 'NA')
        self.studentdata.insert(tk.END, '\n')
        img_ = Image.open('img/1.png').resize((150, 180))
        img1 = ImageTk.PhotoImage(img_)
        meizhao_label = tk.Label(self.root, image=img1, bg='pink')
        meizhao_label.place(x=5, y=170, width=150, height=180)
        def pic_change(name):
            if name:
                name_pic = 'img/' + name + '.png'
            else:
                name_pic = 'img/1.png'
            try:
                img__ = Image.open(name_pic).resize((150, 180))
                img = ImageTk.PhotoImage(img__)
                meizhao_label.configure(image=img)
                meizhao_label.image = img
            except Exception as e:
                img__ = Image.open('img/1.png').resize((150, 180))
                img = ImageTk.PhotoImage(img__)
                meizhao_label.configure(image=img)
                meizhao_label.image = img
        pic_change(stu_dict2['schoolnumber'])
        if stu_dict2['schoolnumber']:
            messagebox.showinfo('提示', '该同学数据查询成功')

    def quit(self):
        self.root.destroy()

if __name__ == '__main__':
    Studentonly()








