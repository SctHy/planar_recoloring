import PlanarRecoloring.Fibre

/-!
# Concatenating an arbitrary chain of fibres

The hypotheses state the precise combinatorial interface used by a fibre
lift: fibre paths are pairwise disjoint, and consecutive endpoints are
joined by bridge edges.  The resulting path is the literal concatenation
of all the supplied paths.  No existence of the individual fibre paths is
assumed beyond the supplied data.
-/

namespace PlanarRecoloring

def fibreChainVertices {α : Type u} {inside : α → α → Prop}
    (ps : List (FibrePath inside)) : List α :=
  (ps.map (fun p => p.fibre.vertices)).flatten

def fibreChainPaths {α : Type u} {inside : α → α → Prop}
    (ps : List (FibrePath inside)) : List α :=
  (ps.map (fun p => p.path)).flatten

def FibreChainDisjoint {α : Type u} {inside : α → α → Prop}
    (ps : List (FibrePath inside)) : Prop :=
  ps.Pairwise (fun p q => DisjointLists p.fibre.vertices q.fibre.vertices)

def FibreChainBridges {α : Type u} {inside : α → α → Prop}
    (bridge : α → α → Prop) (ps : List (FibrePath inside)) : Prop :=
  Consecutive (fun p q => bridge p.finish q.start) ps

theorem mem_fibreChainVertices {α : Type u} {inside : α → α → Prop}
    {ps : List (FibrePath inside)} {x : α} :
    x ∈ fibreChainVertices ps ↔ ∃ p, p ∈ ps ∧ x ∈ p.fibre.vertices := by
  change x ∈ (ps.map (fun p => p.fibre.vertices)).flatten ↔ _
  rw [List.mem_flatten]
  constructor
  · rintro ⟨l, hl, hx⟩
    rcases List.mem_map.mp hl with ⟨p, hp, hpl⟩
    subst l
    exact ⟨p, hp, hx⟩
  · rintro ⟨p, hp, hx⟩
    exact ⟨p.fibre.vertices, List.mem_map_of_mem hp, hx⟩

theorem mem_fibreChainPaths {α : Type u} {inside : α → α → Prop}
    {ps : List (FibrePath inside)} {x : α} :
    x ∈ fibreChainPaths ps ↔ ∃ p, p ∈ ps ∧ x ∈ p.path := by
  change x ∈ (ps.map (fun p => p.path)).flatten ↔ _
  rw [List.mem_flatten]
  constructor
  · rintro ⟨l, hl, hx⟩
    rcases List.mem_map.mp hl with ⟨p, hp, hpl⟩
    subst l
    exact ⟨p, hp, hx⟩
  · rintro ⟨p, hp, hx⟩
    exact ⟨p.path, List.mem_map_of_mem hp, hx⟩

theorem fibreChain_covers {α : Type u} {inside : α → α → Prop}
    (ps : List (FibrePath inside)) (x : α) :
    x ∈ fibreChainVertices ps ↔ x ∈ fibreChainPaths ps := by
  rw [mem_fibreChainVertices, mem_fibreChainPaths]
  constructor
  · rintro ⟨p, hp, hx⟩
    exact ⟨p, hp, (p.covers x).mp hx⟩
  · rintro ⟨p, hp, hx⟩
    exact ⟨p, hp, (p.covers x).mpr hx⟩

theorem fibreChainPaths_ne_nil {α : Type u} {inside : α → α → Prop}
    {ps : List (FibrePath inside)} (hne : ps ≠ []) :
    fibreChainPaths ps ≠ [] := by
  cases ps with
  | nil => exact False.elim (hne rfl)
  | cons p ps =>
    intro heq
    have hp : p.start ∈ p.path := by
      exact List.mem_of_head? p.head_eq
    have hall : p.start ∈ fibreChainPaths (p :: ps) :=
      mem_fibreChainPaths.mpr ⟨p, by simp, hp⟩
    simp [heq] at hall

theorem head_fibreChainPaths {α : Type u} {inside : α → α → Prop}
    {ps : List (FibrePath inside)} (hne : ps ≠ []) :
    (fibreChainPaths ps).head? = some (ps.head hne).start := by
  cases ps with
  | nil => exact False.elim (hne rfl)
  | cons p ps =>
    change (p.path ++ fibreChainPaths ps).head? = some p.start
    rw [head_append_of_ne_nil p.path_ne_nil, p.head_eq]

theorem last_fibreChainPaths {α : Type u} {inside : α → α → Prop}
    {ps : List (FibrePath inside)} (hne : ps ≠ []) :
    (fibreChainPaths ps).getLast? = some (ps.getLast hne).finish := by
  induction ps with
  | nil => exact False.elim (hne rfl)
  | cons p ps ih =>
    cases ps with
    | nil => simpa [fibreChainPaths] using p.last_eq
    | cons q qs =>
      change (p.path ++ fibreChainPaths (q :: qs)).getLast? =
        some ((q :: qs).getLast (by simp)).finish
      rw [getLast_append_of_ne_nil (fibreChainPaths_ne_nil (by simp))]
      exact ih (by simp)

theorem nodup_fibreChainPaths {α : Type u} {inside : α → α → Prop}
    {ps : List (FibrePath inside)} (hdis : FibreChainDisjoint ps) :
    (fibreChainPaths ps).Nodup := by
  induction ps with
  | nil => simp [fibreChainPaths]
  | cons p ps ih =>
    rcases List.pairwise_cons.mp hdis with ⟨hpdis, htail⟩
    change (p.path ++ fibreChainPaths ps).Nodup
    apply nodup_append_of_disjoint p.nodup (ih htail)
    intro x hxp hxall
    rcases mem_fibreChainPaths.mp hxall with ⟨q, hq, hxq⟩
    exact hpdis q hq ((p.covers x).mpr hxp) ((q.covers x).mpr hxq)

theorem consecutive_fibreChainPaths {α : Type u}
    {inside bridge : α → α → Prop} {ps : List (FibrePath inside)}
    (hbridges : FibreChainBridges bridge ps) :
    Consecutive (LayeredEdge inside bridge) (fibreChainPaths ps) := by
  induction ps with
  | nil => trivial
  | cons p ps ih =>
    cases ps with
    | nil =>
      have hp : Consecutive (LayeredEdge inside bridge) p.path :=
        consecutive_mono (r := inside) (s := LayeredEdge inside bridge)
          (fun _ _ h => Or.inl h) p.walk
      simpa [fibreChainPaths] using hp
    | cons q qs =>
      rcases hbridges with ⟨hpq, htail⟩
      change Consecutive (LayeredEdge inside bridge)
        (p.path ++ fibreChainPaths (q :: qs))
      apply consecutive_append
        (consecutive_mono (fun _ _ h => Or.inl h) p.walk)
        (ih htail) p.path_ne_nil
        (fibreChainPaths_ne_nil (by simp)) p.last_eq
        (head_fibreChainPaths (by simp))
      exact Or.inr hpq

/-- Join any nonempty chain, retaining the exact flattened path and fibre. -/
def fibrePath_chain {α : Type u} {inside bridge : α → α → Prop}
    (ps : List (FibrePath inside)) (hne : ps ≠ [])
    (hbridges : FibreChainBridges bridge ps)
    (hdis : FibreChainDisjoint ps) : FibrePath (LayeredEdge inside bridge) :=
  { fibre := ⟨fibreChainVertices ps⟩
    path := fibreChainPaths ps
    start := (ps.head hne).start
    finish := (ps.getLast hne).finish
    head_eq := head_fibreChainPaths hne
    last_eq := last_fibreChainPaths hne
    nodup := nodup_fibreChainPaths hdis
    covers := fibreChain_covers ps
    walk := consecutive_fibreChainPaths hbridges }

theorem fibrePath_chain_path {α : Type u} {inside bridge : α → α → Prop}
    (ps : List (FibrePath inside)) (hne : ps ≠ [])
    (hbridges : FibreChainBridges bridge ps) (hdis : FibreChainDisjoint ps) :
    (fibrePath_chain ps hne hbridges hdis).path =
      (ps.map (fun p => p.path)).flatten := rfl

theorem fibrePath_chain_vertices {α : Type u} {inside bridge : α → α → Prop}
    (ps : List (FibrePath inside)) (hne : ps ≠ [])
    (hbridges : FibreChainBridges bridge ps) (hdis : FibreChainDisjoint ps) :
    (fibrePath_chain ps hne hbridges hdis).fibre.vertices =
      (ps.map (fun p => p.fibre.vertices)).flatten := rfl

/-- A closing bridge turns the concatenation into a closed fibre path. -/
def fibreCycle_chain {α : Type u} {inside bridge : α → α → Prop}
    (ps : List (FibrePath inside)) (hne : ps ≠ [])
    (hbridges : FibreChainBridges bridge ps)
    (hdis : FibreChainDisjoint ps)
    (hclose : bridge (ps.getLast hne).finish (ps.head hne).start) :
    ClosedFibrePath (LayeredEdge inside bridge) :=
  { path := fibrePath_chain ps hne hbridges hdis
    close := Or.inr hclose }

end PlanarRecoloring
