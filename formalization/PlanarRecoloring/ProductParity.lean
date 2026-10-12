import PlanarRecoloring.Core

/-!
# Parity obstruction for binary products

A vertex of a finite binary product is represented by a list of bits.  An edge
flips exactly one coordinate.  The xor parity of the coordinates therefore
changes at every edge; the indexed path results below give the usual bipartite
obstruction to odd cycles.
-/

namespace PlanarRecoloring

/-- Xor of all coordinates in a binary product vertex. -/
def cubeParity : List Bool → Bool
  | [] => false
  | b :: xs => Bool.xor b (cubeParity xs)

@[simp] theorem cubeParity_nil : cubeParity ([] : List Bool) = false := rfl

@[simp] theorem cubeParity_cons (b : Bool) (xs : List Bool) :
    cubeParity (b :: xs) = Bool.xor b (cubeParity xs) := rfl

theorem cubeParity_append (xs ys : List Bool) :
    cubeParity (xs ++ ys) = Bool.xor (cubeParity xs) (cubeParity ys) := by
  induction xs with
  | nil => simp [cubeParity]
  | cons b xs ih => simp [cubeParity, ih]

/-- Flipping one coordinate reverses xor parity. -/
theorem cubeParity_flip (pre suff : List Bool) (b : Bool) :
    cubeParity (pre ++ (b :: suff)) =
      !cubeParity (pre ++ ((!b) :: suff)) := by
  rw [cubeParity_append pre (b :: suff), cubeParity_append pre ((!b) :: suff)]
  simp only [cubeParity_cons]
  cases b <;> cases cubeParity pre <;> cases cubeParity suff <;>
    simp

/-- Two binary-product vertices are adjacent when one coordinate is flipped. -/
def ProductAdj (x y : List Bool) : Prop :=
  ∃ (pre suff : List Bool) (b : Bool),
    x = pre ++ (b :: suff) ∧
      y = pre ++ ((!b) :: suff)

theorem productAdj_parity {x y : List Bool} (h : ProductAdj x y) :
    cubeParity x = !cubeParity y := by
  rcases h with ⟨pre, suff, b, rfl, rfl⟩
  exact cubeParity_flip pre suff b

/-- An indexed edge path records its endpoints and its number of edges. -/
inductive ProductPath : Nat → List Bool → List Bool → Prop
  | refl (x : List Bool) : ProductPath 0 x x
  | step {n : Nat} {x y z : List Bool} :
      ProductAdj x y → ProductPath n y z → ProductPath (n + 1) x z

/-- Along a path, parity is flipped once per edge. -/
def flipN : Nat → Bool → Bool
  | 0, b => b
  | n + 1, b => !flipN n b

theorem productPath_parity {n : Nat} {x y : List Bool}
    (h : ProductPath n x y) :
    cubeParity x = flipN n (cubeParity y) := by
  induction h with
  | refl x => rfl
  | @step n x y z hxy hyz ih =>
      calc
        cubeParity x = !cubeParity y := productAdj_parity hxy
        _ = !flipN n (cubeParity z) := by rw [ih]
        _ = flipN (n + 1) (cubeParity z) := by rfl

/-- Two successive flips cancel. -/
theorem flipN_two_mul (k : Nat) (b : Bool) :
    flipN (2 * k) b = b := by
  induction k with
  | zero => rfl
  | succ k ih =>
      simpa [Nat.mul_succ, flipN] using ih

/-- An odd number of flips reverses parity. -/
theorem flipN_two_mul_succ (k : Nat) (b : Bool) :
    flipN (2 * k + 1) b = !b := by
  rw [Nat.add_comm]
  change flipN (1 + 2 * k) b = !b
  induction k with
  | zero => rfl
  | succ k ih =>
      simpa [Nat.mul_succ, Nat.add_assoc, flipN] using ih

def OddLength (n : Nat) : Prop := ∃ k : Nat, n = 2 * k + 1

theorem odd_productPath_opposite {n : Nat} {x y : List Bool}
    (hodd : OddLength n) (hpath : ProductPath n x y) :
    cubeParity x = !cubeParity y := by
  rcases hodd with ⟨k, rfl⟩
  rw [productPath_parity hpath]
  exact flipN_two_mul_succ k (cubeParity y)

/- A path with an even number of flips preserves the bipartition class.
   This is the endpoint necessity used by the binary-product part of the
   product-fibre argument. -/
theorem even_productPath_same {n : Nat} {x y : List Bool}
    (heven : ∃ k : Nat, n = 2 * k)
    (hpath : ProductPath n x y) :
    cubeParity x = cubeParity y := by
  rcases heven with ⟨k, rfl⟩
  rw [productPath_parity hpath]
  exact flipN_two_mul k (cubeParity y)

theorem no_odd_product_cycle {n : Nat} {x : List Bool}
    (hodd : OddLength n) (hpath : ProductPath n x x) : False := by
  have hflip : cubeParity x = !cubeParity x :=
    odd_productPath_opposite hodd hpath
  cases cubeParity x <;> simp at hflip

end PlanarRecoloring

namespace PlanarRecoloring

/-- A product edge changes no list coordinate count. -/
theorem productAdj_length {x y : List Bool} (h : ProductAdj x y) :
    x.length = y.length := by
  rcases h with ⟨pre, suff, b, rfl, rfl⟩
  simp

/-- Every indexed product path has endpoints of the same list length. -/
theorem productPath_length {n : Nat} {x y : List Bool}
    (h : ProductPath n x y) : x.length = y.length := by
  induction h with
  | refl x => rfl
  | @step n x y z hxy hyz ih =>
      exact (productAdj_length hxy).trans ih

/-- Product adjacency is symmetric, so an indexed path can be traversed in
reverse without changing its edge count. -/
theorem productAdj_symm {x y : List Bool} :
    ProductAdj x y → ProductAdj y x := by
  rintro ⟨pre, suff, b, rfl, rfl⟩
  exact ⟨pre, suff, !b, by simp, by simp⟩

theorem ProductPath.snoc {n : Nat} {x y z : List Bool}
    (h : ProductPath n x y) (hyz : ProductAdj y z) :
    ProductPath (n + 1) x z := by
  induction h with
  | refl x => exact ProductPath.step hyz (.refl z)
  | @step n x y z hxy hyz ih =>
      exact ProductPath.step hxy (ih hyz)

theorem ProductPath.reverse {n : Nat} {x y : List Bool}
    (h : ProductPath n x y) : ProductPath n y x := by
  induction h with
  | refl x => exact .refl x
  | @step n x y z hxy hyz ih =>
      have hrev : ProductPath n z y := ih
      have hlast : ProductAdj y x := productAdj_symm hxy
      have hs := ProductPath.snoc hrev hlast
      simpa [Nat.add_comm] using hs

end PlanarRecoloring
