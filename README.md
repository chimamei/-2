# 外星人入侵 (Alien Invasion)

基于Pygame开发的经典2D射击游戏，实现飞船控制、外星人自动射击、升级子弹奖励、动态难度调整等功能，是Python游戏开发的入门实践项目。

## 项目特点
- 核心玩法：玩家操控飞船射击外星人舰队，躲避敌方子弹，随关卡提升难度
- 扩展功能：得分每达到600分可发射强化子弹、实时计分系统、外星人也会随机向飞船发射子弹，多场景音效反馈
- 技术亮点：面向对象封装游戏元素、Sprite精灵组优化碰撞检测、浮点数坐标实现平滑移动

## 运行环境
- Python 3.8+
- Pygame 2.0+

## 安装与启动
### 1. 安装依赖
```bash
pip install pygame
代码运行步骤
git clone https://github.com/chimamei/-2.git
cd -2  # 仓库文件夹名称
python main.py  # Windows
# 或
python3 main.py  # Mac/Linux
