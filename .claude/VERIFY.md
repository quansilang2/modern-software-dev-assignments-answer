# 手动验证 Slash Commands

## 在 Claude Code 中使用
直接在对话中输入：
- `/test-format` - 运行测试+格式化+覆盖率
- `/run` - 启动开发服务器
- `/test` - 运行测试
- `/format` - 格式化代码
- `/lint` - Lint 检查

## 在终端手动验证

### 步骤 1: 运行测试
```bash
cd week4
python -m pytest backend/tests -q --maxfail=1 -x
```

### 步骤 2: 格式化代码
```bash
cd week4
python -m black .
python -m ruff check . --fix
```

### 步骤 3: 运行覆盖率报告
```bash
cd week4
python -m pytest backend/tests --cov=backend/app --cov-report=term-missing
```

### 步骤 4: 启动服务器
```bash
cd week4
python -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```
然后访问 http://127.0.0.1:8000/docs

## 预期结果

### 测试结果
- 3 个测试通过
- 2 个 Windows 特定警告（SQLite 清理问题，可忽略）

### 覆盖率报告
- 总覆盖率: ~82%
- 关键模块:
  - models.py: 100%
  - schemas.py: 100%
  - extract.py: 100%
  - main.py: 95%
  - action_items.py: 96%
  - notes.py: 87%
  - db.py: 49%

### Lint 修复
- 应该自动修复 `Optional[str]` → `str | None`
