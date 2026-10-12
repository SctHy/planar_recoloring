import PlanarRecoloring.General

/-!
# The star edge with no triangle

For every `k ≥ 4`, the star on `k - 1` vertices is `K_{1,k-2}`.
Its centre is vertex zero.  Give the leaves colours `2, ..., k - 1`,
and switch the centre between colours zero and one (the article's one
and two).  The resulting recolouring edge has no common adjacent state.
This is an obstruction to strengthening vertex-pancyclicity uniformly
to edge-pancyclicity, not a claim about every recolouring edge or graph.
-/

namespace PlanarRecoloring

/-- A star on `n` vertices, with vertex zero as its centre. -/
def StarGraph (n : Nat) : FiniteGraph n where
  adj u v := (u.val == 0 && v.val != 0) || (u.val != 0 && v.val == 0)

theorem star_edge_iff {n : Nat} (u v : Vertex n) :
    Edge (StarGraph n) u v ↔
      (u.val = 0 ∧ v.val ≠ 0) ∨ (u.val ≠ 0 ∧ v.val = 0) := by
  simp [Edge, StarGraph]

theorem star_simple (n : Nat) : Simple (StarGraph n) := by
  constructor
  · intro u v
    simp [StarGraph, Bool.and_comm, Bool.or_comm]
  · intro v
    by_cases h : v.val = 0 <;> simp [StarGraph, h]

/-- The centre exists for the palettes considered in the article. -/
def StarCentre (k : Nat) (hk : 4 ≤ k) : Vertex (k - 1) := ⟨0, by omega⟩

/-- Two explicit centre colours, leaving all other colours on the leaves. -/
def StarColourValue (k : Nat) (hk : 4 ≤ k) (a : Fin 2)
    (v : Vertex (k - 1)) : Colour k :=
  if v.val = 0 then ⟨a.val, by omega⟩ else ⟨v.val + 1, by omega⟩

theorem star_colour_centre (k : Nat) (hk : 4 ≤ k) (a : Fin 2) :
    (StarColourValue k hk a (StarCentre k hk)).val = a.val := by
  simp [StarColourValue, StarCentre]

theorem star_colour_leaf (k : Nat) (hk : 4 ≤ k) (a : Fin 2)
    (v : Vertex (k - 1)) (hv : v.val ≠ 0) :
    (StarColourValue k hk a v).val = v.val + 1 := by
  simp [StarColourValue, hv]

theorem star_colour_proper (k : Nat) (hk : 4 ≤ k) (a : Fin 2) :
    Proper (StarGraph (k - 1)) (StarColourValue k hk a) := by
  intro u v huv heq
  have heqval := congrArg Fin.val heq
  rcases (star_edge_iff u v).mp huv with ⟨hu, hv⟩ | ⟨hu, hv⟩
  · simp [StarColourValue, hu, hv] at heqval
    have ha := a.isLt
    omega
  · simp [StarColourValue, hu, hv] at heqval
    have ha := a.isLt
    omega

def StarColour (k : Nat) (hk : 4 ≤ k) (a : Fin 2) :
    Coloring (StarGraph (k - 1)) k :=
  ⟨StarColourValue k hk a, star_colour_proper k hk a⟩

theorem star_colours_agree_on_leaves (k : Nat) (hk : 4 ≤ k)
    (a b : Fin 2) (v : Vertex (k - 1)) (hv : v ≠ StarCentre k hk) :
    StarColour k hk a v = StarColour k hk b v := by
  have hv0 : v.val ≠ 0 := by
    intro h
    apply hv
    exact Fin.ext h
  change StarColourValue k hk a v = StarColourValue k hk b v
  simp [StarColourValue, hv0]

theorem star_recolour_edge (k : Nat) (hk : 4 ≤ k) :
    RecolourAdjacent (StarColour k hk 0) (StarColour k hk 1) := by
  refine ⟨StarCentre k hk, ?_, ?_⟩
  · intro h
    have hval := congrArg Fin.val h
    change (StarColourValue k hk 0 (StarCentre k hk)).val =
      (StarColourValue k hk 1 (StarCentre k hk)).val at hval
    simp [star_colour_centre] at hval
  · intro v hv
    exact star_colours_agree_on_leaves k hk 0 1 v hv

/-- A common adjacent state must keep every leaf fixed. -/
theorem star_common_adjacent_leaves (k : Nat) (hk : 4 ≤ k)
    (z : Coloring (StarGraph (k - 1)) k)
    (hxz : RecolourAdjacent (StarColour k hk 0) z)
    (hyz : RecolourAdjacent (StarColour k hk 1) z) :
    ∀ v, v ≠ StarCentre k hk → StarColour k hk 0 v = z v := by
  rcases hxz with ⟨u, hu, hrest⟩
  rcases hyz with ⟨w, hw, hrest'⟩
  have hu0 : u = StarCentre k hk := by
    by_cases huc : u = StarCentre k hk
    · exact huc
    · have hwc : w = StarCentre k hk := by
        by_cases hwc : w = StarCentre k hk
        · exact hwc
        · have hsame := (hrest (StarCentre k hk) (Ne.symm huc)).trans
            (hrest' (StarCentre k hk) (Ne.symm hwc)).symm
          have hval := congrArg Fin.val hsame
          change (StarColourValue k hk 0 (StarCentre k hk)).val =
            (StarColourValue k hk 1 (StarCentre k hk)).val at hval
          simp [star_colour_centre] at hval
      apply False.elim
      apply hu
      exact (star_colours_agree_on_leaves k hk 0 1 u huc).trans
        (hrest' u (by simpa [hwc] using huc))
  subst u
  exact hrest

/-- Every colour other than zero and one is used by a fixed leaf. -/
theorem star_fixed_leaves_force_centre (k : Nat) (hk : 4 ≤ k)
    (z : Coloring (StarGraph (k - 1)) k)
    (hleaves : ∀ v, v ≠ StarCentre k hk → StarColour k hk 0 v = z v) :
    (z (StarCentre k hk)).val < 2 := by
  by_cases hlt : (z (StarCentre k hk)).val < 2
  · exact hlt
  · have hc : 2 ≤ (z (StarCentre k hk)).val := by omega
    let v : Vertex (k - 1) := ⟨(z (StarCentre k hk)).val - 1, by
      have hz := (z (StarCentre k hk)).isLt
      omega⟩
    have hv0 : v.val ≠ 0 := by dsimp [v]; omega
    have hvc : v ≠ StarCentre k hk := by
      intro heq
      have heqval := congrArg Fin.val heq
      simp [StarCentre] at heqval
      exact hv0 heqval
    have hedge : Edge (StarGraph (k - 1)) (StarCentre k hk) v := by
      apply (star_edge_iff _ _).mpr
      exact Or.inl ⟨rfl, hv0⟩
    exfalso
    apply (z.proper hedge)
    rw [← hleaves v hvc]
    apply Fin.ext
    change (z (StarCentre k hk)).val = (StarColourValue k hk 0 v).val
    rw [star_colour_leaf k hk 0 v hv0]
    dsimp [v]
    omega

theorem star_edge_has_no_common_adjacent (k : Nat) (hk : 4 ≤ k) :
    ¬ ∃ z : Coloring (StarGraph (k - 1)) k,
      RecolourAdjacent (StarColour k hk 0) z ∧
        RecolourAdjacent (StarColour k hk 1) z := by
  rintro ⟨z, hxz, hyz⟩
  have hleaves := star_common_adjacent_leaves k hk z hxz hyz
  have hzlt := star_fixed_leaves_force_centre k hk z hleaves
  have hxneq : StarColour k hk 0 (StarCentre k hk) ≠ z (StarCentre k hk) := by
    rcases hxz with ⟨v, hv, hrest⟩
    have hvc : v = StarCentre k hk := by
      by_cases h : v = StarCentre k hk
      · exact h
      · exact False.elim (hv (hleaves v h))
    simpa [hvc] using hv
  have hyneq : StarColour k hk 1 (StarCentre k hk) ≠ z (StarCentre k hk) := by
    rcases hyz with ⟨v, hv, hrest⟩
    have hvc : v = StarCentre k hk := by
      by_cases h : v = StarCentre k hk
      · exact h
      · apply False.elim
        apply hv
        exact (star_colours_agree_on_leaves k hk 1 0 v h).trans (hleaves v h)
    simpa [hvc] using hv
  have hz0 : (z (StarCentre k hk)).val ≠ 0 := by
    intro h
    apply hxneq
    apply Fin.ext
    change (StarColourValue k hk 0 (StarCentre k hk)).val =
      (z (StarCentre k hk)).val
    simpa [star_colour_centre] using h.symm
  have hz1 : (z (StarCentre k hk)).val ≠ 1 := by
    intro h
    apply hyneq
    apply Fin.ext
    change (StarColourValue k hk 1 (StarCentre k hk)).val =
      (z (StarCentre k hk)).val
    simpa [star_colour_centre] using h.symm
  omega

/-- The specified recolouring edge lies in no triangle. -/
theorem star_edge_has_no_triangle (k : Nat) (hk : 4 ≤ k) :
    ¬ ∃ z : Coloring (StarGraph (k - 1)) k,
      RecolourAdjacent (StarColour k hk 0) z ∧
        RecolourAdjacent z (StarColour k hk 1) := by
  rintro ⟨z, hxz, hzy⟩
  exact star_edge_has_no_common_adjacent k hk
    ⟨z, hxz, recolour_adjacent_symm hzy⟩

private theorem star_leaf_degree_le_one (k : Nat) (hk : 4 ≤ k)
    (S : List (Vertex (k - 1))) (hS : S.Nodup)
    (v : Vertex (k - 1)) (hv : v.val ≠ 0) :
    DegreeIn (StarGraph (k - 1)) S v ≤ 1 := by
  let q := NeighboursIn (StarGraph (k - 1)) S v
  have hq : q.Nodup := by
    apply List.nodup_iff_pairwise_ne.mp
    apply List.Pairwise.filter
    exact List.nodup_iff_pairwise_ne.mpr hS
  have hsub : q ⊆ [StarCentre k hk] := by
    intro u hu
    have hu' := (mem_neighboursIn_iff (StarGraph (k - 1)) S v u).mp hu
    rcases (star_edge_iff v u).mp hu'.2 with ⟨hv0, hu0⟩ | ⟨hv0, hu0⟩
    · exact False.elim (hv hv0)
    · have huv : u = StarCentre k hk := by
        apply Fin.ext
        simpa [StarCentre] using hu0
      simpa [huv]
  have hlen : q.length ≤ [StarCentre k hk].length :=
    hq.length_le_of_subset hsub
  simpa [q, DegreeIn] using hlen

/-- Every star is 1-degenerate: repeatedly remove a leaf (or the centre alone).
This is the finite-list version of the usual degeneracy ordering. -/
theorem star_degenerate_one (k : Nat) (hk : 4 ≤ k) :
    Degenerate (StarGraph (k - 1)) 1 := by
  intro S hS hne
  cases S with
  | nil => exact False.elim (hne rfl)
  | cons v vs =>
    by_cases hv : v.val = 0
    · have hvcentre : v = StarCentre k hk := by
        apply Fin.ext
        simpa [StarCentre] using hv
      subst v
      cases vs with
      | nil =>
          refine ⟨StarCentre k hk, ?_, ?_⟩
          · simp
          · simp [DegreeIn, NeighboursIn, StarGraph, StarCentre]
      | cons w ws =>
          by_cases hw : w.val = 0
          · have hwcentre : w = StarCentre k hk := by
              apply Fin.ext
              simpa [StarCentre] using hw
            have hbad : StarCentre k hk ∈ w :: ws := by
              simp [hwcentre]
            exact False.elim ((List.nodup_cons.mp hS).1 hbad)
          · refine ⟨w, ?_, star_leaf_degree_le_one k hk
              (StarCentre k hk :: w :: ws) hS w hw⟩
            simp
    · refine ⟨v, ?_, star_leaf_degree_le_one k hk (v :: vs) hS v hv⟩
      simp

end PlanarRecoloring
