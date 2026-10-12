import PlanarRecoloring.General

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

end PlanarRecoloring.SingleVertex
