# Linux大作业项目规划

## 项目概述

本项目旨在开发一个基于Pygame的简单2D联机游戏，通过完整的服务器部署流程，学习Docker容器化、自动化测试和Linux服务器部署等核心技能。

### 项目目标

- 开发一个可联机的2D小游戏
- 实现客户端-服务器架构
- 使用Docker进行容器化部署
- 编写自动化测试脚本
- 在本地Linux虚拟机中完成部署

---

## 技术栈

| 类别 | 技术选型 |
|------|----------|
| 游戏开发 | Python 3.x + Pygame |
| 网络通信 | Socket / WebSocket |
| 后端服务 | Python (asyncio) |
| 容器化 | Docker + Docker Compose |
| 测试框架 | pytest |
| 部署环境 | Ubuntu Server (本地虚拟机) |
| 版本控制 | Git |

---

## 项目结构

```
final/
├── client/                 # 客户端代码
│   ├── game.py            # 游戏主逻辑
│   ├── network.py         # 网络通信模块
│   └── assets/            # 游戏资源(图片、音效等)
│
├── server/                 # 服务器代码
│   ├── main.py            # 服务器主程序
│   ├── game_manager.py    # 游戏状态管理
│   └── config.py          # 服务器配置
│
├── tests/                  # 测试代码
│   ├── test_client.py     # 客户端测试
│   ├── test_server.py     # 服务器测试
│   └── test_network.py    # 网络通信测试
│
├── docker/                 # Docker配置
│   ├── Dockerfile.client  # 客户端镜像
│   ├── Dockerfile.server  # 服务器镜像
│   └── docker-compose.yml # 编排配置
│
├── scripts/                # 部署脚本
│   ├── build.sh           # 构建脚本
│   ├── deploy.sh          # 部署脚本
│   └── test.sh            # 测试脚本
│
├── docs/                   # 文档
│   └── api.md             # API文档
│
├── requirements.txt        # Python依赖
├── README.md              # 项目说明
└── PROJECT_PLAN.md        # 本规划文档
```

---

## 开发阶段规划

### 阶段一：基础框架搭建 (第1周)

**目标**：完成项目基础结构和开发环境配置

**任务清单**：
- [ ] 初始化Git仓库
- [ ] 创建项目目录结构
- [ ] 编写requirements.txt依赖文件
- [ ] 搭建基础Pygame游戏框架
- [ ] 实现简单的游戏窗口和基本渲染

**验收标准**：
- 能够运行并显示一个空白游戏窗口
- 项目结构清晰，依赖可正确安装



### 阶段三：网络通信实现

**目标**：实现客户端-服务器网络通信

**任务清单**：
- [ ] 设计通信协议(JSON格式)
- [ ] 实现服务器端Socket监听
- [ ] 实现客户端网络连接模块
- [ ] 实现玩家状态同步
- [ ] 处理断线重连逻辑

**验收标准**：
- 多个客户端可以连接到服务器
- 玩家位置能够实时同步

---

### 阶段四：联机游戏完善

**目标**：完善联机游戏功能



**验收标准**：
- 多人可以同时游戏
- 游戏体验流畅，无明显延迟

---

### 阶段五：测试编写

**目标**：编写完整的自动化测试

**任务清单**：
- [ ] 编写单元测试(客户端逻辑)
- [ ] 编写单元测试(服务器逻辑)
- [ ] 编写集成测试(网络通信)
- [ ] 编写端到端测试
- [ ] 配置测试覆盖率报告

**验收标准**：
- 测试覆盖率 > 70%
- 所有测试通过

---

### 阶段六：Docker容器化 (第6周)

**目标**：完成Docker容器化配置

**任务清单**：
- [ ] 编写服务器Dockerfile
- [ ] 编写客户端Dockerfile(可选)
- [ ] 编写docker-compose.yml
- [ ] 配置Docker网络
- [ ] 测试容器间通信

**验收标准**：
- 可以通过docker-compose一键启动
- 容器内服务正常运行

---

### 阶段七：Linux部署

**目标**：在本地Linux虚拟机完成部署

**任务清单**：
- [ ] 准备Ubuntu Server虚拟机
- [ ] 安装Docker和Docker Compose
- [ ] 配置防火墙和端口
- [ ] 部署项目到虚拟机
- [ ] 编写部署文档
- [ ] 测试远程连接

**验收标准**：
- 虚拟机中服务正常运行
- 可以从主机连接到虚拟机中的服务器

---

## Docker配置示例

### 服务器Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server/ ./server/

EXPOSE 5555

CMD ["python", "server/main.py"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  game-server:
    build:
      context: .
      dockerfile: docker/Dockerfile.server
    ports:
      - "5555:5555"
    networks:
      - game-network
    restart: unless-stopped

networks:
  game-network:
    driver: bridge
```

---

## 测试策略

### 单元测试
- 测试独立函数和方法
- 使用mock模拟外部依赖
- 覆盖边界条件和异常情况

### 集成测试
- 测试模块间交互
- 测试数据库/网络操作
- 测试配置加载

### 端到端测试
- 模拟真实用户操作
- 测试完整游戏流程
- 测试多人联机场景

### 测试命令

```bash
# 运行所有测试
pytest tests/

# 运行带覆盖率报告
pytest tests/ --cov=. --cov-report=html

# 运行特定测试文件
pytest tests/test_server.py -v
```

---

## 部署流程

### 本地开发环境

```bash
# 1. 克隆项目
git clone <repository-url>
cd final

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动服务器
python server/main.py

# 5. 启动客户端(另一个终端)
python client/game.py
```

### Docker部署

```bash
# 1. 构建镜像
docker-compose -f docker/docker-compose.yml build

# 2. 启动服务
docker-compose -f docker/docker-compose.yml up -d

# 3. 查看日志
docker-compose -f docker/docker-compose.yml logs -f

# 4. 停止服务
docker-compose -f docker/docker-compose.yml down
```

### Linux虚拟机部署

```bash
# 1. SSH连接虚拟机
ssh user@<vm-ip>

# 2. 安装Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# 3. 安装Docker Compose
sudo apt install docker-compose

# 4. 克隆项目
git clone <repository-url>
cd final

# 5. 启动服务
docker-compose -f docker/docker-compose.yml up -d

# 6. 配置防火墙
sudo ufw allow 5555/tcp
```

---

## 学习要点

### Docker相关
- Dockerfile编写最佳实践
- 镜像层缓存优化
- Docker网络模式
- 数据卷挂载
- Docker Compose服务编排

### 测试相关
- pytest框架使用
- 测试驱动开发(TDD)
- Mock和Patch技术
- 测试覆盖率分析
- 持续集成概念

### Linux部署相关
- SSH远程连接
- 系统服务管理(systemd)
- 防火墙配置(ufw/iptables)
- 日志管理
- 进程监控

---

## 里程碑检查点

| 阶段 | 时间 | 检查内容 |
|------|------|----------|
| M1 | 第2周 | 单机游戏可运行 |
| M2 | 第4周 | 联机功能可用 |
| M3 | 第5周 | 测试全部通过 |
| M4 | 第6周 | Docker部署成功 |
| M5 | 第7周 | 虚拟机部署完成 |

---

## 参考资料

- [Pygame官方文档](https://www.pygame.org/docs/)
- [Python Socket编程](https://docs.python.org/3/library/socket.html)
- [Docker官方文档](https://docs.docker.com/)
- [pytest文档](https://docs.pytest.org/)
- [Ubuntu Server指南](https://ubuntu.com/server/docs)
