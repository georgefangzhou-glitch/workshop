<p align="center">
  <img src="assets/workshop-banner.svg" alt="Quant Research Workshop — questions, evidence, reproducibility" width="100%">
</p>

# Quant Research Workshop

**研究问题 → 可检验假设 → 可复现证据 → 适用边界。**

这是 [@georgefangzhou-glitch](https://github.com/georgefangzhou-glitch) 的量化研究展示工作台。关注 A 股横截面研究中的高频信息日频化、股票关系网络、信号拆解，以及回测结果是否值得相信。

> A research portfolio focused on testable hypotheses, signal decomposition, and reproducible validation. The executable lab uses **synthetic data only**; it is not evidence of investment performance.

| 研究判断 | 验证工程 | 表达与边界 |
| :--- | :--- | :--- |
| 先问信号测量什么，再讨论为什么可能有效 | 检查时序、缺失、分组恒等式与复现性 | 分开写清事实、假设、个人实现和未验证事项 |

## 从这里开始

- **快速了解研究思路：** 浏览下面四个主题。
- **检查工程能力：** 在本地运行合成数据样例和自动测试，全程不需要数据库、密钥或商业数据。
- **查看披露范围：** [公开内容边界](docs/disclosure.md)；[本版验证记录](docs/validation.md)。

## 四个研究主题

主题页展示研究问题和实验设计，**不把未公开的真实研究指标当成已交付证据**。

| 主题 | 想回答的问题 | 当前可公开内容 |
| :--- | :--- | :--- |
| [01 · 关系网络与信息扩散](docs/cases/01-coverage-networks.md) | 股票之间的关联能否带来额外信息，而不仅是行业或规模相似？ | 方法说明、时间可得性与反证设计 |
| [02 · 分量拆解与增量信息](docs/cases/02-signal-decomposition.md) | 一个复合信号的收益，究竟来自哪个分量？ | 消融实验、相关性口径与选择偏差讨论 |
| [03 · 跨股票池适用边界](docs/cases/03-universe-transfer.md) | 全市场有效，是否意味着在不同指数内也有效？ | 历史成分、统一基准与同口径比较框架 |
| [04 · 回测可信度](docs/cases/04-backtest-integrity.md) | 一条漂亮曲线，经过时序和缺失检查后还成立吗？ | 可运行的独立合成数据样例与测试 |

## 两条命令，检查样例

需要 Python **3.10+**，无第三方运行依赖。在仓库根目录执行：

```bash
python -m unittest discover -s tests -v
python -m workshop_lab --output artifacts/demo
```

第二条命令会从固定随机种子生成虚构股票与价格，输出：

```text
artifacts/demo/
├── summary.json     # 数据身份、覆盖数量、相关性和恒等式误差
└── ledger.csv       # 每个合成股票池、每个记账日的对齐与分组结果
```

再次运行时请使用新的输出目录，例如 `artifacts/demo-2`。样例保留预热期与不可计算日期的状态，不删除这些日期来美化结果。

### 这个样例实际验证什么？

1. **可得时间与收益标签：** 收盘后信号只能匹配次日入场；在本例的退出日标记下，收益行在信号日之后两个交易位置。
2. **历史股票池：** 使用信号日成员资格，而不是收益记账日或今天的成员；全市场也不等于几个子池的并集。
3. **缺失与覆盖：** 未知价格不填零，已选股票收益缺失时明确报错，预热期不压缩日历。
4. **分组与相关性：** 检查 `H-L = G10 - G1`、绝对／超额收益还原、逐日 Spearman，以及 `mean(abs(corr))`。

完整的[运行与口径说明](docs/reproducibility.md)区分已验证和没有实现的功能。这里不是生产回测引擎，也没有撮合、冲击成本、融券或容量模型。

## 内容与贡献说明

- 仓库中的 Python 样例为公开展示独立编写，不复制公司研究库；没有连接真实行情源。
- 研究主题页是方法说明，不宣称其中的通用方法或经典研究问题属于原创。
- 使用 AI 辅助整理文档和实现样例；研究解释、代码审阅与可复现性检查仍需由维护者负责。
- 本版不发布真实回测数字、商业数据、私有因子面板、研报全文或公司代码。
- 未默认授予额外的软件或数据许可；若需要复用，请先讨论合适的授权范围。

## 更新

见 [更新记录](CHANGELOG.md)。仅在有新证据、可运行实现或实质性更正时更新，不以提交数量代替研究质量。

**联系：** 请通过本仓库的 GitHub Issues 交流公开方法和样例问题；不要提交商业数据、凭证或未经授权的研究资料。

*Research and educational material, not investment advice. Synthetic results are not live or historical strategy returns.*
