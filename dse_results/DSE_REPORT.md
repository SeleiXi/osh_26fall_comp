# 探索记录

目标为 4 条题目数据、5 个页框数共 20 个配置的缺页次数 / OPT 比值的等权平均。第 0 个配置（原 WFM）为 1.1870，窗口扫描最佳固定候选（512）为 1.1550。单步和双页上下文转移预测分别进行搜索，均未超过最佳窗口频率方案；对应结果见 `dse_log.csv` 和 `context_log.csv`。

自适应影子策略先比较 WFM-512、原 WFM、LRU，随后加入 MRU，测试不同统计窗口与切换门槛。最终 1024 次统计窗口、16 次切换门槛的四影子方案为 1.1116。`hysteresis_log.csv` 是最终四影子版本，`outputs/hysteresis_1024_16.json` 记录每个配置。选参数据也是报告数据，存在过拟合风险。

独立生成的扫描、热点及阶段变化序列见 `results/synthetic_validation.csv`；其中循环 21 页、20 页框为 387 次，对应 OPT 369 次；阶段切换、20 页框为 126 次，对应 OPT 80 次，仍需改进。Python 在线实现已与 C++ 探索实现的四条 trace、五个页框数逐一比对。以上不证明未知 trace 一定接近 OPT。

实验可执行文件需要自行编译，例如 `g++ -O3 -std=c++17 src/experiments/adaptive.cpp -o dse_results/adaptive.exe`；实验脚本从仓库根目录运行。`adaptive_log.csv` 为早期三影子版本，`hysteresis_log.csv` 为四影子版本。
