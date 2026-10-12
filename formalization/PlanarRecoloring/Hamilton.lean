import PlanarRecoloring.Core
import PlanarRecoloring.Fibre

/-!
# Hamilton paths and cycles

The graph objects in this project are finite Boolean adjacency matrices.  This
file gives the usual Hamiltonian notions directly in terms of finite lists, so
that they can be used without importing a graph library.  A path list contains
each vertex at most once, and `SpansVertices` requires that every vertex of the
ambient `Fin n` occurs in the list.
-/

namespace PlanarRecoloring

def Adjacent (G : FiniteGraph n) (u v : Vertex n) : Prop :=
  G.adj u v = true

def Walk (G : FiniteGraph n) (path : List (Vertex n)) : Prop :=
  Consecutive (Adjacent G) path

def SpansVertices (path : List (Vertex n)) : Prop :=
  ∀ v : Vertex n, v ∈ path

def SimplePath (G : FiniteGraph n) (path : List (Vertex n)) : Prop :=
  path.Nodup ∧ Walk G path

/-- A spanning simple path whose first and last vertices are prescribed. -/
def HamiltonPath (G : FiniteGraph n) (s t : Vertex n) : Prop :=
  ∃ path : List (Vertex n),
    path.head? = some s ∧
      path.getLast? = some t ∧
      path.Nodup ∧
      SpansVertices path ∧
      Walk G path

def ClosedPath (G : FiniteGraph n) (path : List (Vertex n)) : Prop :=
  ∃ s t : Vertex n,
    path.head? = some s ∧
      path.getLast? = some t ∧
      Walk G path ∧
      Adjacent G t s

/-- A simple cycle visiting every vertex exactly once. -/
def HamiltonCycle (G : FiniteGraph n) : Prop :=
  ∃ path : List (Vertex n),
    path.Nodup ∧ SpansVertices path ∧ ClosedPath G path

def Hamiltonian (G : FiniteGraph n) : Prop := HamiltonCycle G

def HamiltonConnected (G : FiniteGraph n) : Prop :=
  ∀ s t : Vertex n, s ≠ t → HamiltonPath G s t

def Cycle (G : FiniteGraph n) (path : List (Vertex n)) : Prop :=
  path.Nodup ∧ path ≠ [] ∧ ClosedPath G path

def VertexPancyclic (G : FiniteGraph n) : Prop :=
  ∀ v : Vertex n, ∀ ℓ : Nat,
    3 ≤ ℓ → ℓ ≤ n →
      ∃ path : List (Vertex n),
        path.length = ℓ ∧ v ∈ path ∧ Cycle G path

/-- Hamiltonian notions over an explicitly enumerated finite vertex list.
These relation-level versions are useful for colouring states, whose natural
carrier is a structure type rather than `Fin n`. -/
def CoversList (vertices path : List α) : Prop :=
  ∀ v, v ∈ vertices ↔ v ∈ path

def HamiltonPathOn (vertices : List α) (r : α → α → Prop)
    (s t : α) : Prop :=
  ∃ path : List α,
    path.head? = some s ∧
      path.getLast? = some t ∧
      path.Nodup ∧
      CoversList vertices path ∧
      Consecutive r path

def HamiltonConnectedOn (vertices : List α) (r : α → α → Prop) : Prop :=
  ∀ s t, s ∈ vertices → t ∈ vertices → s ≠ t →
    HamiltonPathOn vertices r s t

def ClosedPathOn (r : α → α → Prop) (path : List α) : Prop :=
  ∃ s t : α,
    path.head? = some s ∧
      path.getLast? = some t ∧
      Consecutive r path ∧
      r t s

def HamiltonCycleOn (vertices : List α) (r : α → α → Prop) : Prop :=
  ∃ path : List α,
    path.Nodup ∧ CoversList vertices path ∧ ClosedPathOn r path

/-- Splice two disjoint endpoint-prescribed Hamilton paths into one cycle.
The cross edges are explicit hypotheses; this is the generic cut-and-join
step used by the fibre restoration arguments. -/
theorem HamiltonPathOn.splice
    {α : Type u} {r : α → α → Prop}
    {v₁ v₂ : List α} {a b c d : α}
    (h₁ : HamiltonPathOn v₁ r a b)
    (h₂ : HamiltonPathOn v₂ r c d)
    (hdis : ∀ ⦃x⦄, x ∈ v₁ → x ∉ v₂)
    (hbc : r b c) (hda : r d a) :
    HamiltonCycleOn (v₁ ++ v₂) r := by
  rcases h₁ with ⟨p₁, hp₁, hq₁, hn₁, hc₁, hw₁⟩
  rcases h₂ with ⟨p₂, hp₂, hq₂, hn₂, hc₂, hw₂⟩
  have hdisPath : ∀ ⦃x⦄, x ∈ p₁ → x ∉ p₂ := by
    intro x hx₁ hx₂
    exact hdis (hc₁ x |>.mpr hx₁) (hc₂ x |>.mpr hx₂)
  have hnodup : (p₁ ++ p₂).Nodup := by
    apply List.nodup_append.mpr
    refine ⟨hn₁, hn₂, ?_⟩
    intro x hx₁ y hy₂ hxy
    apply hdisPath hx₁
    exact hxy ▸ hy₂
  have hcon : Consecutive r (p₁ ++ p₂) := by
    apply consecutive_append hw₁ hw₂
      (by intro h; subst p₁; simp at hp₁)
      (by intro h; subst p₂; simp at hp₂)
      hq₁ hp₂ hbc
  have hp₁ne : p₁ ≠ [] := by
    intro h
    subst p₁
    simp at hp₁
  have hp₂ne : p₂ ≠ [] := by
    intro h
    subst p₂
    simp at hp₂
  have hhead : (p₁ ++ p₂).head? = some a := by
    rw [head_append_of_ne_nil hp₁ne, hp₁]
  have hlast : (p₁ ++ p₂).getLast? = some d := by
    rw [getLast_append_of_ne_nil hp₂ne, hq₂]
  refine ⟨p₁ ++ p₂, hnodup, ?_, ?_⟩
  · intro x
    simp only [List.mem_append]
    constructor
    · intro hx
      rcases hx with hx | hx
      · exact Or.inl ((hc₁ x).mp hx)
      · exact Or.inr ((hc₂ x).mp hx)
    · intro hx
      rcases hx with hx | hx
      · exact Or.inl ((hc₁ x).mpr hx)
      · exact Or.inr ((hc₂ x).mpr hx)
  · exact ⟨a, d, hhead, hlast, hcon, hda⟩

private theorem nodup_map_of_injective {α : Type u} {β : Type v}
    (f : α → β) (hf : Function.Injective f) :
    ∀ {xs : List α}, xs.Nodup → (xs.map f).Nodup := by
  intro xs h
  induction xs with
  | nil => simp
  | cons x xs ih =>
      change (f x :: xs.map f).Nodup
      rw [List.nodup_cons] at h ⊢
      refine ⟨?_, ih h.2⟩
      intro hmem
      rcases List.mem_map.mp hmem with ⟨y, hy, hxy⟩
      exact h.1 (hf hxy ▸ hy)

private theorem consecutive_map_of_rel {α : Type u} {β : Type v}
    {r : α → α → Prop} {s : β → β → Prop}
    (f : α → β) (hrel : ∀ ⦃x y⦄, r x y → s (f x) (f y)) :
    ∀ {xs : List α}, Consecutive r xs →
      Consecutive s (xs.map f) := by
  intro xs
  induction xs with
  | nil => intro _; trivial
  | cons x xs ih =>
      cases xs with
      | nil => intro _; trivial
      | cons y ys =>
          intro h
          exact ⟨hrel h.1, ih h.2⟩

theorem HamiltonPathOn.map {α : Type u} {β : Type v}
    {r : α → α → Prop} {s : β → β → Prop}
    (f : α → β) (hf : Function.Injective f)
    (hrel : ∀ ⦃x y⦄, r x y → s (f x) (f y))
    {vertices : List α} {a b : α}
    (h : HamiltonPathOn vertices r a b) :
    HamiltonPathOn (vertices.map f) s (f a) (f b) := by
  rcases h with ⟨path, hhead, hlast, hnodup, hcover, hcon⟩
  refine ⟨path.map f, ?_, ?_, nodup_map_of_injective f hf hnodup, ?_,
    consecutive_map_of_rel f hrel hcon⟩
  · rw [List.head?_map]
    simpa [hhead]
  · rw [List.getLast?_map]
    simpa [hlast]
  · intro y
    constructor
    · intro hy
      rcases List.mem_map.mp hy with ⟨x, hx, rfl⟩
      exact List.mem_map_of_mem ((hcover x).mp hx)
    · intro hy
      rcases List.mem_map.mp hy with ⟨x, hx, rfl⟩
      exact List.mem_map_of_mem ((hcover x).mpr hx)

private theorem consecutive_append_singleton {α : Type u} {r : α → α → Prop}
    : ∀ {ys : List α} {a z : α},
      Consecutive r ys → ys.getLast? = some z → r z a →
      Consecutive r (ys ++ [a]) := by
  intro ys
  induction ys with
  | nil =>
    intro a z h hz hza
    cases hz
  | cons y tail ih =>
    cases tail with
    | nil =>
      intro a z h hz hza
      simp only [List.cons_append, List.nil_append, Consecutive] at h ⊢
      simp only [List.getLast?_eq_some_iff] at hz
      rcases hz with ⟨ys, hys⟩
      cases ys with
      | nil =>
        simp at hys
        subst z
        exact ⟨hza, trivial⟩
      | cons q qs =>
        simp at hys
    | cons y' rest =>
      intro a z h hz hza
      have htail : Consecutive r (y' :: rest) := h.2
      have hz' : (y' :: rest).getLast? = some z := by simpa using hz
      have htail' := ih (a := a) (z := z) htail hz' hza
      simpa [List.cons_append, Consecutive] using And.intro h.1 htail'

theorem consecutive_reverse_of_symmetric {α : Type u} {r : α → α → Prop}
    (hsym : ∀ a b, r a b → r b a) :
    ∀ {xs : List α}, Consecutive r xs → Consecutive r xs.reverse := by
  intro xs
  induction xs with
  | nil => intro _; simp [Consecutive]
  | cons a tail ih =>
    cases tail with
    | nil => intro _; simp [Consecutive]
    | cons b rest =>
      intro h
      have hrest : Consecutive r (b :: rest) := h.2
      have ihh : Consecutive r (b :: rest).reverse := ih hrest
      have hlast : (b :: rest).reverse.getLast? = some b := by
        rw [List.getLast?_eq_some_iff]
        exact ⟨rest.reverse, by simp⟩
      have happ := consecutive_append_singleton ihh hlast (hsym a b h.1)
      simpa [List.reverse_cons, List.reverse_append] using happ

private theorem nodup_reverse {α : Type} :
    ∀ {xs : List α}, xs.Nodup → xs.reverse.Nodup := by
  intro xs
  induction xs with
  | nil =>
      intro _
      simp
  | cons a tail ih =>
      intro h
      have htail : tail.Nodup := (List.nodup_cons.mp h).2
      have ha : ¬ a ∈ tail := (List.nodup_cons.mp h).1
      have ha' : ¬ a ∈ tail.reverse := by
        intro hat
        exact ha ((List.mem_reverse.mp hat))
      rw [List.reverse_cons]
      apply (List.nodup_append).2
      refine ⟨ih htail, by simp, ?_⟩
      intro x hx y hy
      simp only [List.mem_singleton] at hy
      subst y
      intro hxa
      apply ha'
      simpa [hxa] using hx

theorem HamiltonPath.reverse_of_symmetric {n : Nat} {G : FiniteGraph n}
    {s t : Vertex n}
    (hsym : ∀ a b, Adjacent G a b → Adjacent G b a)
    (h : HamiltonPath G s t) : HamiltonPath G t s := by
  rcases h with ⟨path, hhead, hlast, hnodup, hspan, hwalk⟩
  refine ⟨path.reverse, ?_, ?_, ?_, ?_, ?_⟩
  · rw [List.head?_reverse]
    exact hlast
  · rw [List.getLast?_reverse]
    exact hhead
  · exact nodup_reverse hnodup
  · intro v
    exact (List.mem_reverse).2 (hspan v)
  · exact consecutive_reverse_of_symmetric hsym hwalk

theorem mem_of_head?_eq_some {α : Type} {path : List α} {v : α}
    (h : path.head? = some v) : v ∈ path := by
  rw [List.head?_eq_some_iff] at h
  rcases h with ⟨tail, rfl⟩
  exact List.mem_cons_self

theorem mem_of_getLast?_eq_some {α : Type} {path : List α} {v : α}
    (h : path.getLast? = some v) : v ∈ path := by
  rw [List.getLast?_eq_some_iff] at h
  rcases h with ⟨ys, rfl⟩
  exact List.mem_append_right ys (List.mem_singleton_self v)

theorem spans_nonempty {n : Nat} {path : List (Vertex n)}
    (hn : 0 < n) (hspan : SpansVertices path) : path ≠ [] := by
  intro hnil
  subst path
  have hmem := hspan ⟨0, hn⟩
  simp at hmem

theorem HamiltonPath.start_mem {n : Nat} {G : FiniteGraph n} {s t : Vertex n}
    (h : HamiltonPath G s t) :
      ∃ path : List (Vertex n), path.head? = some s ∧ s ∈ path := by
  rcases h with ⟨path, hhead, _, _, _, _⟩
  exact ⟨path, hhead, mem_of_head?_eq_some hhead⟩

theorem HamiltonPath.end_mem {n : Nat} {G : FiniteGraph n} {s t : Vertex n}
    (h : HamiltonPath G s t) :
      ∃ path : List (Vertex n), path.getLast? = some t ∧ t ∈ path := by
  rcases h with ⟨path, _, hlast, _, _, _⟩
  exact ⟨path, hlast, mem_of_getLast?_eq_some hlast⟩

theorem HamiltonPath.spans {n : Nat} {G : FiniteGraph n} {s t : Vertex n}
    (h : HamiltonPath G s t) :
      ∃ path : List (Vertex n), path.Nodup ∧ SpansVertices path := by
  rcases h with ⟨path, _, _, hnodup, hspan, _⟩
  exact ⟨path, hnodup, hspan⟩

theorem HamiltonCycle.spans {n : Nat} {G : FiniteGraph n}
    (h : HamiltonCycle G) :
      ∃ path : List (Vertex n), path.Nodup ∧ SpansVertices path := by
  rcases h with ⟨path, hnodup, hspan, _⟩
  exact ⟨path, hnodup, hspan⟩

theorem Cycle.nonempty {n : Nat} {G : FiniteGraph n} {path : List (Vertex n)}
    (h : Cycle G path) : path ≠ [] := h.2.1

theorem Cycle.length_pos {n : Nat} {G : FiniteGraph n} {path : List (Vertex n)}
    (h : Cycle G path) : 0 < path.length := by
  cases path with
  | nil => exact False.elim (h.2.1 rfl)
  | cons a tail => simp

private theorem spans_nonempty_of_closed {n : Nat} {G : FiniteGraph n}
    {path : List (Vertex n)} (h : ClosedPath G path) : path ≠ [] := by
  rcases h with ⟨s, t, hhead, hlast, _, _⟩
  intro hnil
  subst path
  simp at hhead

theorem HamiltonCycle.isCycle {n : Nat} {G : FiniteGraph n}
    (h : HamiltonCycle G) : ∃ path, Cycle G path := by
  rcases h with ⟨path, hnodup, hspan, hclosed⟩
  exact ⟨path, hnodup, spans_nonempty_of_closed hclosed, hclosed⟩

end PlanarRecoloring
