import PlanarRecoloring.BinaryEndpoints
import PlanarRecoloring.Complete

namespace PlanarRecoloring

/-- The Cartesian product of the binary word graph with a three-vertex
complete graph. -/
def TernaryAdj (x y : List Bool × Fin 3) : Prop :=
  (ProductAdj x.1 y.1 ∧ x.2 = y.2) ∨
    (x.1 = y.1 ∧ x.2 ≠ y.2)

def ternaryStates : Nat → List (List Bool × Fin 3)
  | 0 => [([], 0), ([], 1), ([], 2)]
  | n + 1 =>
      (ternaryStates n).map (fun p => (false :: p.1, p.2)) ++
        (ternaryStates n).map (fun p => (true :: p.1, p.2))

@[simp] theorem ternaryStates_zero : ternaryStates 0 =
    [([], 0), ([], 1), ([], 2)] := rfl

@[simp] theorem ternaryStates_succ (n : Nat) :
    ternaryStates (n + 1) =
      (ternaryStates n).map (fun p => (false :: p.1, p.2)) ++
        (ternaryStates n).map (fun p => (true :: p.1, p.2)) := rfl

private theorem ternary_cons_map {b : Bool}
    {x y : List Bool × Fin 3} (h : TernaryAdj x y) :
    TernaryAdj (b :: x.1, x.2) (b :: y.1, y.2) := by
  rcases h with h | h
  · exact Or.inl ⟨productAdj_cons_map_gray h.1, h.2⟩
  · exact Or.inr ⟨by simp [h.1], h.2⟩

private theorem ternary_layer_map {b : Bool} {n : Nat}
    {x y : List Bool × Fin 3}
    (h : HamiltonPathOn (ternaryStates n) TernaryAdj x y) :
    HamiltonPathOn ((ternaryStates n).map (fun p => (b :: p.1, p.2)))
      TernaryAdj (b :: x.1, x.2) (b :: y.1, y.2) := by
  exact h.map (fun p => (b :: p.1, p.2))
    (fun p q h => by
      apply Prod.ext
      · exact List.cons.inj (Prod.ext_iff.mp h).1 |>.2
      · exact (Prod.ext_iff.mp h).2)
    (fun {_ _} h => ternary_cons_map h)

private theorem ternary_consecutive_map {b : Bool} {xs : List (List Bool × Fin 3)}
    (hc : Consecutive TernaryAdj xs) :
    Consecutive TernaryAdj (xs.map (fun p => (b :: p.1, p.2))) := by
  induction xs with
  | nil => trivial
  | cons x xs ih =>
      cases xs with
      | nil => trivial
      | cons y ys =>
          rcases hc with ⟨hxy, htail⟩
          exact ⟨ternary_cons_map hxy, ih htail⟩

private theorem ternary_layer_disjoint (b : Bool) (n : Nat) :
    DisjointLists ((ternaryStates n).map (fun p => (b :: p.1, p.2)))
      ((ternaryStates n).map (fun p => ((!b) :: p.1, p.2))) := by
  intro x hx hy
  rcases List.mem_map.mp hx with ⟨u, hu, rfl⟩
  rcases List.mem_map.mp hy with ⟨v, hv, h⟩
  have hb : b :: u.1 = (!b) :: v.1 := (Prod.ext_iff.mp h).1.symm
  cases b <;> simp at hb

private theorem ternary_layer_cover (b : Bool) (n : Nat)
    (x : List Bool × Fin 3) :
    x ∈ (ternaryStates n).map (fun p => (b :: p.1, p.2)) ++
      (ternaryStates n).map (fun p => ((!b) :: p.1, p.2)) ↔
      x ∈ ternaryStates (n + 1) := by
  rw [ternaryStates_succ]
  cases b <;> simp [or_comm]

private theorem nodup_ternary_map (b : Bool) {xs : List (List Bool × Fin 3)}
    (h : xs.Nodup) :
    (xs.map (fun p => (b :: p.1, p.2))).Nodup := by
  induction xs with
  | nil => simp
  | cons p ps ih =>
      change ((b :: p.1, p.2) :: (ps.map (fun q => (b :: q.1, q.2)))).Nodup
      rw [List.nodup_cons] at h ⊢
      refine ⟨?_, ih h.2⟩
      intro hm
      rcases List.mem_map.mp hm with ⟨q, hq, heq⟩
      have hpq : p = q := by
        apply Prod.ext
        · exact (List.cons.inj (Prod.ext_iff.mp heq).1).2.symm
        · exact (Prod.ext_iff.mp heq).2.symm
      apply h.1 (hpq ▸ hq)

private theorem ternary_states_mem_word : ∀ n {w : List Bool} {c : Fin 3},
    w ∈ grayWords n → (w, c) ∈ ternaryStates n := by
  intro n
  induction n with
  | zero =>
      intro w c hw
      simp at hw
      subst w
      have hc := c.isLt
      have hv : c.val = 0 ∨ c.val = 1 ∨ c.val = 2 := by omega
      have hv' : c = 0 ∨ c = 1 ∨ c = 2 := by
        rcases hv with h | h | h
        · left; apply Fin.ext; exact h
        · right; left; apply Fin.ext; exact h
        · right; right; apply Fin.ext; exact h
      rcases hv' with rfl | rfl | rfl <;> simp [ternaryStates]
  | succ n ih =>
      intro w c hw
      rw [grayWords_succ] at hw
      simp only [List.mem_append, List.mem_map] at hw
      rcases hw with ⟨u, hu, rfl⟩ | ⟨u, hu, rfl⟩
      · simp [ternaryStates, ih hu]
      · simp [ternaryStates, ih (List.mem_reverse.mp hu)]


/-- The enumeration contains every ternary-product vertex, and no words of
the wrong dimension. -/
theorem ternaryStates_mem_iff : ∀ n (x : List Bool × Fin 3),
    x ∈ ternaryStates n ↔ x.1.length = n := by
  intro n
  induction n with
  | zero =>
      intro x
      constructor
      · intro hx
        simp [ternaryStates] at hx
        rcases hx with rfl | rfl | rfl <;> rfl
      · intro hx
        have hw : x.1 ∈ grayWords 0 := grayWords_mem_iff.mpr hx
        exact ternary_states_mem_word 0 hw
  | succ n ih =>
      intro x
      cases x with
      | mk word c =>
        cases word with
        | nil => simp [ternaryStates]
        | cons b w =>
          cases b <;> simpa [ternaryStates] using ih (w, c)

private theorem ternary_ne_state {n : Nat} (x y : List Bool × Fin 3) :
    ∃ z, z ∈ ternaryStates n ∧ z ≠ x ∧ z ≠ y := by
  let w := List.replicate n false
  have hw : w ∈ grayWords n := by
    rw [grayWords_mem_iff]
    simp [w]
  have hmem (c : Fin 3) : (w, c) ∈ ternaryStates n :=
    ternary_states_mem_word n hw
  have hne (c : Fin 3) (hc : c ≠ x.2) : (w, c) ≠ x := by
    intro h
    apply hc
    exact congrArg Prod.snd h
  have hne' (c : Fin 3) (hc : c ≠ y.2) : (w, c) ≠ y := by
    intro h
    apply hc
    exact congrArg Prod.snd h
  by_cases h0 : x.2 = 0
  · by_cases h1 : y.2 = 0
    · exact ⟨(w, 1), hmem 1, hne 1 (by simp [h0]), hne' 1 (by simp [h1])⟩
    · by_cases h2 : y.2 = 1
      · exact ⟨(w, 2), hmem 2, hne 2 (by simp [h0]), hne' 2 (by simp [h2])⟩
      · exact ⟨(w, 1), hmem 1, hne 1 (by simp [h0]),
          hne' 1 (fun h => h2 h.symm)⟩
  · by_cases h1 : x.2 = 1
    · by_cases h2 : y.2 = 1
      · exact ⟨(w, 0), hmem 0, hne 0 (by simp [h1]),
          hne' 0 (by simp [h2])⟩
      · by_cases h2zero : y.2 = 0
        · exact ⟨(w, 2), hmem 2, hne 2 (by simp [h1]),
            hne' 2 (by simp [h2zero])⟩
        · exact ⟨(w, 0), hmem 0, hne 0 (by simp [h1]),
            hne' 0 (fun h => h2zero h.symm)⟩
    · by_cases h2 : y.2 = 0
      · exact ⟨(w, 1), hmem 1, hne 1 (fun h => h1 h.symm),
          hne' 1 (by simp [h2])⟩
      · by_cases h2one : y.2 = 1
        · exact ⟨(w, 0), hmem 0, hne 0 (fun h => h0 h.symm),
            hne' 0 (by simp [h2one])⟩
        · exact ⟨(w, 0), hmem 0, hne 0 (fun h => h0 h.symm),
            hne' 0 (fun h => h2 h.symm)⟩

private theorem ternary_head_bridge {b : Bool} (z : List Bool × Fin 3) :
    TernaryAdj (b :: z.1, z.2) ((!b) :: z.1, z.2) :=
  Or.inl ⟨⟨[], z.1, b, rfl, rfl⟩, rfl⟩

private theorem ternary_head_bridge_symm {b : Bool} (z : List Bool × Fin 3) :
    TernaryAdj ((!b) :: z.1, z.2) (b :: z.1, z.2) := by
  exact Or.inl ⟨productAdj_symm (⟨[], z.1, b, rfl, rfl⟩), rfl⟩

private theorem ternary_zero_hamiltonConnected :
    HamiltonConnectedOn (ternaryStates 0) TernaryAdj := by
  intro s t hs ht hst
  apply complete_hamiltonPathOn_of_mem (ternaryStates 0)
    (by decide)
  · intro x y hx hy hxy
    simp [ternaryStates] at hx hy
    rcases hx with rfl | rfl | rfl <;>
      rcases hy with rfl | rfl | rfl <;>
        simp_all [TernaryAdj]
  · simpa using hs
  · simpa using ht
  · exact hst

/-- The binary product with a ternary factor is Hamilton-connected.  This is
the non-binary-factor product fragment of the product lemma. -/
theorem ternary_product_hamiltonConnected : ∀ n,
    HamiltonConnectedOn (ternaryStates n) TernaryAdj := by
  intro n
  induction n with
  | zero => exact ternary_zero_hamiltonConnected
  | succ n ih =>
      intro s t hs ht hst
      rcases s with ⟨sword, sc⟩
      rcases t with ⟨tword, tc⟩
      cases sword with
      | nil => simp [ternaryStates] at hs
      | cons sb ss =>
        cases tword with
        | nil => simp [ternaryStates] at ht
        | cons tb ts =>
          have hs' : (ss, sc) ∈ ternaryStates n := by
            cases sb <;> simpa [ternaryStates] using hs
          have ht' : (ts, tc) ∈ ternaryStates n := by
            cases tb <;> simpa [ternaryStates] using ht
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
                have hzmem : z ∈ ternaryStates n := (pc z).mpr (by simp)
                have hz_ne : (ss, sc) ≠ z := by
                  intro hEq
                  subst z
                  exact (List.nodup_cons.mp pn).1 (by simp)
                have hother := ih (ss, sc) z hs' hzmem hz_ne
                have hmappedN := nodup_ternary_map sb pn
                have hmappedCover : CoversList
                    ((ternaryStates n).map (fun p => (sb :: p.1, p.2)))
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
                have hmappedWalk := ternary_consecutive_map (b := sb) pw
                have hinsert := HamiltonPathOn.insertAtFirstEdge
                  hmappedN hmappedCover hmappedLast hmappedWalk
                  (ternary_layer_map (b := !sb) hother)
                  (ternary_layer_disjoint sb n)
                  (ternary_head_bridge (z := (ss, sc)))
                  (ternary_head_bridge_symm (z := z))
                exact hinsert.congr_vertices (ternary_layer_cover sb n)
          · have hne : sb ≠ tb := hab
            rcases ternary_ne_state (n := n) (ss, sc) (ts, tc) with
              ⟨z, hzmem, hzs, hzt⟩
            have hleft := ternary_layer_map (b := sb)
              (ih (ss, sc) z hs' hzmem hzs.symm)
            have hright := ternary_layer_map (b := tb)
              (ih z (ts, tc) hzmem ht' hzt)
            have htb : tb = !sb := by cases sb <;> cases tb <;> simp_all
            have hbridge : TernaryAdj (sb :: z.1, z.2) (tb :: z.1, z.2) := by
              apply Or.inl
              refine ⟨?_, rfl⟩
              subst tb
              exact ⟨[], z.1, sb, rfl, rfl⟩
            exact (hleft.appendOn hright (by
              simpa [htb] using ternary_layer_disjoint sb n)
              hbridge).congr_vertices (by
                simpa [htb] using ternary_layer_cover sb n)

end PlanarRecoloring
