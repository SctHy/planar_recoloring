import PlanarRecoloring.General
import PlanarRecoloring.FibreHamilton
import PlanarRecoloring.Complete

/-!
# Restoring one vertex and its colouring fibres

The restored vertex is `none`; the vertices of the deleted graph are `some u`.
The neighbour predicate records exactly the edges incident with the restored
vertex.  These interfaces formalise the complete fibres in
`main.tex`, equation `eq:clique-fibres`, without cardinality assumptions.
-/

namespace PlanarRecoloring.SingleVertex

/-- A graph obtained by restoring one vertex to a finite base graph. -/
structure RestoredGraph (n : Nat) where
  base : FiniteGraph n
  neighbour : Vertex n → Bool

def RestoredGraph.adj (G : RestoredGraph n) : Option (Vertex n) → Option (Vertex n) → Bool
  | none, none => false
  | none, some v => G.neighbour v
  | some u, none => G.neighbour u
  | some u, some v => G.base.adj u v

def Proper (G : RestoredGraph n) (c : Option (Vertex n) → Colour k) : Prop :=
  ∀ ⦃u v : Option (Vertex n)⦄, G.adj u v = true → c u ≠ c v

structure Coloring (G : RestoredGraph n) (k : Nat) where
  value : Option (Vertex n) → Colour k
  proper : Proper G value

instance (G : RestoredGraph n) (k : Nat) :
    CoeFun (Coloring G k) (fun _ => Option (Vertex n) → Colour k) :=
  ⟨Coloring.value⟩

/-- Colours not used on a neighbour of the restored vertex. -/
def Available (G : RestoredGraph n) (f : Vertex n → Colour k) (a : Colour k) : Prop :=
  ∀ u : Vertex n, G.neighbour u = true → f u ≠ a

def extend (f : Vertex n → Colour k) (a : Colour k) : Option (Vertex n) → Colour k
  | none => a
  | some u => f u

def restrict (c : Option (Vertex n) → Colour k) : Vertex n → Colour k :=
  fun u => c (some u)

theorem extend_none (f : Vertex n → Colour k) (a : Colour k) :
    extend f a none = a := rfl

theorem extend_some (f : Vertex n → Colour k) (a : Colour k) (u : Vertex n) :
    extend f a (some u) = f u := rfl

theorem restrict_extend (f : Vertex n → Colour k) (a : Colour k) :
    restrict (extend f a) = f := rfl

theorem extend_restrict (c : Option (Vertex n) → Colour k) :
    extend (restrict c) (c none) = c := by
  funext u
  cases u <;> rfl

/-- Extension introduces exactly the properness constraints at the new vertex. -/
theorem extend_proper_iff (G : RestoredGraph n) (f : Vertex n → Colour k)
    (a : Colour k) :
    Proper G (extend f a) ↔ PlanarRecoloring.Proper G.base f ∧ Available G f a := by
  constructor
  · intro h
    constructor
    · intro u v huv
      exact h (u := some u) (v := some v) huv
    · intro u hu
      exact h (u := some u) (v := none) hu
  · rintro ⟨hf, ha⟩ u v huv
    cases u with
    | none =>
      cases v with
      | none => contradiction
      | some v => exact Ne.symm (ha v huv)
    | some u =>
      cases v with
      | none => exact ha u huv
      | some v => exact hf huv

theorem restrict_proper {G : RestoredGraph n} {c : Option (Vertex n) → Colour k}
    (hc : Proper G c) : PlanarRecoloring.Proper G.base (restrict c) := by
  intro u v huv
  exact hc (u := some u) (v := some v) huv

theorem restored_colour_available {G : RestoredGraph n}
    {c : Option (Vertex n) → Colour k} (hc : Proper G c) :
    Available G (restrict c) (c none) := by
  intro u hu
  exact hc (u := some u) (v := none) hu

def extendColoring (G : RestoredGraph n) (f : PlanarRecoloring.Coloring G.base k)
    (a : Colour k) (ha : Available G f a) : Coloring G k :=
  ⟨extend f a, (extend_proper_iff G f a).mpr ⟨f.proper, ha⟩⟩

def restrictColoring {G : RestoredGraph n} (c : Coloring G k) :
    PlanarRecoloring.Coloring G.base k :=
  ⟨restrict c, restrict_proper c.proper⟩

/-- The fibre over a base colouring consists of the states restricting to it. -/
def InFibre {G : RestoredGraph n} (f : PlanarRecoloring.Coloring G.base k)
    (c : Coloring G k) : Prop :=
  ∀ u : Vertex n, c (some u) = f u

theorem extendColoring_in_fibre (G : RestoredGraph n)
    (f : PlanarRecoloring.Coloring G.base k) (a : Colour k) (ha : Available G f a) :
    InFibre f (extendColoring G f a ha) := by
  intro u
  rfl

/-- A fibre state is uniquely reconstructed from its colour at the new vertex. -/
theorem fibre_reconstruct {G : RestoredGraph n}
    {f : PlanarRecoloring.Coloring G.base k} {c : Coloring G k}
    (hc : InFibre f c) : c.value = extend f (c none) := by
  funext u
  cases u with
  | none => rfl
  | some u => exact hc u

theorem fibre_colour_available {G : RestoredGraph n}
    {f : PlanarRecoloring.Coloring G.base k} {c : Coloring G k}
    (hc : InFibre f c) : Available G f (c none) := by
  intro u hu
  rw [← hc u]
  exact c.proper (u := some u) (v := none) hu

def RecolourAdjacent {G : RestoredGraph n} (x y : Coloring G k) : Prop :=
  ∃ v : Option (Vertex n), x v ≠ y v ∧
    ∀ w : Option (Vertex n), w ≠ v → x w = y w

/-- Two states in one fibre are adjacent exactly when their new-vertex colours differ. -/
theorem fibre_adjacent_iff {G : RestoredGraph n}
    {f : PlanarRecoloring.Coloring G.base k} {x y : Coloring G k}
    (hx : InFibre f x) (hy : InFibre f y) :
    RecolourAdjacent x y ↔ x none ≠ y none := by
  constructor
  · rintro ⟨v, hv, _⟩
    cases v with
    | none => exact hv
    | some u => exact False.elim (hv ((hx u).trans (hy u).symm))
  · intro h
    refine ⟨none, h, ?_⟩
    intro w hw
    cases w with
    | none => exact False.elim (hw rfl)
    | some u => exact (hx u).trans (hy u).symm

theorem extensions_adjacent_iff (G : RestoredGraph n)
    (f : PlanarRecoloring.Coloring G.base k) (a b : Colour k)
    (ha : Available G f a) (hb : Available G f b) :
    RecolourAdjacent (extendColoring G f a ha) (extendColoring G f b hb) ↔ a ≠ b := by
  exact fibre_adjacent_iff (extendColoring_in_fibre G f a ha)
    (extendColoring_in_fibre G f b hb)

/- A finite enumeration of one restored-vertex fibre has the complete-fibre
   endpoint path promised by the clique-fibre argument.  The relation is only
   complete on the supplied list: the hypotheses explicitly record that every
   listed state lies in the same fibre. -/
theorem fibre_hamiltonPathOn_of_mem
    {G : RestoredGraph n} {k : Nat}
    (f : PlanarRecoloring.Coloring G.base k)
    (states : List (Coloring G k))
    (hnodup : states.Nodup)
    (hstates : ∀ x, x ∈ states → InFibre f x)
    {s t : Coloring G k}
    (hs : s ∈ states) (ht : t ∈ states) (hst : s ≠ t) :
    HamiltonPathOn states (fun x y => RecolourAdjacent x y) s t := by
  classical
  apply complete_hamiltonPathOn_of_mem states hnodup
  · intro x y hx hy hxy
    have hxF := hstates x hx
    have hyF := hstates y hy
    apply (fibre_adjacent_iff hxF hyF).mpr
    intro hnone
    apply hxy
    have hv : x.value = y.value := by
      funext u
      cases u with
      | none => exact hnone
      | some u => exact (hxF u).trans (hyF u).symm
    cases x with
    | mk xv xp =>
      cases y with
      | mk yv yp =>
        dsimp at hv
        cases hv
        rfl
  · exact hs
  · exact ht
  · exact hst

/-- A base edge lifts at every colour available on both ends. -/
theorem shared_colour_lifts_edge {G : RestoredGraph n}
    {f g : PlanarRecoloring.Coloring G.base k}
    (hfg : PlanarRecoloring.RecolourAdjacent f g) (a : Colour k)
    (hfa : Available G f a) (hga : Available G g a) :
    RecolourAdjacent (extendColoring G f a hfa) (extendColoring G g a hga) := by
  rcases hfg with ⟨u, hu, hrest⟩
  refine ⟨some u, hu, ?_⟩
  intro w hw
  cases w with
  | none => rfl
  | some w =>
    apply hrest w
    intro hwu
    exact hw (congrArg some hwu)

/-- Restricting a restored colouring records its values on the old vertices. -/
theorem inFibre_restrictColoring {G : RestoredGraph n} (c : Coloring G k) :
    InFibre (restrictColoring c) c := by
  intro u
  rfl

/-- A base recolouring edge lifts when the restored vertex keeps its colour.

This is the endpoint-sensitive bridge used by product and restoration
constructions: the changed old vertex supplies the witness, while equality at
`none` supplies the unchanged endpoint coordinate. -/
theorem shared_colour_lifts_edge_of_equal_new_colour
    {G : RestoredGraph n} {x y : Coloring G k}
    (hbase : PlanarRecoloring.RecolourAdjacent
      (restrictColoring x) (restrictColoring y))
    (hsame : x none = y none) :
    RecolourAdjacent x y := by
  rcases hbase with ⟨u, hu, hrest⟩
  refine ⟨some u, ?_, ?_⟩
  · simpa [restrictColoring, restrict] using hu
  · intro w hw
    cases w with
    | none => exact hsame
    | some z =>
      have hzu : z ≠ u := by
        intro hzu
        apply hw
        simp [hzu]
      simpa [restrictColoring, restrict] using hrest z hzu

/-- The base edge plus equality of the restored coordinate is the bridge
relation for a restoration product. -/
def RestorationBridge {G : RestoredGraph n} {k : Nat}
    (x y : Coloring G k) : Prop :=
  PlanarRecoloring.RecolourAdjacent (restrictColoring x) (restrictColoring y) ∧
    x none = y none

theorem restorationBridge_adjacent {G : RestoredGraph n} {k : Nat}
    {x y : Coloring G k} (h : RestorationBridge x y) :
    RecolourAdjacent x y :=
  shared_colour_lifts_edge_of_equal_new_colour h.1 h.2

/- A linear chain of fibre paths whose interfaces are restoration bridges
   lifts to an endpoint-prescribed path in the restored recolouring graph.
   This is the path counterpart of `restoration_fibre_cycle`; all endpoint
   information is retained by the chain construction. -/
def restoration_fibre_path
    {G : RestoredGraph n} {k : Nat}
    (ps : List (FibrePath (fun x y : Coloring G k => RecolourAdjacent x y)))
    (hne : ps ≠ [])
    (hbridges : FibreChainBridges
      (fun x y : Coloring G k => RestorationBridge x y) ps)
    (hdis : FibreChainDisjoint ps) :
    FibrePath (fun x y : Coloring G k => RecolourAdjacent x y) := by
  let chain := fibrePath_chain
    (inside := fun x y : Coloring G k => RecolourAdjacent x y)
    (bridge := fun x y : Coloring G k => RestorationBridge x y)
    ps hne hbridges hdis
  exact FibrePath.map
    (fun {x y} hxy => match hxy with
      | Or.inl h => h
      | Or.inr h => restorationBridge_adjacent h) chain

theorem restoration_fibre_path_path
    {G : RestoredGraph n} {k : Nat}
    (ps : List (FibrePath (fun x y : Coloring G k => RecolourAdjacent x y)))
    (hne : ps ≠ [])
    (hbridges : FibreChainBridges
      (fun x y : Coloring G k => RestorationBridge x y) ps)
    (hdis : FibreChainDisjoint ps) :
    (restoration_fibre_path ps hne hbridges hdis).path =
      (ps.map (fun p => p.path)).flatten := by
  rfl

theorem restoration_fibre_path_hamiltonPathOn
    {G : RestoredGraph n} {k : Nat}
    (ps : List (FibrePath (fun x y : Coloring G k => RecolourAdjacent x y)))
    (hne : ps ≠ [])
    (hbridges : FibreChainBridges
      (fun x y : Coloring G k => RestorationBridge x y) ps)
    (hdis : FibreChainDisjoint ps) :
    HamiltonPathOn (fibreChainVertices ps)
      (fun x y : Coloring G k => RecolourAdjacent x y)
      (ps.head hne).start ((ps.getLast hne).finish) := by
  exact FibrePath.toHamiltonPathOn
    (restoration_fibre_path ps hne hbridges hdis)

/-- A closed chain of fibre paths whose interfaces are restoration bridges
is a closed path in the restored recolouring graph. -/
def restoration_fibre_cycle
    {G : RestoredGraph n} {k : Nat}
    (ps : List (FibrePath (fun x y : Coloring G k => RecolourAdjacent x y)))
    (hne : ps ≠ [])
    (hbridges : FibreChainBridges
      (fun x y : Coloring G k => RestorationBridge x y) ps)
    (hdis : FibreChainDisjoint ps)
    (hclose : RestorationBridge
      (ps.getLast hne).finish (ps.head hne).start) :
    ClosedFibrePath (fun x y : Coloring G k => RecolourAdjacent x y) := by
  let closed := fibreCycle_chain
    (inside := fun x y : Coloring G k => RecolourAdjacent x y)
    (bridge := fun x y : Coloring G k => RestorationBridge x y)
    ps hne hbridges hdis hclose
  exact ClosedFibrePath.map
    (fun {x y} hxy => match hxy with
      | Or.inl h => h
      | Or.inr h => restorationBridge_adjacent h) closed

/-- The restoration lift preserves the literal concatenated path. -/
theorem restoration_fibre_cycle_path
    {G : RestoredGraph n} {k : Nat}
    (ps : List (FibrePath (fun x y : Coloring G k => RecolourAdjacent x y)))
    (hne : ps ≠ [])
    (hbridges : FibreChainBridges
      (fun x y : Coloring G k => RestorationBridge x y) ps)
    (hdis : FibreChainDisjoint ps)
    (hclose : RestorationBridge
      (ps.getLast hne).finish (ps.head hne).start) :
    (restoration_fibre_cycle ps hne hbridges hdis hclose).path.path =
      (ps.map (fun p => p.path)).flatten := by
  rfl

/-- The lifted cycle covers exactly the vertices supplied by its fibres. -/
theorem restoration_fibre_cycle_covers
    {G : RestoredGraph n} {k : Nat}
    (ps : List (FibrePath (fun x y : Coloring G k => RecolourAdjacent x y)))
    (hne : ps ≠ [])
    (hbridges : FibreChainBridges
      (fun x y : Coloring G k => RestorationBridge x y) ps)
    (hdis : FibreChainDisjoint ps)
    (hclose : RestorationBridge
      (ps.getLast hne).finish (ps.head hne).start) :
    ∀ x, x ∈ fibreChainVertices ps ↔
      x ∈ (restoration_fibre_cycle ps hne hbridges hdis hclose).path.path := by
  intro x
  rw [restoration_fibre_cycle_path ps hne hbridges hdis hclose]
  exact fibreChain_covers ps x

/-- The same restoration certificate is a Hamilton cycle over the explicitly
listed colouring states.  This relation-level conclusion avoids pretending
that the structure type has already been enumerated by `Fin n`. -/
theorem restoration_fibre_cycle_hamiltonCycleOn
    {G : RestoredGraph n} {k : Nat}
    (ps : List (FibrePath (fun x y : Coloring G k => RecolourAdjacent x y)))
    (hne : ps ≠ [])
    (hbridges : FibreChainBridges
      (fun x y : Coloring G k => RestorationBridge x y) ps)
    (hdis : FibreChainDisjoint ps)
    (hclose : RestorationBridge
      (ps.getLast hne).finish (ps.head hne).start) :
    HamiltonCycleOn (fibreChainVertices ps)
      (fun x y : Coloring G k => RecolourAdjacent x y) := by
  exact ClosedFibrePath.toHamiltonCycleOn
    (restoration_fibre_cycle ps hne hbridges hdis hclose)

end PlanarRecoloring.SingleVertex
