# 项目改造计划：效用AI游戏 → 联机移动游戏

## 当前状态分析

### 项目结构
- **engine/ai/**: 效用AI核心（brain, context, consideration, action）
- **engine/entities/**: NPC实体（依赖AI逻辑）
- **engine/events/**: 事件系统（与AI紧密耦合）
- **engine/pathfinding/**: A*寻路（可能保留用于碰撞检测）
- **engine/grid_world.py**: 格子世界（事件位置相关代码需清理）
- **engine/camera.py**: 摄像机（需改为静态）
- **data/events/**: 7个事件JSON配置
- **data/npcs/**: 3个NPC JSON配置

### 需删除的内容
| 目录/文件 | 原因 |
|----------|------|
| `engine/ai/` | 完整AI逻辑 |
| `engine/entities/` | NPC实体（AI驱动） |
| `engine/events/` | 事件系统（依赖AI） |
| `data/events/` | 7个事件配置文件 |
| `data/npcs/` | 3个NPC配置文件 |
| `data/maps/map_rules.txt` | 事件相关规则文件 |

---

## 改造目标

1. 删除所有AI逻辑
2. 摄像机改为静态（固定在窗口中心）
3. 删除左边的文字显示
4. 添加玩家角色，WASD自由移动（非格子移动）
5. 实现多人联机同步（客户端-服务器模式）
6. 玩家在线时显示角色，离线时隐藏

---

## 具体实施步骤

### 阶段1：清理AI相关代码

**1.1 删除目录**
```
删除:
- engine/ai/ (全部4个文件)
- engine/entities/ (全部2个文件)
- engine/events/ (全部2个文件)
- data/events/ (全部7个JSON)
- data/npcs/ (全部3个JSON)
```

**1.2 修改 engine/__init__.py**
- 移除 AI 相关导入（Context, EventState, Brain, AttributeData）
- 移除 entities 导入（NPC）
- 移除 events 相关导入
- 保留 GridWorld, Camera, AStar, find_path

**1.3 修改 engine/grid_world.py**
- 移除 TILE_TO_EVENT_ID 和 event_positions 相关代码
- 移除 TILE_EVENT_* 常量（保留 TILE_FLOOR, TILE_WALL）
- 移除 get_event_positions(), get_all_event_positions() 方法

### 阶段2：静态摄像机

**2.1 修改 engine/camera.py**
- 将摄像机固定在世界中心
- 移除 update() 中的 WASD 移动逻辑
- 移除鼠标拖拽逻辑
- 移除 target_x, target_y, speed, move_speed 等移动相关属性
- 摄像机位置计算: `x = (world_width - width) / 2`

### 阶段3：创建客户端架构

**3.1 创建 client/ 目录结构**
```
client/
├── __init__.py
├── game.py          # 游戏主循环
├── player.py        # 玩家类
├── network.py       # TCP客户端网络通信
├── input_handler.py # 输入处理
└── constants.py     # 常量配置
```

**3.2 创建 constants.py**
```python
TILE_SIZE = 32
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 24
PLAYER_SPEED = 200  # 像素/秒
SERVER_HOST = 'localhost'
SERVER_PORT = 5555
```

**3.3 创建 player.py**
- Player类：
  - x, y 位置（像素坐标）
  - color 玩家颜色（用于区分不同玩家）
  - player_id 玩家标识
  - is_local 是否本地玩家
- 方法：
  - update(delta_time): 更新位置
  - draw(surface, camera): 绘制玩家

**3.4 创建 input_handler.py**
- 处理WASD键盘输入
- 返回移动方向向量

**3.5 创建 network.py**
- TCP Socket客户端连接
- 发送位置更新到服务器
- 接收服务器广播的其他玩家状态
- 处理连接断开和重连

**3.6 创建 game.py**
- Pygame主循环
- 集成Player、网络通信
- 渲染GridWorld
- 固定摄像机渲染
- 维护在线玩家列表（在线显示，离线隐藏）

### 阶段4：创建服务器端架构

**4.1 创建 server/ 目录结构**
```
server/
├── __init__.py
├── main.py          # 服务器主程序
├── game_server.py   # TCP服务器逻辑
├── player_manager.py # 玩家状态管理
└── protocol.py      # 通信协议定义
```

**4.2 创建 protocol.py**
- 定义消息类型（JSON格式）：
  - JOIN: 玩家加入 `{"type": "join", "player_id": "p1", "name": "Player 1"}`
  - LEAVE: 玩家离开 `{"type": "leave", "player_id": "p1"}`
  - MOVE: 位置更新 `{"type": "move", "player_id": "p1", "x": 100, "y": 200}`
  - SYNC: 状态同步 `{"type": "sync", "players": {...}}`

**4.3 创建 player_manager.py**
- 管理所有连接的玩家
- 存储玩家位置状态
- 处理玩家加入/离开事件
- 维护在线玩家列表

**4.4 创建 game_server.py**
- TCP服务器监听
- 接受客户端连接
- 处理客户端消息
- 广播状态更新到所有客户端

**4.5 创建 main.py**
- 启动TCP服务器
- 运行游戏状态循环

### 阶段5：Docker配置（可选）

**5.1 创建 docker/docker-compose.yml**
- 服务端容器配置
- 客户端容器配置
- 网络端口映射

---

## 文件修改清单

### 需修改的文件
| 文件 | 修改内容 |
|------|---------|
| `engine/__init__.py` | 移除AI/Events/NPC导入 |
| `engine/grid_world.py` | 移除事件系统代码 |
| `engine/camera.py` | 改为静态摄像机 |

### 需删除的目录
| 目录 | 包含文件数 |
|------|----------|
| `engine/ai/` | 5个 |
| `engine/entities/` | 2个 |
| `engine/events/` | 2个 |
| `data/events/` | 7个 |
| `data/npcs/` | 3个 |

### 需新建的文件
| 目录 | 文件 |
|------|------|
| `client/` | __init__.py, game.py, player.py, network.py, input_handler.py, constants.py |
| `server/` | __init__.py, main.py, game_server.py, player_manager.py, protocol.py |

---

## 可行性分析

### 技术可行性
1. **TCP通信**: Python标准库socket模块支持TCP，实现简单可靠
2. **Pygame集成**: Pygame主循环与网络通信可通过线程或asyncio协同
3. **状态同步**: JSON格式消息易于序列化/反序列化
4. **静态摄像机**: 仅需修改camera.py，移除移动逻辑

### 功能可行性
1. **玩家显示逻辑**: 服务器维护在线玩家列表，广播JOIN/LEAVE事件，客户端据此显示/隐藏角色
2. **自由移动**: 使用像素坐标而非格子坐标，实现平滑移动
3. **多人同步**: 服务器作为权威，接收位置更新后广播给所有客户端

### 风险评估
| 风险 | 描述 | 缓解措施 |
|------|------|----------|
| 网络延迟 | 位置更新可能滞后 | 客户端本地预测，服务器权威校正 |
| 并发连接 | 多客户端同步可能冲突 | 服务器统一管理状态，避免客户端直接通信 |
| 断线重连 | 玩家断开后状态丢失 | 服务器保留状态一段时间，支持重连恢复 |

---

## 验证步骤

1. **服务器启动测试**
   - 运行服务器: `python server/main.py`
   - 确认服务器正常监听端口5555

2. **单客户端测试**
   - 运行客户端: `python client/game.py`
   - 玩家可以用WASD移动
   - 摄像机固定不动
   - 位置更新发送到服务器

3. **多客户端联机测试**
   - 启动服务器
   - 启动多个客户端实例
   - 观察不同客户端的玩家位置同步
   - 测试玩家加入/离开时角色显示/隐藏

4. **断线重连测试**
   - 断开一个客户端
   - 观察其他客户端该玩家消失
   - 重新连接后玩家重新出现

5. **功能验证**
   - 确认无AI相关代码残留
   - 确认摄像机固定
   - 确认WASD自由移动
   - 确认联机同步正常工作
