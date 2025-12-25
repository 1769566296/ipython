import pygame
import sys
import math
import random
import numpy as np
from pygame.locals import *

# 初始化pygame
pygame.init()

# 设置窗口尺寸
WIDTH, HEIGHT = 1200, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D立体爱心粒子效果")

# 创建离屏渲染表面
particle_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
heart_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
bg_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

# 颜色定义
BLACK = (0, 0, 0, 255)
RED = (255, 0, 0, 255)
PINK = (255, 105, 180, 255)
DARK_RED = (139, 0, 0, 255)
LIGHT_PINK = (255, 182, 193, 255)
PURPLE = (128, 0, 128, 255)

# 3D颜色渐变
HEART_COLORS = [
    (255, 0, 0),      # 红色 - 最外层
    (255, 20, 147),   # 深粉色
    (255, 105, 180),  # 热粉色
    (255, 182, 193),  # 浅粉色
    (255, 200, 220),  # 更浅粉色 - 最内层
]

# 3D爱心参数
HEART_SCALE = 12
HEART_DEPTH = 5  # 3D深度层数
HEART_OFFSET_X = WIDTH // 2
HEART_OFFSET_Y = HEIGHT // 2 - 50

# 3D粒子类
class Particle3D:
    def __init__(self):
        # 粒子在3D空间中的位置（角度、半径、深度）
        self.angle = random.uniform(0, 2 * math.pi)
        self.radius = random.uniform(0.8, 1.2)  # 爱心半径变化
        self.depth = random.uniform(-1.0, 1.0)  # 深度值，-1到1
        
        # 运动参数
        self.angle_speed = random.uniform(0.003, 0.008)
        self.radius_speed = random.uniform(0.001, 0.003)
        self.depth_speed = random.uniform(0.002, 0.005)
        
        # 粒子物理属性
        self.size = random.uniform(2.5, 5.5)
        self.base_size = self.size
        self.glow_size = self.size * random.uniform(1.5, 2.5)
        
        # 颜色和透明度
        self.base_color = random.choice(HEART_COLORS)
        self.color = self.base_color
        self.alpha = random.randint(180, 255)
        self.alpha_speed = random.uniform(0.5, 1.5)
        
        # 3D投影参数
        self.focal_length = 500
        self.z_offset = 200
        
        # 运动轨迹
        self.trail = []
        self.max_trail_length = random.randint(8, 20)
        self.trail_alpha = 150
        
        # 脉动效果
        self.pulse_speed = random.uniform(0.02, 0.05)
        self.pulse_offset = random.uniform(0, 2 * math.pi)
        
        # 旋转效果
        self.rotation = random.uniform(0, 2 * math.pi)
        self.rotation_speed = random.uniform(-0.02, 0.02)
        
        # 物理模拟
        self.velocity_x = random.uniform(-0.5, 0.5)
        self.velocity_y = random.uniform(-0.5, 0.5)
        self.velocity_z = random.uniform(-0.2, 0.2)
        
    def get_3d_heart_point(self, angle, radius, depth):
        """获取3D爱心形状上的点"""
        t = angle
        # 爱心参数方程
        x = 16 * (math.sin(t) ** 3) * radius
        y = -(13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)) * radius
        
        # 添加深度维度（Z轴）
        z = depth * 3
        
        return x, y, z
    
    def project_3d_to_2d(self, x, y, z):
        """3D投影到2D屏幕"""
        # 透视投影
        scale = self.focal_length / (self.focal_length + z + self.z_offset)
        screen_x = x * scale + HEART_OFFSET_X
        screen_y = y * scale + HEART_OFFSET_Y
        
        return screen_x, screen_y, scale
    
    def update(self, time):
        # 更新3D位置
        self.angle += self.angle_speed
        self.radius += math.sin(time * 0.001) * self.radius_speed
        self.depth += math.sin(time * 0.002) * self.depth_speed
        
        # 限制半径和深度范围
        self.radius = max(0.5, min(1.5, self.radius))
        self.depth = max(-2.0, min(2.0, self.depth))
        
        # 获取3D坐标
        heart_x, heart_y, heart_z = self.get_3d_heart_point(
            self.angle, self.radius, self.depth
        )
        
        # 添加物理运动
        heart_x += self.velocity_x
        heart_y += self.velocity_y
        heart_z += self.velocity_z
        
        # 投影到2D屏幕
        self.screen_x, self.screen_y, self.scale = self.project_3d_to_2d(
            heart_x, heart_y, heart_z
        )
        
        # 根据深度调整大小和颜色
        depth_factor = (self.depth + 2) / 4  # 归一化到0-1范围
        self.size = self.base_size * (0.8 + 0.4 * depth_factor) * self.scale
        
        # 根据深度调整颜色（近处更亮）
        color_factor = 0.7 + 0.3 * depth_factor
        self.color = tuple(
            min(255, int(c * color_factor)) for c in self.base_color
        )
        
        # 脉动效果
        pulse = 0.8 + 0.2 * math.sin(time * self.pulse_speed + self.pulse_offset)
        self.size *= pulse
        
        # 旋转
        self.rotation += self.rotation_speed
        
        # 添加轨迹点
        self.trail.append((self.screen_x, self.screen_y, self.size, self.color))
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)
        
        # 更新透明度（呼吸效果）
        self.alpha = 180 + int(math.sin(time * 0.001 * self.alpha_speed) * 75)
        
    def draw(self, surface):
        # 绘制轨迹（带3D深度效果）
        for i, (trail_x, trail_y, trail_size, trail_color) in enumerate(self.trail):
            # 轨迹越旧，越小越透明
            trail_alpha = int(self.trail_alpha * (i / len(self.trail)))
            trail_current_size = trail_size * (i / len(self.trail))
            
            if trail_current_size > 0.5:
                # 绘制轨迹光晕
                glow_surface = pygame.Surface(
                    (int(trail_current_size * 4), int(trail_current_size * 4)), 
                    pygame.SRCALPHA
                )
                pygame.draw.circle(
                    glow_surface,
                    (*trail_color, trail_alpha // 3),
                    (int(trail_current_size * 2), int(trail_current_size * 2)),
                    int(trail_current_size * 2)
                )
                surface.blit(glow_surface, 
                           (trail_x - trail_current_size * 2, 
                            trail_y - trail_current_size * 2))
                
                # 绘制轨迹核心
                pygame.draw.circle(
                    surface,
                    (*trail_color, trail_alpha),
                    (int(trail_x), int(trail_y)),
                    int(trail_current_size)
                )
        
        # 绘制粒子光晕（3D辉光效果）
        if self.size > 1:
            glow_surface = pygame.Surface(
                (int(self.glow_size * 2), int(self.glow_size * 2)), 
                pygame.SRCALPHA
            )
            
            # 多层光晕增强立体感
            for i in range(3, 0, -1):
                glow_radius = self.glow_size * (i / 3)
                glow_alpha = self.alpha // (i * 2)
                pygame.draw.circle(
                    glow_surface,
                    (*self.color, glow_alpha),
                    (int(self.glow_size), int(self.glow_size)),
                    int(glow_radius)
                )
            
            surface.blit(glow_surface, 
                       (self.screen_x - self.glow_size, 
                        self.screen_y - self.glow_size))
        
        # 绘制粒子核心
        if self.size > 0.5:
            # 绘制具有方向性的粒子（增强3D感）
            particle_surface = pygame.Surface(
                (int(self.size * 2), int(self.size * 2)), 
                pygame.SRCALPHA
            )
            
            # 绘制圆形核心
            pygame.draw.circle(
                particle_surface,
                (255, 255, 255, self.alpha),
                (int(self.size), int(self.size)),
                int(self.size * 0.8)
            )
            
            # 绘制内层（颜色层）
            pygame.draw.circle(
                particle_surface,
                (*self.color, self.alpha),
                (int(self.size), int(self.size)),
                int(self.size * 0.6)
            )
            
            # 绘制高光（增强3D立体感）
            highlight_size = self.size * 0.3
            pygame.draw.circle(
                particle_surface,
                (255, 255, 255, self.alpha // 2),
                (int(self.size * 0.7), int(self.size * 0.7)),
                int(highlight_size)
            )
            
            # 应用旋转
            rotated_particle = pygame.transform.rotate(particle_surface, 
                                                     math.degrees(self.rotation))
            rot_rect = rotated_particle.get_rect(center=(int(self.screen_x), int(self.screen_y)))
            surface.blit(rotated_particle, rot_rect)

# 背景星星类（带3D效果）
class Star3D:
    def __init__(self):
        # 3D位置
        self.x = random.uniform(-WIDTH, WIDTH)
        self.y = random.uniform(-HEIGHT, HEIGHT)
        self.z = random.uniform(0, 1000)
        
        # 外观
        self.base_size = random.uniform(0.1, 1.2)
        self.color = random.choice([(255, 255, 255), (200, 200, 255), (255, 200, 200)])
        
        # 运动
        self.speed = random.uniform(0.1, 0.5)
        self.twinkle_speed = random.uniform(0.5, 2.0)
        
    def update(self, time):
        # 向屏幕移动（产生3D景深效果）
        self.z -= self.speed
        if self.z <= 0:
            self.z = 1000
            self.x = random.uniform(-WIDTH, WIDTH)
            self.y = random.uniform(-HEIGHT, HEIGHT)
    
    def draw(self, surface):
        # 透视投影
        scale = 500 / (self.z + 500)
        screen_x = self.x * scale + WIDTH // 2
        screen_y = self.y * scale + HEIGHT // 2
        size = self.base_size * scale
        
        if 0 <= screen_x < WIDTH and 0 <= screen_y < HEIGHT:
            # 闪烁效果
            twinkle = (math.sin(time * 0.001 * self.twinkle_speed) + 1) / 2
            alpha = int(100 + 155 * twinkle)
            
            # 绘制星星
            if size > 0.3:
                star_surface = pygame.Surface((int(size * 4), int(size * 4)), pygame.SRCALPHA)
                pygame.draw.circle(
                    star_surface,
                    (*self.color, alpha),
                    (int(size * 2), int(size * 2)),
                    int(size)
                )
                surface.blit(star_surface, (screen_x - size * 2, screen_y - size * 2))

# 创建3D粒子
particles_3d = [Particle3D() for _ in range(400)]

# 创建3D星星背景
stars_3d = [Star3D() for _ in range(150)]

# 创建爱心轮廓点（用于绘制边缘光晕）
heart_outline_points = []
for t in np.linspace(0, 2 * math.pi, 200):
    x = 16 * (math.sin(t) ** 3) * HEART_SCALE
    y = -(13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)) * HEART_SCALE
    heart_outline_points.append((x + HEART_OFFSET_X, y + HEART_OFFSET_Y))

# 主循环
clock = pygame.time.Clock()
font_large = pygame.font.SysFont(None, 48)
font_small = pygame.font.SysFont(None, 32)

running = True
while running:
    current_time = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_SPACE:
                # 空格键重新生成粒子
                particles_3d = [Particle3D() for _ in range(400)]
            elif event.key == K_UP:
                HEART_SCALE = min(20, HEART_SCALE + 1)
            elif event.key == K_DOWN:
                HEART_SCALE = max(5, HEART_SCALE - 1)
    
    # 清空所有渲染表面
    screen.fill(BLACK)
    particle_surface.fill((0, 0, 0, 0))
    heart_surface.fill((0, 0, 0, 0))
    bg_surface.fill((0, 0, 0, 0))
    
    # 更新和绘制3D星星背景
    for star in stars_3d:
        star.update(current_time)
        star.draw(bg_surface)
    
    # 绘制爱心轮廓光晕（增强立体感）
    for i in range(len(heart_outline_points)):
        x1, y1 = heart_outline_points[i]
        x2, y2 = heart_outline_points[(i + 1) % len(heart_outline_points)]
        
        # 绘制多层光晕线
        for j in range(5, 0, -1):
            glow_width = j * 2
            glow_alpha = 30 // j
            
            pygame.draw.line(
                heart_surface,
                (255, 100, 100, glow_alpha),
                (int(x1), int(y1)),
                (int(x2), int(y2)),
                glow_width
            )
    
    # 更新和绘制3D粒子
    for particle in particles_3d:
        particle.update(current_time)
        particle.draw(particle_surface)
    
    # 将所有层合成到主屏幕
    screen.blit(bg_surface, (0, 0))
    screen.blit(heart_surface, (0, 0))
    screen.blit(particle_surface, (0, 0))
    
    # 绘制3D信息面板
    info_panel = pygame.Surface((300, 150), pygame.SRCALPHA)
    info_panel.fill((0, 0, 0, 150))
    
    # 绘制面板边框
    pygame.draw.rect(info_panel, (255, 100, 100, 200), info_panel.get_rect(), 2)
    
    # 添加文字信息
    title = font_large.render("3D爱心粒子", True, LIGHT_PINK)
    info_panel.blit(title, (10, 10))
    
    particle_count = font_small.render(f"粒子数量: {len(particles_3d)}", True, (255, 255, 255))
    info_panel.blit(particle_count, (10, 60))
    
    controls = font_small.render("↑↓调整大小 空格重置 ESC退出", True, (200, 200, 200))
    info_panel.blit(controls, (10, 100))
    
    screen.blit(info_panel, (10, 10))
    
    # 绘制深度指示器
    depth_indicator = pygame.Surface((200, 30), pygame.SRCALPHA)
    depth_indicator.fill((0, 0, 0, 150))
    pygame.draw.rect(depth_indicator, (255, 255, 255, 100), depth_indicator.get_rect(), 1)
    
    depth_text = font_small.render("3D深度效果", True, (255, 255, 255))
    screen.blit(depth_text, (WIDTH - 210, HEIGHT - 80))
    
    # 更新显示
    pygame.display.flip()
    
    # 控制帧率
    clock.tick(60)

# 退出pygame
pygame.quit()
sys.exit()