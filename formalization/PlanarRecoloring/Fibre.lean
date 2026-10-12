import PlanarRecoloring.Core

/-!
# Abstract fibre and layer splicing

The analytic lifting arguments in the paper use only a small combinatorial
interface: each fibre comes with a spanning path, consecutive fibres have a
bridge edge, and different fibres are disjoint.  This file formalises that
interface using lists.  It deliberately does not assume a graph library or
make any claim about how the individual fibre paths were found.
-/

namespace PlanarRecoloring

/-- A fibre is represented by the finite list of its vertices. -/
structure Fibre (α : Type u) where
  vertices : List α

/-- The relation used inside each fibre and the relation used at interfaces
are combined into the edge relation of the layered graph. -/
def LayeredEdge {α : Type u} (inside bridge : α → α → Prop) : α → α → Prop :=
  fun x y => inside x y ∨ bridge x y

/-- An interface edge is oriented from one layer to the next. -/
def InterfaceEdge {α : Type u} (bridge : α → α → Prop) (x y : α) : Prop :=
  bridge x y

/-- A spanning path in one fibre, with its prescribed ends recorded. -/
structure FibrePath {α : Type u} (inside : α → α → Prop) where
  fibre : Fibre α
  path : List α
  start : α
  finish : α
  head_eq : path.head? = some start
  last_eq : path.getLast? = some finish
  nodup : path.Nodup
  covers : ∀ x, x ∈ fibre.vertices ↔ x ∈ path
  walk : Consecutive inside path

theorem FibrePath.path_ne_nil {α : Type u} {inside : α → α → Prop}
    (p : FibrePath inside) : p.path ≠ [] := by
  intro h
  have hh : ([] : List α).head? = some p.start := by
    simpa [h] using p.head_eq
  simp at hh

theorem consecutive_mono {α : Type u} {r s : α → α → Prop}
    {xs : List α} (h : ∀ ⦃x y⦄, r x y → s x y)
    (hc : Consecutive r xs) : Consecutive s xs := by
  induction xs with
  | nil => trivial
  | cons x xs ih =>
    cases xs with
    | nil => trivial
    | cons y ys =>
      rcases hc with ⟨hxy, htail⟩
      exact ⟨h hxy, ih htail⟩

theorem consecutive_append {α : Type u} {r : α → α → Prop}
    {xs ys : List α} {x y : α}
    (hx : Consecutive r xs) (hy : Consecutive r ys)
    (hxs : xs ≠ []) (hys : ys ≠ [])
    (hlast : xs.getLast? = some x)
    (hhead : ys.head? = some y)
    (hxy : r x y) :
    Consecutive r (xs ++ ys) := by
  induction xs with
  | nil => exact False.elim (hxs rfl)
  | cons a as ih =>
    cases as with
    | nil =>
      cases ys with
      | nil => exact False.elim (hys rfl)
      | cons b bs =>
        have hlast' : a = x := by simpa using hlast
        have hhead' : b = y := by simpa using hhead
        subst x
        subst y
        exact ⟨hxy, hy⟩
    | cons b bs =>
      rcases hx with ⟨hab, htail⟩
      have htail_last : (b :: bs).getLast? = some x := by
        simpa using hlast
      have ht := ih htail (by simp) htail_last
      exact ⟨hab, ht⟩

def DisjointLists {α : Type u} (xs ys : List α) : Prop :=
  ∀ ⦃x⦄, x ∈ xs → x ∉ ys

theorem disjointLists_append_left {α : Type u} {xs ys zs : List α}
    (hxy : DisjointLists xs zs) (hyz : DisjointLists ys zs) :
    DisjointLists (xs ++ ys) zs := by
  intro x hx
  simp only [List.mem_append] at hx
  cases hx with
  | inl h => exact hxy h
  | inr h => exact hyz h

theorem nodup_append_of_disjoint {α : Type u} {xs ys : List α}
    (hx : xs.Nodup) (hy : ys.Nodup) (hdis : DisjointLists xs ys) :
    (xs ++ ys).Nodup := by
  apply List.nodup_append.mpr
  refine ⟨hx, hy, ?_⟩
  intro a ha b hb hab
  apply hdis ha
  simpa [hab] using hb

theorem head_append_of_ne_nil {α : Type u} {xs ys : List α}
    (hxs : xs ≠ []) : (xs ++ ys).head? = xs.head? := by
  cases xs with
  | nil => exact False.elim (hxs rfl)
  | cons x xs => rfl

theorem getLast_append_of_ne_nil {α : Type u} {xs ys : List α}
    (hys : ys ≠ []) : (xs ++ ys).getLast? = ys.getLast? := by
  have hz : ys.getLast? = some (ys.getLast hys) :=
    List.getLast?_eq_some_getLast hys
  rw [List.getLast?_append, hz]
  rfl

def FibrePath.lift {α : Type u} {inside bridge : α → α → Prop}
    (p : FibrePath inside) : FibrePath (LayeredEdge inside bridge) :=
  { fibre := p.fibre
    path := p.path
    start := p.start
    finish := p.finish
    head_eq := p.head_eq
    last_eq := p.last_eq
    nodup := p.nodup
    covers := p.covers
    walk := consecutive_mono (fun _ _ h => Or.inl h) p.walk }

def fibrePath_splice {α : Type u} {inside bridge : α → α → Prop}
    (p q : FibrePath inside)
    (hbridge : InterfaceEdge bridge p.finish q.start)
    (hdis : DisjointLists p.fibre.vertices q.fibre.vertices) :
    FibrePath (LayeredEdge inside bridge) := by
  have hpathdis : DisjointLists p.path q.path := by
    intro x hxp hxq
    exact hdis ((p.covers x).mpr hxp) ((q.covers x).mpr hxq)
  refine
    { fibre := ⟨p.fibre.vertices ++ q.fibre.vertices⟩
      path := p.path ++ q.path
      start := p.start
      finish := q.finish
      head_eq := ?_
      last_eq := ?_
      nodup := ?_
      covers := ?_
      walk := ?_ }
  · rw [head_append_of_ne_nil p.path_ne_nil, p.head_eq]
  · rw [getLast_append_of_ne_nil q.path_ne_nil, q.last_eq]
  · exact nodup_append_of_disjoint p.nodup q.nodup hpathdis
  · intro x
    simp only [List.mem_append]
    rw [p.covers x, q.covers x]
  · have hpwalk : Consecutive (LayeredEdge inside bridge) p.path :=
      consecutive_mono (fun {x y} h => Or.inl h) p.walk
    have hqwalk : Consecutive (LayeredEdge inside bridge) q.path :=
      consecutive_mono (fun {x y} h => Or.inl h) q.walk
    apply consecutive_append hpwalk hqwalk p.path_ne_nil q.path_ne_nil
      p.last_eq q.head_eq
    exact Or.inr hbridge

/-- A fibre path together with the closing edge of a cycle. -/
structure ClosedFibrePath {α : Type u} (r : α → α → Prop) where
  path : FibrePath r
  close : r path.finish path.start

/-- Two disjoint fibre paths form a closed layered path when both interface
edges are present.  This is the two-layer local form of a cyclic lift. -/
def fibreCycle_splice {α : Type u} {inside bridge : α → α → Prop}
    (p q : FibrePath inside)
    (hforward : InterfaceEdge bridge p.finish q.start)
    (hback : InterfaceEdge bridge q.finish p.start)
    (hdis : DisjointLists p.fibre.vertices q.fibre.vertices) :
    ClosedFibrePath (LayeredEdge inside bridge) :=
  let sp := fibrePath_splice p q hforward hdis
  { path := sp
    close := Or.inr hback }

end PlanarRecoloring
