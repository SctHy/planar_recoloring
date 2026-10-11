Independent verdict: PASS for layer-proof-candidate-v1.tex SHA2567d8db274e8529a31261988b92e2908852a3422952f0c77f5cdda4a5151800d08. No mathematical correction is needed.

The block capacity inequality is valid: after removing the special-edge union, two independently retained sets of sizes x,y in an m-edge universe have at least max(0,x+y-m) common safe edges. Chosen fixed-middle layers and the middle-changing block are pairwise disjoint, so their lower bounds add. The formula for each Cartesian layer and each pair of middle colors counts all edges of the common legal-state graph.

The nine transition families are exhaustive after type ordering E<M<A, color permutations and coordinate reversal. Equal types are retained in the classification. The selected E and A families each give one fixed-boundary edge set, while M has exactly the two coordinate-reversed edge sets. The unused-color swap and A reversal-plus-endpoint-color swap preserve the required edge sets. All336 type-ordered adjacent labelled good-boundary pairs are covered by the nine canonical families; the14 canonical allowed-cycle pairs are all checked without a Hamilton search.

All six appendix layer paths are exact restrictions of the actual printed cycles. The layers not written explicitly follow from the stated symmetries. The three middle-change star descriptions also match those cycles. These are sufficient to derive the seven capacity rows without outside-path profiles:

- E to E end change: the cross block has4 edges and each cycle retains3.
- E repeated-color transfer: the selected square has4 raw edges; the two special edges meet one corner, leaving2 safe edges retained by both cycles.
- E to A middle change: the cross block has exactly2 edges, both retained.
- E to A first-end change: the middle-c square has4 raw edges and one special edge retained by both; its safe universe has3 edges and both cycles retain2. The middle-d edge is safe and retained by both, giving2 across disjoint blocks.
- M to M: the common unused-middle square has4 edges; all four direction combinations retain3 on each side.
- A to A end change: the cross block has6 edges and each cycle retains4.
- A to A middle change: each common endpoint-color layer is a9-edge prism with a selected P6, hence5 retained edges on each side and one guaranteed safe edge per layer.

The E-to-M prism argument covers both target directions with no implicit joint-omission count. In the target image M0(bab), each row triangle contains the one edge used by E; the two rows give distinct safe edges. In M1(bab), both vertical edges used by E are retained. The source E special edges lie in the unused-middle layers, outside the selected middle-b prism; M has no special edges.

The M-to-A argument works for either M direction. In middle-a, the raw9-edge prism contains bab-bac and bab-bad. The M layer isolates bab, and the A path starts bab,dab, so both edges are genuinely omitted by both cycles. Removing them gives a7-edge universe with retained counts3 and5, hence one common edge. In the disjoint middle-c square, retained counts3 and2 out of4 give another. Both special sets are empty, and both omitted edges are legal common-fibre edges. This justifies the omission subtraction without conflating omitted edges with forbidden edges.

The candidate therefore eliminates the complete safe-interface witness table and the twelve outside-path profiles, replacing them by six selected-layer identities, three cross-star rules, seven elementary capacities and two local arguments. It still relies on the selected normalized cycles; the result is not asserted for arbitrary Hamilton cycles. Color permutations and reversal transport the selected-cycle proof to every allowed labelled pair. The main source remains phase6 SHA2567a90f79db489447b0bad3019217fd369a5cc25986288247981cbe7f3462acba3 and was not edited.
