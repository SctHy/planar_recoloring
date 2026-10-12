import Std

/-!
# Finite recolouring graphs

This file fixes the basic objects used by the paper without importing a
graph library.  A graph on `Fin n` is a Boolean adjacency matrix.  The
definitions are intentionally small: they make the one-vertex recolouring
rule executable and are enough to state the finite obstructions in the paper.
The analytic planar lemmas are not hidden in these definitions.
-/

namespace PlanarRecoloring

abbrev Vertex (n : Nat) := Fin n
abbrev Colour (k : Nat) := Fin k

structure FiniteGraph (n : Nat) where
  adj : Vertex n → Vertex n → Bool

def Proper (G : FiniteGraph n) (c : Vertex n → Colour k) : Prop :=
  ∀ ⦃u v : Vertex n⦄, G.adj u v = true → c u ≠ c v

structure Coloring (G : FiniteGraph n) (k : Nat) where
  value : Vertex n → Colour k
  proper : Proper G value

instance (G : FiniteGraph n) (k : Nat) :
    CoeFun (Coloring G k) (fun _ => Vertex n → Colour k) :=
  ⟨Coloring.value⟩

def RecolourAdjacent {n k : Nat} {G : FiniteGraph n}
    (x y : Coloring G k) : Prop :=
  ∃ v : Vertex n,
    x v ≠ y v ∧
      ∀ w : Vertex n, w ≠ v → x w = y w

theorem recolour_adjacent_irrefl {n k : Nat} {G : FiniteGraph n}
    (x : Coloring G k) :
    ¬ RecolourAdjacent x x := by
  intro h
  rcases h with ⟨v, hv, _⟩
  exact hv rfl

theorem recolour_adjacent_symm {n k : Nat} {G : FiniteGraph n}
    {x y : Coloring G k}
    (h : RecolourAdjacent x y) : RecolourAdjacent y x := by
  rcases h with ⟨v, hv, hrest⟩
  exact ⟨v, Ne.symm hv, fun w hw => (hrest w hw).symm⟩

def Available {n k : Nat} (G : FiniteGraph n) (c : Vertex n → Colour k)
    (v : Vertex n) (a : Colour k) : Prop :=
  ∀ u : Vertex n, G.adj v u = true → c u ≠ a

theorem recolour_adjacent_iff {n k : Nat} {G : FiniteGraph n}
    {x y : Coloring G k} :
    RecolourAdjacent x y ↔
      ∃ v : Vertex n, x v ≠ y v ∧ ∀ w, w ≠ v → x w = y w :=
  by rfl

/- A path is represented by its explicit list of states.  This is useful for
   finite checks and avoids making a false claim that all analytic paths in
   the article have already been formalised. -/
def Consecutive (r : α → α → Prop) : List α → Prop
  | [] => True
  | [_] => True
  | x :: y :: xs => r x y ∧ Consecutive r (y :: xs)

def SpanningPath (states : List α) (r : α → α → Prop)
    (s t : α) : Prop :=
  ∃ path : List α,
    path.head? = some s ∧
      path.getLast? = some t ∧
      path.Nodup ∧
      (∀ x, x ∈ states ↔ x ∈ path) ∧
      Consecutive r path

end PlanarRecoloring
