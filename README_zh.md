# 多人联机网格游戏

一个使用 Python、Pygame 和 TCP 网络构建的简单 2D 多人联机网格游戏。

## 功能特性

- **多人联机**: 支持多个客户端连接到中央服务器进行实时游戏
- **实时状态同步**: 玩家位置在所有连接的客户端之间实时同步
- **TCP 网络通信**: 使用 TCP 套接字和 JSON 消息协议进行可靠通信
- **网格世界**: 2D 瓦片地图，包含墙壁和碰撞检测
- **Docker 支持**: 容器化服务器部署，便于托管
- **跨平台**: 服务器运行于 Linux，客户端支持 Windows/Linux

## 快速开始

### 环境要求

- Python 3.8+
- Pygame（客户端）
- Docker（可选，用于容器化部署）

### 安装

```bash
# 克隆仓库
git clone https://github.com/weilu-a/LinuxFinal.git
cd LinuxFinal

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate.bat  # Windows

# 安装依赖（仅客户端）
pip install pygame
```

### 运行游戏

#### 服务器

```bash
# 直接启动服务器
python server/main.py

# 或使用 Docker
docker-compose up -d
```

#### 客户端

```bash
# 连接本地服务器
python client/game.py

# 连接远程服务器（修改 constants.py）
# SERVER_HOST = 'your-server-ip'
```

## 操作说明

- **WASD**: 移动玩家
- **ESC**: 退出游戏

## 项目结构

```
LinuxFinal/
├── client/           # 游戏客户端
│   ├── game.py       # 游戏主循环
│   ├── player.py     # 玩家类
│   ├── network.py    # TCP 客户端
│   ├── input_handler.py  # 输入处理
│   └── constants.py  # 游戏常量
├── server/           # 游戏服务器
│   ├── main.py       # 服务器入口
│   ├── game_server.py    # TCP 服务器逻辑
│   ├── player_manager.py # 玩家状态管理
│   └── protocol.py   # 消息协议
├── engine/           # 游戏引擎
│   ├── grid_world.py # 网格世界
│   └── camera.py     # 静态摄像机
├── data/             # 游戏数据
│   └── maps/         # 地图文件
└── docker-compose.yml # Docker 部署配置
```

## 网络协议

游戏使用基于 JSON 的消息协议：

- `JOIN`: 玩家加入游戏
- `LEAVE`: 玩家离开游戏
- `MOVE`: 玩家位置更新
- `SYNC`: 全局状态同步

## 贡献

欢迎贡献代码！提交 issue 和 pull request 即可。

## 许可证

本项目开源，仅供学习使用。
