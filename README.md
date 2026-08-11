# Threading

> **中文**：一个 local-first、Agent-native 的研究与设计项目工作区，把 brief、sources、evidence、decisions、prototypes、testing 和 writing 连成一条可追溯的链。
>
> **English**: A local-first, Agent-native workspace that connects briefs, sources, evidence, decisions, prototypes, testing and writing into one traceable chain.

Threading is an independent project. Its optional GSA Pack is a course-derived
academic context for Design Innovation-related workflows; it is not produced,
approved, sponsored or endorsed by Glasgow School of Art (GSA).

[中文说明](#中文说明) · [English](#english) · [Licensing](#许可与版权--licensing)

## 中文说明

### 这是什么

Threading 不是一个 Web Dashboard，也不是一个把项目上传到云端的服务。它
是一套在 Codex Agent 或其他 repository-aware Agent 中运行的本地工作流：

```text
Brief → Sources → Evidence → Interpretation → Decision
      → Prototype → Test → Iteration → Writing
```

它帮助你：

- 把项目 brief 变成可工作的 research / design question；
- 记录 Figma、桌面文件夹或其他 repository 的 source pointer；
- 区分原始材料、观察、interpretation、claim、criterion 和 decision；
- 追踪 prototype、testing、iteration 以及仍然缺失的证据；
- 在本地 Managed Workspace 中保留自己的项目 context，而不污染 reusable core。

Threading 不会替你生成证据、自动导入项目材料、提供 ethics approval，或证明
一个设计已经有效。

完整产品仍然是 Threading Workspace；可安装 Skill 是自然语言入口，不是项目
存储空间。每个学校或研究项目的本地知识保存在
`projects/local/<slug>/`，而公共规则、工具和 GSA Pack 保持在可更新的 core。

### 快速开始

先把公开仓库 Clone 到本地，然后在仓库目录中打开 Codex Agent：

```bash
git clone https://github.com/51younglowkey/Threading.git
cd Threading
```

然后对 Agent 说：

```text
Dashboard
```

为了让这些自然语言入口在其他 Codex 项目中也能稳定触发，可以安装仓库内的
Threading skill：

```bash
python3 90_scripts_tools/threading/install_skill.py
```

然后新建一个 Codex 任务并说：

```text
帮我接管这个现有项目
```

Agent 会按照 `docs/AGENT_ONBOARDING.md` 创建完整的 Managed Workspace。
默认位置是 `projects/local/<slug>/`，该目录被 Git 忽略，不会进入 Threading
公共仓库。Figma、本地文件夹和完整聊天导出可以留在原位；经过确认的 derived
knowledge、Current State、decisions 和 outputs 会保存在本地 Workspace。

接管一个已有项目：

```bash
python3 90_scripts_tools/project_workspace/adopt_project.py \
  --slug my-project \
  --title "My project" \
  --pack none
```

如果你明确需要 GSA Pack：

```bash
python3 90_scripts_tools/project_workspace/adopt_project.py \
  --slug my-project \
  --title "My project" \
  --pack gsa
```

已有 Managed Workspace 也可以在确认路径后启用：

```bash
python3 90_scripts_tools/project_workspace/manage_pack.py \
  --project projects/local/my-project \
  --enable-gsa
```

### 可选 GSA Pack

GSA Pack 不会默认启用。它采用 linked、read-only activation，不会复制到项目中，
也不会被项目分析污染。它包括：

- Semester 1 / Semester 2 taught-method catalogues；
- Provotyping 方法说明；
- Reflection Document guidance-video analysis protocol；
- Stage 3 ILO、rubric 和 audit scaffold 的 operational paraphrase。

它是 independent academic pack，不是官方 GSA 文件。公开版不会包含课程 PDF、
assessment form、guidance video、字幕或 displayed student examples。重要的
assessment wording 仍然要以用户有权访问的当前官方 source 为准。

### 独立的 PDF / 图片分析工具

`90_scripts_tools/pdf_method_index/` 是一个**单独启用的本地工具**，不是普通
Threading onboarding 的必需步骤。它可以读取用户明确授权的本地 PDF、PNG、JPG、
JPEG、WEBP、TIFF 或 BMP 文件，并生成带 source label、hash、页码/图像编号和
OCR 文本的本地检索索引。

```text
自己的 PDF / 图片
→ 本地 OCR index
→ 搜索关键词并定位页码或图像
→ 人工检查原始页面
→ 写入自己的 evidence / reading note
```

原始文件不会上传到 Threading，也不会自动复制到公共仓库。索引是 retrieval
aid，不是经过验证的 quotation，也不会自动把 OCR 文本变成 project claim。
使用说明、边界和可选依赖见：

```text
90_scripts_tools/pdf_method_index/README.md
90_scripts_tools/pdf_method_index/requirements-optional.txt
```

### 公共仓库的使用方式

普通使用者不需要成为 collaborator，也不需要 push 权限。他们可以公开查看、
Clone、下载并在自己的本地 Agent 中使用；如果要修改 Threading，应通过自己的
fork 和 pull request 提交。不要把个人项目、participant data、private
correspondence、calendar、raw recording、课程原件或绝对本机路径提交到这里。

### 许可证和版权

- 原始脚本和工具：MIT License；
- 原始文档、模板、示例和独立 paraphrased guidance：CC BY 4.0；
- 第三方课程材料、assessment source、论文和图像：保留其原有权利。

详细边界见 `NOTICE.md`、`THIRD_PARTY_NOTICES.md` 和
`docs/PROVENANCE_AND_LICENSING.md`。

## English

### What this is

Threading is a local-first, Agent-native workspace rather than a web dashboard
or a hosted project service. It gives a project a traceable working structure:

```text
Brief → Sources → Evidence → Interpretation → Decision
      → Prototype → Test → Iteration → Writing
```

It helps an Agent and a project owner to:

- turn an initial brief into a working research or design question;
- record pointers to Figma, desktop folders and other repositories;
- keep raw material, observations, interpretations, claims, criteria and
  decisions distinct;
- connect prototypes to learning questions, tests and iteration records;
- keep project-specific context in a user-owned Managed Workspace rather than in
  the reusable core.

Threading does not invent evidence, automatically import project files, provide
ethics approval or prove that an intervention works.

The complete product remains the Threading Workspace. The installable Skill is a
natural-language entry point, not project storage. Each school or research
project keeps its local knowledge under `projects/local/<slug>/`, while the
reusable rules, tools and GSA Pack remain in the updateable public core.

### Quick start

Clone the public repository locally and open the folder in Codex Agent:

```bash
git clone https://github.com/51younglowkey/Threading.git
cd Threading
```

Then say:

```text
Dashboard
```

The Agent follows `docs/AGENT_ONBOARDING.md` one question at a time and creates
a complete user-owned Managed Workspace. Install the optional natural-language
skill first when Threading should be available from other Codex projects:

```bash
python3 90_scripts_tools/threading/install_skill.py
```

Then start a new Codex task and say `adopt this existing project`. The default
workspace location is `projects/local/<slug>/`, which is ignored by Git and is
not part of the public Threading repository. Raw Figma, local-folder and chat
sources may stay in place while confirmed derived knowledge is stored locally.

Adopt an existing project:

```bash
python3 90_scripts_tools/project_workspace/adopt_project.py \
  --slug my-project \
  --title "My project" \
  --pack none
```

Select the independent GSA Pack only when it is relevant:

```bash
python3 90_scripts_tools/project_workspace/adopt_project.py \
  --slug my-project \
  --title "My project" \
  --pack gsa
```

An existing Managed Workspace can enable it after the user confirms the path:

```bash
python3 90_scripts_tools/project_workspace/manage_pack.py \
  --project projects/local/my-project \
  --enable-gsa
```

### Optional GSA Pack

The GSA Pack is opt-in and uses linked, read-only activation. It contains taught-method catalogues, a Provotyping note,
a reflection-document guidance-video analysis protocol, and an operational
paraphrase of Stage 3 ILO, rubric and audit logic.

It is an independent academic pack, not an official GSA product. The public
repository does not bundle course PDFs, assessment forms, guidance videos,
subtitles or displayed student examples. For consequential assessment decisions,
verify the current authorised official source.

### Standalone PDF / image indexing

`90_scripts_tools/pdf_method_index/` is an optional local analysis tool. It can
index explicitly authorised PDF, PNG, JPG, JPEG, WEBP, TIFF and BMP files, then
return source-linked OCR results by keyword and page or image number.

```text
your PDF / image files
→ local OCR index
→ keyword search and page/image locator
→ visual check of the original source
→ write a bounded evidence or reading note into your Managed Workspace
```

The original files are not uploaded or copied into the public repository. The
index is a retrieval aid, not verified quotation or evidence by itself. See:

```text
90_scripts_tools/pdf_method_index/README.md
90_scripts_tools/pdf_method_index/requirements-optional.txt
```

### Public repository use

Users do not need collaborator access or push permission to use Threading. They
can view, clone and download it, then run it in their own local Agent. Changes to
Threading should come through a fork and pull request. Do not commit personal
projects, participant data, private correspondence, calendars, recordings,
restricted course originals or absolute local paths.

### Licensing

- Original scripts and tools: MIT License.
- Original documentation, templates, examples and independent paraphrased
  guidance: CC BY 4.0.
- Third-party course materials, assessment sources, papers and images retain
  their original rights.

See `NOTICE.md`, `THIRD_PARTY_NOTICES.md` and
`docs/PROVENANCE_AND_LICENSING.md` for the detailed boundary.

<a id="许可与版权--licensing"></a>

Threading is an independent personal/community project. The optional GSA Pack
is not produced, approved, sponsored or endorsed by Glasgow School of Art.
