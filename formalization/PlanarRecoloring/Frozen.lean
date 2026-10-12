import Std

namespace PlanarRecoloring

/-!
## Explicit frozen colourings

The paper uses two small frozen colourings for sharpness.  This file checks
the local assertion that every legal one-vertex move would change a colour to
one already used at a neighbour.  The finite case split is performed by the
kernel-checked `simp` proof below.
-/

structure CubeVertex where
  x : Bool
  y : Bool
  z : Bool
  deriving DecidableEq

def cubeAdj (u v : CubeVertex) : Prop :=
  (u.x != v.x ∧ u.y = v.y ∧ u.z = v.z) ∨
  (u.x = v.x ∧ u.y != v.y ∧ u.z = v.z) ∨
  (u.x = v.x ∧ u.y = v.y ∧ u.z != v.z)

def bit (b : Bool) : Nat := if b then 1 else 0

def encodeBits (a b : Bool) : Fin 4 :=
  ⟨bit a + 2 * bit b, by cases a <;> cases b <;> decide⟩

def cubeColor (v : CubeVertex) : Fin 4 :=
  encodeBits (Bool.xor v.x v.z) (Bool.xor v.y v.z)

theorem cube_colouring_proper :
    ∀ u v, cubeAdj u v → cubeColor u ≠ cubeColor v := by
  intro u v h
  cases u with
  | mk ux uy uz =>
    cases v with
    | mk vx vy vz =>
      cases ux <;> cases uy <;> cases uz <;>
        cases vx <;> cases vy <;> cases vz <;>
        simp [cubeAdj, cubeColor, encodeBits, bit] at h ⊢

def flipX (u : CubeVertex) : CubeVertex := ⟨!u.x, u.y, u.z⟩
def flipY (u : CubeVertex) : CubeVertex := ⟨u.x, !u.y, u.z⟩
def flipZ (u : CubeVertex) : CubeVertex := ⟨u.x, u.y, !u.z⟩

theorem flipX_adj (u : CubeVertex) : cubeAdj u (flipX u) := by
  cases u with
  | mk ux uy uz => cases ux <;> simp [cubeAdj, flipX]

theorem flipY_adj (u : CubeVertex) : cubeAdj u (flipY u) := by
  cases u with
  | mk ux uy uz => cases uy <;> simp [cubeAdj, flipY]

theorem flipZ_adj (u : CubeVertex) : cubeAdj u (flipZ u) := by
  cases u with
  | mk ux uy uz => cases uz <;> simp [cubeAdj, flipZ]

theorem cube_flip_colour_separation (u : CubeVertex) :
    let x := cubeColor (flipX u)
    let y := cubeColor (flipY u)
    let z := cubeColor (flipZ u)
    cubeColor u ≠ x ∧ cubeColor u ≠ y ∧ cubeColor u ≠ z ∧
      x ≠ y ∧ x ≠ z ∧ y ≠ z := by
  cases u with
  | mk ux uy uz =>
    cases ux <;> cases uy <;> cases uz <;>
      simp [flipX, flipY, flipZ, cubeColor, encodeBits, bit]

theorem fin4_cover_of_four_distinct {a b c d x : Fin 4}
    (hab : a ≠ b) (hac : a ≠ c) (had : a ≠ d)
    (hbc : b ≠ c) (hbd : b ≠ d) (hcd : c ≠ d)
    (hx : x ≠ a) (hxa : x ≠ b) (hxb : x ≠ c) (hxc : x ≠ d) :
    False := by
  have hab' : a.val ≠ b.val := by
    intro h
    exact hab (Fin.ext h)
  have hac' : a.val ≠ c.val := by
    intro h
    exact hac (Fin.ext h)
  have had' : a.val ≠ d.val := by
    intro h
    exact had (Fin.ext h)
  have hbc' : b.val ≠ c.val := by
    intro h
    exact hbc (Fin.ext h)
  have hbd' : b.val ≠ d.val := by
    intro h
    exact hbd (Fin.ext h)
  have hcd' : c.val ≠ d.val := by
    intro h
    exact hcd (Fin.ext h)
  have hxa' : x.val ≠ a.val := by
    intro h
    exact hx (Fin.ext h)
  have hxb' : x.val ≠ b.val := by
    intro h
    exact hxa (Fin.ext h)
  have hxc' : x.val ≠ c.val := by
    intro h
    exact hxb (Fin.ext h)
  have hxd' : x.val ≠ d.val := by
    intro h
    exact hxc (Fin.ext h)
  omega

theorem cube_colouring_is_frozen :
    ∀ u (a : Fin 4), a ≠ cubeColor u →
      ∃ v, cubeAdj u v ∧ cubeColor v = a := by
  intro u a ha
  let x := cubeColor (flipX u)
  let y := cubeColor (flipY u)
  let z := cubeColor (flipZ u)
  have hsep := cube_flip_colour_separation u
  dsimp at hsep
  have hcover : a = x ∨ a = y ∨ a = z := by
    rcases hsep with ⟨h₀x, h₀y, h₀z, hxy, hxz, hyz⟩
    by_cases hax : a = x
    · exact Or.inl hax
    · by_cases hay : a = y
      · exact Or.inr (Or.inl hay)
      · by_cases haz : a = z
        · exact Or.inr (Or.inr haz)
        · exact False.elim
            (fin4_cover_of_four_distinct h₀x h₀y h₀z hxy hxz hyz ha hax hay haz)
  rcases hcover with h | h | h
  · exact ⟨flipX u, flipX_adj u, h.symm⟩
  · exact ⟨flipY u, flipY_adj u, h.symm⟩
  · exact ⟨flipZ u, flipZ_adj u, h.symm⟩

end PlanarRecoloring
