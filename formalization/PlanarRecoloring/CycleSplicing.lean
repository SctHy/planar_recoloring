import PlanarRecoloring.Hamilton

/-!
# Generic cyclic edge cutting and cycle splicing

The restoration proofs repeatedly cut one edge from a reference cycle and use
its two endpoints as the ends of a Hamilton path.  A `CyclicWitness` records
the actual cycle list, so an edge selected for cutting is a concrete edge of
the witness.  `CycleCut` records the corresponding cyclic rotation and its
walk proof; nodup and coverage are derived from a list permutation.  No
concrete Appendix A--D certificate is imported here.
-/

namespace PlanarRecoloring

/-- A nonempty simple cycle witness over an explicitly listed vertex set. -/
structure CyclicWitness {α : Type u} (vertices : List α)
    (r : α → α → Prop) where
  path : List α
  nodup : path.Nodup
  covers : CoversList vertices path
  head : α
  last : α
  head_eq : path.head? = some head
  last_eq : path.getLast? = some last
  walk : Consecutive r path
  close : r last head

/-- Explicit data for cutting the directed edge `x → y` from a cycle.  The
rotation hypothesis is the local, checkable statement that the cyclic order
remaining after the cut is a walk. -/
structure CycleCut {α : Type u} {vertices : List α}
    {r : α → α → Prop} (C : CyclicWitness vertices r) where
  x : α
  y : α
  leftPart : List α
  rightPart : List α
  decomposition : C.path = leftPart ++ [x, y] ++ rightPart
  edge : r x y
  rotated_walk : Consecutive r (y :: rightPart ++ leftPart ++ [x])

private theorem cycle_rotation_perm {α : Type u}
    (leftPart rightPart : List α) (x y : α) :
    (y :: rightPart ++ leftPart ++ [x]).Perm (leftPart ++ [x, y] ++ rightPart) := by
  have ha : (y :: rightPart ++ leftPart ++ [x]).Perm (y :: x :: rightPart ++ leftPart) := by
    simpa [List.append_assoc] using
      (List.Perm.cons y (List.perm_append_singleton x (rightPart ++ leftPart)))
  have hb : (y :: x :: rightPart ++ leftPart).Perm (leftPart ++ (y :: x :: rightPart)) := by
    simpa [List.append_assoc] using (List.perm_append_comm :
      ((y :: x :: rightPart) ++ leftPart).Perm (leftPart ++ (y :: x :: rightPart)))
  have hc : (leftPart ++ (y :: x :: rightPart)).Perm (leftPart ++ (x :: y :: rightPart)) :=
    List.Perm.append_left leftPart (List.Perm.swap x y rightPart)
  exact ha.trans (hb.trans (by simpa [List.append_assoc] using hc))

/-- Cutting a selected cycle edge yields a Hamilton path from its head to its
tail.  The path is the cyclic rotation after the selected edge. -/
theorem CyclicWitness.cut
    {α : Type u} {vertices : List α} {r : α → α → Prop}
    {C : CyclicWitness vertices r} (cut : CycleCut C) :
    HamiltonPathOn vertices r cut.y cut.x := by
  let q : List α := cut.y :: cut.rightPart ++ cut.leftPart ++ [cut.x]
  have hperm : q.Perm C.path := by
    rw [cut.decomposition]
    exact cycle_rotation_perm cut.leftPart cut.rightPart cut.x cut.y
  have hq_nodup : q.Nodup := hperm.symm.nodup C.nodup
  have hq_cover : CoversList vertices q := by
    intro z
    constructor
    · intro hz
      exact (hperm.mem_iff).mpr ((C.covers z).mp hz)
    · intro hz
      exact (C.covers z).mpr ((hperm.mem_iff).mp hz)
  refine ⟨q, ?_, ?_, hq_nodup, hq_cover, ?_⟩
  · simp [q]
  · rw [getLast_append_of_ne_nil (xs := cut.y :: cut.rightPart ++ cut.leftPart)
      (ys := [cut.x]) (by simp)]
    simp
  · exact cut.rotated_walk

/-- Two disjoint cycles can be joined after cutting one concrete edge from
 each.  The two cross edges are the only additional hypotheses needed. -/
theorem splice_cut_cycles
    {α : Type u} {v₁ v₂ : List α} {r : α → α → Prop}
    {C₁ : CyclicWitness v₁ r} {C₂ : CyclicWitness v₂ r}
    (cut₁ : CycleCut C₁) (cut₂ : CycleCut C₂)
    (hdis : ∀ ⦃x⦄, x ∈ v₁ → x ∉ v₂)
    (hcross₁ : r cut₁.x cut₂.y)
    (hcross₂ : r cut₂.x cut₁.y) :
    HamiltonCycleOn (v₁ ++ v₂) r := by
  exact HamiltonPathOn.splice (C₁.cut cut₁) (C₂.cut cut₂) hdis
    hcross₁ hcross₂

/-- A witness-level alias for the usual two-cycle operation. -/
theorem CyclicWitness.splice
    {α : Type u} {v₁ v₂ : List α} {r : α → α → Prop}
    (C₁ : CyclicWitness v₁ r) (C₂ : CyclicWitness v₂ r)
    (cut₁ : CycleCut C₁) (cut₂ : CycleCut C₂)
    (hdis : ∀ ⦃x⦄, x ∈ v₁ → x ∉ v₂)
    (hcross₁ : r cut₁.x cut₂.y)
    (hcross₂ : r cut₂.x cut₁.y) :
    HamiltonCycleOn (v₁ ++ v₂) r :=
  splice_cut_cycles cut₁ cut₂ hdis hcross₁ hcross₂

end PlanarRecoloring
