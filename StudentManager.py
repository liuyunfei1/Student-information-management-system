from tkinter import messagebox
from PIL import Image, ImageTk
import csv
import tkinter as tk
import redis
import json


class StudentManager(object):
    def __init__(self, master=None):
        self.root = master
        self.root.title('学生信息管理系统-教师端')
        self.root.geometry('910x450')
        self.root.geometry('+300+200')
        self.data = {}
        self.status_a = self.status_b = self.status_c = self.status_d = self.status_e = 0
        self.db2 = redis.Redis(host='127.0.0.1', port=6379, db=3, decode_responses=True)
        self.db0 = redis.Redis(host='127.0.0.1', port=6379, db=1, decode_responses=True)
        self.db1 = redis.Redis(host='127.0.0.1', port=6379, db=2, decode_responses=True)
        self.data2 = self.db2.hgetall('student')
        self.data0 = self.db0.hgetall('student')
        pic1 = Image.open('img/background1.jpg').resize((1200, 500))
        pic = ImageTk.PhotoImage(pic1)

        render = tk.Label(self.root, image=pic, compound=tk.CENTER, justify=tk.LEFT)
        render.place(x=0, y=0)

        label = tk.Label(self.root, text='输入内容', font=('微软雅黑', 15), fg='black', bg='#FFD700')
        label.place(x=0, y=10, width=100, height=40)

        label = tk.Label(self.root, text='name', font=('微软雅黑', 15), fg='black', bg='#87CEFA')
        label.place(x=430, y=10, width=80, height=40)

        self.entry1 = tk.Entry(self.root, font=('宋体', 15), width=15, bg='#F5DEB3')
        self.entry1.place(x=430, y=50, width=80, height=40)

        label = tk.Label(self.root, text='chinese', font=('微软雅黑', 15), fg='black', bg='#87CEFA')
        label.place(x=520, y=10, width=80, height=40)

        self.entry2 = tk.Entry(self.root, font=('宋体', 15), width=15, bg='#F5DEB3')
        self.entry2.place(x=520, y=50, width=80, height=40)

        label = tk.Label(self.root, text='math', font=('微软雅黑', 15), fg='black', bg='#87CEFA')
        label.place(x=610, y=10, width=80, height=40)

        self.entry3 = tk.Entry(self.root, font=('宋体', 15), width=15, bg='#F5DEB3')
        self.entry3.place(x=610, y=50, width=80, height=40)

        label = tk.Label(self.root, text='english', font=('微软雅黑', 15), fg='black', bg='#87CEFA')
        label.place(x=700, y=10, width=80, height=40)

        self.entry4 = tk.Entry(self.root, font=('宋体', 15), width=15, bg='#F5DEB3')
        self.entry4.place(x=700, y=50, width=80, height=40)

        label = tk.Label(self.root, text='schoolnumber', font=('微软雅黑', 15), fg='black', bg='#87CEFA')
        label.place(x=130, y=10, width=140, height=40)

        self.entry5 = tk.Entry(self.root, font=('宋体', 15), width=15, bg='#F5DEB3')
        self.entry5.place(x=130, y=50, width=140, height=40)

        xueqi_label = tk.Label(self.root, text='mid/last(1/2)', font=('微软雅黑', 15), fg='black', bg='#87CEFA')
        xueqi_label.place(x=280, y=10, width=140, height=40)

        self.entry6 = tk.Entry(self.root, font=('宋体', 15), width=15, bg='#F5DEB3')
        self.entry6.place(x=280, y=50, width=140, height=40)

        confilm_button1 = tk.Button(self.root, text='信息确定', font=('微软雅黑', 15), bg='#00BFFF', command=self.check1)
        confilm_button1.place(x=790, y=50, width=100, height=40)

        start_button = tk.Button(self.root, text='启动系统', font=('微软雅黑', 15), bg='#DC143C', command=self.get_next1)
        start_button.place(x=0, y=60, width=100, height=40)

        meizhao_label = tk.Label(self.root, text='美照专栏', font=('微软雅黑', 15), bg='#EE82EE', fg='#9400D3')
        meizhao_label.place(x=10, y=120, width=150, height=40)

        self.studentdata = tk.Text(self.root, bg='#87CEFA', fg='#1E90FF', font=('微软雅黑', 15))
        self.studentdata.place(x=170, y=120, width=550, height=300)

        create_button = tk.Button(self.root, text='新建学生信息', font=('微软雅黑', 15), bg='#98FB98', command=self.create_data)
        create_button.place(x=740, y=120, width=150, height=40)

        show_button = tk.Button(self.root, text='显示全部信息', font=('微软雅黑', 15), bg='#00FF7F', command=self.show_data)
        show_button.place(x=740, y=170, width=150, height=40)

        acquire_button = tk.Button(self.root, text='查询学生信息', font=('微软雅黑', 15), bg='#00FF00', command=self.acquire_data)
        acquire_button.place(x=740, y=220, width=150, height=40)

        delete_button = tk.Button(self.root, text='删除学生信息', font=('微软雅黑', 15), bg='#32CD32', command=self.delete_data)
        delete_button.place(x=740, y=270, width=150, height=40)

        modify_button = tk.Button(self.root, text='修改学生信息', font=('微软雅黑', 15), bg='#22BB22', command=self.modify_data)
        modify_button.place(x=740, y=320, width=150, height=40)

        quit_button = tk.Button(self.root, text='退出学生系统', font=('微软雅黑', 15), bg='#006400', command=self.quit)
        quit_button.place(x=740, y=370, width=150, height=40)
        self.root.mainloop()

    def get_next1(self):
        #清空显示
        self.studentdata.delete('1.0', 'end')
        self.str1 = """
        ****************************
        欢迎使用【学生信息管理系统】V1.0
          请从右侧选择你想要进行的操作
                新建学生信息
                显示全部信息
                查询学生信息
                删除学生信息
                修改学生信息
                退出学生系统
        ****************************
        """
        self.studentdata.insert(tk.END, self.str1)

    def get_next2(self):
        self.studentdata.delete('1.0', 'end')
        self.str2 = """
        ==========================
         请从输入框输入要增加的学生的
         学号，学期，姓名，语文，数学，英语成绩
        ==========================
        全部填写完按右侧的---信息确认
        ==========================
        """
        self.studentdata.insert(tk.END, self.str2)

    def check(self):
        messagebox.showinfo('提示', '一定要合法输入，否则文件保存会出错哦')

    def check1(self):
        if self.status_a:
            self.status_a = 0
            reply = self.entry1.get()
            num1 = int(self.entry2.get())
            num2 = int(self.entry3.get())
            num3 = int(self.entry4.get())
            num4 = self.entry5.get()
            num5 = int(self.entry6.get())
            if num4:
                messagebox.showinfo('提示', '学号填写合法')
                self.entry5.delete(0, tk.END)
            else:
                messagebox.showinfo('提示', '回答不合法，请重试')
                self.entry5.delete(0, tk.END)
            if num5 == 1 or num5 == 2:
                messagebox.showinfo('提示', '学期填写合法')
                self.entry6.delete(0, tk.END)
            else:
                messagebox.showinfo('提示', '回答不合法，请重试')
                self.entry6.delete(0, tk.END)
            if reply:
                messagebox.showinfo('提示', '姓名填写合法')
                self.entry1.delete(0, tk.END)
            else:
                messagebox.showinfo('提示', '回答不合法，请重试')
                self.entry1.delete(0, tk.END)
            if 0 <= num1 <= 100:
                messagebox.showinfo('提示', '语文填写合法')
                self.entry2.delete(0, tk.END)
            else:
                messagebox.showinfo('提示', '回答不合法，请重试')
                self.entry2.delete(0, tk.END)
            if 0 <= num2 <= 100:
                messagebox.showinfo('提示', '数学填写合法')
                self.entry3.delete(0, tk.END)
            else:
                messagebox.showinfo('提示', '回答不合法，请重试')
                self.entry3.delete(0, tk.END)
            if 0 <= num3 <= 100:
                messagebox.showinfo('提示', '英语填写合法')
                self.entry4.delete(0, tk.END)
            else:
                messagebox.showinfo('提示', '回答不合法，请重试')
                self.entry4.delete(0, tk.END)
            if reply and num1 and num2 and num3 and num4 and num5:
                if num5 == 1:
                    self.data0.update({num4: json.dumps(
                        {'schoolnumber': num4, 'name': reply, 'chinese': num1, 'math': num2, 'english': num3,
                         'total': num1 + num2 + num3})})
                    self.db0.hset('student', num4, json.dumps(
                        {'schoolnumber': num4, 'name': reply, 'chinese': num1, 'math': num2, 'english': num3,
                         'total': num1 + num2 + num3}))
                    self.data0 = self.db0.hgetall('student')
                    self.db1.set(num4, '123456')
                    self.data2.update({num4: json.dumps(
                        {'schoolnumber': num4, 'name': reply, 'chinese': -1, 'math': -1, 'english': -1,
                         'total': -3})})
                    self.db2.hset('student', num4, json.dumps(
                        {'schoolnumber': num4, 'name': reply, 'chinese': -1, 'math': -1, 'english': -1,
                         'total': -3}))
                    self.data2 = self.db2.hgetall('student')
                    messagebox.showinfo('提示', '新建学生数据成功，数据成功保存到期中数据库，用户初始密码为 123456，可登录账户进行重置密码')
                    messagebox.showinfo('提示', '期末数据库初始化成功，语,数,英,总分,默认成绩均为 NA，您可直接进行修改期末成绩，省去了新建期末成绩的操作')
                elif num5 == 2:
                    self.data2.update({num4: json.dumps(
                        {'schoolnumber': num4, 'name': reply, 'chinese': num1, 'math': num2, 'english': num3,
                         'total': num1 + num2 + num3})})
                    self.db2.hset('student', num4, json.dumps(
                        {'schoolnumber': num4, 'name': reply, 'chinese': num1, 'math': num2, 'english': num3,
                         'total': num1 + num2 + num3}))
                    self.data2 = self.db2.hgetall('student')
                    self.db1.set(num4, '123456')
                    self.data0.update({num4: json.dumps(
                        {'schoolnumber': num4, 'name': reply, 'chinese': -1, 'math': -1, 'english': -1,
                         'total': -3})})
                    self.db0.hset('student', num4, json.dumps(
                        {'schoolnumber': num4, 'name': reply, 'chinese': -1, 'math': -1, 'english': -1,
                         'total': -3}))
                    self.data0 = self.db0.hgetall('student')
                    messagebox.showinfo('提示', '新建学生数据成功，数据成功保存到期末数据库，用户初始密码为 123456，可登录账户进行重置密码')
                    messagebox.showinfo('提示', '期中数据库初始化成功，语,数,英,总分,默认成绩均为 NA，您可直接进行修改期中成绩，省去了新建期中成绩的操作')
                else:
                    messagebox.showinfo('提示', '学期输入不符合要求，请重新输入')
            else:
                messagebox.showinfo('提示', '输入数据数量不足，请重新输入')
        if self.status_b:
            self.status_b = 0
            num4 = self.entry5.get()
            num5 = int(self.entry6.get())
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
            if num5 == 1:
                if num4 in self.data0.keys():
                    for key in self.data0.keys():
                        if key == num4:
                            data_one = eval(self.data0[num4])
                            self.studentdata.delete('0.0', 'end')
                            self.studentdata.insert(tk.END, '**********************期中成绩展示*********************\n')
                            self.studentdata.insert(tk.END, 'schoolnumber   \tname  \tchinese \tmath\t english\t total\n')
                            self.studentdata.insert(tk.END, data_one['schoolnumber'])
                            self.studentdata.insert(tk.END, '\t ')
                            self.studentdata.insert(tk.END, data_one['name'])
                            self.studentdata.insert(tk.END, '\t    ')
                            if int(data_one['chinese']) >= 0:
                                self.studentdata.insert(tk.END, data_one['chinese'])
                            else:
                                self.studentdata.insert(tk.END, 'NA')
                            self.studentdata.insert(tk.END, '\t     ')
                            if int(data_one['math']) >= 0:
                                self.studentdata.insert(tk.END, data_one['math'])
                            else:
                                self.studentdata.insert(tk.END, 'NA')
                            self.studentdata.insert(tk.END, '\t   ')
                            if int(data_one['english']) >= 0:
                                self.studentdata.insert(tk.END, data_one['english'])
                            else:
                                self.studentdata.insert(tk.END, 'NA')
                            self.studentdata.insert(tk.END, '\t  ')
                            if int(data_one['total']) >= 0:
                                self.studentdata.insert(tk.END, data_one['total'])
                            else:
                                self.studentdata.insert(tk.END, 'NA')
                            self.studentdata.insert(tk.END, '\n')
                            # 美照展示
                            img_ = Image.open('img/1.png').resize((150, 180))
                            img1 = ImageTk.PhotoImage(img_)
                            meizhao_label = tk.Label(self.root, image=img1, bg='pink')
                            meizhao_label.place(x=10, y=170, width=150, height=180)
                            pic_change(num4)
                            messagebox.showinfo('提示', '您查询的期中学生信息成功全部展示')
                else:
                    messagebox.showinfo('提示', '该学生的信息不存在，请重试')
            elif num5 == 2:
                if num4 in self.data2.keys():
                    for key in self.data2.keys():
                        if key == num4:
                            data_one = eval(self.data2[num4])
                            self.studentdata.delete('0.0', 'end')
                            self.studentdata.insert(tk.END, '**********************期末成绩展示*********************\n')
                            self.studentdata.insert(tk.END, 'schoolnumber   \tname  \tchinese \tmath\t english\t total\n')
                            self.studentdata.insert(tk.END, data_one['schoolnumber'])
                            self.studentdata.insert(tk.END, '\t ')
                            self.studentdata.insert(tk.END, data_one['name'])
                            self.studentdata.insert(tk.END, '\t    ')
                            if int(data_one['chinese']) >= 0:
                                self.studentdata.insert(tk.END, data_one['chinese'])
                            else:
                                self.studentdata.insert(tk.END, 'NA')
                            self.studentdata.insert(tk.END, '\t     ')
                            if int(data_one['math']) >= 0:
                                self.studentdata.insert(tk.END, data_one['math'])
                            else:
                                self.studentdata.insert(tk.END, 'NA')
                            self.studentdata.insert(tk.END, '\t   ')
                            if int(data_one['english']) >= 0:
                                self.studentdata.insert(tk.END, data_one['english'])
                            else:
                                self.studentdata.insert(tk.END, 'NA')
                            self.studentdata.insert(tk.END, '\t  ')
                            if int(data_one['total']) >= 0:
                                self.studentdata.insert(tk.END, data_one['total'])
                            else:
                                self.studentdata.insert(tk.END, 'NA')
                            self.studentdata.insert(tk.END, '\n')
                            # 美照展示
                            img_ = Image.open('img/1.png').resize((150, 180))
                            img1 = ImageTk.PhotoImage(img_)
                            meizhao_label = tk.Label(self.root, image=img1, bg='pink')
                            meizhao_label.place(x=10, y=170, width=150, height=180)
                            pic_change(num4)
                            messagebox.showinfo('提示', '您查询的期末学生信息成功全部展示')
                else:
                    messagebox.showinfo('提示', '该学生的信息不存在，请重试')
            else:
                messagebox.showinfo('提示', '学期输入不符合要求，请重新输入')

        if self.status_c:
            self.status_c = 0
            num4 = self.entry5.get()
            if num4:
                self.data0.pop(num4)
                self.db0.hdel('student', num4)
                self.data0 = self.db0.hgetall('student')
                self.data2.pop(num4)
                self.db2.hdel('student', num4)
                self.data2 = self.db2.hgetall('student')
                self.db1.delete(num4)
                messagebox.showinfo('提示', '该同学数据删除成功,数据成功同步到数据库')
            else:
                messagebox.showinfo('提示', '学号输入不正确，请重新输入')
        if self.status_d:
            self.status_d = 0
            reply = self.entry1.get()
            num1 = int(self.entry2.get())
            num2 = int(self.entry3.get())
            num3 = int(self.entry4.get())
            num4 = self.entry5.get()
            num5 = int(self.entry6.get())
            if num4:
                messagebox.showinfo('提示', '学号填写合法')
                self.entry5.delete(0, tk.END)
            else:
                messagebox.showinfo('提示', '回答不合法，请重试')
                self.entry5.delete(0, tk.END)
            if num5 == 1 or num5 == 2:
                messagebox.showinfo('提示', '学期填写合法')
                self.entry6.delete(0, tk.END)
            else:
                messagebox.showinfo('提示', '回答不合法，请重试')
                self.entry6.delete(0, tk.END)
            if reply:
                messagebox.showinfo('提示', '姓名填写合法')
                self.entry1.delete(0, tk.END)
            else:
                messagebox.showinfo('提示', '回答不合法，请重试')
                self.entry1.delete(0, tk.END)
            if 0 <= num1 <= 100:
                messagebox.showinfo('提示', '语文填写合法')
                self.entry2.delete(0, tk.END)
            else:
                messagebox.showinfo('提示', '回答不合法，请重试')
                self.entry2.delete(0, tk.END)
            if 0 <= num2 <= 100:
                messagebox.showinfo('提示', '数学填写合法')
                self.entry3.delete(0, tk.END)
            else:
                messagebox.showinfo('提示', '回答不合法，请重试')
                self.entry3.delete(0, tk.END)
            if 0 <= num3 <= 100:
                messagebox.showinfo('提示', '英语填写合法')
                self.entry4.delete(0, tk.END)
            else:
                messagebox.showinfo('提示', '回答不合法，请重试')
                self.entry4.delete(0, tk.END)
            if reply and num1 and num2 and num3 and num4 and num5:
                if num5 == 1:
                    self.data0.update({num4: json.dumps(
                        {'schoolnumber': num4, 'name': reply, 'chinese': num1, 'math': num2, 'english': num3,
                         'total': num1 + num2 + num3})})
                    self.db0.hset('student', num4, json.dumps(
                        {'schoolnumber': num4, 'name': reply, 'chinese': num1, 'math': num2, 'english': num3,
                         'total': num1 + num2 + num3}))
                    self.data0 = self.db0.hgetall('student')
                    messagebox.showinfo('提示', '新建学生数据成功，数据成功保存到期中数据库')
                elif num5 == 2:
                    self.data2.update({num4: json.dumps(
                        {'schoolnumber': num4, 'name': reply, 'chinese': num1, 'math': num2, 'english': num3,
                         'total': num1 + num2 + num3})})
                    self.db2.hset('student', num4, json.dumps(
                        {'schoolnumber': num4, 'name': reply, 'chinese': num1, 'math': num2, 'english': num3,
                         'total': num1 + num2 + num3}))
                    self.data2 = self.db2.hgetall('student')
                    messagebox.showinfo('提示', '新建学生数据成功，数据成功保存到期末数据库')
                else:
                    messagebox.showinfo('提示', '学期输入不符合要求，请重新输入')
            else:
                messagebox.showinfo('提示', '输入数据数量不足，请重新输入')
        if self.status_e:
            self.status_e = 0
            num5 = int(self.entry6.get())
            if num5 == 1 or num5 == 2:
                messagebox.showinfo('提示', '学期填写合法')
                self.entry6.delete(0, tk.END)
            else:
                messagebox.showinfo('提示', '回答不合法，请重试')
                self.entry6.delete(0, tk.END)
            if num5 == 1:
                self.studentdata.delete('0.0', 'end')
                self.studentdata.insert(tk.END, '**********************期中成绩展示*********************\n')
                self.studentdata.insert(tk.END, 'schoolnumber   \tname  \tchinese \tmath\t english\t total\n')
                for data in self.data0.values():
                    real_data = eval(data)
                    self.studentdata.insert(tk.END, real_data['schoolnumber'])
                    self.studentdata.insert(tk.END, '\t ')
                    self.studentdata.insert(tk.END, real_data['name'])
                    self.studentdata.insert(tk.END, '\t    ')
                    if int(real_data['chinese']) >= 0:
                        self.studentdata.insert(tk.END, real_data['chinese'])
                    else:
                        self.studentdata.insert(tk.END, 'NA')
                    self.studentdata.insert(tk.END, '\t     ')
                    if int(real_data['math']) >= 0:
                        self.studentdata.insert(tk.END, real_data['math'])
                    else:
                        self.studentdata.insert(tk.END, 'NA')
                    self.studentdata.insert(tk.END, '\t   ')
                    if int(real_data['english']) >= 0:
                        self.studentdata.insert(tk.END, real_data['english'])
                    else:
                        self.studentdata.insert(tk.END, 'NA')
                    self.studentdata.insert(tk.END, '\t  ')
                    if int(real_data['total']) >= 0:
                        self.studentdata.insert(tk.END, real_data['total'])
                    else:
                        self.studentdata.insert(tk.END, 'NA')
                    self.studentdata.insert(tk.END, '\n')
                    img_ = Image.open('img/1.png').resize((150, 180))
                    img1 = ImageTk.PhotoImage(img_)
                    meizhao_label = tk.Label(self.root, image=img1, bg='pink')
                    meizhao_label.place(x=10, y=170, width=150, height=180)
                messagebox.showinfo('提示', '期中数据成功全部展示')
            elif num5 == 2:
                self.studentdata.delete('0.0', 'end')
                self.studentdata.insert(tk.END, '**********************期末成绩展示*********************\n')
                self.studentdata.insert(tk.END, 'schoolnumber   \tname  \tchinese \tmath\t english\t total\n')
                for data in self.data2.values():
                    real_data = eval(data)
                    self.studentdata.insert(tk.END, real_data['schoolnumber'])
                    self.studentdata.insert(tk.END, '\t ')
                    self.studentdata.insert(tk.END, real_data['name'])
                    self.studentdata.insert(tk.END, '\t    ')
                    if int(real_data['chinese']) >= 0:
                        self.studentdata.insert(tk.END, real_data['chinese'])
                    else:
                        self.studentdata.insert(tk.END, 'NA')
                    self.studentdata.insert(tk.END, '\t     ')
                    if int(real_data['math']) >= 0:
                        self.studentdata.insert(tk.END, real_data['math'])
                    else:
                        self.studentdata.insert(tk.END, 'NA')
                    self.studentdata.insert(tk.END, '\t   ')
                    if int(real_data['english']) >= 0:
                        self.studentdata.insert(tk.END, real_data['english'])
                    else:
                        self.studentdata.insert(tk.END, 'NA')
                    self.studentdata.insert(tk.END, '\t  ')
                    if int(real_data['total']) >= 0:
                        self.studentdata.insert(tk.END, real_data['total'])
                    else:
                        self.studentdata.insert(tk.END, 'NA')
                    self.studentdata.insert(tk.END, '\n')
                    img_ = Image.open('img/1.png').resize((150, 180))
                    img1 = ImageTk.PhotoImage(img_)
                    meizhao_label = tk.Label(self.root, image=img1, bg='pink')
                    meizhao_label.place(x=10, y=170, width=150, height=180)
                messagebox.showinfo('提示', '期末数据成功全部展示')
            else:
                messagebox.showinfo('提示', '学期输入不符合要求，请重新输入')

    def create_data(self):
        self.get_next2()
        self.status_a = 1

    def show_data(self):
        self.studentdata.delete('1.0', 'end')
        self.str6 = """
                ==========================
                 请从输入框输入要展示的学期
                ==========================
                    点击右边的---信息确定
                ==========================
                """
        self.studentdata.insert(tk.END, self.str6)
        self.status_e = 1

    def acquire_data(self):
        self.studentdata.delete('1.0', 'end')
        self.str3 = """
        ==========================
         请从输入框输入要查询的学生的
                学号，学期
        ==========================
            点击右边的---信息确定
        ==========================
        """
        self.studentdata.insert(tk.END, self.str3)
        self.status_b = 1

    def delete_data(self):
        self.studentdata.delete('0.0', 'end')
        self.str4 = """
        ==========================
         请从输入框输入要删除的学生的
                    学号
        ==========================
            点击右边的---信息确定
        ==========================
        """
        self.studentdata.insert(tk.END, self.str4)
        self.status_c = 1

    def modify_data(self):
        self.studentdata.delete('0.0', 'end')
        self.str5 = """
                ==========================
                 请从输入框输入要修改的学生的
             学号，学期，姓名，语文，数学，英语成绩
                ==========================
                      点击右边的---信息确定
                ==========================
                """
        self.studentdata.insert(tk.END, self.str5)
        self.status_d = 1

    def quit(self):
        self.root.destroy()

if __name__ == '__main__':
    StudentManager()








