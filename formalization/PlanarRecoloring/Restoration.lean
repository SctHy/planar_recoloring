import PlanarRecoloring.Hamilton

/-!
# Generic restoration interfaces

This file records two combinatorial steps used by the restoration arguments in
Chapter 5.  The first is the exact component-label quotient for two fibres:
constant fibres have labels `0,1`, while a nonconstant fibre has the single
label `*`.  The second is the finite port-counting step behind a protected
spanning-tree splice.  Neither result mentions the concrete Appendix A--D
certificates; those certificates can be supplied as separate hypotheses.
-/

namespace PlanarRecoloring

/-- The two components of a constant fibre and the unique component of a
nonconstant fibre.  `none` denotes the latter. -/
abbrev ComponentLabel := Option (Fin 2)

/-- Exact one-factor overlap rule across one base edge.

Two constant fibres preserve the component label.  Whenever at least one side
is nonconstant, every label on the constant side meets the unique component on
the other side. -/
def componentTransition : ComponentLabel → ComponentLabel → Prop
  | some a, some b => a = b
  | _, _ => True

/-- Product component labels for two restored fibres. -/
abbrev ProductComponentLabel := ComponentLabel × ComponentLabel

def productComponentTransition :
    ProductComponentLabel → ProductComponentLabel → Prop
  | (a₁, a₂), (b₁, b₂) =>
      componentTransition a₁ b₁ ∧ componentTransition a₂ b₂

/-- Reflexive-transitive closure used for component-graph paths. -/
inductive Reachable {α : Type u} (r : α → α → Prop) : α → α → Prop
  | refl (a : α) : Reachable r a a
  | step {a b c : α} : r a b → Reachable r b c → Reachable r a c

namespace Reachable

@[simp] theorem refl_eq {α : Type u} {r : α → α → Prop} (a : α) :
    Reachable r a a := .refl a

theorem trans {α : Type u} {r : α → α → Prop}
    {a b c : α} (hab : Reachable r a b) (hbc : Reachable r b c) :
    Reachable r a c := by
  induction hab with
  | refl => exact hbc
  | step hab _ ih => exact .step hab (ih hbc)

theorem of_edge {α : Type u} {r : α → α → Prop}
    {a b : α} (h : r a b) : Reachable r a b :=
  .step h (.refl b)

end Reachable

@[simp] theorem componentTransition_to_star (a : ComponentLabel) :
    componentTransition a none := by
  cases a <;> simp [componentTransition]

@[simp] theorem componentTransition_star (a : ComponentLabel) :
    componentTransition none a := by
  simp [componentTransition]

/-- Every product component reaches the component in which both labels have
been reset to `*`.  The two coordinates are reset independently. -/
theorem productComponentLabel_reaches_reset
    (x : ProductComponentLabel) :
    Reachable productComponentTransition x (none, none) := by
  rcases x with ⟨a, b⟩
  have h₁ : productComponentTransition (a, b) (none, b) := by
    have hbb : componentTransition b b := by
      cases b <;> simp [componentTransition]
    exact ⟨componentTransition_to_star a, hbb⟩
  have h₂ : productComponentTransition (none, b) (none, none) := by
    have haa : componentTransition none none := by simp [componentTransition]
    exact ⟨haa, componentTransition_to_star b⟩
  exact Reachable.trans (Reachable.of_edge h₁) (Reachable.of_edge h₂)

/-- The quotient component graph is connected once both coordinates have a
reset transition.  The path is oriented toward the common reset checkpoint;
reversing the edge relation gives the corresponding undirected statement. -/
theorem productComponentLabel_connected
    (x y : ProductComponentLabel) :
    Reachable productComponentTransition x (none, none) ∧
      Reachable productComponentTransition y (none, none) := by
  exact ⟨productComponentLabel_reaches_reset x,
    productComponentLabel_reaches_reset y⟩

/-- A finite list of ports contains one port outside every shorter list of
already-used ports, provided the ports are pairwise distinct. -/
theorem exists_unused_port
    {α : Type u} [BEq α] [LawfulBEq α]
    (ports used : List α)
    (hports : ports.Nodup) (hused : used.Nodup)
    (hlen : used.length < ports.length) :
    ∃ p, p ∈ ports ∧ p ∉ used := by
  have length_le_of_mem_of_nodup :
      ∀ {xs ys : List α}, xs.Nodup → ys.Nodup →
        (∀ a, a ∈ xs → a ∈ ys) → xs.length ≤ ys.length := by
    intro xs
    induction xs with
    | nil =>
      intro ys _ _ _
      simp
    | cons x xs ih =>
      intro ys hxs hys hsub
      have hxys : x ∈ ys := hsub x (by simp)
      have hxs_tail : xs.Nodup := (List.nodup_cons.mp hxs).2
      have hys_erase : (ys.erase x).Nodup :=
        List.Nodup.sublist List.erase_sublist hys
      have hsub_tail : ∀ a, a ∈ xs → a ∈ ys.erase x := by
        intro a ha
        have hax : a ≠ x := by
          intro hax
          subst a
          exact (List.nodup_cons.mp hxs).1 ha
        exact (List.mem_erase_of_ne hax).mpr (hsub a (by simp [ha]))
      have htail : xs.length ≤ (ys.erase x).length :=
        ih hxs_tail hys_erase hsub_tail
      have htail' : xs.length + 1 ≤ (ys.erase x).length + 1 :=
        Nat.add_le_add_right htail 1
      have hyspos : 0 < ys.length := by
        cases ys with
        | nil => simp at hxys
        | cons y ys => simp
      have herase : (ys.erase x).length + 1 = ys.length := by
        rw [List.length_erase_of_mem hxys]
        omega
      simpa [List.length_cons, herase, Nat.add_comm, Nat.add_left_comm,
        Nat.add_assoc] using htail'
  by_cases hex : ∃ p, p ∈ ports ∧ p ∉ used
  · exact hex
  · have hall : ∀ a, a ∈ ports → a ∈ used := by
      intro a ha
      by_cases hau : a ∈ used
      · exact hau
      · exact False.elim (hex ⟨a, ha, hau⟩)
    have hle : ports.length ≤ used.length :=
      length_le_of_mem_of_nodup hports hused hall
    exact False.elim ((Nat.not_lt_of_ge hle) hlen)

/-- The port-counting inequality used when a tree vertex has at most `Δ`
incident attachments.  At the moment of attaching a child, at most
`degree - 1` ports at the parent have been consumed, so `Δ + 2` protected
ports leave a fresh one. -/
theorem exists_unused_protected_port
    {α : Type u} [BEq α] [LawfulBEq α]
    (ports used : List α) (Δ degree : Nat)
    (hports : ports.Nodup) (hused : used.Nodup)
    (hdegree : degree ≤ Δ)
    (hconsumed : used.length ≤ degree - 1)
    (hreserve : Δ + 2 ≤ ports.length) :
    ∃ p, p ∈ ports ∧ p ∉ used := by
  apply exists_unused_port ports used hports hused
  omega

end PlanarRecoloring
