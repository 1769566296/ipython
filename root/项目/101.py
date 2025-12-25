import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *

class DesktopWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.click_through = True  # 默认点击穿透
        self.auto_hide = True      # 默认鼠标移入隐藏
        self.hide_timeout = 2000   # 隐藏超时时间（毫秒）
        self.margin = 10           # 窗口边距
        self.is_hidden = False     # 当前是否隐藏
        self.initUI()
        
    def initUI(self):
        # 设置窗口属性
        self.setWindowTitle('时间纪念日计数器 - 桌面挂件')
        self.setGeometry(100, 100, 400, 600)  # 初始大小
        
        # 设置窗口无边框、置顶、工具窗口样式
        self.setWindowFlags(
            Qt.FramelessWindowHint |      # 无边框
            Qt.WindowStaysOnTopHint |     # 始终置顶
            Qt.Tool |                     # 工具窗口（不在任务栏显示）
            Qt.WindowTransparentForInput  # 初始为点击穿透
        )
        
        # 设置窗口半透明（可选）
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        
        # 创建中央部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建浏览器部件
        self.browser = QWebEngineView()
        self.browser.setContextMenuPolicy(Qt.NoContextMenu)  # 禁用右键菜单
        
        # 加载本地HTML文件
        self.load_html_file()
        
        # 创建控制面板（默认隐藏）
        self.control_panel = self.create_control_panel()
        
        # 添加到布局
        layout.addWidget(self.control_panel)
        layout.addWidget(self.browser)
        
        # 初始隐藏控制面板
        self.control_panel.hide()
        
        # 设置窗口位置（右上角）
        self.move_to_corner()
        
        # 安装事件过滤器
        self.installEventFilter(self)
        
        # 创建隐藏计时器
        self.hide_timer = QTimer()
        self.hide_timer.timeout.connect(self.hide_widget)
        self.hide_timer.setSingleShot(True)
        
        # 创建系统托盘
        self.create_system_tray()
        
        # 应用样式
        self.apply_styles()
        
    def create_control_panel(self):
        """创建控制面板"""
        panel = QWidget()
        panel.setMaximumHeight(40)
        layout = QHBoxLayout(panel)
        layout.setContentsMargins(5, 2, 5, 2)
        
        # 点击穿透复选框
        self.click_through_check = QCheckBox("点击穿透")
        self.click_through_check.setChecked(self.click_through)
        self.click_through_check.stateChanged.connect(self.toggle_click_through)
        
        # 自动隐藏复选框
        self.auto_hide_check = QCheckBox("鼠标移入隐藏")
        self.auto_hide_check.setChecked(self.auto_hide)
        self.auto_hide_check.stateChanged.connect(self.toggle_auto_hide)
        
        # 关闭按钮
        close_btn = QPushButton("×")
        close_btn.setFixedSize(20, 20)
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #999;
                border-radius: 10px;
                background-color: #ff6b6b;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff5252;
            }
        """)
        
        # 设置按钮
        settings_btn = QPushButton("⚙")
        settings_btn.setFixedSize(20, 20)
        settings_btn.clicked.connect(self.show_settings)
        settings_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #999;
                border-radius: 10px;
                background-color: #4a6baf;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3a5a9a;
            }
        """)
        
        # 添加到布局
        layout.addWidget(self.click_through_check)
        layout.addWidget(self.auto_hide_check)
        layout.addStretch()
        layout.addWidget(settings_btn)
        layout.addWidget(close_btn)
        
        return panel
        
    def create_system_tray(self):
        """创建系统托盘"""
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon.fromTheme("clock"))
        
        # 创建托盘菜单
        tray_menu = QMenu()
        
        show_action = tray_menu.addAction("显示挂件")
        show_action.triggered.connect(self.show_widget)
        
        hide_action = tray_menu.addAction("隐藏挂件")
        hide_action.triggered.connect(self.hide_widget)
        
        tray_menu.addSeparator()
        
        settings_action = tray_menu.addAction("设置")
        settings_action.triggered.connect(self.show_settings)
        
        tray_menu.addSeparator()
        
        quit_action = tray_menu.addAction("退出")
        quit_action.triggered.connect(self.quit_application)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
        # 托盘图标点击事件
        self.tray_icon.activated.connect(self.on_tray_activated)
        
    def on_tray_activated(self, reason):
        """托盘图标激活事件"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.toggle_widget_visibility()
            
    def toggle_widget_visibility(self):
        """切换挂件可见性"""
        if self.is_hidden:
            self.show_widget()
        else:
            self.hide_widget()
            
    def show_widget(self):
        """显示挂件"""
        self.show()
        self.is_hidden = False
        self.activateWindow()  # 激活窗口
        
    def hide_widget(self):
        """隐藏挂件到边缘"""
        screen_geometry = QApplication.desktop().screenGeometry()
        
        # 计算隐藏位置（右边只露出5像素）
        x = screen_geometry.width() - 5
        y = self.y()
        
        # 动画隐藏
        animation = QPropertyAnimation(self, b"geometry")
        animation.setDuration(300)
        animation.setStartValue(self.geometry())
        animation.setEndValue(QRect(x, y, 5, self.height()))
        animation.start()
        
        self.is_hidden = True
        
    def move_to_corner(self):
        """移动窗口到屏幕右上角"""
        screen_geometry = QApplication.desktop().screenGeometry()
        x = screen_geometry.width() - self.width() - self.margin
        y = self.margin
        self.move(x, y)
        
    def load_html_file(self):
        """加载HTML文件"""
        # 尝试不同的文件路径
        possible_paths = [
            "101.html",
            "./101.html",
            os.path.expanduser("~/Desktop/101.html"),
            os.path.join(os.path.dirname(__file__), "101.html")
        ]
        
        html_file = None
        for path in possible_paths:
            if os.path.exists(path):
                html_file = path
                break
                
        if html_file:
            # 使用file://协议加载本地文件
            url = QUrl.fromLocalFile(os.path.abspath(html_file))
            self.browser.load(url)
            print(f"已加载HTML文件: {html_file}")
        else:
            # 如果找不到文件，使用示例HTML
            print("未找到101.html文件，使用示例内容")
            self.load_example_html()
            
    def load_example_html(self):
        """加载示例HTML（当找不到文件时使用）"""
        example_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {
                    margin: 0;
                    padding: 0;
                    background: rgba(255, 255, 255, 0.9);
                    border-radius: 15px;
                    font-family: Arial, sans-serif;
                }
                .widget-content {
                    padding: 20px;
                    text-align: center;
                }
                .time {
                    font-size: 48px;
                    color: #ff4500;
                    font-weight: bold;
                    margin: 10px 0;
                }
                .date {
                    font-size: 24px;
                    color: #4a6baf;
                    margin: 10px 0;
                }
                .info {
                    font-size: 14px;
                    color: #666;
                    margin-top: 20px;
                }
            </style>
        </head>
        <body>
            <div class="widget-content">
                <div class="time" id="current-time">--:--:--</div>
                <div class="date" id="current-date">--</div>
                <div class="info">桌面时间挂件<br>双击显示控制面板</div>
            </div>
            <script>
                function updateTime() {
                    const now = new Date();
                    document.getElementById('current-time').textContent = 
                        now.toLocaleTimeString('zh-CN', {hour12: false});
                    document.getElementById('current-date').textContent = 
                        now.toLocaleDateString('zh-CN', {year: 'numeric', month: 'long', day: 'numeric'});
                }
                setInterval(updateTime, 1000);
                updateTime();
            </script>
        </body>
        </html>
        """
        self.browser.setHtml(example_html)
        
    def toggle_click_through(self, state):
        """切换点击穿透"""
        self.click_through = (state == Qt.Checked)
        
        if self.click_through:
            # 启用点击穿透
            self.setWindowFlags(
                self.windowFlags() | Qt.WindowTransparentForInput
            )
            self.control_panel.hide()
        else:
            # 禁用点击穿透
            self.setWindowFlags(
                self.windowFlags() & ~Qt.WindowTransparentForInput
            )
            
        self.show()  # 重新显示以应用新的窗口标志
        
    def toggle_auto_hide(self, state):
        """切换自动隐藏"""
        self.auto_hide = (state == Qt.Checked)
        
    def show_settings(self):
        """显示设置对话框"""
        dialog = QDialog(self)
        dialog.setWindowTitle("挂件设置")
        dialog.setFixedSize(300, 200)
        
        layout = QVBoxLayout(dialog)
        
        # 透明度设置
        opacity_label = QLabel("窗口透明度:")
        opacity_slider = QSlider(Qt.Horizontal)
        opacity_slider.setRange(20, 100)
        opacity_slider.setValue(int(self.windowOpacity() * 100))
        opacity_slider.valueChanged.connect(
            lambda v: self.setWindowOpacity(v / 100.0)
        )
        
        # 大小设置
        size_label = QLabel("窗口大小:")
        size_combo = QComboBox()
        size_combo.addItems(["小 (300x400)", "中 (400x600)", "大 (500x800)"])
        size_combo.currentIndexChanged.connect(self.change_size)
        
        # 位置设置
        pos_label = QLabel("窗口位置:")
        pos_combo = QComboBox()
        pos_combo.addItems(["右上角", "右下角", "左上角", "左下角"])
        pos_combo.currentIndexChanged.connect(self.change_position)
        
        # 保存按钮
        save_btn = QPushButton("保存设置")
        save_btn.clicked.connect(dialog.accept)
        
        layout.addWidget(opacity_label)
        layout.addWidget(opacity_slider)
        layout.addWidget(size_label)
        layout.addWidget(size_combo)
        layout.addWidget(pos_label)
        layout.addWidget(pos_combo)
        layout.addStretch()
        layout.addWidget(save_btn)
        
        dialog.exec_()
        
    def change_size(self, index):
        """改变窗口大小"""
        sizes = [(300, 400), (400, 600), (500, 800)]
        if index < len(sizes):
            self.resize(sizes[index][0], sizes[index][1])
            self.move_to_corner()
            
    def change_position(self, index):
        """改变窗口位置"""
        screen_geometry = QApplication.desktop().screenGeometry()
        positions = [
            (screen_geometry.width() - self.width() - self.margin, self.margin),  # 右上
            (screen_geometry.width() - self.width() - self.margin, 
             screen_geometry.height() - self.height() - self.margin),  # 右下
            (self.margin, self.margin),  # 左上
            (self.margin, screen_geometry.height() - self.height() - self.margin)  # 左下
        ]
        
        if index < len(positions):
            self.move(positions[index][0], positions[index][1])
            
    def apply_styles(self):
        """应用样式表"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 15px;
                border: 2px solid #4a6baf;
            }
            QCheckBox {
                padding: 2px;
                font-size: 11px;
            }
            QCheckBox::indicator {
                width: 12px;
                height: 12px;
            }
        """)
        
    def eventFilter(self, obj, event):
        """事件过滤器"""
        if obj == self:
            if event.type() == QEvent.Enter:
                # 鼠标进入窗口
                if self.auto_hide and not self.is_hidden:
                    self.hide_timer.start(self.hide_timeout)
                    
                # 如果点击穿透启用，显示控制面板
                if self.click_through and not self.control_panel.isVisible():
                    self.control_panel.show()
                    
            elif event.type() == QEvent.Leave:
                # 鼠标离开窗口
                self.hide_timer.stop()
                if self.click_through and self.control_panel.isVisible():
                    self.control_panel.hide()
                    
            elif event.type() == QEvent.MouseButtonDblClick:
                # 双击窗口切换控制面板
                if not self.click_through:
                    if self.control_panel.isVisible():
                        self.control_panel.hide()
                    else:
                        self.control_panel.show()
                        
            elif event.type() == QEvent.MouseMove and not self.click_through:
                # 支持拖动窗口
                if event.buttons() == Qt.LeftButton:
                    self.move(event.globalPos() - self.drag_position)
                    
            elif event.type() == QEvent.MouseButtonPress and not self.click_through:
                # 记录拖动起始位置
                if event.button() == Qt.LeftButton:
                    self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
                    
        return super().eventFilter(obj, event)
        
    def quit_application(self):
        """退出应用程序"""
        self.tray_icon.hide()
        QApplication.quit()
        
    def closeEvent(self, event):
        """关闭事件"""
        event.ignore()  # 忽略关闭事件，最小化到托盘
        self.hide()
        self.is_hidden = True

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # 防止关闭所有窗口时退出
    
    # 设置应用程序信息
    app.setApplicationName("桌面时间挂件")
    app.setApplicationDisplayName("时间纪念日计数器")
    
    widget = DesktopWidget()
    widget.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()