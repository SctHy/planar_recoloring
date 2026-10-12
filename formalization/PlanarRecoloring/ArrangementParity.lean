import PlanarRecoloring.General

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

theorem arrangement_adjacent_symm {n : Nat} {s t : CompletedArrangement n}
    (h : ArrangementAdjacent s t) : ArrangementAdjacent t s := by
  rcases h with ⟨pre, middle, a, b, hs, ht⟩
  exact ⟨pre, middle, b, a, ht, hs⟩

/-- Generic parity obstruction for an arrangement-like relation.  Supplying
an independently verified parity labelling is enough to rule out triangles.
The inversion-parity labelling above is kept separate because its exchange
lemma is the arithmetic part of the arrangement-graph formalization. -/
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

end PlanarRecoloring
