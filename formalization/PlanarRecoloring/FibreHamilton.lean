import PlanarRecoloring.FibreChain
import PlanarRecoloring.Hamilton

/-!
# Turning fibre certificates into Hamilton certificates

The fibre files describe paths by their exact lists of vertices.  This file
records the small interface needed to use such a certificate in the finite
graph language of `Hamilton.lean`: covering the ambient vertex type upgrades a
fibre path to a Hamilton path, and a closing edge upgrades it to a Hamilton
cycle.  No existence of the fibre path is asserted here.
-/

namespace PlanarRecoloring

def FibrePath.map {α : Type u} {r s : α → α → Prop}
    (h : ∀ ⦃x y⦄, r x y → s x y) (p : FibrePath r) : FibrePath s :=
  { fibre := p.fibre
    path := p.path
    start := p.start
    finish := p.finish
    head_eq := p.head_eq
    last_eq := p.last_eq
    nodup := p.nodup
    covers := p.covers
    walk := consecutive_mono h p.walk }

def ClosedFibrePath.map {α : Type u} {r s : α → α → Prop}
    (h : ∀ ⦃x y⦄, r x y → s x y) (p : ClosedFibrePath r) :
    ClosedFibrePath s :=
  { path := p.path.map h
    close := h p.close }

theorem FibrePath.toHamiltonPathOn {α : Type u} {r : α → α → Prop}
    (p : FibrePath r) :
    HamiltonPathOn p.fibre.vertices r p.start p.finish := by
  refine ⟨p.path, p.head_eq, p.last_eq, p.nodup, ?_, p.walk⟩
  intro v
  exact p.covers v

/- Reversing a supplied fibre path is the endpoint-exchange operation used
   when a lift is constructed in the opposite direction. -/
def FibrePath.reverse_of_symmetric {α : Type u} {r : α → α → Prop}
    (hsym : ∀ ⦃x y⦄, r x y → r y x) (p : FibrePath r) :
    FibrePath r := by
  refine
    { fibre := p.fibre
      path := p.path.reverse
      start := p.finish
      finish := p.start
      head_eq := ?_
      last_eq := ?_
      nodup := ?_
      covers := ?_
      walk := ?_ }
  · rw [List.head?_reverse]
    exact p.last_eq
  · rw [List.getLast?_reverse]
    exact p.head_eq
  · exact (List.reverse_perm p.path).symm.nodup p.nodup
  · intro x
    rw [List.mem_reverse]
    exact p.covers x
  · exact consecutive_reverse_of_symmetric hsym p.walk

theorem ClosedFibrePath.toHamiltonCycleOn {α : Type u} {r : α → α → Prop}
    (p : ClosedFibrePath r) :
    HamiltonCycleOn p.path.fibre.vertices r := by
  refine ⟨p.path.path, p.path.nodup, ?_, ?_⟩
  · intro v
    exact p.path.covers v
  · exact ⟨p.path.start, p.path.finish, p.path.head_eq, p.path.last_eq,
      p.path.walk, p.close⟩

theorem FibrePath.toHamiltonPath {n : Nat} {G : FiniteGraph n}
    (p : FibrePath (Adjacent G))
    (hspan : ∀ v : Vertex n, v ∈ p.fibre.vertices) :
    HamiltonPath G p.start p.finish := by
  refine ⟨p.path, p.head_eq, p.last_eq, p.nodup, ?_, p.walk⟩
  intro v
  exact (p.covers v).mp (hspan v)

theorem ClosedFibrePath.toHamiltonCycle {n : Nat} {G : FiniteGraph n}
    (p : ClosedFibrePath (Adjacent G))
    (hspan : ∀ v : Vertex n, v ∈ p.path.fibre.vertices) :
    HamiltonCycle G := by
  refine ⟨p.path.path, p.path.nodup, ?_, ?_⟩
  · intro v
    exact (p.path.covers v).mp (hspan v)
  · refine ⟨p.path.start, p.path.finish, p.path.head_eq, p.path.last_eq,
      p.path.walk, p.close⟩

theorem fibreCycle_chain_toHamiltonCycle {n : Nat} {G : FiniteGraph n}
    {inside bridge : Vertex n → Vertex n → Prop}
    (ps : List (FibrePath inside)) (hne : ps ≠ [])
    (hbridges : FibreChainBridges bridge ps)
    (hdis : FibreChainDisjoint ps)
    (hclose : bridge (ps.getLast hne).finish (ps.head hne).start)
    (hinside : ∀ ⦃x y⦄, inside x y → Adjacent G x y)
    (hbridge : ∀ ⦃x y⦄, bridge x y → Adjacent G x y)
    (hspan : ∀ v : Vertex n, v ∈ fibreChainVertices ps) :
    HamiltonCycle G := by
  let hlayer : ∀ ⦃x y⦄, LayeredEdge inside bridge x y → Adjacent G x y := by
    intro x y hxy
    rcases hxy with hxy | hxy
    · exact hinside hxy
    · exact hbridge hxy
  let closed := fibreCycle_chain ps hne hbridges hdis hclose
  exact ClosedFibrePath.toHamiltonCycle (ClosedFibrePath.map hlayer closed) hspan

end PlanarRecoloring
