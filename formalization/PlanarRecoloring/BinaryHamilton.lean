import PlanarRecoloring.ProductParity
import PlanarRecoloring.Fibre

namespace PlanarRecoloring

def grayWords : Nat → List (List Bool)
  | 0 => [[]]
  | n + 1 =>
      (grayWords n).map (fun w => false :: w) ++
        (grayWords n).reverse.map (fun w => true :: w)

@[simp] theorem grayWords_zero : grayWords 0 = [[]] := rfl
@[simp] theorem grayWords_succ (n : Nat) :
    grayWords (n + 1) =
      (grayWords n).map (fun w => false :: w) ++
        (grayWords n).reverse.map (fun w => true :: w) := rfl

theorem nodup_map_cons_bool (b : Bool) :
    ∀ {xs : List (List Bool)}, xs.Nodup →
      (xs.map (fun w => b :: w)).Nodup := by
  intro xs h
  induction xs with
  | nil => simp
  | cons x xs ih =>
      simp only [List.map]
      rw [List.nodup_cons] at h ⊢
      refine ⟨?_, ih h.2⟩
      intro hz
      rcases List.mem_map.mp hz with ⟨y, hy, hyeq⟩
      have hxy : x = y := by
        exact (List.cons.inj hyeq.symm).2
      exact h.1 (hxy ▸ hy)

theorem grayWords_nodup : ∀ n, (grayWords n).Nodup := by
  intro n
  induction n with
  | zero => simp [grayWords]
  | succ n ih =>
      apply List.nodup_append.mpr
      refine ⟨?_, ?_, ?_⟩
      · exact nodup_map_cons_bool false ih
      · exact nodup_map_cons_bool true ((List.reverse_perm (grayWords n)).symm.nodup ih)
      · intro a ha b hb hab
        rcases List.mem_map.mp ha with ⟨x, hx, rfl⟩
        rcases List.mem_map.mp hb with ⟨y, hy, rfl⟩
        simp at hab

theorem grayWords_mem_iff {n : Nat} {x : List Bool} :
    x ∈ grayWords n ↔ x.length = n := by
  induction n generalizing x with
  | zero => simp [grayWords]
  | succ n ih =>
      simp only [grayWords, List.mem_append, List.mem_map, List.mem_reverse]
      constructor
      · rintro (⟨w, hw, rfl⟩ | ⟨w, hw, rfl⟩) <;> simp [ih.mp hw]
      · intro hx
        cases x with
        | nil => simp at hx
        | cons h xs =>
            have hxs : xs.length = n := by simpa using hx
            cases h <;> simp [ih.mpr hxs]

theorem grayWords_nonempty (n : Nat) : grayWords n ≠ [] := by
  induction n with
  | zero => simp [grayWords]
  | succ n ih => simp [grayWords, ih]

theorem grayWords_head : ∀ n, (grayWords n).head? = some (List.replicate n false) := by
  intro n
  induction n with
  | zero => simp [grayWords]
  | succ n ih => simpa [grayWords, List.replicate_succ] using ih

theorem grayWords_last_succ (n : Nat) :
    (grayWords (n + 1)).getLast (grayWords_nonempty (n + 1)) =
      true :: List.replicate n false := by
  apply Option.some.inj
  rw [← List.getLast?_eq_some_getLast (grayWords_nonempty (n + 1))]
  rw [grayWords_succ, List.getLast?_append]
  simp [grayWords_head n]

theorem cubeParity_replicate_false : ∀ n, cubeParity (List.replicate n false) = false := by
  intro n
  induction n with
  | zero => rfl
  | succ n ih => simpa [List.replicate_succ, cubeParity] using ih

theorem grayWords_last_succ_parity (n : Nat) :
    cubeParity ((grayWords (n + 1)).getLast (grayWords_nonempty (n + 1))) = true := by
  rw [grayWords_last_succ]
  simp [cubeParity, cubeParity_replicate_false]

theorem productAdj_cons_map_gray {h : Bool} {x y : List Bool}
    (ha : ProductAdj x y) : ProductAdj (h :: x) (h :: y) := by
  rcases ha with ⟨pre, suff, b, rfl, rfl⟩
  exact ⟨h :: pre, suff, b, by simp [List.cons_append], by simp [List.cons_append]⟩

theorem productAdj_gray_bridge (x : List Bool) :
    ProductAdj (false :: x) (true :: x) := by
  exact ⟨[], x, false, by simp, by simp⟩

theorem consecutive_map_gray {h : Bool} {xs : List (List Bool)}
    (hc : Consecutive ProductAdj xs) :
    Consecutive ProductAdj (xs.map (fun x => h :: x)) := by
  induction xs with
  | nil => trivial
  | cons x xs ih =>
      cases xs with
      | nil => trivial
      | cons y ys =>
          rcases hc with ⟨hxy, htail⟩
          exact ⟨productAdj_cons_map_gray hxy, ih htail⟩

theorem grayWords_consecutive : ∀ n, Consecutive ProductAdj (grayWords n) := by
  intro n
  induction n with
  | zero => trivial
  | succ n ih =>
      have hleft := consecutive_map_gray (h := false) ih
      have hright := consecutive_map_gray (h := true)
        (consecutive_reverse_of_symmetric
          (fun a b hab => productAdj_symm hab) ih)
      have hleftlast :
          ((grayWords n).map (fun w => false :: w)).getLast? =
            some (false :: (grayWords n).getLast (grayWords_nonempty n)) := by
        rw [List.getLast?_map,
          List.getLast?_eq_some_getLast (grayWords_nonempty n)]
        rfl
      have hrighthead :
          ((grayWords n).reverse.map (fun w => true :: w)).head? =
            some (true :: (grayWords n).getLast (grayWords_nonempty n)) := by
        rw [List.head?_map, List.head?_reverse,
          List.getLast?_eq_some_getLast (grayWords_nonempty n)]
        rfl
      rw [grayWords_succ]
      apply consecutive_append hleft hright
        (by simp [grayWords_nonempty n]) (by simp [grayWords_nonempty n])
        hleftlast hrighthead
      exact productAdj_gray_bridge
        ((grayWords n).getLast (grayWords_nonempty n))

theorem gray_hamiltonPathOn (n : Nat) :
    HamiltonPathOn (grayWords n) ProductAdj
      (List.replicate n false) ((grayWords n).getLast (grayWords_nonempty n)) := by
  refine ⟨grayWords n, grayWords_head n, ?_,
    grayWords_nodup n, ?_, grayWords_consecutive n⟩
  · exact List.getLast?_eq_some_getLast (grayWords_nonempty n)
  intro x
  rfl

end PlanarRecoloring
