最终 root-created v3 的只读源码、编译及附录视觉核验 PASS。此次未修改任何 candidate 源码或主稿。

- 源码：`layer-capacity-manuscript-candidate-v3.tex`，SHA `3806a0c7f8ec374ea92e70152f939e92e35c3c76564f9e69e8c06160999bcb58`。
- PDF：`layer-capacity-manuscript-candidate-v3.pdf`，SHA `d08e6d71953039e7b4825f76c6a99bb6ca9e9cf49f0d8719054fc4939c5cb042`，42页。
- 结果：`full-candidate-review-v3.json`；精确 diff：`candidate-v3.diff`、`v2-to-v3.diff`；最终日志：`final-latex-v3.log`。

v3 与已完整核验 v2 恰只差公式前一句：`For common endpoint lists L,R and distinct allowed middle colours v,w, the layer H_v is ...`。它明确把 Cartesian-layer/cross-edge 公式限制到共同允许的 middle-colour 列表，且 v≠w，消除了之前的范围读法歧义。所有实际容量表行本来即满足这些条件。去掉该限定后，v3 源码逐字还原 v2，故全部14个 canonical orientation cases 的 source-word核验和独立符号证明原样继承。

41个主要数学陈述、53个marked literal blocks及DE/DM/DA公式与phase6基准逐字一致，55个标签与v2逐字同序，所有引用有效。仅旧safe-witness table辅助标签已在v1/v2移除，没有其他陈述或原有限证书变化。没有outside coordinate-deletion profiles，也没有任意Hamilton cycle的外推。

完整 `latexmk -pdf -interaction=nonstopmode -halt-on-error` 返回0，最终无Warning/Overfull/Underfull，仍42页。已实际渲染和检查附录31页：三圈字面、层支持、允许middle-colour限定和全部七行容量数均整齐，末行与footer分开，无截断或重叠。正文及Verification note继承此前v2的19/27页渲染检查，正文未改。

最终粗略字母token为正文204、附录355、合计559；旧404、layer v1为602，旧DP v1/v2为658/757。完整源码140978字节，phase6原稿140523字节。结果是以更统一的自然边块原则和两个局部机制替代复杂删点资料及逐项共边，在原42页内完成；不能宣称总文字少于旧表方案。

审读时live main为phase6 SHA7a90f79d…。主稿采用由root另行负责。此记录是只读精确delta、完整build及视觉核验，不是形式化证明或正式MRS审稿；没有新graph核或Hamilton搜索。
