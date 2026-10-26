<p align="center">
  <img src="assets/workshop-banner.svg" alt="Quant Research Workshop — questions, evidence, reproducibility" width="100%">
</p>

# Quant Research Workshop

**研究问题 → 可检验假设 → 可复现证据 → 适用边界。**

这是 [@georgefangzhou-glitch](https://github.com/georgefangzhou-glitch) 的量化研究展示工作台。关注 A 股横截面研究中的高频信息日频化、股票关系网络、信号拆解，以及回测结果是否值得相信。

> A research portfolio covering ten selected factor topics, a research-environment overview, and reproducible validation. Real factor implementations and commercial data are not published. The separate executable lab uses **synthetic data only**.

| 研究判断 | 验证工程 | 表达与边界 |
| :--- | :--- | :--- |
| 先问信号测量什么，再讨论为什么可能有效 | 检查时序、缺失、分组恒等式与复现性 | 分开写清事实、假设、个人实现和未验证事项 |

## 从这里开始

- **先看研究内容：** [10个因子：英文名称与中文介绍](docs/factors/README.md)。
- **深入看一个案例：** [Analyst Co-Coverage Reversal](docs/factors/analyst-co-coverage-reversal.md)，解释共同覆盖关系、相对反转、版本区别与反证。
- **了解研究环境：** [技术栈、研究流程与验证规范](docs/research-environment.md)，只展示工作方式，不提供内网环境或真实数据接入。
- **查看通用研究思路：** 浏览下面四个主题。
- **检查工程能力：** 在本地运行合成数据样例和自动测试，全程不需要数据库、密钥或商业数据。
- **查看披露范围：** [公开内容边界](docs/disclosure.md)；[本版验证记录](docs/validation.md)。

## Ten Selected Factors

因子采用英文展示名，介绍使用中文。这里只给研究对象与经济假设，**不公开真实因子源码、精确参数、交易信号或绩效数字**；“精选”不是同口径回测排名前十，也不是可交易性认证。

| English name | 中文介绍 |
| :--- | :--- |
| [Analyst Co-Coverage Reversal](docs/factors/analyst-co-coverage-reversal.md) | 利用分析师共同覆盖关系，研究股票相对直接关联公司的价格反应差异与修复可能。 |
| [Residual Non-Isolated Trade Imbalance](docs/factors/residual-non-isolated-trade-imbalance.md) | 观察非孤立成交的买卖不平衡，研究剥离规模与同期涨跌后是否仍有增量信息。 |
| [Turnover Distribution Uniformity](docs/factors/turnover-distribution-uniformity.md) | 从分钟换手率的波动及其跨日稳定性，研究交易活跃度是否均匀分布。 |
| [Information Distribution Uniformity](docs/factors/information-distribution-uniformity.md) | 从日内收益波动的跨日变化，研究价格信息是持续释放还是集中冲击。 |
| [Minute Ideal Amplitude](docs/factors/minute-ideal-amplitude.md) | 比较较高与较低价格位置附近的分钟振幅，区分同样波动背后的不同路径。 |
| [Climb the Peak](docs/factors/climb-the-peak.md) | 联合考察局部波动状态的变化与稳定性，研究价格过程的波动结构。 |
| [Intraday Time-Center Divergence](docs/factors/intraday-time-center-divergence.md) | 比较上涨与下跌发生的时间重心，研究涨跌力量在日内何时集中。 |
| [Upward Price Resonance](docs/factors/upward-price-resonance.md) | 从个股与市场上涨活动的同步程度，研究共同波动之外的截面差异。 |
| [Turnover Growth Stability](docs/factors/turnover-growth-stability.md) | 研究换手率变化是否稳定，而不是单纯寻找换手率高或低的股票。 |
| [Regret-Aversion Buying Volume](docs/factors/regret-aversion-buying-volume.md) | 观察主动买入成交在收盘时的相对价格位置，研究不同成交群体的行为差异。 |

## 四个研究主题

主题页展示通用研究问题和实验设计；上面的因子卡片是具体研究对象。两者都不把未公开的真实指标当成已交付证据。

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
- 十个因子只提供英文名称与中文介绍；原有合成教学样例不是它们的构造源码。研究环境页也不是可下载的公司环境镜像。
- 未默认授予额外的软件或数据许可；若需要复用，请先讨论合适的授权范围。

## 更新

见 [更新记录](CHANGELOG.md)。仅在有新证据、可运行实现或实质性更正时更新，不以提交数量代替研究质量。

**联系：** 请通过本仓库的 GitHub Issues 交流公开方法和样例问题；不要提交商业数据、凭证或未经授权的研究资料。

*Research and educational material, not investment advice. Synthetic results are not live or historical strategy returns.*
