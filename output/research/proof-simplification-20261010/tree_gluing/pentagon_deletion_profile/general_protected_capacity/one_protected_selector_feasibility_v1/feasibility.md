# One fixed protected side: finite selector feasibility

The frozen observations are sufficient for exact reuse. They save all313
original interface identities, original target first maps, all10706 forward and
10808 reverse local observations, HC-side full degrees, safe fixed-K neighbor
lists, and actual source-coordinate words. This job rereads those observations
and optimizes word masks; it does not compute any graph or normalization map.

## Actual result and the current125 comparison

| Selector scheme | Covered nonconstant interfaces | Source rows | Word memberships | Distinct selected words | Residual individual interfaces |
| --- | ---: | ---: | ---: | ---: | ---: |
| Current three-edge-union scheme | 125 | 15 | 48 | 27 | 158 |
| Independently select all one-fixed-side positives | 236 | 21 | 78 | 47 | 47 |
| Select only111 additional positives | 111 additional | 18 | 64 additional | 42 in added table | 47 after retaining125 |
| Retain current48 memberships, add exact minimum | 236 total | 21 total | 92 total (44 added) | 48 total | 47 |

The current125 identities are a subset of the236 frozen one-fixed-side positive
identities. Retained selector words already support34 of the111 additional
interfaces under the weaker one-fixed-side criterion. Only16 of the18 extra
source rows require new words; source00121 and00124 need none. Six source rows
are newly introduced relative to the current15. The44 added memberships contain
33 different words, and the union with the current27 words contains48 words.

Two endpoint-word occurrences per residual individual edge plus selector-word
memberships gives the rough comparison364(current),172(full re-selection),
186(retained125 plus extras). This proxy omits safe K membership, pool exclusion,
full-degree premises, interface directions and original-map restoration. It is
not a proof-length or page-count result. No full manuscript candidate is written.

The47 residual identities split into28 ordinary/ordinary,7 hard-source/ordinary-
target,7 ordinary-source/hard-target and5 hard/hard. The30 constant-source cases
are intentionally outside the optimization. The frozen overall count266/308
therefore remains unchanged.

## Exact statement and quantifiers

Let v be a common actual state. On the fixed side let K be the prescribed
protected edge set, already excluding that side's pool. On the opposite side
let G be the full component graph with degree d at v and prescribed pool Q.
Let g be the number of edges incident with v belonging to K, lying in G, and
avoiding Q. Every whole-component Hamilton cycle H in G uses two incident
edges, so at least max(0,2+g-d) lie in this safe fixed set. Thus d-g<=1 is a
sufficient local certificate. Observations include d2/g1, d3/g2 and also d2/g2;
the last type supplies a lower bound of two and must not be silently discarded.

Forward F means fixed source K versus any target-component HC, excluding the
restored target pool. Reverse R means fixed restored target K versus any
source-component HC, excluding the source pool. Reverse always uses the
original interface's recorded first map; it does not re-normalize the swapped
pair. A hard component can supply the fixed K but never the arbitrary whole HC.
The whole fixed-side template does not become arbitrary when selecting a word.

A source word can be reused across interfaces. Each interface must still carry
its own chosen direction, actual source-coordinate state, original map,
component identities and saved safe-incidence certificate. The results retain
all these fields, including every selected alternative support. The full236
selection uses139 F and97 R assignments; retaining125 leaves43 F and68 R
assignments for its111 additional interfaces. These counts are deterministic
choices among positive alternatives, not directional minima.

The existing125 theorem can retain its stronger arbitrary-both-HC quantifier.
The111 additions retain the one-fixed-side quantifier above. Their union must
not be stated as a236-case arbitrary-both-HC theorem.

## DP sufficiency, scope and checks

For each original source, each observed positive actual word has a fixed mask
of the covered interfaces where at least one recorded direction is positive.
The DP processes sorted words once, retaining the shortest and then
lexicographically first subset for each attained union mask. A longer subset
with the same mask cannot improve a future extension: every future word has
the same mask effect. This gives exact minimum memberships per source among
the frozen positive words. In the retained-word variant, the initial mask is
the union of all retained-word masks and retained words have zero new cost.

Each optimization universe has at most15 interfaces, hence at most2^15 masks.
The nonconstant source00001 has16 original interfaces, but only11 positives
enter its cover. The actual CPython3.14.6 primary run took0.079 seconds and
reread every saved observation's scalar/list identities. It asserted all313
identities, all236 positives, the125 containment,111 extras, all witness masks,
and preservation of both frozen input hashes. No author generator was rerun.

Independent combinations checks recovered the same first minimum for source
00001(11 candidates,4 members,370 subsets checked) and00112(6 candidates,
3 members,27 subsets checked). Separate boundary checks confirm the exact
zero-addition result for00121 and00124. These checks concern saved masks only.

This is a bounded finite feasibility result. The minimum is per source within
the frozen candidate set; distinct words across sources are not jointly
optimized. Component completeness, actual safe K membership and pool
restoration are inherited from the frozen v2 checker and manuscript context,
not re-proved by mask optimization. A future symbolic replacement must expose
and justify those premises and directions. The counts alone do not establish
a uniform symbolic C5 family or a shorter complete proof. Main and all existing
frozen records are unchanged.

The standard computation-record validator checks schema, file presence and
SHA256 only. Its PASS does not certify this mathematical implication or DP
semantics; those are stated and reviewed separately above.
