# Threading Capability Guide

## Product definition

Threading 是一个面向 Research and Design 的 Agent-native、evidence-led 项目工作流。
它可以从零开始、陪伴完整生命周期，也可以接入已经形成的项目，把问题、来源、证据、
洞察、决策、原型、测试和成果连接起来。

Threading is an Agent-native, evidence-led project workflow for Research and Design. It can
start a project, accompany its full lifecycle or join an already-developed project.

## Three entry points

| 入口 | 适合什么情况 | 示例 |
| --- | --- | --- |
| Start | 从一个问题、brief 或设计目标开始 | `帮我新建一个项目空间` |
| Join | Figma、文件、PDF 或聊天记录已经存在 | `帮我接管这个现有项目` |
| Continue | 已经有 Managed Workspace，需要继续推进 | `继续推进这个项目` |

## Natural-language capability menu

### 项目建立与 framing

```text
帮我新建一个项目空间
帮我把这个 brief 变成一个 working question
帮我建立一个 service design project structure
帮我建立一个 evidence-led product design workflow
帮我定义项目的 intended outcome 和当前 uncertainty
```

### Dashboard 与 Current State

```text
Dashboard
现在这个项目进行到哪一步了？
帮我找出这个项目当前真正工作的方向
帮我提出一个 Current State 草案
给我一个有证据支持的 next move
```

### 来源与项目材料

```text
帮我登记这个 Figma 文件
帮我建立这个项目的 source map
帮我整理这个本地项目文件夹
帮我分析这些 PDF，并建立本地 index
```

### Figma 与聊天记录

```text
帮我整理 Figma 的演变
帮我提出最近版本的 current candidate
整理已经导入的聊天记录
从聊天记录中提取 candidate insights 和 decisions
帮我比较聊天记录和当前 Figma 方向
```

### Evidence 与 reasoning

```text
把这段材料整理成 evidence record
帮我区分 observation、interpretation 和 claim
帮我找出这个项目的 evidence gaps
帮我把 evidence chain 补完整
帮我检查这个 claim 是否有足够来源
```

### Decisions、criteria 与 prototypes

```text
帮我整理这个项目已经做过的 decisions
比较这两个方向，并说明它们各自的证据
帮我把旧方向记录为 superseded decision
帮我把 insight 转成 design opportunity
帮我把 opportunity 转成 design criteria
帮我从 criteria 写一个 prototype brief
```

### Testing、iteration 与 writing

```text
帮我为这个 prototype 写 testing plan
帮我记录 response、interpretation 和 design decision
根据 testing feedback 生成下一轮 iteration
帮我把 evidence chain 变成 document outline
帮我检查这段文字的 claim、evidence 和 limitation
帮我整理一个可以交接的 project summary
```

### GSA Pack

```text
加载 GSA Pack
用 Provotyping 方法分析这个项目
用 Stage 3 criteria 检查当前项目
分析这个 Reflection Document
```

### Maintenance

```text
Update Threading
升级 Threading，并接续我已有的项目
Threading doctor
迁移我的旧 Threading profile
显示当前 Threading 和 GSA Pack 版本
```

## How the Agent handles these prompts

自然语言入口不是固定的 slash command。Agent 会把用户的意图路由到对应 workflow，并
在需要读取 Figma、本地文件、PDF、图片或聊天记录时先请求明确权限。

- project sources 先登记，再检查；
- imported material 先标记为 `candidate`；
- Current State 需要 owner 确认；
- superseded decisions 保留在历史记录；
- project knowledge 写入 Git-ignored Managed Workspace；
- GSA Pack 以 linked read-only 方式启用。

自然语言可以表达同一个工作目标的不同说法；如果意图不清楚，Agent 应先问一个最小
澄清问题，而不是猜测项目状态。

## Evidence-to-outcome chain

```text
source → note / observation → interpretation → insight → opportunity
       → criteria → decision → prototype → testing → iteration → outcome
```

Threading 会帮助你记录这条链路，但 method、summary 或 model-generated prose 不会自动
成为 empirical evidence。Claim、decision 和 output 仍然需要 provenance、confirmation
status 和 limitation。

## Public and local boundary

公共仓库提供 reusable core、templates、tools、documentation 和 optional packs。个人项目
资料、raw sources 和 derived project knowledge 保存在用户自己的本地空间；公开仓库不应
包含 participant data、private correspondence 或受限课程原件。
