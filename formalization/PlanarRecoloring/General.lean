import PlanarRecoloring.Core

/-!
# General finite recolouring interfaces

This file records the elementary graph-theoretic interfaces used by the
paper.  The core graph type stores a Boolean adjacency matrix; `Symmetric`
and `Loopless` make its intended simple-graph interpretation explicit.
The finite-subset formulation of degeneracy uses lists with `Nodup`, so no
external finite-set library is needed.
-/

namespace PlanarRecoloring

/-- The Boolean adjacency matrix is symmetric. -/
def Symmetric {n : Nat} (G : FiniteGraph n) : Prop :=
  ∀ u v : Vertex n, G.adj u v = G.adj v u

/-- The graph has no loops. -/
def Loopless {n : Nat} (G : FiniteGraph n) : Prop :=
  ∀ v : Vertex n, G.adj v v = false

/-- A simple graph is loopless and has symmetric adjacency. -/
def Simple {n : Nat} (G : FiniteGraph n) : Prop :=
  Symmetric G ∧ Loopless G

/-- The directed Boolean edge predicate underlying `FiniteGraph`. -/
def Edge {n : Nat} (G : FiniteGraph n) (u v : Vertex n) : Prop :=
  G.adj u v = true

theorem edge_iff_adj {n : Nat} (G : FiniteGraph n) (u v : Vertex n) :
    Edge G u v ↔ G.adj u v = true := by rfl

theorem edge_symm {n : Nat} {G : FiniteGraph n} (hs : Symmetric G)
    {u v : Vertex n} (h : Edge G u v) : Edge G v u := by
  unfold Edge at h ⊢
  rw [hs u v] at h
  exact h

theorem edge_irrefl {n : Nat} {G : FiniteGraph n} (hl : Loopless G)
    (v : Vertex n) : ¬ Edge G v v := by
  intro h
  unfold Edge at h
  rw [hl v] at h
  cases h

/-- Equivalent orientation-free properness for a symmetric adjacency matrix. -/
theorem proper_edge_iff {n k : Nat} {G : FiniteGraph n} (hs : Symmetric G)
    (c : Vertex n → Colour k) :
    Proper G c ↔ ∀ ⦃u v : Vertex n⦄, Edge G u v → c u ≠ c v := by
  rfl

/-- Every induced neighbour list has length at most the original list. -/
def NeighboursIn {n : Nat} (G : FiniteGraph n)
    (S : List (Vertex n)) (v : Vertex n) : List (Vertex n) :=
  S.filter (G.adj v)

def DegreeIn {n : Nat} (G : FiniteGraph n)
    (S : List (Vertex n)) (v : Vertex n) : Nat :=
  (NeighboursIn G S v).length

theorem degreeIn_le_length {n : Nat} (G : FiniteGraph n)
    (S : List (Vertex n)) (v : Vertex n) :
    DegreeIn G S v ≤ S.length := by
  unfold DegreeIn NeighboursIn
  exact List.length_filter_le (G.adj v) S

theorem mem_neighboursIn_iff {n : Nat} (G : FiniteGraph n)
    (S : List (Vertex n)) (v w : Vertex n) :
    w ∈ NeighboursIn G S v ↔ w ∈ S ∧ Edge G v w := by
  unfold NeighboursIn Edge
  exact List.mem_filter

/-- The list formulation of `d`-degeneracy for a finite graph. -/
def Degenerate {n : Nat} (G : FiniteGraph n) (d : Nat) : Prop :=
  ∀ S : List (Vertex n), S.Nodup → S ≠ [] →
    ∃ v, v ∈ S ∧ DegreeIn G S v ≤ d

theorem degenerate_mono {n : Nat} {G : FiniteGraph n} {d e : Nat}
    (h : Degenerate G d) (hde : d ≤ e) : Degenerate G e := by
  intro S hS hne
  rcases h S hS hne with ⟨v, hv, hd⟩
  exact ⟨v, hv, Nat.le_trans hd hde⟩

theorem degenerate_of_le {n : Nat} {G : FiniteGraph n} {d : Nat}
    (h : ∀ S : List (Vertex n), S.Nodup → S ≠ [] →
      ∃ v, v ∈ S ∧ DegreeIn G S v ≤ d) : Degenerate G d := by
  exact h

/-- A colour occurs at a vertex's neighbourhood. -/
def UsedAt {n k : Nat} (G : FiniteGraph n)
    (c : Vertex n → Colour k) (v : Vertex n) (a : Colour k) : Prop :=
  ∃ u : Vertex n, Edge G v u ∧ c u = a

theorem available_iff_no_used {n k : Nat} {G : FiniteGraph n}
    {c : Vertex n → Colour k} {v : Vertex n} {a : Colour k} :
    Available G c v a ↔ ¬ UsedAt G c v a := by
  constructor
  · intro ha hu
    rcases hu with ⟨u, hu, hcu⟩
    exact (ha u hu) hcu
  · intro h u hu hca
    apply h
    exact ⟨u, hu, hca⟩

/-- In a proper colouring, the colour currently at `v` is available at `v`. -/
theorem current_available {n k : Nat} {G : FiniteGraph n}
    {c : Vertex n → Colour k} (hc : Proper G c) (v : Vertex n) :
    Available G c v (c v) := by
  intro u huv hsame
  exact (hc huv) hsame.symm

/-- The changed colour in a legal recolouring is available in the old state. -/
theorem target_available_of_recolour {n k : Nat} {G : FiniteGraph n}
    {x y : Coloring G k} {v : Vertex n}
    (hv : x v ≠ y v)
    (hrest : ∀ w : Vertex n, w ≠ v → x w = y w) :
    Available G x v (y v) := by
  intro u huv hcolour
  by_cases huv' : u = v
  · subst u
    exact hv hcolour
  · have heq : x u = y u := hrest u huv'
    have hy : y v ≠ y u := y.proper huv
    exact hy (hcolour.symm.trans heq)

/-- Any witness to recolouring adjacency has the advertised available colour. -/
theorem target_available_of_adjacent {n k : Nat} {G : FiniteGraph n}
    {x y : Coloring G k} (h : RecolourAdjacent x y) :
    ∃ v : Vertex n, x v ≠ y v ∧ Available G x v (y v) := by
  rcases h with ⟨v, hv, hrest⟩
  exact ⟨v, hv, target_available_of_recolour hv hrest⟩

/-- A state pair related by one-vertex recolouring has at most one changed vertex. -/
theorem changed_vertex_unique {n k : Nat} {G : FiniteGraph n}
    {x y : Coloring G k} {v w : Vertex n}
    (hv : x v ≠ y v)
    (hw : x w ≠ y w)
    (hrest : ∀ z : Vertex n, z ≠ v → x z = y z) :
    w = v := by
  by_cases hne : w = v
  · exact hne
  · exact False.elim (hw (hrest w hne))

/-- Explicitly recolour one vertex. -/
def RecolourAt {n k : Nat} (c : Vertex n → Colour k)
    (v : Vertex n) (a : Colour k) : Vertex n → Colour k :=
  fun w => if w = v then a else c w

theorem recolourAt_eq {n k : Nat} (c : Vertex n → Colour k)
    (v : Vertex n) (a : Colour k) : RecolourAt c v a v = a := by
  unfold RecolourAt
  simp

theorem recolourAt_ne {n k : Nat} (c : Vertex n → Colour k)
    (v w : Vertex n) (a : Colour k) (h : w ≠ v) :
    RecolourAt c v a w = c w := by
  unfold RecolourAt
  simp [h]

/-- Recolouring is proper on a symmetric graph when the new colour is available. -/
theorem recolourAt_proper {n k : Nat} {G : FiniteGraph n}
    (hs : Symmetric G) {c : Vertex n → Colour k}
    (hc : Proper G c) (v : Vertex n) (a : Colour k)
    (ha : Available G c v a) :
    Proper G (RecolourAt c v a) := by
  intro u w huw
  by_cases hu : u = v
  · subst u
    by_cases hw : w = v
    · subst w
      exact False.elim ((hc huw) rfl)
    · rw [recolourAt_eq, recolourAt_ne _ _ _ _ hw]
      exact (ha w huw).symm
  · by_cases hw : w = v
    · subst w
      rw [recolourAt_ne _ _ _ _ hu, recolourAt_eq]
      have hvu : G.adj v u = true := by
        calc
          G.adj v u = G.adj u v := (hs u v).symm
          _ = true := huw
      exact ha u hvu
    · rw [recolourAt_ne _ _ _ _ hu, recolourAt_ne _ _ _ _ hw]
      exact hc huw

/-- Constructing a colouring after a legal recolouring. -/
def RecolourAtState {n k : Nat} {G : FiniteGraph n}
    (x : Coloring G k) (hs : Symmetric G) (v : Vertex n) (a : Colour k)
    (ha : Available G x v a) : Coloring G k :=
  ⟨RecolourAt x v a, recolourAt_proper hs x.proper v a ha⟩

theorem recolourAt_adjacent {n k : Nat} {G : FiniteGraph n}
    (x : Coloring G k) (hs : Symmetric G) (v : Vertex n) (a : Colour k)
    (ha : Available G x v a) (hneq : x v ≠ a) :
    RecolourAdjacent x (RecolourAtState x hs v a ha) := by
  refine ⟨v, ?_, ?_⟩
  · change x v ≠ RecolourAt x v a v
    rw [recolourAt_eq]
    exact hneq
  · intro w hw
    change x w = RecolourAt x v a w
    exact (recolourAt_ne x v w a hw).symm

end PlanarRecoloring
