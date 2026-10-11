# Independent four safe-K deletion cuts

The four requested actualinterfaces pass independent source/map/K/pool andcut checks. Adoptedsource is main-input.tex, SHA256 b7a048389c00d075d733581bc98fbfd397765b384777e5959076264ab0dbd557. The proof obligation is that deleting the safe fixedK edges leaves a graph with a nontrivial cut having exactly one remaining edge. A Hamilton cycle cannot be contained in that graph. This establishes a universal intersection with fixedK only on the whole-HC side, not a universal claim about both selected cycles.

## Correct mathematical scope

Let B be the complete HCside graph, K the other side's fixed protected set, and P_B its pool, all in one coordinate system. Put T=(K intersect E(B)) minusP_B, and H=B minusT. Every spanning cycle crosses any nonempty proper vertex set a positive even number of times. If delta_H(U) consists of one edge, an HC of B cannot avoid T. It must use at least one deleted crossing edge, which is in K and outsideP_B. K is already outside its own side's pool. The remaining bridge itself need not belong toK and need not avoid either pool. Minimumdegree2 of H is insufficient to prove a Hamilton cycle exists; all four cases indeed retain minimumdegree2 but have the certified cuts.

The graph/cycle quantified is only B. OppositeK is fixed from the printed template. Source/target role reversal preserves the originalinterface firstnormalizer. Full component classification andselectedcycle pool/reserve containment in the gluing pipeline remain inherited. The argument does not permit arbitrary replacement cycles on the fixedK side or removal of reserve-edge requirements.

## Originalmaps andcoordinate conventions

The supplied bridge names were in originalstandard-source coordinates. In forward cases, this checker transformed the originalsource K,pool andbridge by the originalfirstmap and worked in canonicaltarget HCcoordinates. In reverse, it restored the target K,pool by that same map and worked in the standard source HCcoordinates. No reverse interface or secondnormalizer was introduced.

| Actual interface | Direction | Original firstmap(start,sign,permutation) | HCside |
|---|---|---|---|
|00101 position3→3,target00121|F|(0,+1,[0,1,3,2])|00121:0|
|01014 position2→3,target01024|F|(3,-1,[2,0,3,1])|01024:0|
|01024 position0→3,target01234|R|(0,+1,[2,1,3,0])|01024:0|
|01234 position0→2,target01024|F|(0,+1,[3,1,0,2])|01024:0|

These are actualremaining47record indices12,38,39,44. Every printed cycle/POOL andits exactK subtraction matches this reviewer's own frozenphase10componentbasis. Originaltarget type andexact inverseK/POOL recovery were independently checked. The completeHCside graph was rebuilt from legal one-coordinate mutations of theactual printedvertices, not from the selectedcycleedges. Only two distinctfullgraphs were needed:00121:0 has58vertices/126edges and01024:0 has85vertices/218edges. Ownfrozen wholecomponentclosure is inherited afterexactblock/hash readback, andthe localfullgraph construction also checks allneighbors stay in these vertexsets.

## Concrete cut certificates

All cutsets andedge names below use the HCcoordinates justspecified. The result JSON also records their originalinterface-coordinate versions, allfixedK/pool sets,fullcut edges anddeletedcrossing edges.

For00101 position3→3, take U={23010,23013,23030,23210,23213,23230}. Exactlyone H-edge crosses it:23203–23213. The twelve other fullgraph crossingedges are safe fixedKedges andwere deleted. The supplied originalcoordinate bridge32302–32312 maps to23203–23213. T has37edges globally; H has89edges andminimumdegree2.

For01014 position2→3, take U={13210,13212,13213,23210,23213}. Exactlyone H-edge crosses it:10212–13212. The ten other fullgraph crossingedges are safe fixedKedges andwere deleted. The supplied originalcoordinate bridge30130–30230 maps to10212–13212. T has55edges globally; H has163edges andminimumdegree2.

For01024 position0→3 inreverse, take U={23101,23103,23130,23131,23201,23203,23210,23213,23230,23231}. Exactlyone H-edge crosses it:13130–23130. The fifteen other fullgraph crossingedges are safe fixedKedges andwere deleted. T has44edges globally; H has174edges andminimumdegree2. This remaining bridge belongs to the oppositepool andis therefore outside the fixedprotectedK. That fact is permitted anddoes not weaken the cutproof.

For01234 position0→2 inforward, exactlythe samecanonical01024 graph, T, H, U andbridge occur. Its originalbridge10102–30102 maps to13130–23130. The two colour maps in the last pair are inverse, so no symmetry of an independently chosen cycle orpool is claimed: the literal transformed K,pool andsafe-deletion sets are equal. Bothcases separately retain their originalmap andrecord identity.

The exact shortercut predicates were verified against the actualprintedvertex sets without rerunning thegraphs: firstU is x0x1=23 andx3≠0; secondU is x1x2x3=321; thirdU is x0x1=23. The firstU is not the unrestrictedprefix23cylinder:23203 is an additional legalstate in00121 andis the outsidebridge endpoint. The threepredicates describe6,5,10vertices, butdo not remove the12,10,15actualsafe-crossing membership obligations.

## Failure preservation

The firstpartialattempt interpreted the givenbridge directly in canonicaltarget coordinates andstopped on the firstcase beforewritingresults. Root clarified that givenbridges use originalsource coordinates. Its exactfailedscript anddiagnostic summary are retained. The secondpartialattempt usedcorrectcoordinates butasserted the unnecessarily strong condition that everyfullcutedge avoided bothpools. It stopped beforewritingresults. The correctedscript requires poolavoidance onlyfor thedeletedsafe crossingedges andrecords the survivingbridge poolstatus. That failure andits exactscript are also retained. Finalfour-cut-results.json waswritten onlyafterallfournecessarychecks passed andhasnotbeenmodified.

## Scope andshortness

No rootcuthelper orcomputedcutJSON values were imported/read. Exactlyfourrequesteddirections were checked;root's42eligible/70direction producer and236predicate computation were not repeated. Main andoldrecords were not changed. Existingglobalclassification andownfrozencomponentclosure premises are statedabove;these finitechecks do not certify everymanuscript theorem orformalverification.

The three-cut candidate uses concretecoordinate predicates andthecheckedcutproperty. It is a reviewed mathematical replacement of fourindividualproofpremises, butnot an adopted orrendered wholemanuscript replacement. The fourexisting literalrecord texts total124UTF-8bytes beforeseparators. The standalonecandidate adds a generalcutargument,coordinate conventions,threecutrows andtheactualsafe-crossing conditions. Its bytecomparison is saved separately. Fewerindividualrecords alone doesnot establish a shorterproof orPDF;no43record/shorterpage adoption is recommended fromthisscope.

The additionalconditionalclosure rule was handreviewed in conditional-closure-rule-review.md. Its necessary invariant andcontradiction rules are valid, butthe sixnewcase-specific closuretraces were not independently readback orrecomputed in thisscope. None is labeled independentPASS here. There wasno56direction closureproducer replay andno use of oldintrinsicclosure results asconditionalproofs.
