import PlanarRecoloring.Core

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
  simpa using hmem

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
