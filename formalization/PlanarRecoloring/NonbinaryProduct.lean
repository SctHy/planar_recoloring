import PlanarRecoloring.BinaryEndpoints
import PlanarRecoloring.Complete

/-!
# Binary products with an arbitrary non-binary complete factor

The product lemma in the article uses the fact that a Boolean product becomes
Hamilton-connected as soon as one factor has at least three available values.
This file proves the finite factor statement needed for that step in the
normal form `Q_n □ K_r`, uniformly for every `r ≥ 3`.  The recursive proof is
the same cut-and-insert construction as the reflected Gray-code proof, but the
third colour is selected from an arbitrary `Fin r` rather than hard-coding
`Fin 3`.
-/

namespace PlanarRecoloring

def NonbinaryAdj (r : Nat) (x y : List Bool × Fin r) : Prop :=
  (ProductAdj x.1 y.1 ∧ x.2 = y.2) ∨
    (x.1 = y.1 ∧ x.2 ≠ y.2)

def nonbinaryStates (r n : Nat) : List (List Bool × Fin r) :=
  match n with
  | 0 => (List.finRange r).map (fun c => ([], c))
  | n + 1 =>
      (nonbinaryStates r n).map (fun p => (false :: p.1, p.2)) ++
        (nonbinaryStates r n).map (fun p => (true :: p.1, p.2))

@[simp] theorem nonbinaryStates_zero (r : Nat) :
    nonbinaryStates r 0 = (List.finRange r).map (fun c => ([], c)) := rfl

@[simp] theorem nonbinaryStates_succ (r n : Nat) :
    nonbinaryStates r (n + 1) =
      (nonbinaryStates r n).map (fun p => (false :: p.1, p.2)) ++
        (nonbinaryStates r n).map (fun p => (true :: p.1, p.2)) := rfl

private theorem nonbinary_cons_map {r : Nat} {b : Bool}
    {x y : List Bool × Fin r} (h : NonbinaryAdj r x y) :
    NonbinaryAdj r (b :: x.1, x.2) (b :: y.1, y.2) := by
  rcases h with h | h
  · exact Or.inl ⟨productAdj_cons_map_gray h.1, h.2⟩
  · exact Or.inr ⟨by simp [h.1], h.2⟩

private theorem nonbinary_layer_map {r n : Nat} {b : Bool}
    {x y : List Bool × Fin r}
    (h : HamiltonPathOn (nonbinaryStates r n) (NonbinaryAdj r) x y) :
    HamiltonPathOn ((nonbinaryStates r n).map (fun p => (b :: p.1, p.2)))
      (NonbinaryAdj r) (b :: x.1, x.2) (b :: y.1, y.2) := by
  exact h.map (fun p => (b :: p.1, p.2))
    (fun p q h => by
      apply Prod.ext
      · exact List.cons.inj (Prod.ext_iff.mp h).1 |>.2
      · exact (Prod.ext_iff.mp h).2)
    (fun {_ _} h => nonbinary_cons_map h)

private theorem nonbinary_consecutive_map {r : Nat} {b : Bool}
    {xs : List (List Bool × Fin r)}
    (hc : Consecutive (NonbinaryAdj r) xs) :
    Consecutive (NonbinaryAdj r)
      (xs.map (fun p => (b :: p.1, p.2))) := by
  induction xs with
  | nil => trivial
  | cons x xs ih =>
      cases xs with
      | nil => trivial
      | cons y ys =>
          rcases hc with ⟨hxy, htail⟩
          exact ⟨nonbinary_cons_map hxy, ih htail⟩

private theorem nonbinary_layer_disjoint (r n : Nat) (b : Bool) :
    DisjointLists ((nonbinaryStates r n).map
        (fun p => (b :: p.1, p.2)))
      ((nonbinaryStates r n).map
        (fun p => ((!b) :: p.1, p.2))) := by
  intro x hx hy
  rcases List.mem_map.mp hx with ⟨u, hu, rfl⟩
  rcases List.mem_map.mp hy with ⟨v, hv, h⟩
  have hb : b :: u.1 = (!b) :: v.1 := (Prod.ext_iff.mp h).1.symm
  cases b <;> simp at hb

private theorem nonbinary_layer_cover (r n : Nat) (b : Bool)
    (x : List Bool × Fin r) :
    x ∈ (nonbinaryStates r n).map (fun p => (b :: p.1, p.2)) ++
      (nonbinaryStates r n).map (fun p => ((!b) :: p.1, p.2)) ↔
      x ∈ nonbinaryStates r (n + 1) := by
  rw [nonbinaryStates_succ]
  cases b <;> simp [or_comm]

private theorem nodup_nonbinary_map (r : Nat) (b : Bool)
    {xs : List (List Bool × Fin r)} (h : xs.Nodup) :
    (xs.map (fun p => (b :: p.1, p.2))).Nodup := by
  induction xs with
  | nil => simp
  | cons p ps ih =>
      change ((b :: p.1, p.2) ::
        (ps.map (fun q => (b :: q.1, q.2)))).Nodup
      rw [List.nodup_cons] at h ⊢
      refine ⟨?_, ih h.2⟩
      intro hm
      rcases List.mem_map.mp hm with ⟨q, hq, heq⟩
      have hpq : p = q := by
        apply Prod.ext
        · exact (List.cons.inj (Prod.ext_iff.mp heq).1).2.symm
        · exact (Prod.ext_iff.mp heq).2.symm
      exact h.1 (hpq ▸ hq)

theorem nonbinaryStates_mem_iff (r : Nat) : ∀ n (x : List Bool × Fin r),
    x ∈ nonbinaryStates r n ↔ x.1.length = n := by
  intro n
  induction n with
  | zero =>
      intro x
      rcases x with ⟨word, c⟩
      constructor
      · intro hx
        simp [nonbinaryStates] at hx
        rcases hx with ⟨d, hd, rfl⟩
        rfl
      · intro hx
        cases word with
        | nil =>
            simp [nonbinaryStates]
        | cons b w => simp at hx
  | succ n ih =>
      intro x
      cases x with
      | mk word c =>
        cases word with
        | nil => simp [nonbinaryStates]
        | cons b w =>
          cases b <;> simpa [nonbinaryStates] using ih (w, c)

private theorem exists_fin_three_avoid {r : Nat} (hr : 3 ≤ r)
    (a b : Fin r) : ∃ c : Fin r, c ≠ a ∧ c ≠ b := by
  have hr0 : 0 < r := by omega
  have hr1 : 1 < r := by omega
  have hr2 : 2 < r := by omega
  let c0 : Fin r := ⟨0, hr0⟩
  let c1 : Fin r := ⟨1, by omega⟩
  let c2 : Fin r := ⟨2, by omega⟩
  have h01 : c0 ≠ c1 := by
    intro h
    have := congrArg Fin.val h
    simp [c0, c1] at this
  have h02 : c0 ≠ c2 := by
    intro h
    have := congrArg Fin.val h
    simp [c0, c2] at this
  have h12 : c1 ≠ c2 := by
    intro h
    have := congrArg Fin.val h
    simp [c1, c2] at this
  by_cases h0 : c0 ≠ a ∧ c0 ≠ b
  · exact ⟨c0, h0.1, h0.2⟩
  by_cases h1 : c1 ≠ a ∧ c1 ≠ b
  · exact ⟨c1, h1.1, h1.2⟩
  have h0' : c0 = a ∨ c0 = b := by
    by_cases hca : c0 = a
    · exact Or.inl hca
    by_cases hcb : c0 = b
    · exact Or.inr hcb
    exact False.elim (h0 ⟨hca, hcb⟩)
  have h1' : c1 = a ∨ c1 = b := by
    by_cases hca : c1 = a
    · exact Or.inl hca
    by_cases hcb : c1 = b
    · exact Or.inr hcb
    exact False.elim (h1 ⟨hca, hcb⟩)
  refine ⟨c2, ?_, ?_⟩
  · intro hca
    rcases h0' with h0a | h0b
    · rcases h1' with h1a | h1b
      · exact h02 (h0a.trans hca.symm)
      · exact h02 (h0a.trans hca.symm)
    · rcases h1' with h1a | h1b
      · exact h12 (h1a.trans hca.symm)
      · exact h01 (h0b.trans h1b.symm)
  · intro hcb
    rcases h0' with h0a | h0b
    · rcases h1' with h1a | h1b
      · exact h01 (h0a.trans h1a.symm)
      · exact h12 (h1b.trans hcb.symm)
    · exact h02 (h0b.trans hcb.symm)

private theorem nonbinary_ne_state {r : Nat} (hr : 3 ≤ r) (n : Nat)
    (x y : List Bool × Fin r) :
    ∃ z, z ∈ nonbinaryStates r n ∧ z ≠ x ∧ z ≠ y := by
  let w := List.replicate n false
  rcases exists_fin_three_avoid hr x.2 y.2 with ⟨c, hcx, hcy⟩
  refine ⟨(w, c), ?_, ?_, ?_⟩
  · rw [nonbinaryStates_mem_iff]
    simp [w]
  · intro h
    exact hcx (congrArg Prod.snd h)
  · intro h
    exact hcy (congrArg Prod.snd h)

private theorem nonbinary_head_bridge {r : Nat} {b : Bool}
    (z : List Bool × Fin r) :
    NonbinaryAdj r (b :: z.1, z.2) ((!b) :: z.1, z.2) :=
  Or.inl ⟨⟨[], z.1, b, rfl, rfl⟩, rfl⟩

private theorem nonbinary_head_bridge_symm {r : Nat} {b : Bool}
    (z : List Bool × Fin r) :
    NonbinaryAdj r ((!b) :: z.1, z.2) (b :: z.1, z.2) := by
  exact Or.inl ⟨productAdj_symm (⟨[], z.1, b, rfl, rfl⟩), rfl⟩

private theorem nonbinary_zero_hamiltonConnected {r : Nat} (hr : 3 ≤ r) :
    HamiltonConnectedOn (nonbinaryStates r 0) (NonbinaryAdj r) := by
  intro s t hs ht hst
  apply complete_hamiltonPathOn_of_mem (nonbinaryStates r 0)
    (by
      have hmap : ∀ {xs : List (Fin r)}, xs.Nodup →
          (xs.map (fun c => (([] : List Bool), c))).Nodup := by
        intro xs hxs
        induction xs with
        | nil => simp
        | cons c cs ih =>
            simp only [List.map]
            rw [List.nodup_cons] at hxs ⊢
            refine ⟨?_, ih hxs.2⟩
            intro hm
            rcases List.mem_map.mp hm with ⟨d, hd, heq⟩
            have hdc : d = c := by
              simpa using congrArg Prod.snd heq
            exact hxs.1 (hdc ▸ hd)
      simpa [nonbinaryStates] using hmap (List.nodup_finRange r))
  · intro x y hx hy hxy
    simp [nonbinaryStates] at hx hy
    rcases hx with ⟨cx, hcx, rfl⟩
    rcases hy with ⟨cy, hcy, rfl⟩
    have hxy' : cx ≠ cy := by
      intro heq
      apply hxy
      cases heq
      rfl
    exact Or.inr ⟨rfl, hxy'⟩
  · exact hs
  · exact ht
  · exact hst

theorem nonbinary_product_hamiltonConnected {r : Nat} (hr : 3 ≤ r) : ∀ n,
    HamiltonConnectedOn (nonbinaryStates r n) (NonbinaryAdj r) := by
  intro n
  induction n with
  | zero => exact nonbinary_zero_hamiltonConnected hr
  | succ n ih =>
      intro s t hs ht hst
      rcases s with ⟨sword, sc⟩
      rcases t with ⟨tword, tc⟩
      cases sword with
      | nil => simp [nonbinaryStates] at hs
      | cons sb ss =>
        cases tword with
        | nil => simp [nonbinaryStates] at ht
        | cons tb ts =>
          have hs' : (ss, sc) ∈ nonbinaryStates r n := by
            cases sb <;> simpa [nonbinaryStates] using hs
          have ht' : (ts, tc) ∈ nonbinaryStates r n := by
            cases tb <;> simpa [nonbinaryStates] using ht
          by_cases hab : sb = tb
          · subst tb
            have htailne : (ss, sc) ≠ (ts, tc) := by
              intro hEq
              apply hst
              cases hEq
              rfl
            rcases ih (ss, sc) (ts, tc) hs' ht' htailne with
              ⟨p, hp, hq, pn, pc, pw⟩
            cases p with
            | nil => simp at hp
            | cons z p =>
              have hz : z = (ss, sc) := by simpa using hp
              subst z
              cases p with
              | nil =>
                have hEq : (ts, tc) = (ss, sc) := by simpa using hq.symm
                exact False.elim (htailne hEq.symm)
              | cons z tail =>
                have hzmem : z ∈ nonbinaryStates r n :=
                  (pc z).mpr (by simp)
                have hz_ne : (ss, sc) ≠ z := by
                  intro hEq
                  subst z
                  exact (List.nodup_cons.mp pn).1 (by simp)
                have hother := ih (ss, sc) z hs' hzmem hz_ne
                have hmappedN := nodup_nonbinary_map r sb pn
                have hmappedCover : CoversList
                    ((nonbinaryStates r n).map
                      (fun p => (sb :: p.1, p.2)))
                    (((ss, sc) :: z :: tail).map
                      (fun p => (sb :: p.1, p.2))) := by
                  intro u
                  simp only [List.mem_map]
                  constructor
                  · rintro ⟨v, hv, rfl⟩
                    exact ⟨v, (pc v).mp hv, rfl⟩
                  · rintro ⟨v, hv, rfl⟩
                    exact ⟨v, (pc v).mpr hv, rfl⟩
                have hmappedLast :
                    (((ss, sc) :: z :: tail).map
                      (fun p => (sb :: p.1, p.2))).getLast? =
                      some (sb :: ts, tc) := by
                  rw [List.getLast?_map, hq]
                  rfl
                have hmappedWalk :=
                  nonbinary_consecutive_map (b := sb) pw
                have hinsert := HamiltonPathOn.insertAtFirstEdge
                  hmappedN hmappedCover hmappedLast hmappedWalk
                  (nonbinary_layer_map (b := !sb) hother)
                  (nonbinary_layer_disjoint r n sb)
                  (nonbinary_head_bridge (z := (ss, sc)))
                  (nonbinary_head_bridge_symm (z := z))
                exact hinsert.congr_vertices
                  (nonbinary_layer_cover r n sb)
          · rcases nonbinary_ne_state hr n (ss, sc) (ts, tc) with
              ⟨z, hzmem, hzs, hzt⟩
            have hleft := nonbinary_layer_map (b := sb)
              (ih (ss, sc) z hs' hzmem hzs.symm)
            have hright := nonbinary_layer_map (b := tb)
              (ih z (ts, tc) hzmem ht' hzt)
            have htb : tb = !sb := by cases sb <;> cases tb <;> simp_all
            have hbridge : NonbinaryAdj r (sb :: z.1, z.2)
                (tb :: z.1, z.2) := by
              apply Or.inl
              refine ⟨?_, rfl⟩
              subst tb
              exact ⟨[], z.1, sb, rfl, rfl⟩
            exact (hleft.appendOn hright (by
              simpa [htb] using nonbinary_layer_disjoint r n sb)
              hbridge).congr_vertices (by
                simpa [htb] using nonbinary_layer_cover r n sb)

end PlanarRecoloring
