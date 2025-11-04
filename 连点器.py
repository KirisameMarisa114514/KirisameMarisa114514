import time
import threading
from PIL import ImageTk, Image
from pynput.mouse import Button, Controller
import tkinter as tk
import ctypes,sys
import pyautogui
import os
   
def is_admin():
    """
    检查是否具有管理员权限
    """
    try:
        # 检查用户是否具有管理员权限
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
class ClickerApp():
    def __init__(self):
        """
        创建主窗口对象
        """
        self.window = tk.Tk()
        self.clicking = False
        self.ui() 
        self.run() 
    
    def ui(self):
        """
        用户界面
        """       
        self.window.geometry("1257x793")  # 窗口大小
        self.window.title("连点器")  # 标题

        #添加背景图片    
        self.canvas = tk.Canvas(self.window, width=1257, height=793)
        self.canvas.place(x=0, y=0)
        try:
            self.bg_image = ImageTk.PhotoImage(Image.open(r"D:\vscode\code\Pyhon\clicking_picture.png"))  # 加载背景图片
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image)
        except:
            pass        #控件区域
        self.frame = tk.Frame(self.canvas,bg='', relief=tk.FLAT, bd=0)
        self.canvas.create_window(628,369,window=self.frame)
        
        tk.Label(self.frame, text="连点间隔（秒） :").grid(row=0, column=0)  # 标签并用网格布局
        self.entry_time = tk.Entry(self.frame)
        self.entry_time.grid(row=0, column=1)  # 创建一个文本框
        self.content_time = self.entry_time.get()
        
        try:
            self.window.iconbitmap(r"D:\vscode\code\Pyhon\favicon.ico")  # 设置窗口图标
        except:
            pass
        
        tk.Label(self.frame, text="连点的按键        :").grid(row=1, column=0)  # 标签并用网格布局
        
        self.entry_clicks = tk.Entry(self.frame)
        self.entry_clicks.grid(row=1, column=1)  # 创建文本框
        
        button_start = tk.Button(self.frame, text="开始",command=self.start_clicking, font=("微软雅黑",10,"bold"), width=4, height=1)
        button_start.grid(row=2, column=0, columnspan=2) # 开始按钮
        button_stop = tk.Button(self.frame, text="停止",command=self.stop_clicking, font=("微软雅黑",10,"bold"), width=4, height=1)
        button_stop.grid(row=3, column=0, columnspan=2) # 停止按钮
    def start_clicking(self):
        """
        开始
        """
        self.clicking = True
        def click_loop():
            while self.clicking:
                try:
                    pyautogui.press(self.entry_clicks.get()) # 用户设置的按键
                    time.sleep(float(self.entry_time.get())) # 用户设置的间隔时间
                except:
                    break
        self.click_thread = threading.Thread(target=click_loop)
        self.click_thread.daemon = True
        self.click_thread.start()
    
    def stop_clicking(self):
        """
        停止
        """
        self.clicking = False
        print("连点器已停止")
    
    def run(self):
        self.window.mainloop()

if is_admin():
    app = ClickerApp()
    app.run()
    print("程序已退出")

else:
    if sys.version_info[0] == 3:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)