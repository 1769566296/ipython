import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import json
import os
from datetime import datetime
import time
import threading

class DesktopWidget:
    def __init__(self):
        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("时间纪念日计数器 - 桌面挂件")
        
        # 窗口设置
        self.setup_window()
        
        # 控制变量
        self.click_through = tk.BooleanVar(value=False)
        self.auto_hide = tk.BooleanVar(value=True)
        self.always_top = tk.BooleanVar(value=True)
        self.is_hidden = False
        self.drag_data = {"x": 0, "y": 0}
        
        # 创建界面
        self.create_widgets()
        
        # 加载配置
        self.load_config()
        
        # 绑定事件
        self.bind_events()
        
        # 启动时间更新
        self.update_time()
        
        # 启动鼠标检测线程
        self.start_mouse_tracker()
        
    def setup_window(self):
        """设置窗口属性"""
        # 设置窗口大小
        self.root.geometry("400x600")
        
        # 设置窗口位置（右上角）
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = screen_width - 420  # 留出20px边距
        y = 20
        self.root.geometry(f"+{x}+{y}")
        
        # 设置窗口透明色
        self.root.config(bg='#f0f0f0')
        self.root.attributes('-alpha', 0.95)  # 透明度
        
        # 设置窗口置顶
        self.root.attributes('-topmost', True)
        
        # 移除窗口边框
        self.root.overrideredirect(True)
        
    def create_widgets(self):
        """创建界面组件"""
        # 主框架
        main_frame = tk.Frame(self.root, bg='#f0f0f0', 
                             relief='solid', bd=2)
        main_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # 标题栏
        title_bar = tk.Frame(main_frame, bg='#4a6baf', height=30)
        title_bar.pack(fill='x')
        title_bar.pack_propagate(False)  # 固定高度
        
        # 标题
        title_label = tk.Label(title_bar, text="时间纪念日计数器", 
                              bg='#4a6baf', fg='white',
                              font=('Microsoft YaHei', 10, 'bold'))
        title_label.pack(side='left', padx=10)
        
        # 控制按钮区域
        control_frame = tk.Frame(title_bar, bg='#4a6baf')
        control_frame.pack(side='right', padx=5)
        
        # 最小化按钮
        min_btn = tk.Button(control_frame, text="─", 
                           bg='#4a6baf', fg='white',
                           bd=0, font=('Arial', 12),
                           command=self.toggle_hide,
                           activebackground='#3a5a9a')
        min_btn.pack(side='left', padx=2)
        
        # 关闭按钮
        close_btn = tk.Button(control_frame, text="×", 
                             bg='#ff6b6b', fg='white',
                             bd=0, font=('Arial', 12),
                             command=self.quit_app,
                             activebackground='#ff5252')
        close_btn.pack(side='left', padx=2)
        
        # 内容区域
        content_frame = tk.Frame(main_frame, bg='white')
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # 当前时间显示
        time_frame = tk.Frame(content_frame, bg='white')
        time_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(time_frame, text="当前时间", 
                bg='white', font=('Microsoft YaHei', 12),
                fg='#666').pack(anchor='w')
        
        self.time_label = tk.Label(time_frame, 
                                  text="00:00:00",
                                  bg='white',
                                  font=('Microsoft YaHei', 24, 'bold'),
                                  fg='#ff4500')
        self.time_label.pack(anchor='w')
        
        self.date_label = tk.Label(time_frame,
                                  text="2024年1月1日 星期一",
                                  bg='white',
                                  font=('Microsoft YaHei', 12),
                                  fg='#4a6baf')
        self.date_label.pack(anchor='w')
        
        # 分割线
        ttk.Separator(content_frame, orient='horizontal').pack(fill='x', pady=10)
        
        # 生日倒计时
        birthday_frame = tk.Frame(content_frame, bg='white')
        birthday_frame.pack(fill='x', pady=10)
        
        tk.Label(birthday_frame, text="生日倒计时", 
                bg='white', font=('Microsoft YaHei', 12),
                fg='#666').pack(anchor='w')
        
        birthday_input_frame = tk.Frame(birthday_frame, bg='white')
        birthday_input_frame.pack(fill='x', pady=5)
        
        tk.Label(birthday_input_frame, text="生日:", 
                bg='white').pack(side='left')
        
        self.birthday_entry = tk.Entry(birthday_input_frame, width=15)
        self.birthday_entry.pack(side='left', padx=5)
        self.birthday_entry.insert(0, "2007-05-01")
        
        tk.Button(birthday_input_frame, text="设置",
                 command=self.set_birthday,
                 bg='#4a6baf', fg='white',
                 relief='flat').pack(side='left')
        
        self.birthday_countdown = tk.Label(birthday_frame,
                                          text="距离生日还有: -- 天",
                                          bg='white',
                                          font=('Microsoft YaHei', 14),
                                          fg='#ff4500')
        self.birthday_countdown.pack(anchor='w', pady=5)
        
        # 节日倒计时区域
        holiday_frame = tk.Frame(content_frame, bg='white')
        holiday_frame.pack(fill='both', expand=True, pady=10)
        
        tk.Label(holiday_frame, text="近期节日", 
                bg='white', font=('Microsoft YaHei', 12),
                fg='#666').pack(anchor='w')
        
        # 创建滚动区域
        canvas = tk.Canvas(holiday_frame, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(holiday_frame, orient='vertical', 
                                command=canvas.yview)
        self.holiday_scrollable = tk.Frame(canvas, bg='white')
        
        self.holiday_scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.holiday_scrollable, 
                            anchor="nw", width=canvas.winfo_reqwidth())
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 节日数据
        self.holidays = [
            {"name": "春节", "date": "2025-01-29", "days": 0},
            {"name": "元宵节", "date": "2025-02-12", "days": 0},
            {"name": "清明节", "date": "2025-04-04", "days": 0},
            {"name": "劳动节", "date": "2025-05-01", "days": 0},
            {"name": "端午节", "date": "2025-05-31", "days": 0},
            {"name": "中秋节", "date": "2025-09-06", "days": 0},
            {"name": "国庆节", "date": "2025-10-01", "days": 0},
            {"name": "圣诞节", "date": "2025-12-25", "days": 0}
        ]
        
        # 显示节日
        self.display_holidays()
        
        # 控制面板（默认隐藏）
        self.create_control_panel(main_frame)
        
    def create_control_panel(self, parent):
        """创建控制面板"""
        self.control_panel = tk.Frame(parent, bg='#2c3e50', height=80)
        self.control_panel.pack(fill='x')
        self.control_panel.pack_propagate(False)
        
        # 设置内容
        control_content = tk.Frame(self.control_panel, bg='#2c3e50')
        control_content.pack(fill='both', padx=10, pady=5)
        
        # 点击穿透选项
        click_check = tk.Checkbutton(control_content, 
                                    text="点击穿透",
                                    variable=self.click_through,
                                    command=self.toggle_click_through,
                                    bg='#2c3e50', fg='white',
                                    selectcolor='#2c3e50',
                                    activebackground='#2c3e50',
                                    activeforeground='white')
        click_check.pack(anchor='w', pady=2)
        
        # 自动隐藏选项
        hide_check = tk.Checkbutton(control_content,
                                   text="自动隐藏",
                                   variable=self.auto_hide,
                                   bg='#2c3e50', fg='white',
                                   selectcolor='#2c3e50',
                                   activebackground='#2c3e50',
                                   activeforeground='white')
        hide_check.pack(anchor='w', pady=2)
        
        # 始终置顶选项
        top_check = tk.Checkbutton(control_content,
                                  text="始终置顶",
                                  variable=self.always_top,
                                  command=self.toggle_always_top,
                                  bg='#2c3e50', fg='white',
                                  selectcolor='#2c3e50',
                                  activebackground='#2c3e50',
                                  activeforeground='white')
        top_check.pack(anchor='w', pady=2)
        
        # 隐藏控制面板
        self.control_panel.pack_forget()
        
    def display_holidays(self):
        """显示节日列表"""
        for widget in self.holiday_scrollable.winfo_children():
            widget.destroy()
        
        # 计算并排序节日
        today = datetime.now()
        for holiday in self.holidays:
            holiday_date = datetime.strptime(holiday["date"], "%Y-%m-%d")
            days = (holiday_date - today).days
            holiday["days"] = days
        
        # 只显示未来的节日
        future_holidays = [h for h in self.holidays if h["days"] >= 0]
        future_holidays.sort(key=lambda x: x["days"])
        
        # 显示最多8个节日
        for holiday in future_holidays[:8]:
            frame = tk.Frame(self.holiday_scrollable, bg='white')
            frame.pack(fill='x', pady=2)
            
            tk.Label(frame, text=holiday["name"], 
                    bg='white', width=15, anchor='w').pack(side='left')
            
            tk.Label(frame, text=holiday["date"], 
                    bg='white', width=15, anchor='w').pack(side='left')
            
            color = '#2ecc71' if holiday["days"] > 30 else '#e74c3c' if holiday["days"] > 7 else '#ff4500'
            tk.Label(frame, text=f"{holiday['days']}天后", 
                    bg='white', fg=color, anchor='w').pack(side='left')
    
    def bind_events(self):
        """绑定事件"""
        # 标题栏拖动
        self.root.bind('<Button-1>', self.start_drag)
        self.root.bind('<B1-Motion>', self.drag)
        
        # 鼠标进入/离开事件
        self.root.bind('<Enter>', self.on_mouse_enter)
        self.root.bind('<Leave>', self.on_mouse_leave)
        
        # 右键显示控制面板
        self.root.bind('<Button-3>', self.show_control_panel)
        
        # 双击事件
        self.root.bind('<Double-Button-1>', self.toggle_control_panel)
        
        # 快捷键
        self.root.bind('<Escape>', lambda e: self.quit_app())
        self.root.bind('<Control-h>', lambda e: self.toggle_hide())
        
    def start_drag(self, event):
        """开始拖动"""
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        
    def drag(self, event):
        """拖动窗口"""
        x = self.root.winfo_x() + (event.x - self.drag_data["x"])
        y = self.root.winfo_y() + (event.y - self.drag_data["y"])
        
        # 限制窗口在屏幕内
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        
        x = max(0, min(x, screen_width - window_width))
        y = max(0, min(y, screen_height - window_height))
        
        self.root.geometry(f"+{x}+{y}")
        
    def on_mouse_enter(self, event):
        """鼠标进入窗口"""
        if self.auto_hide.get() and self.is_hidden:
            self.show_widget()
            
        # 取消自动隐藏计时
        if hasattr(self, 'hide_timer'):
            self.root.after_cancel(self.hide_timer)
            
    def on_mouse_leave(self, event):
        """鼠标离开窗口"""
        if self.auto_hide.get() and not self.is_hidden:
            # 延迟隐藏
            self.hide_timer = self.root.after(2000, self.auto_hide_widget)
            
    def auto_hide_widget(self):
        """自动隐藏窗口到边缘"""
        if self.auto_hide.get() and not self.is_hidden:
            self.hide_to_edge()
            
    def hide_to_edge(self):
        """隐藏到屏幕边缘"""
        screen_width = self.root.winfo_screenwidth()
        x = screen_width - 20  # 只露出20px
        y = self.root.winfo_y()
        
        # 动画效果
        current_x = self.root.winfo_x()
        for i in range(10):
            new_x = current_x + (x - current_x) * (i + 1) / 10
            self.root.geometry(f"+{int(new_x)}+{y}")
            self.root.update()
            time.sleep(0.01)
        
        self.is_hidden = True
        
    def show_widget(self):
        """显示窗口"""
        screen_width = self.root.winfo_screenwidth()
        x = screen_width - self.root.winfo_width() - 20
        y = self.root.winfo_y()
        
        # 动画效果
        current_x = self.root.winfo_x()
        for i in range(10):
            new_x = current_x + (x - current_x) * (i + 1) / 10
            self.root.geometry(f"+{int(new_x)}+{y}")
            self.root.update()
            time.sleep(0.01)
        
        self.is_hidden = False
        
    def toggle_hide(self):
        """切换隐藏/显示"""
        if self.is_hidden:
            self.show_widget()
        else:
            self.hide_to_edge()
            
    def toggle_click_through(self):
        """切换点击穿透"""
        if self.click_through.get():
            # 设置点击穿透（模拟效果）
            self.root.attributes('-alpha', 0.3)
            self.root.attributes('-topmost', False)
        else:
            self.root.attributes('-alpha', 0.95)
            if self.always_top.get():
                self.root.attributes('-topmost', True)
                
    def toggle_always_top(self):
        """切换始终置顶"""
        self.root.attributes('-topmost', self.always_top.get())
        
    def show_control_panel(self, event):
        """右键显示控制面板"""
        if not self.control_panel.winfo_ismapped():
            self.control_panel.pack(fill='x', before=self.root.winfo_children()[0])
            
    def toggle_control_panel(self, event):
        """双击切换控制面板"""
        if self.control_panel.winfo_ismapped():
            self.control_panel.pack_forget()
        else:
            self.control_panel.pack(fill='x', before=self.root.winfo_children()[0])
            
    def update_time(self):
        """更新时间显示"""
        now = datetime.now()
        
        # 更新时间
        current_time = now.strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        
        # 更新日期
        current_date = now.strftime("%Y年%m月%d日 %A")
        weekday_map = {
            "Monday": "星期一", "Tuesday": "星期二", 
            "Wednesday": "星期三", "Thursday": "星期四",
            "Friday": "星期五", "Saturday": "星期六",
            "Sunday": "星期日"
        }
        for eng, chn in weekday_map.items():
            current_date = current_date.replace(eng, chn)
        self.date_label.config(text=current_date)
        
        # 更新生日倒计时
        self.update_birthday_countdown()
        
        # 每秒更新一次
        self.root.after(1000, self.update_time)
        
    def set_birthday(self):
        """设置生日"""
        birthday_str = self.birthday_entry.get()
        try:
            datetime.strptime(birthday_str, "%Y-%m-%d")
            self.save_config()
            self.update_birthday_countdown()
            messagebox.showinfo("成功", "生日设置成功！")
        except ValueError:
            messagebox.showerror("错误", "日期格式不正确，请使用 YYYY-MM-DD 格式")
            
    def update_birthday_countdown(self):
        """更新生日倒计时"""
        try:
            birthday = datetime.strptime(self.birthday_entry.get(), "%Y-%m-%d")
            today = datetime.now()
            
            # 计算下一个生日
            next_birthday = birthday.replace(year=today.year)
            if next_birthday < today:
                next_birthday = next_birthday.replace(year=today.year + 1)
                
            days_left = (next_birthday - today).days
            
            # 计算年龄
            age = today.year - birthday.year
            if (today.month, today.day) < (birthday.month, birthday.day):
                age -= 1
            next_age = age + 1 if days_left < 365 else age
            
            self.birthday_countdown.config(
                text=f"距离{next_age}岁生日还有: {days_left} 天"
            )
            
            # 更新节日显示
            self.display_holidays()
            
        except ValueError:
            self.birthday_countdown.config(text="生日日期格式错误")
            
    def start_mouse_tracker(self):
        """启动鼠标位置追踪线程"""
        def track_mouse():
            while True:
                try:
                    # 获取鼠标位置
                    x = self.root.winfo_pointerx()
                    y = self.root.winfo_pointery()
                    
                    # 获取窗口位置
                    wx = self.root.winfo_x()
                    wy = self.root.winfo_y()
                    ww = self.root.winfo_width()
                    wh = self.root.winfo_height()
                    
                    # 检查鼠标是否在窗口边缘（用于显示隐藏的窗口）
                    if self.is_hidden and self.auto_hide.get():
                        screen_width = self.root.winfo_screenwidth()
                        if x >= screen_width - 5:  # 鼠标在最右边5px内
                            self.show_widget()
                            
                    time.sleep(0.1)  # 每0.1秒检查一次
                except:
                    break
                    
        thread = threading.Thread(target=track_mouse, daemon=True)
        thread.start()
        
    def load_config(self):
        """加载配置"""
        config_file = "ini.json"
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.birthday_entry.delete(0, tk.END)
                    self.birthday_entry.insert(0, config.get('birthday', '2007-05-01'))
                    self.click_through.set(config.get('click_through', False))
                    self.auto_hide.set(config.get('auto_hide', True))
                    self.always_top.set(config.get('always_top', True))
                    
                    # 应用设置
                    self.toggle_click_through()
                    self.toggle_always_top()
                    
            except:
                pass
                
    def save_config(self):
        """保存配置"""
        config = {
            'birthday': self.birthday_entry.get(),
            'click_through': self.click_through.get(),
            'auto_hide': self.auto_hide.get(),
            'always_top': self.always_top.get()
        }
        
        try:
            with open("ini.json", 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except:
            pass
            
    def quit_app(self):
        """退出应用程序"""
        self.save_config()
        self.root.quit()
        self.root.destroy()

def main():
    """主函数"""
    # 创建并运行应用
    widget = DesktopWidget()
    
    # 设置窗口图标（如果有）
    try:
        widget.root.iconbitmap(default='icon.ico')
    except:
        pass
        
    # 运行主循环
    widget.root.mainloop()

if __name__ == "__main__":
    main()