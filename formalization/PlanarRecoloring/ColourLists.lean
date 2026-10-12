import PlanarRecoloring.CyclicBinary

namespace PlanarRecoloring

/-- One colour from each finite list, in the same order. -/
def ChoosesFromLists : List (List α) → List α → Prop
  | [], [] => True
  | L :: sets, x :: xs => x ∈ L ∧ ChoosesFromLists sets xs
  | _, _ => False

/-- Duplicate-free lists represent the finite colour sets in the article.
    Their order has no effect on the membership predicates. -/
theorem atLeastTwo_of_nodup_length {L : List α}
    (hn : L.Nodup) (hlen : 2 ≤ L.length) :
    AtLeastTwo (fun x => x ∈ L) := by
  cases L with
  | nil => simp at hlen
  | cons a L =>
      cases L with
      | nil => simp at hlen
      | cons b L =>
          have hab : a ≠ b := by
            intro heq
            subst b
            exact (List.nodup_cons.mp hn).1 (by simp)
          exact ⟨a, b, hab, by simp, by simp⟩

theorem atLeastThree_of_nodup_length {L : List α}
    (hn : L.Nodup) (hlen : 3 ≤ L.length) :
    AtLeastThree (fun x => x ∈ L) := by
  cases L with
  | nil => simp at hlen
  | cons a L =>
      cases L with
      | nil => simp at hlen
      | cons b L =>
          cases L with
          | nil => simp at hlen
          | cons c L =>
              have ha := (List.nodup_cons.mp hn).1
              have hb := (List.nodup_cons.mp (List.nodup_cons.mp hn).2).1
              refine ⟨a, b, c, ?_, ?_, ?_, by simp, by simp, by simp⟩
              · intro heq; subst b; exact ha (by simp)
              · intro heq; subst c; exact ha (by simp)
              · intro heq; subst c; exact hb (by simp)

theorem supports_membership_choices {sets : List (List α)} {xs : List α}
    (h : Supports (sets.map (fun L => fun x => x ∈ L)) xs) :
    ChoosesFromLists sets xs := by
  induction sets generalizing xs with
  | nil =>
      cases xs with
      | nil => trivial
      | cons x xs => exact False.elim h
  | cons L sets ih =>
      cases xs with
      | nil => exact False.elim h
      | cons x xs => exact ⟨h.1, ih h.2.2⟩

/-- The complete finite-set statement of `lem:list-cycle`.  Equality of sets
    is extensional, so the exceptional pair may be listed in either order. -/
theorem finite_list_cycle [DecidableEq α]
    (sets : List (List α)) (hlen : 3 ≤ sets.length)
    (hsets : ∀ L ∈ sets, L.Nodup ∧ 2 ≤ L.length)
    (hnot : ¬ ∃ k a b, sets.length = 2 * k + 1 ∧ a ≠ b ∧
      ∀ L ∈ sets, ∀ x, x ∈ L ↔ x = a ∨ x = b) :
    ∃ xs, ChoosesFromLists sets xs ∧
      CyclicDifferent xs := by
  let predicates := sets.map (fun L => fun x => x ∈ L)
  have htwo : ∀ S ∈ predicates, AtLeastTwo S := by
    intro S hS
    obtain ⟨L, hL, rfl⟩ := List.mem_map.mp hS
    exact atLeastTwo_of_nodup_length (hsets L hL).1 (hsets L hL).2
  have hexception : ¬ ∃ k S a b,
      predicates.length = 2 * k + 1 ∧ ExactlyTwo S a b ∧
        ∀ U ∈ predicates, U = S := by
    rintro ⟨k, S, a, b, hk, hpair, hall⟩
    apply hnot
    refine ⟨k, a, b, by simpa [predicates] using hk, hpair.1, ?_⟩
    intro L hL x
    have hLS := hall (fun x => x ∈ L) (List.mem_map.mpr ⟨L, hL, rfl⟩)
    change (fun x => x ∈ L) x ↔ x = a ∨ x = b
    rw [hLS]
    exact hpair.2 x
  obtain ⟨xs, hxs, hcycle⟩ := cyclic_colours_list_cycle predicates
    (by simpa [predicates] using hlen) htwo hexception
  exact ⟨xs, supports_membership_choices hxs, hcycle⟩

/-- The complete finite-set statement of `lem:bridge-colours`, including
    endpoint avoidance and the one-layer case. -/
theorem finite_bridge_colours [DecidableEq α]
    (sets : List (List α))
    (hsets : ∀ L ∈ sets, L.Nodup ∧ 2 ≤ L.length)
    (hthree : ∃ L ∈ sets, 3 ≤ L.length) (a b : α) :
    ∃ xs, ChoosesFromLists sets xs ∧
      Consecutive (· ≠ ·) xs ∧ StartsAway a xs ∧ EndsAway b xs := by
  let predicates := sets.map (fun L => fun x => x ∈ L)
  have htwo : ∀ S ∈ predicates, AtLeastTwo S := by
    intro S hS
    obtain ⟨L, hL, rfl⟩ := List.mem_map.mp hS
    exact atLeastTwo_of_nodup_length (hsets L hL).1 (hsets L hL).2
  obtain ⟨L, hL, hlen⟩ := hthree
  have hspecial : ∃ S, S ∈ predicates ∧ AtLeastThree S :=
    ⟨fun x => x ∈ L, List.mem_map.mpr ⟨L, hL, rfl⟩,
      atLeastThree_of_nodup_length (hsets L hL).1 hlen⟩
  obtain ⟨xs, hxs, hstart, hend⟩ :=
    bridge_colours_lists predicates htwo hspecial a b
  exact ⟨xs, supports_membership_choices hxs, hxs.consecutive, hstart, hend⟩

end PlanarRecoloring
