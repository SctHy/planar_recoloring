# 固定一侧保护边集的局部准则

固定接口的一侧保护边集为 K，另一侧是有 Hamilton 圈的完整分量 B，
该侧固定 pool 为 P_B。共同合法状态 x 的完整 B 度数记为 d；
在 x 关联、属于 K 和 B 的边且避开 P_B 的边数记为 g。

若 d-g <= 1，则 B 中任意 Hamilton 圈在 x 使用两条边，而这两条边
不可能都来自剩余至多一条边。因此至少一条属于 K 并避 P_B。
固定 K 已避开自身 pool，故这条边同时在两侧指定的保护集内：
把任意圈专门取成原稿指定的 B 分量 Hamilton 圈即可。

Forward (F) 固定原 source K，要求 restored target 分量有 Hamilton 圈，
并计数避 restored target pool 的 source K 边。Reverse (R) 固定按原
接口 first-normalizer 恢复的 target K，要求原 source 分量有 Hamilton
圈，并计数避 source pool 的 restored target K 边。两方向可以按接口
任选，但同一接口不会因此获得任意两侧 Hamilton 圈的量词；固定侧
始终是原指定模板 K。固定 K 侧可为 hard component，不需要 Hamilton
圈。Hard/hard 五个接口不能用本准则。

所有 selector state 都保留原 source 坐标。交换固定侧与 Hamilton 圈
侧不会重新 firstnormalize；原 mapping、component 和 pool 原样使用。
g 可以等于 d，d=2/g=2 也满足准则，不应误写成仅 d-g=1。

本文件先供 root 与 independent transport 审查一般数学机制；21 行
表和 236 实际接口的有限读取另行保留，不能由本机制推出未检查类型
或 pool 的分类结论。当前主稿与 stage9 强三边并集证据均未修改。
