# SubAgents 技术原理解析

## 层次 1: Task Tool (Claude Code 内置)

```python
# 伪代码示例
def launch_subagent(
    subagent_type: str,    # "test-agent", "code-agent", etc.
    prompt: str,           # 任务描述
    model: str = "sonnet"  # 使用的模型
):
    # 1. 创建新的会话
    new_session = Session()

    # 2. 加载 Agent 配置
    agent_config = load_config(f".claude/agents/{subagent_type}.md")

    # 3. 组合系统提示词
    system_prompt = f"""
    {agent_config.role_description}
    {agent_config.responsibilities}
    {agent_config.guidelines}
    """

    # 4. 运行独立上下文
    result = new_session.complete(
        system_prompt=system_prompt,
        user_prompt=prompt,
        tools=agent_config.allowed_tools  # 可选：限制工具访问
    )

    # 5. 返回结果给主 Agent
    return result
```

## 层次 2: Agent SDK (Anthropic 官方)

```python
from anthropic import Anthropic
from claude_agent_sdk import Agent, Tool

# 定义 TestAgent
test_agent = Agent(
    name="TestAgent",
    system_prompt="""You are a QA specialist...
    Write tests first, ensure 80%+ coverage...
    """,
    tools=[  # 限制可用的工具
        Tool.read_file,
        Tool.write_file,
        Tool.bash_command  # 只能运行测试命令
    ]
)

# 定义 CodeAgent
code_agent = Agent(
    name="CodeAgent",
    system_prompt="""You are a developer...
    Follow TDD, maintain code quality...
    """,
    tools=[  # 不同的工具集
        Tool.read_file,
        Tool.write_file,
        Tool.edit_file,
        Tool.bash_command  # 可以运行更多命令
    ]
)

# 编排工作流
def develop_feature(feature_description):
    # 串行执行
    tests = test_agent.run(f"Write tests for: {feature_description}")
    implementation = code_agent.run(f"Implement this: {tests}")
    verification = test_agent.run(f"Verify: {implementation}")

    return verification

# 或并行执行
async def parallel_work():
    results = await asyncio.gather(
        test_agent.run("Test module A"),
        code_agent.run("Implement module B")
    )
    return results
```

## 层次 3: 我们演示的方式（提示词工程）

```markdown
# .claude/agents/test-agent.md
You are a TestAgent...

# .claude/agents/code-agent.md
You are a CodeAgent...

# 用户手动切换
User: "Act as TestAgent and write tests..."
[Claude 读取 test-agent.md，执行任务]

User: "/clear"  # 重置上下文

User: "Act as CodeAgent and implement..."
[Claude 读取 code-agent.md，执行任务]
```

## 关键区别

| 特性 | Task Tool | Agent SDK | 我们的演示 |
|------|-----------|-----------|-----------|
| 上下文隔离 | ✅ 自动 | ✅ 自动 | ⚠️ 手动(/clear) |
| 并行执行 | ✅ 支持 | ✅ 支持 | ❌ 不支持 |
| 工具限制 | ✅ 可配置 | ✅ 可编程 | ❌ 无限制 |
| 状态管理 | ✅ 自动 | ✅ 手动 | ❌ 无状态 |
| 实现难度 | 低 | 中 | 低 |
| 灵活性 | 中 | 高 | 低 |

## 底层通信

```
主 Agent (Claude Code)
    │
    │ Task(tool_use)
    │   {
    │     "subagent_type": "test-agent",
    │     "prompt": "Write tests for PUT endpoint",
    │     "context": {...}
    │   }
    ↓
┌─────────────────────────────────────────┐
│  SubAgent Process (独立 Python 进程)     │
│  ┌─────────────────────────────────────┐ │
│  │ 1. 接收任务                          │ │
│  │ 2. 加载 Agent 配置                   │ │
│  │ 3. 调用 Claude API                   │ │
│  │ 4. 执行工具调用                      │ │
│  │ 5. 返回结果                          │ │
│  └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
    │
    │ TaskResult
    │   {
    │     "status": "success",
    │     "output": "Tests written...",
    │     "artifacts": [...]
    │   }
    ↓
主 Agent 处理结果
```

## 状态共享机制

```python
class AgentState:
    """Agent 之间共享状态"""

    def __init__(self):
        self.shared_context = {}
        self.artifacts = []  # 生成的文件、测试结果等

    def update(self, key, value):
        self.shared_context[key] = value

    def get(self, key):
        return self.shared_context.get(key)

# 使用示例
state = AgentState()

# TestAgent 写完测试后
test_agent.update("test_file", "test_notes.py")
test_agent.update("test_status", "failing")

# CodeAgent 可以访问
test_file = code_agent.state.get("test_file")
# CodeAgent 知道要实现什么来通过测试
```

## 工具访问控制

```python
# TestAgent 只能：
TEST_AGENT_TOOLS = [
    "read_file",      # 读取代码
    "write_file",     # 写测试
    "bash_test",      # 运行 pytest
]

# CodeAgent 可以：
CODE_AGENT_TOOLS = [
    "read_file",
    "write_file",
    "edit_file",      # 编辑代码
    "bash_format",    # black, ruff
    "bash_test",
]

# 通过工具限制实现职责分离
```
