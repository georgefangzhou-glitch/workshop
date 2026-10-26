# 04 · 回测可信度：从一条日期链开始

**研究问题：** 结果看起来很好，是否只是信号与收益错配、过滤了未来缺失，或把不同口径混到了一起？

*English summary: A small, inspectable validation lab for timing, missingness, membership, and accounting identities. Passing it is not proof that a real strategy is unbiased.*

## 一条必须能解释的日期链

本例信号在 `t` 收盘后可得，`t+1` 的 VWAP 入场，`t+2` 的 VWAP 退出。收益按**退出日**标记：

```text
signal[t]  →  entry VWAP[t+1]  →  exit VWAP[t+2]
                               return[t+2] = VWAP[t+2]/VWAP[t+1] - 1
```

这里的两个位置来自上述定义，不是所有回测通用的 `shift(2)` 口诀。换成开盘、收盘或其他收益标签，必须重新解释日期链。

## 常见陷阱与样例中的检查

| 陷阱 | 可观察的失败 |
| --- | --- |
| 当天收盘后信号参与当天入场 | 日期配对测试失败 |
| 根据收益记账日成员筛选 | 成员切换边界测试失败 |
| 缺价格时直接填零收益 | 缺失收益阻断测试失败 |
| 只保留有数据的日期再做位移 | 保留预热／缺失日历的测试失败 |
| 把超额收益当绝对收益 | `G10_absolute = G10_excess + benchmark` 不成立 |
| `abs(mean(corr))` 代替每天的接近程度 | 正负相关抵消的测试失败 |

运行方法见[复现说明](../reproducibility.md)，实现位于 [`workshop_lab`](../../workshop_lab)。

## 没有被这组测试证明的事情

没有证明真实历史数据在当时已经可得，没有证明实际可以用全天 VWAP 成交，也没有覆盖退市收益、税费、冲击成本、融券、容量或生产交易系统。这些需要各自的数据和证据。

合成测试可以发现一类实现错误，但不能把一条现实策略认证为“完全无偏”或“可盈利”。

[返回首页](../../README.md)
