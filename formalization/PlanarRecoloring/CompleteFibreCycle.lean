import PlanarRecoloring.Complete
import PlanarRecoloring.FibreChain
import PlanarRecoloring.FibreHamilton

/-!
# Complete-fibre cycle lifting

The single-vertex lift in the article first chooses one interface colour at
each base edge and then traverses every available-colour clique between its
two interface colours.  This file packages that final construction without
assuming the clique paths as extra data: `complete_hamiltonPathOn` supplies
them from a duplicate-free finite fibre list and its two endpoint witnesses.
The bridge and disjointness hypotheses remain explicit, so this is a finite
combinatorial lift and does not hide planar or colouring arguments.
-/

namespace PlanarRecoloring

noncomputable section

structure CompleteLayer (α : Type u) where
  vertices : List α
  start : α
  finish : α
  nodup : vertices.Nodup
  start_mem : start ∈ vertices
  finish_mem : finish ∈ vertices
  distinct : start ≠ finish

noncomputable def CompleteLayer.toPath [DecidableEq α]
    (L : CompleteLayer α) : FibrePath (fun x y : α => x ≠ y) := by
  let h := complete_hamiltonPathOn L.vertices L.nodup L.start_mem L.finish_mem
    L.distinct
  let path := Classical.choose h
  have hp := Classical.choose_spec h
  exact
    { fibre := ⟨L.vertices⟩
      path := path
      start := L.start
      finish := L.finish
      head_eq := hp.1
      last_eq := hp.2.1
      nodup := hp.2.2.1
      covers := hp.2.2.2.1
      walk := hp.2.2.2.2 }

def CompleteLayer.paths [DecidableEq α]
    (layers : List (CompleteLayer α)) :
    List (FibrePath (fun x y : α => x ≠ y)) :=
  layers.map CompleteLayer.toPath

def CompleteLayer.Disjoint (L M : CompleteLayer α) : Prop :=
  DisjointLists L.vertices M.vertices

def CompleteLayer.PairwiseDisjoint (layers : List (CompleteLayer α)) : Prop :=
  layers.Pairwise CompleteLayer.Disjoint

def CompleteLayer.BridgeChain (bridge : α → α → Prop)
    (layers : List (CompleteLayer α)) : Prop :=
  Consecutive (fun L M => bridge L.finish M.start) layers

theorem completeLayer_paths_ne_nil [DecidableEq α]
    {layers : List (CompleteLayer α)} (hne : layers ≠ []) :
    CompleteLayer.paths layers ≠ [] := by
  cases layers with
  | nil => exact False.elim (hne rfl)
  | cons L Ls => simp [CompleteLayer.paths]

theorem completeLayer_paths_bridges [DecidableEq α]
    {bridge : α → α → Prop} {layers : List (CompleteLayer α)}
    (hchain : CompleteLayer.BridgeChain bridge layers) :
    FibreChainBridges bridge (CompleteLayer.paths layers) := by
  induction layers with
  | nil => trivial
  | cons L Ls ih =>
      cases Ls with
      | nil => trivial
      | cons M Ms =>
          rcases hchain with ⟨hLM, htail⟩
          refine ⟨?_, ih htail⟩
          change bridge L.finish M.start
          exact hLM

theorem completeLayer_paths_disjoint [DecidableEq α]
    {layers : List (CompleteLayer α)}
    (hdis : CompleteLayer.PairwiseDisjoint layers) :
    FibreChainDisjoint (CompleteLayer.paths layers) := by
  induction layers with
  | nil => simp [FibreChainDisjoint, CompleteLayer.paths]
  | cons L Ls ih =>
      rcases List.pairwise_cons.mp hdis with ⟨hL, htail⟩
      refine List.pairwise_cons.mpr ⟨?_, ih htail⟩
      intro P hP
      rcases List.mem_map.mp hP with ⟨M, hM, rfl⟩
      change DisjointLists L.vertices M.vertices
      exact hL M hM

theorem completeLayer_cycle
    [DecidableEq α]
    {bridge : α → α → Prop}
    {layers : List (CompleteLayer α)}
    (hne : layers ≠ [])
    (hchain : CompleteLayer.BridgeChain bridge layers)
    (hdis : CompleteLayer.PairwiseDisjoint layers)
    (hclose : bridge (layers.getLast hne).finish
      (layers.head hne).start) :
    HamiltonCycleOn
      (fibreChainVertices (CompleteLayer.paths layers))
      (LayeredEdge (fun x y : α => x ≠ y) bridge) := by
  let ps := CompleteLayer.paths layers
  have hps : ps ≠ [] := by
    exact completeLayer_paths_ne_nil hne
  have hbridges : FibreChainBridges bridge ps := by
    exact completeLayer_paths_bridges hchain
  have hdis' : FibreChainDisjoint ps := by
    exact completeLayer_paths_disjoint hdis
  have hclose' : bridge ((ps.getLast hps).finish) ((ps.head hps).start) := by
    change bridge
      ((layers.map CompleteLayer.toPath).getLast hps).finish
      ((layers.map CompleteLayer.toPath).head hps).start
    have hlastmap := List.getLast_map (f := CompleteLayer.toPath)
      (l := layers) hps
    have hheadmap := List.head_map (f := CompleteLayer.toPath)
      (l := layers) hps
    rw [hlastmap]
    rw [hheadmap]
    exact hclose
  exact ClosedFibrePath.toHamiltonCycleOn
    (fibreCycle_chain ps hps hbridges hdis' hclose')

end
end PlanarRecoloring
