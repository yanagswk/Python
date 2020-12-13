import tkinter as tk
import re

from tkinter import messagebox


class NumberCheck(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.RE_ADRESS = r'\w+@\w+.com'
        
        # windowの大きさ
        self.master.geometry('240x240')

        # UI上部のタイトル
        self.master.title('NumberCheck')

        # 入力ボックス
        self.entry = tk.Entry(self.master)

        self.pack()
        self.entry.pack()
        self.number_check()
        self.quit_button()


    def judgment(self, event):
        # 正規表現
        self.pattern = re.fullmatch(self.RE_ADRESS, self.entry.get())
        if self.pattern:
            messagebox.showinfo('正常', '正しいメールアドレスです。')
        else:
            messagebox.showinfo('異常', '正確にメールアドレスを入力してください。')


    def number_check(self):
        self.judgment_button = tk.Button(self, text="判定", fg='red')
        self.judgment_button.bind('<Button-1>', self.judgment)
        self.judgment_button.pack()

    
    def quit_button(self):
        self.quit = tk.Button(self, text='QUIT', command=self.master.destroy)
        self.quit.pack(side='bottom')


root = tk.Tk()
app = NumberCheck(master=root)
app.mainloop()
