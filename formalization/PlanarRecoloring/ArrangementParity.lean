import PlanarRecoloring.General
import PlanarRecoloring.ProductParity

namespace PlanarRecoloring

/-! Inversion parity is the natural candidate labelling for completed ordered
colourings.  The append lemma is exposed here for the later exchange proof. -/
def inversionRow (a : Nat) : List Nat → Bool
  | [] => false
  | b :: bs => Bool.xor (decide (b < a)) (inversionRow a bs)

def inversionParity : List Nat → Bool
  | [] => false
  | a :: as => Bool.xor (inversionRow a as) (inversionParity as)

theorem inversionRow_append (a : Nat) (xs ys : List Nat) :
    inversionRow a (xs ++ ys) =
      Bool.xor (inversionRow a xs) (inversionRow a ys) := by
  induction xs with
  | nil => simp [inversionRow]
  | cons x xs ih => simp [inversionRow, ih]


private theorem comparison_complement (a b : Nat) (hab : a ≠ b) :
    decide (b < a) = !decide (a < b) := by
  by_cases hba : b < a
  · have hab' : ¬ a < b := by omega
    simp [hba, hab']
  · have hab' : a < b := by omega
    simp [hba, hab']

private theorem exchange_step (a b x : Nat) (tail : List Nat)
    (hab : a ≠ b) (hax : a ≠ x) (hbx : b ≠ x)
    (hi : inversionParity (a :: (tail ++ [b])) =
      !inversionParity (b :: (tail ++ [a]))) :
    inversionParity (a :: (x :: (tail ++ [b]))) =
      !inversionParity (b :: (x :: (tail ++ [a]))) := by
  have hi' := hi
  simp only [inversionParity] at hi'
  rw [inversionRow_append a tail [b], inversionRow_append b tail [a]] at hi'
  change ((decide (x < a) ^^ inversionRow a (tail ++ [b])) ^^
      (inversionRow x (tail ++ [b]) ^^ inversionParity (tail ++ [b]))) =
    !((decide (x < b) ^^ inversionRow b (tail ++ [a])) ^^
      (inversionRow x (tail ++ [a]) ^^ inversionParity (tail ++ [a])))
  rw [inversionRow_append a tail [b], inversionRow_append b tail [a],
      inversionRow_append x tail [b], inversionRow_append x tail [a]]
  by_cases hba : b < a
  · have hab' : ¬ a < b := by omega
    by_cases hxa : x < a <;> by_cases hxb : x < b
    all_goals
      have hax' : a < x ↔ ¬ x < a := by omega
      have hbx' : b < x ↔ ¬ x < b := by omega
      cases hRA : inversionRow a tail <;> cases hRB : inversionRow b tail <;>
        cases inversionRow x tail <;>
        cases hPb : inversionParity (tail ++ [b]) <;>
        cases hPa : inversionParity (tail ++ [a]) <;>
        simp [inversionRow, hRA, hRB, hPb, hPa,
          hba, hab', hxa, hxb, hax', hbx'] at hi' ⊢
  · have hab' : a < b := by omega
    by_cases hxa : x < a <;> by_cases hxb : x < b
    all_goals
      have hax' : a < x ↔ ¬ x < a := by omega
      have hbx' : b < x ↔ ¬ x < b := by omega
      cases hRA : inversionRow a tail <;> cases hRB : inversionRow b tail <;>
        cases inversionRow x tail <;>
        cases hPb : inversionParity (tail ++ [b]) <;>
        cases hPa : inversionParity (tail ++ [a]) <;>
        simp [inversionRow, hRA, hRB, hPb, hPa,
          hba, hab', hxa, hxb, hax', hbx'] at hi' ⊢

/-- Swapping two distinct endpoints of a duplicate-free middle block reverses
inversion parity. -/
theorem inversionParity_exchange_ends (a b : Nat) (middle : List Nat)
    (hab : a ≠ b)
    (hm : ∀ x, x ∈ middle → a ≠ x ∧ b ≠ x) :
    inversionParity (a :: (middle ++ [b])) =
      !inversionParity (b :: (middle ++ [a])) := by
  induction middle with
  | nil =>
      simp [inversionParity, inversionRow, comparison_complement a b hab]
  | cons x xs ih =>
      have hx := hm x (by simp)
      have hxs : ∀ y, y ∈ xs → a ≠ y ∧ b ≠ y := by
        intro y hy
        exact hm y (by simp [hy])
      exact exchange_step a b x xs hab hx.1 hx.2 (ih hxs)

/-- A common prefix does not affect the parity reversal of an endpoint swap. -/
theorem inversionParity_exchange_last (pre middle : List Nat) (a b : Nat)
    (hab : a ≠ b)
    (hm : ∀ x, x ∈ middle → a ≠ x ∧ b ≠ x) :
    inversionParity (pre ++ (a :: middle ++ [b])) =
      !inversionParity (pre ++ (b :: middle ++ [a])) := by
  induction pre with
  | nil => exact inversionParity_exchange_ends a b middle hab hm
  | cons x xs ih =>
      have hrow : inversionRow x (xs ++ (a :: middle ++ [b])) =
          inversionRow x (xs ++ (b :: middle ++ [a])) := by
        rw [inversionRow_append x xs (a :: middle ++ [b]),
            inversionRow_append x xs (b :: middle ++ [a])]
        have hm' : inversionRow x (a :: middle ++ [b]) =
            inversionRow x (b :: middle ++ [a]) := by
          simp [inversionRow, inversionRow_append,
            Bool.xor_comm, Bool.xor_left_comm]
        rw [hm']
      change (inversionRow x (xs ++ (a :: middle ++ [b])) ^^
          inversionParity (xs ++ (a :: middle ++ [b]))) =
        !(inversionRow x (xs ++ (b :: middle ++ [a])) ^^
          inversionParity (xs ++ (b :: middle ++ [a])))
      rw [hrow, ih]
      cases inversionRow x (xs ++ (b :: middle ++ [a])) <;>
        cases inversionParity (xs ++ (b :: middle ++ [a])) <;> rfl

/-- A completed arrangement is a permutation of the `n+1` labels.  The
last entry is the omitted colour; the first `n` entries are the ordered
colouring of `K_n`. -/
structure CompletedArrangement (n : Nat) where
  word : List Nat
  nodup : word.Nodup
  length : word.length = n + 1
  bounded : ∀ x, x ∈ word → x < n + 1

/-- A move exchanges a used coordinate with the final, unused colour. -/
def ArrangementAdjacent {n : Nat} (s t : CompletedArrangement n) : Prop :=
  ∃ pre middle : List Nat, ∃ a b : Nat,
    s.word = pre ++ (a :: middle ++ [b]) ∧
      t.word = pre ++ (b :: middle ++ [a])

def arrangementParity {n : Nat} (s : CompletedArrangement n) : Bool :=
  inversionParity s.word

theorem arrangement_adjacent_parity {n : Nat} {s t : CompletedArrangement n}
    (h : ArrangementAdjacent s t) :
    arrangementParity s = !arrangementParity t := by
  rcases h with ⟨pre, middle, a, b, hs, ht⟩
  have hfull : (pre ++ (a :: middle ++ [b])).Nodup := by
    rw [← hs]
    exact s.nodup
  have hrest : (a :: middle ++ [b]).Nodup :=
    (List.nodup_append.mp hfull).2.1
  have hna : a ∉ middle ++ [b] := (List.nodup_cons.mp hrest).1
  have hab : a ≠ b := by
    intro h
    exact hna (by simp [h])
  have hdis : ∀ x, x ∈ middle → x ≠ b := by
    intro x hx
    exact (List.nodup_append.mp (List.nodup_cons.mp hrest).2).2.2
      x hx b (by simp)
  have hm : ∀ x, x ∈ middle → a ≠ x ∧ b ≠ x := by
    intro x hx
    constructor
    · intro hax
      exact hna (by simp [hax, hx])
    · intro hbx
      exact hdis x hx hbx.symm
  change inversionParity s.word = !inversionParity t.word
  rw [hs, ht]
  exact inversionParity_exchange_last pre middle a b hab hm

theorem arrangement_adjacent_symm {n : Nat} {s t : CompletedArrangement n}
    (h : ArrangementAdjacent s t) : ArrangementAdjacent t s := by
  rcases h with ⟨pre, middle, a, b, hs, ht⟩
  exact ⟨pre, middle, b, a, ht, hs⟩

/-- Generic parity obstruction for an arrangement-like relation. -/
theorem no_triangle_of_edge_flip
    {α : Type} (r : α → α → Prop) (p : α → Bool)
    (hflip : ∀ ⦃x y⦄, r x y → p x != p y) :
    ¬ ∃ a b c : α, r a b ∧ r b c ∧ r c a := by
  rintro ⟨a, b, c, hab, hbc, hca⟩
  have h₁ := hflip hab
  have h₂ := hflip hbc
  have h₃ := hflip hca
  cases hpa : p a <;> cases hpb : p b <;> cases hpc : p c <;>
    simp [hpa, hpb, hpc] at h₁ h₂ h₃

/-- The same obstruction phrased for `CompletedArrangement`. -/
theorem arrangement_no_triangle_of_parity
    {n : Nat} (p : CompletedArrangement n → Bool)
    (hflip : ∀ ⦃x y⦄, ArrangementAdjacent x y → p x != p y) :
    ¬ ∃ a b c : CompletedArrangement n,
      ArrangementAdjacent a b ∧ ArrangementAdjacent b c ∧
        ArrangementAdjacent c a :=
  no_triangle_of_edge_flip ArrangementAdjacent p hflip

/-- No triangle exists in any completed arrangement graph. This statement
now uses the proved inversion-parity labelling rather than a parity input. -/
theorem arrangement_no_triangle {n : Nat} :
    ¬ ∃ a b c : CompletedArrangement n,
      ArrangementAdjacent a b ∧ ArrangementAdjacent b c ∧
        ArrangementAdjacent c a := by
  apply arrangement_no_triangle_of_parity arrangementParity
  intro x y h
  have hf := arrangement_adjacent_parity h
  cases hx : arrangementParity x <;> cases hy : arrangementParity y <;>
    simp [hx, hy] at hf ⊢

private theorem flipN_injective (n : Nat) :
    Function.Injective (flipN n) := by
  intro a b hab
  induction n with
  | zero => exact hab
  | succ n ih =>
      apply ih
      simpa [flipN] using hab

private theorem consecutive_endpoint_parity
    {α : Type} {r : α → α → Prop} (p : α → Bool)
    (hf : ∀ ⦃x y⦄, r x y → p x = !p y) :
    ∀ {xs : List α} {s t : α}, xs.head? = some s →
      xs.getLast? = some t → Consecutive r xs →
      p s = flipN (xs.length - 1) (p t) := by
  intro xs
  induction xs with
  | nil => intro s t hs; simp at hs
  | cons x xs ih =>
      cases xs with
      | nil =>
          intro s t hs ht _
          have hxs : x = s := Option.some.inj hs
          have hxt : x = t := by simpa using ht
          subst s
          subst t
          rfl
      | cons y ys =>
          intro s t hs ht hc
          have hxs : x = s := Option.some.inj hs
          subst s
          have htail : (y :: ys).getLast? = some t := by simpa using ht
          have hip := ih (s := y) (t := t) rfl htail hc.2
          have hxy := hf hc.1
          change p x = !flipN ys.length (p t)
          simpa using hxy.trans (congrArg Bool.not hip)

private theorem hamiltonPath_length
    {α : Type} {vertices path : List α}
    (hvn : vertices.Nodup) (hpn : path.Nodup)
    (hcover : CoversList vertices path) : vertices.length = path.length := by
  apply Nat.le_antisymm
  · exact hvn.length_le_of_subset (fun x hx => (hcover x).mp hx)
  · exact hpn.length_le_of_subset (fun x hx => (hcover x).mpr hx)

/-- Every finite bipartite graph of order at least three fails
Hamilton-connectedness. No factorial enumeration or part-size calculation
is needed: all spanning paths have the same length, while the second and
third vertices of one such path have different parity. -/
theorem not_hamiltonConnectedOn_of_edge_flip
    {α : Type} {r : α → α → Prop} (p : α → Bool)
    (hf : ∀ ⦃x y⦄, r x y → p x = !p y)
    (vertices : List α) (hvn : vertices.Nodup) (hsize : 3 ≤ vertices.length) :
    ¬ HamiltonConnectedOn vertices r := by
  intro hhc
  cases vertices with
  | nil => simp at hsize
  | cons a vs =>
      cases vs with
      | nil => simp at hsize
      | cons b rest =>
          have hab : a ≠ b := by
            intro heq
            exact (List.nodup_cons.mp hvn).1 (by simp [heq])
          rcases hhc a b (by simp) (by simp) hab with
            ⟨path, hhead, hlast, hpn, hcover, hwalk⟩
          have hlen := hamiltonPath_length hvn hpn hcover
          have hpathsize : 3 ≤ path.length := by omega
          cases path with
          | nil => simp at hpathsize
          | cons x xs =>
              cases xs with
              | nil => simp at hpathsize
              | cons y ys =>
                  cases ys with
                  | nil => simp at hpathsize
                  | cons z zs =>
                      have hxa : x = a := Option.some.inj hhead
                      subst x
                      have hay : a ≠ y := by
                        intro h
                        exact (List.nodup_cons.mp hpn).1 (by simp [h])
                      have haz : a ≠ z := by
                        intro h
                        exact (List.nodup_cons.mp hpn).1 (by simp [h])
                      have hym : y ∈ a :: b :: rest :=
                        (hcover y).mpr (by simp)
                      have hzm : z ∈ a :: b :: rest :=
                        (hcover z).mpr (by simp)
                      rcases hhc a y (by simp) hym hay with
                        ⟨py, hhy, hly, hny, hcy, hwy⟩
                      rcases hhc a z (by simp) hzm haz with
                        ⟨pz, hhz, hlz, hnz, hcz, hwz⟩
                      have hleny := hamiltonPath_length hvn hny hcy
                      have hlenz := hamiltonPath_length hvn hnz hcz
                      have hpy := consecutive_endpoint_parity p hf hhy hly hwy
                      have hpz := consecutive_endpoint_parity p hf hhz hlz hwz
                      have hsame : p y = p z := by
                        apply flipN_injective ((a :: b :: rest).length - 1)
                        rw [← hleny] at hpy
                        rw [← hlenz] at hpz
                        exact hpy.symm.trans hpz
                      have hyz : p y = !p z := hf hwalk.2.1
                      rw [hsame] at hyz
                      cases hz : p z <;> simp [hz] at hyz

theorem arrangement_not_hamiltonConnectedOn {n : Nat}
    (vertices : List (CompletedArrangement n))
    (hvn : vertices.Nodup) (hsize : 3 ≤ vertices.length) :
    ¬ HamiltonConnectedOn vertices ArrangementAdjacent :=
  not_hamiltonConnectedOn_of_edge_flip (r := ArrangementAdjacent)
    arrangementParity (fun {x y} h => arrangement_adjacent_parity h) vertices hvn hsize

end PlanarRecoloring
