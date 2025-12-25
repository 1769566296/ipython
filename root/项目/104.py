"""
import tkinter as tk
import time

class SimpleWidget:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("简单时间显示")
        self.root.geometry("300x200+100+100")
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        
        # 时间标签
        self.label = tk.Label(self.root, font=('楷体', 40), fg='red')
        self.label.pack(expand=True)


        # self.label = tk.Label(self.root, font=('楷体', 50), fg='red')
        # self.label.pack(expand=True)
        # 退出按钮
        tk.Button(self.root, text="退出", command=self.root.quit).pack()
        
        self.update_time()
        self.root.mainloop()
        
    def update_time(self):
        # 更新时间
        # current_time = time.strftime("%H:%M:%S")
        current_time = time.strftime("%H:%M:%sS.%f")[:-3]  # 显示到毫秒


        self.label.config(text=current_time)
        self.root.after(10, self.update_time)

SimpleWidget()"""




import tkinter as tk
# import time
from datetime import datetime, timedelta

class DesktopWidget:
    def __init__(self):
        # 创建主窗口
        self.root = tk.Tk()
        self.setup_window()
        
        # 设置生日（可以在这里修改）
        self.birthday = "2007-05-01"
        
        self.create_widgets()
        self.bind_events()
        self.update_time()
        
    def setup_window(self):
        """设置窗口属性"""
        self.root.title("时间纪念日计数器")
        
        # 窗口大小和位置
        self.root.geometry("380x280")
        
        # 设置到右上角
        screen_width = self.root.winfo_screenwidth()
        x = screen_width - 400  # 留出边距
        self.root.geometry(f"+{x}+20")
        
        # 无边框、置顶
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        
        # 设置背景色和透明度
        self.root.config(bg='#f0f0f0')
        self.root.attributes('-alpha', 0.92)  # 92%不透明
        
    def create_widgets(self):
        """创建界面组件"""
        # 主框架
        main_frame = tk.Frame(self.root, bg='#f0f0f0', relief='solid', bd=1)
        main_frame.pack(fill='both', expand=True, padx=1, pady=1)
        
        # 标题栏（可拖动区域）
        title_frame = tk.Frame(main_frame, bg='#4a6baf', height=28)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)  # 固定高度
        
        # 标题
        ik = input("看这里")
        title_label = tk.Label(title_frame, text=f"时间计数器{ik}", 
                              bg='#4a6baf', fg='white',
                              font=('Microsoft YaHei', 10))
        title_label.pack(side='left', padx=10)
        
        # 关闭按钮
        close_btn = tk.Button(title_frame, text="×", 
                             bg='#ff6b6b', fg='white',
                             bd=0, font=('Arial', 12),
                             command=self.root.quit,
                             activebackground='#ff5252')
        close_btn.pack(side='right', padx=5)
        
        # 内容区域
        content_frame = tk.Frame(main_frame, bg='white')
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # 当前时间（精确到毫秒）
        time_frame = tk.Frame(content_frame, bg='white')
        time_frame.pack(fill='x', pady=(0, 5))
        
        tk.Label(time_frame, text="当前时间", 
                bg='white', font=('Microsoft YaHei', 11),
                fg='#666').pack(anchor='w')
        
        # 小时:分钟:秒
        self.hms_label = tk.Label(time_frame,
                                 text="--:--:--",
                                 bg='white',
                                 font=('Consolas', 28, 'bold'),
                                 fg='#ff4500')
        self.hms_label.pack(anchor='w')
        
        # 毫秒和日期
        ms_date_frame = tk.Frame(time_frame, bg='white')
        ms_date_frame.pack(fill='x', pady=(2, 0))
        
        # 毫秒显示
        self.ms_label = tk.Label(ms_date_frame,
                                text=".---",
                                bg='white',
                                font=('Consolas', 14),
                                fg='#ff7f50')
        self.ms_label.pack(side='left')
        
        # 日期显示
        self.date_label = tk.Label(ms_date_frame,
                                  text="0000-00-00 星期-",
                                  bg='white',
                                  font=('Microsoft YaHei', 10),
                                  fg='#4a6baf')
        self.date_label.pack(side='right')
        
        # 分割线
        tk.Frame(content_frame, height=1, bg='#e0e0e0').pack(fill='x', pady=10)
        
        # 天数计算区域
        calc_frame = tk.Frame(content_frame, bg='white')
        calc_frame.pack(fill='x', pady=5)
        
        # 生日显示
        birthday_label = tk.Label(calc_frame, 
                                 text=f"生日: {self.birthday}",
                                 bg='white',
                                 font=('Microsoft YaHei', 10),
                                 fg='#666')
        birthday_label.pack(anchor='w')
        
        # 已活天数
        lived_frame = tk.Frame(calc_frame, bg='white')
        lived_frame.pack(fill='x', pady=(5, 2))
        
        tk.Label(lived_frame, text="已活天数", 
                bg='white', font=('Microsoft YaHei', 10),
                fg='#666').pack(side='left')
        
        self.lived_days_label = tk.Label(lived_frame,
                                        text="0 天",
                                        bg='white',
                                        font=('Microsoft YaHei', 12, 'bold'),
                                        fg='#9b59b6')
        self.lived_days_label.pack(side='right')
        
        # 生日倒计时
        birthday_frame = tk.Frame(calc_frame, bg='white')
        birthday_frame.pack(fill='x', pady=(2, 0))
        
        tk.Label(birthday_frame, text="生日倒计时", 
                bg='white', font=('Microsoft YaHei', 10),
                fg='#666').pack(side='left')
        
        self.birthday_countdown_label = tk.Label(birthday_frame,
                                                text="0 天",
                                                bg='white',
                                                font=('Microsoft YaHei', 12, 'bold'),
                                                fg='#e74c3c')
        self.birthday_countdown_label.pack(side='right')
        
        # 年龄信息
        age_frame = tk.Frame(calc_frame, bg='white')
        age_frame.pack(fill='x', pady=(2, 0))
        
        tk.Label(age_frame, text="下次生日年龄", 
                bg='white', font=('Microsoft YaHei', 10),
                fg='#666').pack(side='left')
        
        self.next_age_label = tk.Label(age_frame,
                                      text="0 岁",
                                      bg='white',
                                      font=('Microsoft YaHei', 11),
                                      fg='#3498db')
        self.next_age_label.pack(side='right')
        
    def bind_events(self):
        """绑定事件"""
        # 拖动窗口
        self.root.bind('<Button-1>', self.start_drag)
        self.root.bind('<B1-Motion>', self.drag)
        
        # 右键关闭窗口
        self.root.bind('<Button-3>', lambda e: self.root.quit())
        
        # ESC键关闭
        self.root.bind('<Escape>', lambda e: self.root.quit())
        
    def start_drag(self, event):
        """开始拖动"""
        self.drag_x = event.x
        self.drag_y = event.y
        
    def drag(self, event):
        """拖动窗口"""
        x = self.root.winfo_x() + (event.x - self.drag_x)
        y = self.root.winfo_y() + (event.y - self.drag_y)
        self.root.geometry(f"+{x}+{y}")
        
    def calculate_days(self):
        """计算天数相关数据"""
        try:
            # 解析生日日期
            birth_date = datetime.strptime(self.birthday, "%Y-%m-%d")
            now = datetime.now()
            
            # 1. 计算已活天数
            lived_days = (now - birth_date).days
            
            # 2. 计算下一个生日
            next_birthday = birth_date.replace(year=now.year)
            if next_birthday < now:
                next_birthday = next_birthday.replace(year=now.year + 1)
            
            # 3. 计算生日倒计时天数
            days_to_birthday = (next_birthday - now).days
            # 如果今天就是生日，倒计时为0
            if days_to_birthday < 0:
                days_to_birthday = 0
            
            # 4. 计算下一个生日的年龄
            next_age = now.year - birth_date.year
            if (now.month, now.day) < (birth_date.month, birth_date.day):
                next_age += 1
            else:
                next_age += 1 if days_to_birthday < 365 else 0
            
            return lived_days, days_to_birthday, next_age
            
        except Exception as e:
            print(f"日期计算错误: {e}")
            return 0, 0, 0
            
    def update_time(self):
        """更新时间显示 - 每10毫秒刷新一次"""
        # 获取当前时间（精确到毫秒）
        now = datetime.now()
        
        # 格式化时间显示
        # 小时:分钟:秒
        hms_str = now.strftime("%H:%M:%S")
        self.hms_label.config(text=hms_str)
        
        # 毫秒（3位）
        ms_str = f".{now.microsecond // 1000:03d}"
        self.ms_label.config(text=ms_str)
        
        # 日期和星期
        date_str = now.strftime("%Y-%m-%d")
        weekday_str = ["一", "二", "三", "四", "五", "六", "日"][now.weekday()]
        self.date_label.config(text=f"{date_str} 星期{weekday_str}")
        
        # 计算并更新天数
        lived_days, days_to_birthday, next_age = self.calculate_days()
        
        # 格式化数字（添加千位分隔符）
        lived_days_formatted = f"{lived_days:,}"
        
        # 更新标签
        self.lived_days_label.config(text=f"{lived_days_formatted} 天")
        self.birthday_countdown_label.config(text=f"{days_to_birthday} 天")
        self.next_age_label.config(text=f"{next_age} 岁")
        
        # 特殊颜色提醒
        if days_to_birthday <= 7:  # 一周内生日
            self.birthday_countdown_label.config(fg="#8cff09dc")
        elif days_to_birthday <= 30:  # 一月内生日
            self.birthday_countdown_label.config(fg='#ff6b35')
        else:
            self.birthday_countdown_label.config(fg='#e74c3c')
        
        # 10毫秒后再次更新
        self.root.after(10, self.update_time)

# 运行程序
if __name__ == "__main__":
    app = DesktopWidget()
    app.root.mainloop()
