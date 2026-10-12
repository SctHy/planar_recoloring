import PlanarRecoloring.Hamilton

namespace PlanarRecoloring

/-!
# Finite fibres for the adjacent degree-two reduction

The local fibre in `lem:adjacent-two-four` is
`{(a,b) | a ∈ A, b ∈ B, a ≠ b}` for two three-element subsets of a
four-colour palette.  This file replays a canonical cycle for each of the
sixteen labelled mask pairs and checks the common-edge invariant for every
one-list change.  The later base-cycle splice is kept as an explicit
interface, because it also needs the list of base colourings and their
cross-fibre edges.
-/

set_option maxHeartbeats 0
set_option maxRecDepth 100000

abbrev PairFourState := Fin 16
abbrev PairFourMask := Fin 16

def p4 (n : Nat) : Fin 4 := Fin.ofNat 4 n
def p16 (n : Nat) : PairFourState := Fin.ofNat 16 n

def pairFourFst (s : PairFourState) : Fin 4 := ⟨s.val / 4, by omega⟩
def pairFourSnd (s : PairFourState) : Fin 4 := ⟨s.val % 4, by omega⟩
def pairFourHas (m : PairFourMask) (c : Fin 4) : Bool := Nat.testBit m.val c.val

def pairFourAdjB (s t : PairFourState) : Bool :=
  (decide (pairFourFst s ≠ pairFourFst t) &&
      decide (pairFourSnd s = pairFourSnd t)) ||
    (decide (pairFourFst s = pairFourFst t) &&
      decide (pairFourSnd s ≠ pairFourSnd t))

def PairFourAdjacent (s t : PairFourState) : Prop := pairFourAdjB s t = true

def PairFourStates (m n : PairFourMask) : List PairFourState :=
  (List.finRange 16).filter (fun s =>
    pairFourHas m (pairFourFst s) &&
      pairFourHas n (pairFourSnd s) &&
      decide (pairFourFst s ≠ pairFourSnd s))

def pairFourList (m : PairFourMask) : List (Fin 4) :=
  (List.finRange 4).filter (fun c => pairFourHas m c)

def pairFourSmall (m : PairFourMask) : Prop := (pairFourList m).length = 3

def pairFourWalkB : List PairFourState → Bool
  | [] => true
  | [_] => true
  | x :: y :: xs => pairFourAdjB x y && pairFourWalkB (y :: xs)

def pairFourCloseB : List PairFourState → Bool
  | [] => false
  | path => match path.head?, path.getLast? with
    | some a, some b => pairFourAdjB b a
    | _, _ => false

def pairFourCycleValid (m n : PairFourMask) (path : List PairFourState) : Prop :=
  path.Nodup ∧
    (∀ q : PairFourState, q ∈ PairFourStates m n ↔ q ∈ path) ∧
    pairFourWalkB path = true ∧ pairFourCloseB path = true

def p4s (a b : Nat) : PairFourState := p16 (a * 4 + b)

def pairFourCanonicalPath (m n : PairFourMask) : List PairFourState :=
  match m.val, n.val with
  | 7, 7 => [p4s 0 1, p4s 0 2, p4s 1 2, p4s 1 0, p4s 2 0, p4s 2 1]
  | 7, 11 => [p4s 0 1, p4s 0 3, p4s 1 3, p4s 1 0, p4s 2 0, p4s 2 3, p4s 2 1]
  | 7, 13 => [p4s 0 2, p4s 0 3, p4s 1 3, p4s 2 3, p4s 2 0, p4s 1 0, p4s 1 2]
  | 7, 14 => [p4s 0 1, p4s 0 2, p4s 1 2, p4s 1 3, p4s 0 3, p4s 2 3, p4s 2 1]
  | 11, 7 => [p4s 0 1, p4s 0 2, p4s 1 2, p4s 1 0, p4s 3 0, p4s 3 2, p4s 3 1]
  | 11, 11 => [p4s 0 1, p4s 0 3, p4s 1 3, p4s 1 0, p4s 3 0, p4s 3 1]
  | 11, 13 => [p4s 0 2, p4s 0 3, p4s 1 3, p4s 1 0, p4s 3 0, p4s 3 2, p4s 1 2]
  | 11, 14 => [p4s 0 1, p4s 0 2, p4s 0 3, p4s 1 3, p4s 1 2, p4s 3 2, p4s 3 1]
  | 13, 7 => [p4s 0 1, p4s 0 2, p4s 3 2, p4s 3 0, p4s 2 0, p4s 2 1, p4s 3 1]
  | 13, 11 => [p4s 0 1, p4s 0 3, p4s 2 3, p4s 2 0, p4s 3 0, p4s 3 1, p4s 2 1]
  | 13, 13 => [p4s 0 2, p4s 0 3, p4s 2 3, p4s 2 0, p4s 3 0, p4s 3 2]
  | 13, 14 => [p4s 0 1, p4s 0 2, p4s 3 2, p4s 3 1, p4s 2 1, p4s 2 3, p4s 0 3]
  | 14, 7 => [p4s 1 0, p4s 1 2, p4s 3 2, p4s 3 0, p4s 3 1, p4s 2 1, p4s 2 0]
  | 14, 11 => [p4s 1 0, p4s 1 3, p4s 2 3, p4s 2 0, p4s 2 1, p4s 3 1, p4s 3 0]
  | 14, 13 => [p4s 1 0, p4s 1 2, p4s 3 2, p4s 3 0, p4s 2 0, p4s 2 3, p4s 1 3]
  | 14, 14 => [p4s 1 2, p4s 1 3, p4s 2 3, p4s 2 1, p4s 3 1, p4s 3 2]
  | _, _ => []

def pairFourEdgeB (s t x y : PairFourState) : Bool :=
  (decide (x = s) && decide (y = t)) ||
    (decide (x = t) && decide (y = s))

def pairFourEdgeScan (s t first prev : PairFourState) : List PairFourState → Bool
  | [] => pairFourEdgeB s t prev first
  | y :: ys => pairFourEdgeB s t prev y || pairFourEdgeScan s t first y ys

def pairFourEdgeInB (s t : PairFourState) : List PairFourState → Bool
  | [] => false
  | first :: rest => pairFourEdgeScan s t first first rest

def pairFourEdgeIn (s t : PairFourState) (path : List PairFourState) : Prop :=
  pairFourEdgeInB s t path = true

def pairFourOneChangeB (m n : PairFourMask) : Bool :=
  decide (m = n ∨ m.val.xor n.val = 3 ∨ m.val.xor n.val = 5 ∨
    m.val.xor n.val = 6 ∨ m.val.xor n.val = 9 ∨ m.val.xor n.val = 10 ∨
    m.val.xor n.val = 12)

def pairFourAllowedB (m n m' n' : PairFourMask) : Bool :=
  (decide (m = m') && decide (n = n')) ||
    (decide (n = n') && pairFourOneChangeB m m') ||
    (decide (m = m') && pairFourOneChangeB n n')

def pairFourCommonCount (m n m' n' : PairFourMask) : Nat :=
  ((List.finRange 16).flatMap (fun s =>
    (List.finRange 16).filter (fun t =>
      pairFourEdgeInB s t (pairFourCanonicalPath m n) &&
        pairFourEdgeInB s t (pairFourCanonicalPath m' n')))).length

instance pairFourAdjacentDecidable (s t : PairFourState) : Decidable (PairFourAdjacent s t) := by
  unfold PairFourAdjacent
  infer_instance

instance pairFourSmallDecidable (m : PairFourMask) : Decidable (pairFourSmall m) := by
  unfold pairFourSmall pairFourList
  infer_instance

instance pairFourCycleValidDecidable (m n : PairFourMask)
    (path : List PairFourState) : Decidable (pairFourCycleValid m n path) := by
  unfold pairFourCycleValid
  infer_instance

theorem pairFour_canonical_cycle :
    ∀ m n : PairFourMask, pairFourSmall m → pairFourSmall n →
      pairFourCycleValid m n (pairFourCanonicalPath m n) := by
  decide

theorem pairFour_common_edges_at_least_two :
    ∀ m n m' n' : PairFourMask,
      pairFourSmall m → pairFourSmall n → pairFourSmall m' → pairFourSmall n' →
      pairFourAllowedB m n m' n' = true →
      2 ≤ pairFourCommonCount m n m' n' := by
  decide

private theorem pairFour_canonical_path_nonempty :
    ∀ m n : PairFourMask, pairFourSmall m → pairFourSmall n →
      pairFourCanonicalPath m n ≠ [] := by
  decide

private theorem pairFour_getLast_some {α : Type} :
    ∀ (path : List α), path ≠ [] → ∃ z, path.getLast? = some z := by
  intro path
  induction path with
  | nil => intro h; exact False.elim (h rfl)
  | cons x xs ih =>
      cases xs with
      | nil => intro _; exact ⟨x, rfl⟩
      | cons y ys =>
          intro _
          rcases ih (by simp) with ⟨z, hz⟩
          exact ⟨z, by simpa using hz⟩

private theorem pairFour_consecutive_of_walk
    (path : List PairFourState) (h : pairFourWalkB path = true) :
    Consecutive PairFourAdjacent path := by
  induction path with
  | nil => simp [Consecutive]
  | cons x xs ih =>
      cases xs with
      | nil => simp [Consecutive]
      | cons y ys =>
          simp only [pairFourWalkB, Bool.and_eq_true] at h
          exact ⟨h.1, ih h.2⟩

private theorem pairFour_close_of_head_last
    {path : List PairFourState} {a z : PairFourState}
    (ha : path.head? = some a) (hz : path.getLast? = some z)
    (hc : pairFourCloseB path = true) : PairFourAdjacent z a := by
  cases path with
  | nil => simp at ha
  | cons x xs =>
      cases xs with
      | nil => simp [pairFourCloseB, pairFourAdjB] at hc
      | cons y ys =>
          have hxa : x = a := by simpa using ha
          subst x
          have hlast : (y :: ys).getLast? = some z := by simpa using hz
          change pairFourAdjB z a = true
          simpa [pairFourCloseB, hlast] using hc

theorem pairFour_hamiltonCycle
    {m n : PairFourMask} (hm : pairFourSmall m) (hn : pairFourSmall n) :
    HamiltonCycleOn (PairFourStates m n) PairFourAdjacent := by
  have hc := pairFour_canonical_cycle m n hm hn
  let path := pairFourCanonicalPath m n
  have hne : path ≠ [] := pairFour_canonical_path_nonempty m n hm hn
  rcases pairFour_getLast_some path hne with ⟨z, hz⟩
  have ha : ∃ a, path.head? = some a :=
    ⟨path.head hne, List.head?_eq_some_head hne⟩
  rcases ha with ⟨a, ha⟩
  have hclose := pairFour_close_of_head_last ha hz hc.2.2.2
  refine ⟨path, hc.1, ?_, ?_⟩
  · intro q
    exact hc.2.1 q
  · exact ⟨a, z, ha, hz, pairFour_consecutive_of_walk path hc.2.2.1, hclose⟩

end PlanarRecoloring
