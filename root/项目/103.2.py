import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime, timedelta
import time
import threading
from math import floor

class DesktopWidget:
    def __init__(self):
        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("时间计数器")
        
        # 窗口设置
        self.setup_window()
        
        # 控制变量
        self.click_through = tk.BooleanVar(value=False)
        self.auto_hide = tk.BooleanVar(value=False)  # 默认关闭自动隐藏
        self.always_top = tk.BooleanVar(value=True)
        self.is_hidden = False
        self.drag_data = {"x": 0, "y": 0}
        
        # 数据变量
        self.birthday = "2007-05-04"
        self.custom_events = []
        
        # 右键菜单相关变量
        self.selected_event_id = None
        self.event_context_menu = None
        
        # 创建界面
        self.create_widgets()
        
        # 设置右键菜单
        self.setup_right_click_menu()
        
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
        self.root.geometry("420x700")
        
        # 设置窗口位置（右上角）
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = screen_width - 440  # 留出20px边距
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
        
        # 隐藏按钮
        hide_btn = tk.Button(control_frame, text="▁", 
                           bg='#4a6baf', fg='white',
                           bd=0, font=('Arial', 12),
                           command=self.toggle_hide,
                           activebackground='#3a5a9a')
        hide_btn.pack(side='left', padx=2)
        
        # 关闭按钮
        close_btn = tk.Button(control_frame, text="×", 
                             bg='#ff6b6b', fg='white',
                             bd=0, font=('Arial', 12),
                             command=self.quit_app,
                             activebackground='#ff5252')
        close_btn.pack(side='left', padx=2)
        
        # 内容区域
        content_frame = tk.Frame(main_frame, bg='white')
        content_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # ========== 当前时间显示 ==========
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
        
        # ========== 已活天数计算 ==========
        lived_frame = tk.Frame(content_frame, bg='white')
        lived_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(lived_frame, text="已活天数", 
                bg='white', font=('Microsoft YaHei', 12),
                fg='#666').pack(anchor='w')
        
        self.lived_days_label = tk.Label(lived_frame,
                                        text="计算中...",
                                        bg='white',
                                        font=('Microsoft YaHei', 16, 'bold'),
                                        fg='#9b59b6')
        self.lived_days_label.pack(anchor='w')
        
        # ========== 生日设置 ==========
        birthday_frame = tk.Frame(content_frame, bg='white')
        birthday_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(birthday_frame, text="生日设置", 
                bg='white', font=('Microsoft YaHei', 12),
                fg='#666').pack(anchor='w')
        
        # 生日输入区域
        birthday_input_frame = tk.Frame(birthday_frame, bg='white')
        birthday_input_frame.pack(fill='x', pady=5)
        
        # 年份
        year_frame = tk.Frame(birthday_input_frame, bg='white')
        year_frame.pack(side='left', padx=(0, 10))
        tk.Label(year_frame, text="年:", bg='white').pack(side='left')
        self.year_var = tk.StringVar(value="2007")
        year_spinbox = tk.Spinbox(year_frame, from_=1900, to=2100, 
                                 textvariable=self.year_var, width=6,
                                 command=self.update_birthday)
        year_spinbox.pack(side='left', padx=2)
        
        # 月份
        month_frame = tk.Frame(birthday_input_frame, bg='white')
        month_frame.pack(side='left', padx=(0, 10))
        tk.Label(month_frame, text="月:", bg='white').pack(side='left')
        self.month_var = tk.StringVar(value="5")
        month_spinbox = tk.Spinbox(month_frame, from_=1, to=12, 
                                  textvariable=self.month_var, width=4,
                                  command=self.update_birthday)
        month_spinbox.pack(side='left', padx=2)
        
        # 日期
        day_frame = tk.Frame(birthday_input_frame, bg='white')
        day_frame.pack(side='left')
        tk.Label(day_frame, text="日:", bg='white').pack(side='left')
        self.day_var = tk.StringVar(value="1")
        day_spinbox = tk.Spinbox(day_frame, from_=1, to=31, 
                                textvariable=self.day_var, width=4,
                                command=self.update_birthday)
        day_spinbox.pack(side='left', padx=2)
        
        # 生日倒计时
        self.birthday_countdown_label = tk.Label(birthday_frame,
                                                text="距离下次生日还有: -- 天",
                                                bg='white',
                                                font=('Microsoft YaHei', 12),
                                                fg='#ff4500')
        self.birthday_countdown_label.pack(anchor='w', pady=(5, 0))
        
        self.next_age_label = tk.Label(birthday_frame,
                                      text="这将是你第 -- 岁生日",
                                      bg='white',
                                      font=('Microsoft YaHei', 10),
                                      fg='#666')
        self.next_age_label.pack(anchor='w')
        
        # 分割线
        ttk.Separator(content_frame, orient='horizontal').pack(fill='x', pady=10)
        
        # ========== 自定义事件 ==========
        event_frame = tk.Frame(content_frame, bg='white')
        event_frame.pack(fill='both', expand=True)
        
        # 事件标题和添加按钮
        event_header = tk.Frame(event_frame, bg='white')
        event_header.pack(fill='x', pady=(0, 10))
        
        tk.Label(event_header, text="自定义倒计时", 
                bg='white', font=('Microsoft YaHei', 12),
                fg='#666').pack(side='left')
        
        add_event_btn = tk.Button(event_header, text="+ 添加事件",
                                 command=self.add_custom_event,
                                 bg='#3498db', fg='white',
                                 relief='flat', font=('Microsoft YaHei', 9))
        add_event_btn.pack(side='right')
        
        # 创建滚动区域用于事件列表
        event_canvas = tk.Canvas(event_frame, bg='white', highlightthickness=0, height=200)
        event_scrollbar = tk.Scrollbar(event_frame, orient='vertical', 
                                      command=event_canvas.yview)
        self.event_scrollable = tk.Frame(event_canvas, bg='white')
        
        self.event_scrollable.bind(
            "<Configure>",
            lambda e: event_canvas.configure(scrollregion=event_canvas.bbox("all"))
        )
        
        event_canvas.create_window((0, 0), window=self.event_scrollable, 
                                 anchor="nw", width=event_canvas.winfo_reqwidth())
        event_canvas.configure(yscrollcommand=event_scrollbar.set)
        
        event_canvas.pack(side="left", fill="both", expand=True)
        event_scrollbar.pack(side="right", fill="y")
        
        # 控制面板（默认隐藏）
        self.create_control_panel(main_frame)
        
    def create_control_panel(self, parent):
        """创建控制面板"""
        self.control_panel = tk.Frame(parent, bg='#2c3e50', height=100)
        self.control_panel.pack(fill='x')
        self.control_panel.pack_propagate(False)
        
        
        # 隐藏控制面板
        self.control_panel.pack_forget()
        
    def setup_right_click_menu(self):
        """设置右键菜单"""
        # 为事件区域创建右键菜单
        self.event_context_menu = tk.Menu(self.root, tearoff=0, bg='white', fg='black')
        # 设置内容
        control_content = tk.Frame(self.control_panel, bg='#2c3e50')
        control_content.pack(fill='both', padx=10, pady=5)
        # 右键菜单样式
        self.event_context_menu.config(
            font=('Microsoft YaHei', 9),
            activebackground='#4a6baf',
            activeforeground='white'
        )
        
        # 添加菜单项
        self.event_context_menu.add_command(
            label="📝 编辑事件",
            command=self.edit_selected_event,
            accelerator="Enter"
        )
        
        self.event_context_menu.add_command(
            label="🗑️ 删除事件",
            command=self.delete_selected_event,
            accelerator="Del"
        )
        
        self.event_context_menu.add_separator()
        
        self.event_context_menu.add_command(
            label="📋 复制事件信息",
            command=self.copy_event_info
        )
        
        self.event_context_menu.add_command(
            label="📅 添加到日历提醒",
            command=self.add_to_calendar_reminder
        )


        
        # 批量操作按钮
        batch_frame = tk.Frame(control_content, bg='#2c3e50')
        batch_frame.pack(fill='x', pady=(10, 0))
        
        tk.Button(batch_frame, text="删除过期事件",
                  command=self.delete_past_events,
                  bg='#e74c3c', fg='white',
                  font=('Microsoft YaHei', 9), width=15).pack(side='left', padx=2)
        
        tk.Button(batch_frame, text="删除所有事件",
                  command=self.delete_all_events,
                  bg='#c0392b', fg='white',
                  font=('Microsoft YaHei', 9), width=15).pack(side='left', padx=2)


        
        
        #  自动隐藏选项（默认关闭）
        # hide_check = tk.Checkbutton(control_content,
        #                            text="自动隐藏（移出窗口2秒后隐藏到边缘）",
        #                            variable=self.auto_hide,
        #                            bg='#2c3e50', fg='white',
        #                            selectcolor='#2c3e50',
        #                            activebackground='#2c3e50',
        #                            activeforeground='white')
        # hide_check.pack(anchor='w', pady=2)
        
       
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
        
        


        # 绑定键盘快捷键
        self.root.bind('<Delete>', lambda e: self.delete_selected_event())
        self.root.bind('<Return>', lambda e: self.edit_selected_event())
        
    def show_event_context_menu(self, event, event_id):
        """显示事件右键菜单"""
        self.selected_event_id = event_id
        
        # 显示菜单
        try:
            self.event_context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            # 确保释放菜单
            self.event_context_menu.grab_release()
            
    # ========== 天数计算函数 ==========
    
    def calculate_lived_days(self):
        """计算已活天数"""
        try:
            birth_date = datetime.strptime(self.birthday, "%Y-%m-%d")
            now = datetime.now()
            lived_days = (now - birth_date).days
            return lived_days
        except:
            return 0
    
    def calculate_birthday_countdown(self):
        """计算生日倒计时"""
        try:
            birth_date = datetime.strptime(self.birthday, "%Y-%m-%d")
            now = datetime.now()
            
            # 计算下一个生日
            next_birthday = birth_date.replace(year=now.year)
            if next_birthday < now:
                next_birthday = next_birthday.replace(year=now.year + 1)
            
            # 计算天数差
            days_left = (next_birthday - now).days
            
            # 计算下一个生日的年龄
            next_age = now.year - birth_date.year
            if (now.month, now.day) < (birth_date.month, birth_date.day):
                next_age += 1
            else:
                next_age += 1 if days_left < 365 else 0
            
            return days_left, next_age
        except:
            return 0, 0
    
    def calculate_days_until(self, target_date_str):
        """计算到目标日期的天数"""
        try:
            target_date = datetime.strptime(target_date_str, "%Y-%m-%d")
            now = datetime.now()
            days = (target_date - now).days
            return max(days, 0)  # 返回0或正数
        except:
            return -1
    
    def format_large_number(self, num):
        """格式化大数字，添加千位分隔符"""
        return f"{num:,}"
    
    # ========== 事件处理函数 ==========
    
    def update_birthday(self):
        """更新生日日期"""
        try:
            year = int(self.year_var.get())
            month = int(self.month_var.get())
            day = int(self.day_var.get())
            
            # 验证日期有效性
            datetime(year, month, day)
            self.birthday = f"{year:04d}-{month:02d}-{day:02d}"
            self.save_config()
        except ValueError:
            messagebox.showerror("错误", "无效的日期")
    
    def add_custom_event(self):
        """添加自定义事件"""
        # 创建对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("添加倒计时事件")
        dialog.geometry("300x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - dialog.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # 事件名称
        tk.Label(dialog, text="事件名称:").pack(anchor='w', padx=20, pady=(20, 5))
        event_name_var = tk.StringVar()
        event_name_entry = tk.Entry(dialog, textvariable=event_name_var, width=30)
        event_name_entry.pack(padx=20)
        
        # 事件日期
        tk.Label(dialog, text="事件日期 (YYYY-MM-DD):").pack(anchor='w', padx=20, pady=(10, 5))
        event_date_var = tk.StringVar()
        event_date_entry = tk.Entry(dialog, textvariable=event_date_var, width=30)
        event_date_entry.pack(padx=20)
        event_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # 事件描述
        tk.Label(dialog, text="事件描述 (可选):").pack(anchor='w', padx=20, pady=(10, 5))
        event_desc_var = tk.StringVar()
        event_desc_entry = tk.Entry(dialog, textvariable=event_desc_var, width=30)
        event_desc_entry.pack(padx=20)
        
        def save_event():
            name = event_name_var.get().strip()
            date_str = event_date_var.get().strip()
            
            if not name:
                messagebox.showerror("错误", "请输入事件名称")
                return
            
            if not date_str:
                messagebox.showerror("错误", "请输入事件日期")
                return
            
            try:
                # 验证日期格式
                datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("错误", "日期格式错误，请使用 YYYY-MM-DD 格式")
                return
            
            event = {
                "id": len(self.custom_events),
                "name": name,
                "date": date_str,
                "desc": event_desc_var.get().strip(),
                "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            self.custom_events.append(event)
            self.save_config()
            self.display_custom_events()
            dialog.destroy()
            
            messagebox.showinfo("成功", "事件添加成功")
        
        # 按钮区域
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="取消", command=dialog.destroy).pack(side='left', padx=10)
        tk.Button(button_frame, text="保存", command=save_event, bg='#4a6baf', fg='white').pack(side='left', padx=10)
    
    def display_custom_events(self):
        """显示自定义事件列表"""
        # 清除现有事件
        for widget in self.event_scrollable.winfo_children():
            widget.destroy()
        
        if not self.custom_events:
            no_event_label = tk.Label(self.event_scrollable, 
                                     text="暂无自定义事件\n点击右上角'+添加事件'按钮创建",
                                     bg='white', fg='#999',
                                     font=('Microsoft YaHei', 10))
            no_event_label.pack(pady=20)
            return
        
        # 按日期排序
        sorted_events = sorted(self.custom_events, key=lambda x: x['date'])
        
        for event in sorted_events:
            days = self.calculate_days_until(event['date'])
            
            event_frame = tk.Frame(self.event_scrollable, bg='white', 
                                   relief='ridge', bd=1)
            event_frame.pack(fill='x', pady=3, padx=5)
            
            # 左侧信息区域
            info_frame = tk.Frame(event_frame, bg='white')
            info_frame.pack(side='left', fill='both', expand=True, padx=5, pady=3)
            
            # 事件名称（第一行）
            name_frame = tk.Frame(info_frame, bg='white')
            name_frame.pack(fill='x')
            
            name_label = tk.Label(name_frame, text=event['name'], 
                                 bg='white', font=('Microsoft YaHei', 10, 'bold'),
                                 anchor='w')
            name_label.pack(side='left')
            
            # 倒计时天数
            if days >= 0:
                color = '#2ecc71' if days > 30 else '#e74c3c' if days > 7 else '#ff4500'
                days_text = f"{days}天后" if days > 0 else "就是今天！"
            else:
                color = '#999'
                days_text = "已过期"
            
            days_label = tk.Label(name_frame, text=days_text, 
                                 bg='white', font=('Microsoft YaHei', 9),
                                 fg=color, anchor='w')
            days_label.pack(side='right', padx=(10, 0))
            
            # 事件日期和描述（第二行）
            date_desc_frame = tk.Frame(info_frame, bg='white')
            date_desc_frame.pack(fill='x')
            
            date_label = tk.Label(date_desc_frame, text=event['date'], 
                                 bg='white', font=('Microsoft YaHei', 8),
                                 fg='#666', anchor='w')
            date_label.pack(side='left')
            
            # 事件描述（如果有）
            if event.get('desc'):
                desc_label = tk.Label(date_desc_frame, text=f" | {event['desc']}", 
                                     bg='white', font=('Microsoft YaHei', 8),
                                     fg='#999', anchor='w')
                desc_label.pack(side='left', padx=(5, 0))
            
            # ========== 绑定右键事件 ==========
            def make_right_click_handler(event_id):
                return lambda e: self.show_event_context_menu(e, event_id)
            
            # 绑定到事件框架
            right_click_handler = make_right_click_handler(event['id'])
            event_frame.bind("<Button-3>", right_click_handler)
            info_frame.bind("<Button-3>", right_click_handler)
            name_frame.bind("<Button-3>", right_click_handler)
            date_desc_frame.bind("<Button-3>", right_click_handler)
            name_label.bind("<Button-3>", right_click_handler)
            days_label.bind("<Button-3>", right_click_handler)
            date_label.bind("<Button-3>", right_click_handler)
            if event.get('desc'):
                desc_label.bind("<Button-3>", right_click_handler)
            
            # 添加鼠标悬停效果
            def on_enter(e):
                event_frame.config(bg='#f0f8ff')  # 浅蓝色背景
                info_frame.config(bg='#f0f8ff')
                date_desc_frame.config(bg='#f0f8ff')
                name_frame.config(bg='#f0f8ff')
                name_label.config(bg='#f0f8ff')
                days_label.config(bg='#f0f8ff')
                date_label.config(bg='#f0f8ff')
                if event.get('desc'):
                    desc_label.config(bg='#f0f8ff')
            
            def on_leave(e):
                event_frame.config(bg='white')
                info_frame.config(bg='white')
                date_desc_frame.config(bg='white')
                name_frame.config(bg='white')
                name_label.config(bg='white')
                days_label.config(bg='white')
                date_label.config(bg='white')
                if event.get('desc'):
                    desc_label.config(bg='white')
            
            event_frame.bind("<Enter>", on_enter)
            event_frame.bind("<Leave>", on_leave)
            info_frame.bind("<Enter>", on_enter)
            info_frame.bind("<Leave>", on_leave)
            
            # 添加右键提示标签
            hint_label = tk.Label(event_frame, 
                                 text="🖱️ 右键菜单",
                                 bg='white', 
                                 font=('Microsoft YaHei', 7),
                                 fg='#4a6baf',
                                 cursor='hand2')
            hint_label.pack(side='right', padx=5)
            hint_label.bind("<Button-3>", right_click_handler)
            
            # 绑定左键清除选中
            event_frame.bind("<Button-1>", lambda e: self.clear_event_selection())
    
    def delete_event(self, event_id):
        """删除事件"""
        # 找到要删除的事件
        event_to_delete = None
        for event in self.custom_events:
            if event['id'] == event_id:
                event_to_delete = event
                break
        
        if event_to_delete:
            # 确认对话框
            response = messagebox.askyesno(
                "确认删除",
                f"确定要删除事件 '{event_to_delete['name']}' 吗？\n"
                f"日期: {event_to_delete['date']}\n"
                f"此操作不可撤销！"
            )
            
            if response:
                # 从列表中删除
                self.custom_events = [e for e in self.custom_events if e['id'] != event_id]
                
                # 重新生成ID，保持连续
                for i, event in enumerate(self.custom_events):
                    event['id'] = i
                
                # 保存配置
                self.save_config()
                
                # 刷新显示
                self.display_custom_events()
                
                # 清除选中的事件ID
                self.selected_event_id = None
                print("ok6666")
                # messagebox.showinfo("成功", "事件已删除")
    
    def delete_selected_event(self):
        """删除选中的事件"""
        if self.selected_event_id is not None:
            self.delete_event(self.selected_event_id)
    
    def edit_selected_event(self):
        """编辑选中的事件"""
        if self.selected_event_id is not None:
            self.edit_event_dialog(self.selected_event_id)
    
    def edit_event_dialog(self, event_id):
        """编辑事件对话框"""
        # 找到要编辑的事件
        event_to_edit = None
        for event in self.custom_events:
            if event['id'] == event_id:
                event_to_edit = event
                break
        
        if not event_to_edit:
            return
        
        # 创建对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("编辑事件")
        dialog.geometry("300x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - dialog.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # 事件名称
        tk.Label(dialog, text="事件名称:").pack(anchor='w', padx=20, pady=(20, 5))
        event_name_var = tk.StringVar(value=event_to_edit['name'])
        event_name_entry = tk.Entry(dialog, textvariable=event_name_var, width=30)
        event_name_entry.pack(padx=20)
        
        # 事件日期
        tk.Label(dialog, text="事件日期 (YYYY-MM-DD):").pack(anchor='w', padx=20, pady=(10, 5))
        event_date_var = tk.StringVar(value=event_to_edit['date'])
        event_date_entry = tk.Entry(dialog, textvariable=event_date_var, width=30)
        event_date_entry.pack(padx=20)
        
        # 事件描述
        tk.Label(dialog, text="事件描述 (可选):").pack(anchor='w', padx=20, pady=(10, 5))
        event_desc_var = tk.StringVar(value=event_to_edit.get('desc', ''))
        event_desc_entry = tk.Entry(dialog, textvariable=event_desc_var, width=30)
        event_desc_entry.pack(padx=20)
        
        def save_edited_event():
            name = event_name_var.get().strip()
            date_str = event_date_var.get().strip()
            
            if not name:
                messagebox.showerror("错误", "请输入事件名称")
                return
            
            if not date_str:
                messagebox.showerror("错误", "请输入事件日期")
                return
            
            try:
                # 验证日期格式
                datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("错误", "日期格式错误，请使用 YYYY-MM-DD 格式")
                return
            
            # 更新事件
            for event in self.custom_events:
                if event['id'] == event_id:
                    event['name'] = name
                    event['date'] = date_str
                    event['desc'] = event_desc_var.get().strip()
                    event['modified'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    break
            
            self.save_config()
            self.display_custom_events()
            dialog.destroy()
            messagebox.showinfo("成功", "事件已更新")
        
        def delete_and_close():
            dialog.destroy()
            self.delete_event(event_id)
        
        # 按钮区域
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="取消", command=dialog.destroy).pack(side='left', padx=5)
        tk.Button(button_frame, text="删除", command=delete_and_close,
                 bg='#ff6b6b', fg='white').pack(side='left', padx=5)
        tk.Button(button_frame, text="保存", command=save_edited_event, 
                 bg='#4a6baf', fg='white').pack(side='left', padx=5)
    
    def copy_event_info(self):
        """复制事件信息到剪贴板"""
        if self.selected_event_id is not None:
            for event in self.custom_events:
                if event['id'] == self.selected_event_id:
                    info = f"{event['name']}\n日期: {event['date']}\n"
                    
                    # 计算倒计时
                    days = self.calculate_days_until(event['date'])
                    if days > 0:
                        info += f"倒计时: 还有{days}天"
                    elif days == 0:
                        info += "倒计时: 就是今天！"
                    else:
                        info += f"状态: 已过期{-days}天"
                    
                    if event.get('desc'):
                        info += f"\n备注: {event['desc']}"
                    
                    # 复制到剪贴板
                    self.root.clipboard_clear()
                    self.root.clipboard.append(info)
                    
                    # 显示提示
                    messagebox.showinfo("复制成功", "事件信息已复制到剪贴板")
                    break
    
    def add_to_calendar_reminder(self):
        """添加到日历提醒（示例功能）"""
        if self.selected_event_id is not None:
            messagebox.showinfo("提示", "日历提醒功能需要系统支持\n此功能为示例功能")
    
    def delete_past_events(self):
        """删除已过期的事件"""
        current_date = datetime.now().strftime("%Y-%m-%d")
        past_events = [e for e in self.custom_events if e['date'] < current_date]
        
        if not past_events:
            messagebox.showinfo("提示", "没有已过期的事件")
            return
        
        response = messagebox.askyesno(
            "确认删除过期事件",
            f"确定要删除 {len(past_events)} 个已过期的事件吗？"
        )
        
        if response:
            self.custom_events = [e for e in self.custom_events if e['date'] >= current_date]
            
            # 重新生成ID
            for i, event in enumerate(self.custom_events):
                event['id'] = i
            
            self.save_config()
            self.display_custom_events()
            messagebox.showinfo("成功", f"已删除 {len(past_events)} 个过期事件")
    
    def delete_all_events(self):
        """删除所有事件"""
        if not self.custom_events:
            messagebox.showinfo("提示", "没有可删除的事件")
            return
        
        response = messagebox.askyesno(
            "确认删除全部",
            f"确定要删除所有 {len(self.custom_events)} 个事件吗？\n此操作不可撤销！"
        )
        
        if response:
            self.custom_events = []
            self.save_config()
            self.display_custom_events()
            messagebox.showinfo("成功", "所有事件已删除")
    
    # ========== 窗口控制函数 ==========
    
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
        
        # 绑定左键清除事件选择
        self.root.bind('<Button-1>', lambda e: self.clear_event_selection())
    
    def clear_event_selection(self):
        """清除事件选择"""
        self.selected_event_id = None
    
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
        pass
    
    def on_mouse_leave(self, event):
        """鼠标离开窗口"""
        pass
    
    def toggle_hide(self):
        """隐藏窗口（最小化到任务栏）"""
        self.root.withdraw()  # 隐藏窗口
        self.is_hidden = True
    
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
            
    # ========== 更新函数 ==========
    
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
        
        # 更新已活天数
        lived_days = self.calculate_lived_days()
        self.lived_days_label.config(text=f"{self.format_large_number(lived_days)} 天")
        
        # 更新生日倒计时
        days_left, next_age = self.calculate_birthday_countdown()
        self.birthday_countdown_label.config(
            text=f"距离下次生日还有: {days_left} 天"
        )
        self.next_age_label.config(
            text=f"这将是你第 {next_age} 岁生日"
        )
        
        # 更新自定义事件显示
        self.display_custom_events()
        
        # 每秒更新一次
        self.root.after(1000, self.update_time)
    
    # ========== 配置管理 ==========
    
    def load_config(self):
        """加载配置"""
        config_file = "ini.json"
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.birthday = config.get('birthday', '2007-05-04')
                    self.click_through.set(config.get('click_through', False))
                    self.auto_hide.set(config.get('auto_hide', False))
                    self.always_top.set(config.get('always_top', True))
                    self.custom_events = config.get('custom_events', [])
                    
                    # 更新生日输入框
                    if self.birthday:
                        try:
                            birth_date = datetime.strptime(self.birthday, "%Y-%m-%d")
                            self.year_var.set(str(birth_date.year))
                            self.month_var.set(str(birth_date.month))
                            self.day_var.set(str(birth_date.day))
                        except:
                            pass
                    
                    # 应用设置
                    self.toggle_click_through()
                    self.toggle_always_top()
                    
            except Exception as e:
                print(f"加载配置错误: {e}")
                
    def save_config(self):
        """保存配置"""
        config = {
            'birthday': self.birthday,
            'click_through': self.click_through.get(),
            'auto_hide': self.auto_hide.get(),
            'always_top': self.always_top.get(),
            'custom_events': self.custom_events
        }
        
        try:
            with open("ini.json", 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存配置错误: {e}")
    
    # ========== 其他函数 ==========
    
    def start_mouse_tracker(self):
        """启动鼠标位置追踪线程"""
        def track_mouse():
            while True:
                try:
                    time.sleep(0.1)  # 每0.1秒检查一次
                except:
                    break
                    
        thread = threading.Thread(target=track_mouse, daemon=True)
        thread.start()
    
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