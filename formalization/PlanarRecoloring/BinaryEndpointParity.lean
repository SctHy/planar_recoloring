import PlanarRecoloring.BinaryEndpoints

namespace PlanarRecoloring

/-- The reflected binary enumeration has exactly `2^n` words. -/
theorem grayWords_length : ∀ n, (grayWords n).length = 2 ^ n := by
  intro n
  induction n with
  | zero => simp [grayWords]
  | succ n ih =>
      simp [grayWords, ih, Nat.pow_succ, Nat.mul_comm]
      omega

/-- A consecutive nonempty list gives an indexed product path whose index is
exactly its number of edges. -/
theorem productPath_of_consecutive_length
    {xs : List (List Bool)} (hne : xs ≠ [])
    (hcon : Consecutive ProductAdj xs) :
    ∃ n x y, xs.head? = some x ∧ xs.getLast? = some y ∧
      xs.length = n + 1 ∧ ProductPath n x y := by
  induction xs with
  | nil => exact False.elim (hne rfl)
  | cons x xs ih =>
      cases xs with
      | nil =>
          exact ⟨0, x, x, rfl, by simp, by simp, ProductPath.refl x⟩
      | cons y ys =>
          have htail : Consecutive ProductAdj (y :: ys) := hcon.2
          obtain ⟨n, y', z, hhead, hlast, hlen, hpath⟩ :=
            ih (by simp) htail
          have hy' : y' = y := by simpa using hhead.symm
          subst y'
          refine ⟨n + 1, x, z, rfl, ?_, ?_, ProductPath.step hcon.1 hpath⟩
          · simpa using hlast
          · simpa [Nat.add_assoc] using congrArg Nat.succ hlen

private theorem grayWords_hamilton_path_parity
    {n : Nat} (hn : 0 < n) {x y : List Bool}
    (hx : x.length = n) (hy : y.length = n)
    (h : HamiltonPathOn (grayWords n) ProductAdj x y) :
    cubeParity x = !cubeParity y := by
  rcases h with ⟨path, hhead, hlast, hnodup, hcover, hcon⟩
  have hne : path ≠ [] := by
    intro hnil
    subst path
    simp at hhead
  obtain ⟨m, a, b, ha, hb, hlen, hpath⟩ :=
    productPath_of_consecutive_length hne hcon
  have hxa : a = x := by simpa using ha.symm.trans hhead
  have hby : b = y := by simpa using hb.symm.trans hlast
  subst a
  subst b
  have hgraynodup := grayWords_nodup n
  have hperm : path.Perm (grayWords n) :=
    (List.perm_ext_iff_of_nodup hnodup hgraynodup).2 (fun z => (hcover z).symm)
  have hlenall : path.length = (grayWords n).length := hperm.length_eq
  have hpow : path.length = 2 ^ n := hlenall.trans (grayWords_length n)
  cases n with
  | zero => omega
  | succ q =>
      have hpow' : path.length = 2 ^ q * 2 := by
        simpa [Nat.pow_succ, Nat.mul_comm] using hpow
      have hmn : m + 1 = 2 ^ q * 2 := hlen.symm.trans hpow'
      have hpos : 0 < 2 ^ q := Nat.pow_pos (by omega)
      obtain ⟨k, hk⟩ := Nat.exists_eq_succ_of_ne_zero (Nat.ne_of_gt hpos)
      have hodd : OddLength m := by
        refine ⟨k, ?_⟩
        omega
      exact odd_productPath_opposite hodd hpath

/-- For a binary product with at least one coordinate, prescribed endpoints
admit a Hamilton path exactly when their xor parities are opposite. -/
theorem binary_hamiltonPathOn_iff {n : Nat} (hn : 0 < n)
    {x y : List Bool} (hx : x.length = n) (hy : y.length = n) :
    HamiltonPathOn (grayWords n) ProductAdj x y ↔
      cubeParity x = !cubeParity y := by
  constructor
  · exact grayWords_hamilton_path_parity hn hx hy
  · exact binary_hamiltonPathOn hn hx hy

end PlanarRecoloring
