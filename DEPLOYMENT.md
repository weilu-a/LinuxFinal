# 项目部署指南

## 1. 项目概述

这是一个基于Pygame的多人联机游戏项目，采用客户端-服务器架构。

### 项目结构
```
final/
├── client/          # 客户端代码（需要pygame）
├── server/          # 服务器代码（纯Python，无需pygame）
├── engine/          # 游戏引擎核心
├── data/            # 地图数据
└── requirements.txt # 客户端依赖
```

---

## 2. Linux服务器部署

### 2.1 环境要求
- Python 3.8+
- 网络端口 5555 开放

### 2.2 安装步骤

```bash
# 1. 更新系统
sudo apt update && sudo apt upgrade -y

# 2. 安装Python和虚拟环境
sudo apt install python3 python3-venv -y

# 3. 创建项目目录
mkdir -p ~/game_server
cd ~/game_server

# 4. 使用git克隆项目（或上传项目文件）
git clone <your-repository-url> .

# 5. 创建虚拟环境
python3 -m venv venv

# 6. 激活虚拟环境
source venv/bin/activate

# 7. 服务器端无需安装pygame，直接启动即可
```

### 2.3 启动服务器

```bash
# 进入项目目录
cd ~/game_server

# 激活虚拟环境
source venv/bin/activate

# 启动服务器
python server/main.py
```

### 2.4 后台运行（推荐）

使用 nohup 在后台运行：

```bash
nohup python server/main.py > server.log 2>&1 &
```

查看日志：
```bash
tail -f server.log
```

### 2.5 配置防火墙

确保端口5555对外开放：

```bash
# 检查ufw状态
sudo ufw status

# 允许5555端口
sudo ufw allow 5555/tcp
sudo ufw reload
```

---

## 3. Windows客户端部署

### 3.1 安装步骤

```cmd
# 1. 进入项目目录
cd e:\path\to\final

# 2. 激活虚拟环境
venv\Scripts\activate.bat

# 3. 安装依赖
pip install pygame>=2.5.0

# 4. 修改服务器地址（如果服务器不在本地）
# 编辑 client/constants.py，修改 SERVER_HOST
```

### 3.2 启动客户端

```cmd
python client/game.py
```

---

## 4. 配置说明

### 4.1 服务器配置

服务器默认配置：
- 监听地址：0.0.0.0（所有网络接口）
- 监听端口：5555

### 4.2 客户端配置

编辑 client/constants.py：

```python
SERVER_HOST = 'localhost'  # 修改为服务器IP
SERVER_PORT = 5555
```

---

## 5. 故障排除

### 5.1 客户端无法连接
1. 确认服务器已启动
2. 确认服务器IP和端口正确
3. 确认防火墙已开放端口
4. 确认网络可达（使用 ping 测试）

### 5.2 服务器启动失败
1. 确认Python版本 >= 3.8
2. 确认端口5555未被占用
3. 查看日志文件 server.log

### 5.3 性能问题
- 确保服务器有足够的CPU和内存资源
- 考虑使用进程管理工具（如systemd）

---

## 6. 系统服务配置（可选）

创建 systemd 服务以便开机自启：

```bash
sudo nano /etc/systemd/system/game-server.service
```

添加以下内容：

```ini
[Unit]
Description=Multiplayer Game Server
After=network.target

[Service]
User=your_username
WorkingDirectory=/home/your_username/game_server
Environment="PATH=/home/your_username/game_server/venv/bin"
ExecStart=/home/your_username/game_server/venv/bin/python server/main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable game-server
sudo systemctl start game-server
```

查看状态：

```bash
sudo systemctl status game-server
```