固定层容量路线已有完整证明候选，所有研究文件独立保存，主稿未改。

初始纯 middle-layer 计数的精确禁边损失公式是 `max(0,a+b−m−x−y+f)`：a,b 是原占边数，x,y 是各自占用禁边数，f 是禁边并集数。九族中仅四族给出至少二；失败族 aab→aac、aab→acb、aab→bab、aba→cba、abc→abd 的最小容量分别为 1,1,0,1,0。结果见 `layer-capacity-results-v1.json`。这些失败是真实的容量缺口，不是 safe-common-edge lemma 的反例。EE aab→aac 的两个 square 各只有一个实际安全共边，不能重用错误的“同一 square 有二”论证。

把所有改变 middle coordinate 的边另作一个自然、与固定层不交的边块，容量直接覆盖七族，只剩 EM、MA 两族。`layer-capacity-results-v2.json` 保存其 14 个 canonical orientation cases；没有重跑原接口全核或 Hamilton 搜索。三组选定循环在 middle-colour 投影上均是一个三点 star，每条 star link 有两条改色边，总计四条。这使 EE aac、EA acb、AA abd 的共同 cross-edge 宇宙与双方保边数分别为 `(4,3,3),(2,2,2),(6,4,4)`，直接容斥给二。

完整候选 `layer-proof-candidate-v1.tex` 用安全边宇宙 `(m,x,y)` 的通用分块容斥，给七行可见容量数。其余四族的自然 block 分别是 EE abb 的安全 square `(2,2,2)`、EA cab 的安全 square 加 K2 `(3,2,2)+(1,1,1)`、MM aca 的 Q4 `(4,3,3)`、AA adc 的两个 prism，各 `(9,5,5)`。这些 graph universes 由共同 endpoint lists 的 Cartesian products 和 middle-coordinate 改色边直接计数。

EM 的共同 middle-b prism 中，E 保一条每 row triangle 的边和两条 rung；M0 包含前两条，M1 包含后两条。MA 的共同 middle-a prism 中，M 隔离 bab，A 在该层只用 bab–dab，所以双方遗漏 bab–bac、bab–bad；宇宙从九减至七，双方占三和五，得一；共同 middle-c square 的 3+2−4 再给一。不需要原 DP 的第三条跨层遗漏，也不需要任何十二个 outside coordinate-deletion profiles。

`check_layer_proof_v1.py` 直接从冻结的原 `eq:path232-cycles` 读字面，不导入旧 checker。它解析候选中的六条层路径描述、七行容量数，核验所有 14 个 canonical orientation cases、三个 star 规律、EM 的两种包含机制和 MA 两方向的两条共同遗漏。`layer-proof-review-v1.json` 为 PASS。色置换、反射的 fixed-boundary stabilizers 也从原三个边集直接核验，支持全部原 allowed-cycles 量词；不声称任意 Hamilton cycles 具有这些支持。

与旧全局 DP 的关系：把每个自然边块的安全占边数相加可恢复全局边数，但逐块取正部保留了某些块的正容量，避免其他块负容量的抵消。这是真正不同的证法组织，取消十二项删点路径资料；它仍使用原三个选定循环的单侧层支持。不能把完整共同-unused edges 枚举再加到容量中冒充结构证明；候选只用 MA 的两条解析遗漏。

本地候选 proof 为粗略字母 token 318，附录支持 284，合计 602；旧 proof+conventions/table 为404，phase7 v1/v2 为658/757。当前完整适配版仍43页，原稿42页。因此它简化了推理机制并比 phase7 短，但尚不能称相对原稿的篇幅压缩。主稿仍 SHA7a90f79d…。完整候选、编译和源码保存记录另在 `continuation-8/path232-candidate/`。
