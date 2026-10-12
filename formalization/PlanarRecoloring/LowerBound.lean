import Std

namespace PlanarRecoloring

structure State where
  c₀ : Bool
  c₁ : Bool
  deriving DecidableEq

def Adj (x y : State) : Prop :=
  (x.c₀ != y.c₀ ∧ x.c₁ = y.c₁) ∨
  (x.c₀ = y.c₀ ∧ x.c₁ != y.c₁)

def parity (x : State) : Bool := Bool.xor x.c₀ x.c₁

theorem adj_parity (x y : State) (h : Adj x y) : parity x != parity y := by
  cases x with | mk x0 x1 =>
    cases y with | mk y0 y1 =>
      cases x0 <;> cases x1 <;> cases y0 <;> cases y1 <;>
        simp [Adj, parity] at h ⊢

theorem parity_flip (x y : State) (h : Adj x y) : parity x = !parity y := by
  have h' := adj_parity x y h
  cases hp : parity x <;> cases hq : parity y <;> simp_all

theorem no_three_step_path_00_11 : ¬ ∃ (a b c d : State),
      a = ⟨false, false⟩ ∧ d = ⟨true, true⟩ ∧
      Adj a b ∧ Adj b c ∧ Adj c d := by
  rintro ⟨a,b,c,d,ha,hd,hab,hbc,hcd⟩
  subst a
  subst d
  have h1 := parity_flip _ _ hab
  have h2 := parity_flip _ _ hbc
  have h3 := parity_flip _ _ hcd
  simp [parity] at h1 h2 h3
  cases b with | mk b0 b1 =>
    cases c with | mk c0 c1 =>
      cases b0 <;> cases b1 <;> cases c0 <;> cases c1 <;>
        simp at h1 h2 h3

def Distinct4 (a b c d : State) : Prop :=
  a ≠ b ∧ a ≠ c ∧ a ≠ d ∧ b ≠ c ∧ b ≠ d ∧ c ≠ d

def Covers (a b c d : State) : Prop :=
  (⟨false, false⟩ = a ∨ ⟨false, false⟩ = b ∨ ⟨false, false⟩ = c ∨ ⟨false, false⟩ = d) ∧
  (⟨false, true⟩ = a ∨ ⟨false, true⟩ = b ∨ ⟨false, true⟩ = c ∨ ⟨false, true⟩ = d) ∧
  (⟨true, false⟩ = a ∨ ⟨true, false⟩ = b ∨ ⟨true, false⟩ = c ∨ ⟨true, false⟩ = d) ∧
  (⟨true, true⟩ = a ∨ ⟨true, true⟩ = b ∨ ⟨true, true⟩ = c ∨ ⟨true, true⟩ = d)

/-- A four-vertex spanning path in the two-cube, written without importing a graph library. -/
def FourVertexPath (s t : State) : Prop :=
  ∃ (a b c d : State),
    a = s ∧ d = t ∧ Adj a b ∧ Adj b c ∧ Adj c d ∧
      Distinct4 a b c d ∧ Covers a b c d

/-- The two-cube is not Hamilton-connected: the two even-parity states cannot be endpoints
    of a spanning path. -/
theorem q2_not_hamilton_connected :
    ¬ (∀ s t : State, s ≠ t → FourVertexPath s t) := by
  intro h
  have hpath := h ⟨false, false⟩ ⟨true, true⟩ (by decide)
  rcases hpath with ⟨a, b, c, d, ha, hd, hab, hbc, hcd, _, _⟩
  exact no_three_step_path_00_11 ⟨a, b, c, d, ha, hd, hab, hbc, hcd⟩

theorem q2_has_no_triangle :
    ¬ ∃ a b c : State, Adj a b ∧ Adj b c ∧ Adj c a := by
  rintro ⟨a, b, c, hab, hbc, hca⟩
  cases a with
  | mk a₀ a₁ =>
    cases b with
    | mk b₀ b₁ =>
      cases c with
      | mk c₀ c₁ =>
        cases a₀ <;> cases a₁ <;> cases b₀ <;> cases b₁ <;>
          cases c₀ <;> cases c₁ <;>
          simp [Adj] at hab hbc hca

end PlanarRecoloring
