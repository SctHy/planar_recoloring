import PlanarRecoloring.Hamilton

/-!
# Kernel replay of the adjacent-pair fibres

The seven finite fibre types in Chapter 4 are represented by two five-bit
masks.  The tables below are generated from the literal Appendix A words; the
Lean theorems replay every table entry and then transport it through the
finite list of colour renamings.  No computational oracle is used.
-/

namespace PlanarRecoloring

set_option maxHeartbeats 0
set_option maxRecDepth 100000

abbrev PairFiveState := Fin 25
abbrev PairFiveMask := Fin 32
abbrev PairFiveKind := Fin 7

def p5 (n : Nat) : Fin 5 := Fin.ofNat 5 n
def p25 (n : Nat) : PairFiveState := Fin.ofNat 25 n
def p32 (n : Nat) : PairFiveMask := Fin.ofNat 32 n

def pairFiveFst (s : PairFiveState) : Fin 5 := ⟨s.val / 5, by omega⟩
def pairFiveSnd (s : PairFiveState) : Fin 5 := ⟨s.val % 5, by omega⟩
def pairFiveEncode (a b : Fin 5) : PairFiveState := p25 (a.val * 5 + b.val)

def pairFiveHas (m : PairFiveMask) (c : Fin 5) : Bool := Nat.testBit m.val c.val

def pairFiveAdjB (s t : PairFiveState) : Bool :=
  (decide (pairFiveFst s ≠ pairFiveFst t) &&
      decide (pairFiveSnd s = pairFiveSnd t)) ||
    (decide (pairFiveFst s = pairFiveFst t) &&
      decide (pairFiveSnd s ≠ pairFiveSnd t))

def PairFiveAdjacent (s t : PairFiveState) : Prop := pairFiveAdjB s t = true

def PairFiveStates (m n : PairFiveMask) : List PairFiveState :=
  (List.finRange 25).filter (fun s =>
    pairFiveHas m (pairFiveFst s) &&
      pairFiveHas n (pairFiveSnd s) &&
      decide (pairFiveFst s ≠ pairFiveSnd s))

def pairFiveList (m : PairFiveMask) : List (Fin 5) :=
  (List.finRange 5).filter (fun c => pairFiveHas m c)
def pairFiveSmall (m : PairFiveMask) : Prop :=
  (pairFiveList m).length = 3 ∨ (pairFiveList m).length = 4

def pairFiveWalkB : List PairFiveState → Bool
  | [] => true
  | [_] => true
  | x :: y :: xs => pairFiveAdjB x y && pairFiveWalkB (y :: xs)

def pairFivePathValid (m n : PairFiveMask) (s t : PairFiveState)
    (path : List PairFiveState) : Prop :=
  path.head? = some s ∧ path.getLast? = some t ∧ path.Nodup ∧
    (∀ q : PairFiveState, q ∈ PairFiveStates m n ↔ q ∈ path) ∧
    pairFiveWalkB path = true

def pairFiveCloseB : List PairFiveState → Bool
  | [] => false
  | path => match path.head?, path.getLast? with
    | some a, some b => pairFiveAdjB b a
    | _, _ => false

def pairFiveCycleValid (m n : PairFiveMask)
    (path : List PairFiveState) : Prop :=
  path.Nodup ∧
    (∀ q : PairFiveState, q ∈ PairFiveStates m n ↔ q ∈ path) ∧
    pairFiveWalkB path = true ∧ pairFiveCloseB path = true

def pairFiveEdgeInB (s t : PairFiveState) : List PairFiveState → Bool
  | [] => false
  | x :: xs =>
      (decide (x = s) && decide (xs.head? = some t)) ||
        (decide (x = t) && decide (xs.head? = some s))
def pairFiveEdgeIn (s t : PairFiveState) (path : List PairFiveState) : Prop :=
  pairFiveEdgeInB s t path = true

structure PairFiveEntry where
  start : PairFiveState
  finish : PairFiveState
  path : List PairFiveState
structure PairFiveNorm where
  kind : Nat
  swap : Bool
  p : List Nat
  q : List Nat

def pairFivePerm (xs : List Nat) (c : Fin 5) : Fin 5 := p5 (xs.getD c.val 0)
def pairFiveMap (d : PairFiveNorm) (s : PairFiveState) : PairFiveState :=
  if d.swap then
    pairFiveEncode (pairFivePerm d.p (pairFiveSnd s))
      (pairFivePerm d.p (pairFiveFst s))
  else
    pairFiveEncode (pairFivePerm d.p (pairFiveFst s))
      (pairFivePerm d.p (pairFiveSnd s))
def pairFiveUnmap (d : PairFiveNorm) (s : PairFiveState) : PairFiveState :=
  if d.swap then
    pairFiveEncode (pairFivePerm d.q (pairFiveSnd s))
      (pairFivePerm d.q (pairFiveFst s))
  else
    pairFiveEncode (pairFivePerm d.q (pairFiveFst s))
      (pairFivePerm d.q (pairFiveSnd s))
def pairFiveMapPath (d : PairFiveNorm) (path : List PairFiveState) : List PairFiveState :=
  path.map (pairFiveMap d)


def pairFiveCycle331 : List PairFiveEntry := [
  { start := p25 3, finish := p25 4, path := [(p25 3), (p25 4), (p25 9), (p25 5), (p25 10), (p25 14), (p25 13), (p25 8)] },
  { start := p25 4, finish := p25 9, path := [(p25 4), (p25 9), (p25 5), (p25 10), (p25 14), (p25 13), (p25 8), (p25 3)] },
  { start := p25 9, finish := p25 5, path := [(p25 9), (p25 5), (p25 10), (p25 14), (p25 13), (p25 8), (p25 3), (p25 4)] },
  { start := p25 5, finish := p25 10, path := [(p25 5), (p25 10), (p25 14), (p25 13), (p25 8), (p25 3), (p25 4), (p25 9)] },
  { start := p25 10, finish := p25 14, path := [(p25 10), (p25 14), (p25 13), (p25 8), (p25 3), (p25 4), (p25 9), (p25 5)] },
  { start := p25 14, finish := p25 13, path := [(p25 14), (p25 13), (p25 8), (p25 3), (p25 4), (p25 9), (p25 5), (p25 10)] },
  { start := p25 13, finish := p25 8, path := [(p25 13), (p25 8), (p25 3), (p25 4), (p25 9), (p25 5), (p25 10), (p25 14)] },
  { start := p25 8, finish := p25 3, path := [(p25 8), (p25 3), (p25 4), (p25 9), (p25 5), (p25 10), (p25 14), (p25 13)] },
  { start := p25 8, finish := p25 13, path := [(p25 8), (p25 13), (p25 14), (p25 10), (p25 5), (p25 9), (p25 4), (p25 3)] },
  { start := p25 13, finish := p25 14, path := [(p25 13), (p25 14), (p25 10), (p25 5), (p25 9), (p25 4), (p25 3), (p25 8)] },
  { start := p25 14, finish := p25 10, path := [(p25 14), (p25 10), (p25 5), (p25 9), (p25 4), (p25 3), (p25 8), (p25 13)] },
  { start := p25 10, finish := p25 5, path := [(p25 10), (p25 5), (p25 9), (p25 4), (p25 3), (p25 8), (p25 13), (p25 14)] },
  { start := p25 5, finish := p25 9, path := [(p25 5), (p25 9), (p25 4), (p25 3), (p25 8), (p25 13), (p25 14), (p25 10)] },
  { start := p25 9, finish := p25 4, path := [(p25 9), (p25 4), (p25 3), (p25 8), (p25 13), (p25 14), (p25 10), (p25 5)] },
  { start := p25 4, finish := p25 3, path := [(p25 4), (p25 3), (p25 8), (p25 13), (p25 14), (p25 10), (p25 5), (p25 9)] },
  { start := p25 3, finish := p25 8, path := [(p25 3), (p25 8), (p25 13), (p25 14), (p25 10), (p25 5), (p25 9), (p25 4)] },
  { start := p25 8, finish := p25 5, path := [(p25 8), (p25 5), (p25 10), (p25 13), (p25 14), (p25 9), (p25 4), (p25 3)] },
  { start := p25 10, finish := p25 13, path := [(p25 10), (p25 13), (p25 14), (p25 9), (p25 4), (p25 3), (p25 8), (p25 5)] },
  { start := p25 14, finish := p25 9, path := [(p25 14), (p25 9), (p25 4), (p25 3), (p25 8), (p25 5), (p25 10), (p25 13)] },
  { start := p25 9, finish := p25 14, path := [(p25 9), (p25 14), (p25 13), (p25 10), (p25 5), (p25 8), (p25 3), (p25 4)] },
  { start := p25 13, finish := p25 10, path := [(p25 13), (p25 10), (p25 5), (p25 8), (p25 3), (p25 4), (p25 9), (p25 14)] },
  { start := p25 5, finish := p25 8, path := [(p25 5), (p25 8), (p25 3), (p25 4), (p25 9), (p25 14), (p25 13), (p25 10)] },
  { start := p25 4, finish := p25 14, path := [(p25 4), (p25 14), (p25 10), (p25 5), (p25 9), (p25 8), (p25 13), (p25 3)] },
  { start := p25 9, finish := p25 8, path := [(p25 9), (p25 8), (p25 13), (p25 3), (p25 4), (p25 14), (p25 10), (p25 5)] },
  { start := p25 13, finish := p25 3, path := [(p25 13), (p25 3), (p25 4), (p25 14), (p25 10), (p25 5), (p25 9), (p25 8)] },
  { start := p25 8, finish := p25 9, path := [(p25 8), (p25 9), (p25 5), (p25 10), (p25 14), (p25 4), (p25 3), (p25 13)] },
  { start := p25 14, finish := p25 4, path := [(p25 14), (p25 4), (p25 3), (p25 13), (p25 8), (p25 9), (p25 5), (p25 10)] },
  { start := p25 3, finish := p25 13, path := [(p25 3), (p25 13), (p25 8), (p25 9), (p25 5), (p25 10), (p25 14), (p25 4)] },
]
def pairFiveCycle332 : List PairFiveEntry := [
  { start := p25 13, finish := p25 3, path := [(p25 13), (p25 3), (p25 1), (p25 11), (p25 10), (p25 5), (p25 8)] },
  { start := p25 3, finish := p25 1, path := [(p25 3), (p25 1), (p25 11), (p25 10), (p25 5), (p25 8), (p25 13)] },
  { start := p25 1, finish := p25 11, path := [(p25 1), (p25 11), (p25 10), (p25 5), (p25 8), (p25 13), (p25 3)] },
  { start := p25 11, finish := p25 10, path := [(p25 11), (p25 10), (p25 5), (p25 8), (p25 13), (p25 3), (p25 1)] },
  { start := p25 10, finish := p25 5, path := [(p25 10), (p25 5), (p25 8), (p25 13), (p25 3), (p25 1), (p25 11)] },
  { start := p25 5, finish := p25 8, path := [(p25 5), (p25 8), (p25 13), (p25 3), (p25 1), (p25 11), (p25 10)] },
  { start := p25 8, finish := p25 13, path := [(p25 8), (p25 13), (p25 3), (p25 1), (p25 11), (p25 10), (p25 5)] },
  { start := p25 8, finish := p25 5, path := [(p25 8), (p25 5), (p25 10), (p25 11), (p25 1), (p25 3), (p25 13)] },
  { start := p25 5, finish := p25 10, path := [(p25 5), (p25 10), (p25 11), (p25 1), (p25 3), (p25 13), (p25 8)] },
  { start := p25 10, finish := p25 11, path := [(p25 10), (p25 11), (p25 1), (p25 3), (p25 13), (p25 8), (p25 5)] },
  { start := p25 11, finish := p25 1, path := [(p25 11), (p25 1), (p25 3), (p25 13), (p25 8), (p25 5), (p25 10)] },
  { start := p25 1, finish := p25 3, path := [(p25 1), (p25 3), (p25 13), (p25 8), (p25 5), (p25 10), (p25 11)] },
  { start := p25 3, finish := p25 13, path := [(p25 3), (p25 13), (p25 8), (p25 5), (p25 10), (p25 11), (p25 1)] },
  { start := p25 13, finish := p25 8, path := [(p25 13), (p25 8), (p25 5), (p25 10), (p25 11), (p25 1), (p25 3)] },
  { start := p25 13, finish := p25 10, path := [(p25 13), (p25 10), (p25 5), (p25 8), (p25 3), (p25 1), (p25 11)] },
  { start := p25 8, finish := p25 3, path := [(p25 8), (p25 3), (p25 1), (p25 11), (p25 13), (p25 10), (p25 5)] },
  { start := p25 11, finish := p25 13, path := [(p25 11), (p25 13), (p25 10), (p25 5), (p25 8), (p25 3), (p25 1)] },
  { start := p25 3, finish := p25 8, path := [(p25 3), (p25 8), (p25 5), (p25 10), (p25 13), (p25 11), (p25 1)] },
  { start := p25 10, finish := p25 13, path := [(p25 10), (p25 13), (p25 11), (p25 1), (p25 3), (p25 8), (p25 5)] },
  { start := p25 13, finish := p25 11, path := [(p25 13), (p25 11), (p25 1), (p25 3), (p25 8), (p25 5), (p25 10)] },
]
def pairFiveCycle333 : List PairFiveEntry := [
  { start := p25 5, finish := p25 10, path := [(p25 5), (p25 10), (p25 11), (p25 1), (p25 2), (p25 7)] },
  { start := p25 10, finish := p25 11, path := [(p25 10), (p25 11), (p25 1), (p25 2), (p25 7), (p25 5)] },
  { start := p25 11, finish := p25 1, path := [(p25 11), (p25 1), (p25 2), (p25 7), (p25 5), (p25 10)] },
  { start := p25 1, finish := p25 2, path := [(p25 1), (p25 2), (p25 7), (p25 5), (p25 10), (p25 11)] },
  { start := p25 2, finish := p25 7, path := [(p25 2), (p25 7), (p25 5), (p25 10), (p25 11), (p25 1)] },
  { start := p25 7, finish := p25 5, path := [(p25 7), (p25 5), (p25 10), (p25 11), (p25 1), (p25 2)] },
  { start := p25 7, finish := p25 2, path := [(p25 7), (p25 2), (p25 1), (p25 11), (p25 10), (p25 5)] },
  { start := p25 2, finish := p25 1, path := [(p25 2), (p25 1), (p25 11), (p25 10), (p25 5), (p25 7)] },
  { start := p25 1, finish := p25 11, path := [(p25 1), (p25 11), (p25 10), (p25 5), (p25 7), (p25 2)] },
  { start := p25 11, finish := p25 10, path := [(p25 11), (p25 10), (p25 5), (p25 7), (p25 2), (p25 1)] },
  { start := p25 10, finish := p25 5, path := [(p25 10), (p25 5), (p25 7), (p25 2), (p25 1), (p25 11)] },
  { start := p25 5, finish := p25 7, path := [(p25 5), (p25 7), (p25 2), (p25 1), (p25 11), (p25 10)] },
]
def pairFiveCycle342 : List PairFiveEntry := [
  { start := p25 14, finish := p25 4, path := [(p25 14), (p25 4), (p25 1), (p25 3), (p25 8), (p25 9), (p25 5), (p25 10), (p25 11), (p25 13)] },
  { start := p25 4, finish := p25 1, path := [(p25 4), (p25 1), (p25 3), (p25 8), (p25 9), (p25 5), (p25 10), (p25 11), (p25 13), (p25 14)] },
  { start := p25 1, finish := p25 3, path := [(p25 1), (p25 3), (p25 8), (p25 9), (p25 5), (p25 10), (p25 11), (p25 13), (p25 14), (p25 4)] },
  { start := p25 3, finish := p25 8, path := [(p25 3), (p25 8), (p25 9), (p25 5), (p25 10), (p25 11), (p25 13), (p25 14), (p25 4), (p25 1)] },
  { start := p25 8, finish := p25 9, path := [(p25 8), (p25 9), (p25 5), (p25 10), (p25 11), (p25 13), (p25 14), (p25 4), (p25 1), (p25 3)] },
  { start := p25 9, finish := p25 5, path := [(p25 9), (p25 5), (p25 10), (p25 11), (p25 13), (p25 14), (p25 4), (p25 1), (p25 3), (p25 8)] },
  { start := p25 5, finish := p25 10, path := [(p25 5), (p25 10), (p25 11), (p25 13), (p25 14), (p25 4), (p25 1), (p25 3), (p25 8), (p25 9)] },
  { start := p25 10, finish := p25 11, path := [(p25 10), (p25 11), (p25 13), (p25 14), (p25 4), (p25 1), (p25 3), (p25 8), (p25 9), (p25 5)] },
  { start := p25 11, finish := p25 13, path := [(p25 11), (p25 13), (p25 14), (p25 4), (p25 1), (p25 3), (p25 8), (p25 9), (p25 5), (p25 10)] },
  { start := p25 13, finish := p25 14, path := [(p25 13), (p25 14), (p25 4), (p25 1), (p25 3), (p25 8), (p25 9), (p25 5), (p25 10), (p25 11)] },
  { start := p25 13, finish := p25 11, path := [(p25 13), (p25 11), (p25 10), (p25 5), (p25 9), (p25 8), (p25 3), (p25 1), (p25 4), (p25 14)] },
  { start := p25 11, finish := p25 10, path := [(p25 11), (p25 10), (p25 5), (p25 9), (p25 8), (p25 3), (p25 1), (p25 4), (p25 14), (p25 13)] },
  { start := p25 10, finish := p25 5, path := [(p25 10), (p25 5), (p25 9), (p25 8), (p25 3), (p25 1), (p25 4), (p25 14), (p25 13), (p25 11)] },
  { start := p25 5, finish := p25 9, path := [(p25 5), (p25 9), (p25 8), (p25 3), (p25 1), (p25 4), (p25 14), (p25 13), (p25 11), (p25 10)] },
  { start := p25 9, finish := p25 8, path := [(p25 9), (p25 8), (p25 3), (p25 1), (p25 4), (p25 14), (p25 13), (p25 11), (p25 10), (p25 5)] },
  { start := p25 8, finish := p25 3, path := [(p25 8), (p25 3), (p25 1), (p25 4), (p25 14), (p25 13), (p25 11), (p25 10), (p25 5), (p25 9)] },
  { start := p25 3, finish := p25 1, path := [(p25 3), (p25 1), (p25 4), (p25 14), (p25 13), (p25 11), (p25 10), (p25 5), (p25 9), (p25 8)] },
  { start := p25 1, finish := p25 4, path := [(p25 1), (p25 4), (p25 14), (p25 13), (p25 11), (p25 10), (p25 5), (p25 9), (p25 8), (p25 3)] },
  { start := p25 4, finish := p25 14, path := [(p25 4), (p25 14), (p25 13), (p25 11), (p25 10), (p25 5), (p25 9), (p25 8), (p25 3), (p25 1)] },
  { start := p25 14, finish := p25 13, path := [(p25 14), (p25 13), (p25 11), (p25 10), (p25 5), (p25 9), (p25 8), (p25 3), (p25 1), (p25 4)] },
  { start := p25 13, finish := p25 3, path := [(p25 13), (p25 3), (p25 1), (p25 4), (p25 9), (p25 8), (p25 5), (p25 10), (p25 11), (p25 14)] },
  { start := p25 4, finish := p25 9, path := [(p25 4), (p25 9), (p25 8), (p25 5), (p25 10), (p25 11), (p25 14), (p25 13), (p25 3), (p25 1)] },
  { start := p25 8, finish := p25 5, path := [(p25 8), (p25 5), (p25 10), (p25 11), (p25 14), (p25 13), (p25 3), (p25 1), (p25 4), (p25 9)] },
  { start := p25 11, finish := p25 14, path := [(p25 11), (p25 14), (p25 13), (p25 3), (p25 1), (p25 4), (p25 9), (p25 8), (p25 5), (p25 10)] },
  { start := p25 14, finish := p25 11, path := [(p25 14), (p25 11), (p25 10), (p25 5), (p25 8), (p25 9), (p25 4), (p25 1), (p25 3), (p25 13)] },
  { start := p25 5, finish := p25 8, path := [(p25 5), (p25 8), (p25 9), (p25 4), (p25 1), (p25 3), (p25 13), (p25 14), (p25 11), (p25 10)] },
  { start := p25 9, finish := p25 4, path := [(p25 9), (p25 4), (p25 1), (p25 3), (p25 13), (p25 14), (p25 11), (p25 10), (p25 5), (p25 8)] },
  { start := p25 3, finish := p25 13, path := [(p25 3), (p25 13), (p25 14), (p25 11), (p25 10), (p25 5), (p25 8), (p25 9), (p25 4), (p25 1)] },
  { start := p25 14, finish := p25 9, path := [(p25 14), (p25 9), (p25 5), (p25 8), (p25 3), (p25 4), (p25 1), (p25 11), (p25 10), (p25 13)] },
  { start := p25 3, finish := p25 4, path := [(p25 3), (p25 4), (p25 1), (p25 11), (p25 10), (p25 13), (p25 14), (p25 9), (p25 5), (p25 8)] },
  { start := p25 1, finish := p25 11, path := [(p25 1), (p25 11), (p25 10), (p25 13), (p25 14), (p25 9), (p25 5), (p25 8), (p25 3), (p25 4)] },
  { start := p25 10, finish := p25 13, path := [(p25 10), (p25 13), (p25 14), (p25 9), (p25 5), (p25 8), (p25 3), (p25 4), (p25 1), (p25 11)] },
  { start := p25 13, finish := p25 10, path := [(p25 13), (p25 10), (p25 11), (p25 1), (p25 4), (p25 3), (p25 8), (p25 5), (p25 9), (p25 14)] },
  { start := p25 11, finish := p25 1, path := [(p25 11), (p25 1), (p25 4), (p25 3), (p25 8), (p25 5), (p25 9), (p25 14), (p25 13), (p25 10)] },
  { start := p25 4, finish := p25 3, path := [(p25 4), (p25 3), (p25 8), (p25 5), (p25 9), (p25 14), (p25 13), (p25 10), (p25 11), (p25 1)] },
  { start := p25 9, finish := p25 14, path := [(p25 9), (p25 14), (p25 13), (p25 10), (p25 11), (p25 1), (p25 4), (p25 3), (p25 8), (p25 5)] },
  { start := p25 13, finish := p25 8, path := [(p25 13), (p25 8), (p25 5), (p25 9), (p25 4), (p25 3), (p25 1), (p25 11), (p25 10), (p25 14)] },
  { start := p25 10, finish := p25 14, path := [(p25 10), (p25 14), (p25 13), (p25 8), (p25 5), (p25 9), (p25 4), (p25 3), (p25 1), (p25 11)] },
  { start := p25 14, finish := p25 10, path := [(p25 14), (p25 10), (p25 11), (p25 1), (p25 3), (p25 4), (p25 9), (p25 5), (p25 8), (p25 13)] },
  { start := p25 8, finish := p25 13, path := [(p25 8), (p25 13), (p25 14), (p25 10), (p25 11), (p25 1), (p25 3), (p25 4), (p25 9), (p25 5)] },
]
def pairFiveCycle343 : List PairFiveEntry := [
  { start := p25 7, finish := p25 5, path := [(p25 7), (p25 5), (p25 10), (p25 11), (p25 1), (p25 2), (p25 3), (p25 13), (p25 8)] },
  { start := p25 5, finish := p25 10, path := [(p25 5), (p25 10), (p25 11), (p25 1), (p25 2), (p25 3), (p25 13), (p25 8), (p25 7)] },
  { start := p25 10, finish := p25 11, path := [(p25 10), (p25 11), (p25 1), (p25 2), (p25 3), (p25 13), (p25 8), (p25 7), (p25 5)] },
  { start := p25 11, finish := p25 1, path := [(p25 11), (p25 1), (p25 2), (p25 3), (p25 13), (p25 8), (p25 7), (p25 5), (p25 10)] },
  { start := p25 1, finish := p25 2, path := [(p25 1), (p25 2), (p25 3), (p25 13), (p25 8), (p25 7), (p25 5), (p25 10), (p25 11)] },
  { start := p25 2, finish := p25 3, path := [(p25 2), (p25 3), (p25 13), (p25 8), (p25 7), (p25 5), (p25 10), (p25 11), (p25 1)] },
  { start := p25 3, finish := p25 13, path := [(p25 3), (p25 13), (p25 8), (p25 7), (p25 5), (p25 10), (p25 11), (p25 1), (p25 2)] },
  { start := p25 13, finish := p25 8, path := [(p25 13), (p25 8), (p25 7), (p25 5), (p25 10), (p25 11), (p25 1), (p25 2), (p25 3)] },
  { start := p25 8, finish := p25 7, path := [(p25 8), (p25 7), (p25 5), (p25 10), (p25 11), (p25 1), (p25 2), (p25 3), (p25 13)] },
  { start := p25 8, finish := p25 13, path := [(p25 8), (p25 13), (p25 3), (p25 2), (p25 1), (p25 11), (p25 10), (p25 5), (p25 7)] },
  { start := p25 13, finish := p25 3, path := [(p25 13), (p25 3), (p25 2), (p25 1), (p25 11), (p25 10), (p25 5), (p25 7), (p25 8)] },
  { start := p25 3, finish := p25 2, path := [(p25 3), (p25 2), (p25 1), (p25 11), (p25 10), (p25 5), (p25 7), (p25 8), (p25 13)] },
  { start := p25 2, finish := p25 1, path := [(p25 2), (p25 1), (p25 11), (p25 10), (p25 5), (p25 7), (p25 8), (p25 13), (p25 3)] },
  { start := p25 1, finish := p25 11, path := [(p25 1), (p25 11), (p25 10), (p25 5), (p25 7), (p25 8), (p25 13), (p25 3), (p25 2)] },
  { start := p25 11, finish := p25 10, path := [(p25 11), (p25 10), (p25 5), (p25 7), (p25 8), (p25 13), (p25 3), (p25 2), (p25 1)] },
  { start := p25 10, finish := p25 5, path := [(p25 10), (p25 5), (p25 7), (p25 8), (p25 13), (p25 3), (p25 2), (p25 1), (p25 11)] },
  { start := p25 5, finish := p25 7, path := [(p25 5), (p25 7), (p25 8), (p25 13), (p25 3), (p25 2), (p25 1), (p25 11), (p25 10)] },
  { start := p25 7, finish := p25 8, path := [(p25 7), (p25 8), (p25 13), (p25 3), (p25 2), (p25 1), (p25 11), (p25 10), (p25 5)] },
  { start := p25 7, finish := p25 2, path := [(p25 7), (p25 2), (p25 1), (p25 3), (p25 8), (p25 13), (p25 11), (p25 10), (p25 5)] },
  { start := p25 1, finish := p25 3, path := [(p25 1), (p25 3), (p25 8), (p25 13), (p25 11), (p25 10), (p25 5), (p25 7), (p25 2)] },
  { start := p25 3, finish := p25 8, path := [(p25 3), (p25 8), (p25 13), (p25 11), (p25 10), (p25 5), (p25 7), (p25 2), (p25 1)] },
  { start := p25 13, finish := p25 11, path := [(p25 13), (p25 11), (p25 10), (p25 5), (p25 7), (p25 2), (p25 1), (p25 3), (p25 8)] },
  { start := p25 8, finish := p25 3, path := [(p25 8), (p25 3), (p25 1), (p25 2), (p25 7), (p25 5), (p25 10), (p25 11), (p25 13)] },
  { start := p25 3, finish := p25 1, path := [(p25 3), (p25 1), (p25 2), (p25 7), (p25 5), (p25 10), (p25 11), (p25 13), (p25 8)] },
  { start := p25 2, finish := p25 7, path := [(p25 2), (p25 7), (p25 5), (p25 10), (p25 11), (p25 13), (p25 8), (p25 3), (p25 1)] },
  { start := p25 11, finish := p25 13, path := [(p25 11), (p25 13), (p25 8), (p25 3), (p25 1), (p25 2), (p25 7), (p25 5), (p25 10)] },
  { start := p25 5, finish := p25 8, path := [(p25 5), (p25 8), (p25 3), (p25 13), (p25 10), (p25 11), (p25 1), (p25 2), (p25 7)] },
  { start := p25 13, finish := p25 10, path := [(p25 13), (p25 10), (p25 11), (p25 1), (p25 2), (p25 7), (p25 5), (p25 8), (p25 3)] },
  { start := p25 8, finish := p25 5, path := [(p25 8), (p25 5), (p25 7), (p25 2), (p25 1), (p25 11), (p25 10), (p25 13), (p25 3)] },
  { start := p25 10, finish := p25 13, path := [(p25 10), (p25 13), (p25 3), (p25 8), (p25 5), (p25 7), (p25 2), (p25 1), (p25 11)] },
]
def pairFiveCycle443 : List PairFiveEntry := [
  { start := p25 17, finish := p25 7, path := [(p25 17), (p25 7), (p25 5), (p25 10), (p25 11), (p25 1), (p25 2), (p25 4), (p25 14), (p25 9), (p25 19), (p25 16), (p25 15)] },
  { start := p25 7, finish := p25 5, path := [(p25 7), (p25 5), (p25 10), (p25 11), (p25 1), (p25 2), (p25 4), (p25 14), (p25 9), (p25 19), (p25 16), (p25 15), (p25 17)] },
  { start := p25 5, finish := p25 10, path := [(p25 5), (p25 10), (p25 11), (p25 1), (p25 2), (p25 4), (p25 14), (p25 9), (p25 19), (p25 16), (p25 15), (p25 17), (p25 7)] },
  { start := p25 10, finish := p25 11, path := [(p25 10), (p25 11), (p25 1), (p25 2), (p25 4), (p25 14), (p25 9), (p25 19), (p25 16), (p25 15), (p25 17), (p25 7), (p25 5)] },
  { start := p25 11, finish := p25 1, path := [(p25 11), (p25 1), (p25 2), (p25 4), (p25 14), (p25 9), (p25 19), (p25 16), (p25 15), (p25 17), (p25 7), (p25 5), (p25 10)] },
  { start := p25 1, finish := p25 2, path := [(p25 1), (p25 2), (p25 4), (p25 14), (p25 9), (p25 19), (p25 16), (p25 15), (p25 17), (p25 7), (p25 5), (p25 10), (p25 11)] },
  { start := p25 2, finish := p25 4, path := [(p25 2), (p25 4), (p25 14), (p25 9), (p25 19), (p25 16), (p25 15), (p25 17), (p25 7), (p25 5), (p25 10), (p25 11), (p25 1)] },
  { start := p25 4, finish := p25 14, path := [(p25 4), (p25 14), (p25 9), (p25 19), (p25 16), (p25 15), (p25 17), (p25 7), (p25 5), (p25 10), (p25 11), (p25 1), (p25 2)] },
  { start := p25 14, finish := p25 9, path := [(p25 14), (p25 9), (p25 19), (p25 16), (p25 15), (p25 17), (p25 7), (p25 5), (p25 10), (p25 11), (p25 1), (p25 2), (p25 4)] },
  { start := p25 9, finish := p25 19, path := [(p25 9), (p25 19), (p25 16), (p25 15), (p25 17), (p25 7), (p25 5), (p25 10), (p25 11), (p25 1), (p25 2), (p25 4), (p25 14)] },
  { start := p25 19, finish := p25 16, path := [(p25 19), (p25 16), (p25 15), (p25 17), (p25 7), (p25 5), (p25 10), (p25 11), (p25 1), (p25 2), (p25 4), (p25 14), (p25 9)] },
  { start := p25 16, finish := p25 15, path := [(p25 16), (p25 15), (p25 17), (p25 7), (p25 5), (p25 10), (p25 11), (p25 1), (p25 2), (p25 4), (p25 14), (p25 9), (p25 19)] },
  { start := p25 15, finish := p25 17, path := [(p25 15), (p25 17), (p25 7), (p25 5), (p25 10), (p25 11), (p25 1), (p25 2), (p25 4), (p25 14), (p25 9), (p25 19), (p25 16)] },
  { start := p25 15, finish := p25 16, path := [(p25 15), (p25 16), (p25 19), (p25 9), (p25 14), (p25 4), (p25 2), (p25 1), (p25 11), (p25 10), (p25 5), (p25 7), (p25 17)] },
  { start := p25 16, finish := p25 19, path := [(p25 16), (p25 19), (p25 9), (p25 14), (p25 4), (p25 2), (p25 1), (p25 11), (p25 10), (p25 5), (p25 7), (p25 17), (p25 15)] },
  { start := p25 19, finish := p25 9, path := [(p25 19), (p25 9), (p25 14), (p25 4), (p25 2), (p25 1), (p25 11), (p25 10), (p25 5), (p25 7), (p25 17), (p25 15), (p25 16)] },
  { start := p25 9, finish := p25 14, path := [(p25 9), (p25 14), (p25 4), (p25 2), (p25 1), (p25 11), (p25 10), (p25 5), (p25 7), (p25 17), (p25 15), (p25 16), (p25 19)] },
  { start := p25 14, finish := p25 4, path := [(p25 14), (p25 4), (p25 2), (p25 1), (p25 11), (p25 10), (p25 5), (p25 7), (p25 17), (p25 15), (p25 16), (p25 19), (p25 9)] },
  { start := p25 4, finish := p25 2, path := [(p25 4), (p25 2), (p25 1), (p25 11), (p25 10), (p25 5), (p25 7), (p25 17), (p25 15), (p25 16), (p25 19), (p25 9), (p25 14)] },
  { start := p25 2, finish := p25 1, path := [(p25 2), (p25 1), (p25 11), (p25 10), (p25 5), (p25 7), (p25 17), (p25 15), (p25 16), (p25 19), (p25 9), (p25 14), (p25 4)] },
  { start := p25 1, finish := p25 11, path := [(p25 1), (p25 11), (p25 10), (p25 5), (p25 7), (p25 17), (p25 15), (p25 16), (p25 19), (p25 9), (p25 14), (p25 4), (p25 2)] },
  { start := p25 11, finish := p25 10, path := [(p25 11), (p25 10), (p25 5), (p25 7), (p25 17), (p25 15), (p25 16), (p25 19), (p25 9), (p25 14), (p25 4), (p25 2), (p25 1)] },
  { start := p25 10, finish := p25 5, path := [(p25 10), (p25 5), (p25 7), (p25 17), (p25 15), (p25 16), (p25 19), (p25 9), (p25 14), (p25 4), (p25 2), (p25 1), (p25 11)] },
  { start := p25 5, finish := p25 7, path := [(p25 5), (p25 7), (p25 17), (p25 15), (p25 16), (p25 19), (p25 9), (p25 14), (p25 4), (p25 2), (p25 1), (p25 11), (p25 10)] },
  { start := p25 7, finish := p25 17, path := [(p25 7), (p25 17), (p25 15), (p25 16), (p25 19), (p25 9), (p25 14), (p25 4), (p25 2), (p25 1), (p25 11), (p25 10), (p25 5)] },
  { start := p25 17, finish := p25 15, path := [(p25 17), (p25 15), (p25 16), (p25 19), (p25 9), (p25 14), (p25 4), (p25 2), (p25 1), (p25 11), (p25 10), (p25 5), (p25 7)] },
  { start := p25 14, finish := p25 11, path := [(p25 14), (p25 11), (p25 1), (p25 2), (p25 7), (p25 5), (p25 10), (p25 15), (p25 17), (p25 16), (p25 19), (p25 9), (p25 4)] },
  { start := p25 2, finish := p25 7, path := [(p25 2), (p25 7), (p25 5), (p25 10), (p25 15), (p25 17), (p25 16), (p25 19), (p25 9), (p25 4), (p25 14), (p25 11), (p25 1)] },
  { start := p25 10, finish := p25 15, path := [(p25 10), (p25 15), (p25 17), (p25 16), (p25 19), (p25 9), (p25 4), (p25 14), (p25 11), (p25 1), (p25 2), (p25 7), (p25 5)] },
  { start := p25 17, finish := p25 16, path := [(p25 17), (p25 16), (p25 19), (p25 9), (p25 4), (p25 14), (p25 11), (p25 1), (p25 2), (p25 7), (p25 5), (p25 10), (p25 15)] },
  { start := p25 9, finish := p25 4, path := [(p25 9), (p25 4), (p25 14), (p25 11), (p25 1), (p25 2), (p25 7), (p25 5), (p25 10), (p25 15), (p25 17), (p25 16), (p25 19)] },
  { start := p25 4, finish := p25 9, path := [(p25 4), (p25 9), (p25 19), (p25 16), (p25 17), (p25 15), (p25 10), (p25 5), (p25 7), (p25 2), (p25 1), (p25 11), (p25 14)] },
  { start := p25 16, finish := p25 17, path := [(p25 16), (p25 17), (p25 15), (p25 10), (p25 5), (p25 7), (p25 2), (p25 1), (p25 11), (p25 14), (p25 4), (p25 9), (p25 19)] },
  { start := p25 15, finish := p25 10, path := [(p25 15), (p25 10), (p25 5), (p25 7), (p25 2), (p25 1), (p25 11), (p25 14), (p25 4), (p25 9), (p25 19), (p25 16), (p25 17)] },
  { start := p25 7, finish := p25 2, path := [(p25 7), (p25 2), (p25 1), (p25 11), (p25 14), (p25 4), (p25 9), (p25 19), (p25 16), (p25 17), (p25 15), (p25 10), (p25 5)] },
  { start := p25 11, finish := p25 14, path := [(p25 11), (p25 14), (p25 4), (p25 9), (p25 19), (p25 16), (p25 17), (p25 15), (p25 10), (p25 5), (p25 7), (p25 2), (p25 1)] },
  { start := p25 16, finish := p25 11, path := [(p25 16), (p25 11), (p25 10), (p25 5), (p25 7), (p25 2), (p25 1), (p25 4), (p25 9), (p25 14), (p25 19), (p25 17), (p25 15)] },
  { start := p25 1, finish := p25 4, path := [(p25 1), (p25 4), (p25 9), (p25 14), (p25 19), (p25 17), (p25 15), (p25 16), (p25 11), (p25 10), (p25 5), (p25 7), (p25 2)] },
  { start := p25 14, finish := p25 19, path := [(p25 14), (p25 19), (p25 17), (p25 15), (p25 16), (p25 11), (p25 10), (p25 5), (p25 7), (p25 2), (p25 1), (p25 4), (p25 9)] },
  { start := p25 19, finish := p25 17, path := [(p25 19), (p25 17), (p25 15), (p25 16), (p25 11), (p25 10), (p25 5), (p25 7), (p25 2), (p25 1), (p25 4), (p25 9), (p25 14)] },
  { start := p25 17, finish := p25 19, path := [(p25 17), (p25 19), (p25 14), (p25 9), (p25 4), (p25 1), (p25 2), (p25 7), (p25 5), (p25 10), (p25 11), (p25 16), (p25 15)] },
  { start := p25 19, finish := p25 14, path := [(p25 19), (p25 14), (p25 9), (p25 4), (p25 1), (p25 2), (p25 7), (p25 5), (p25 10), (p25 11), (p25 16), (p25 15), (p25 17)] },
  { start := p25 4, finish := p25 1, path := [(p25 4), (p25 1), (p25 2), (p25 7), (p25 5), (p25 10), (p25 11), (p25 16), (p25 15), (p25 17), (p25 19), (p25 14), (p25 9)] },
  { start := p25 11, finish := p25 16, path := [(p25 11), (p25 16), (p25 15), (p25 17), (p25 19), (p25 14), (p25 9), (p25 4), (p25 1), (p25 2), (p25 7), (p25 5), (p25 10)] },
  { start := p25 9, finish := p25 7, path := [(p25 9), (p25 7), (p25 2), (p25 1), (p25 11), (p25 10), (p25 5), (p25 15), (p25 16), (p25 17), (p25 19), (p25 14), (p25 4)] },
  { start := p25 5, finish := p25 15, path := [(p25 5), (p25 15), (p25 16), (p25 17), (p25 19), (p25 14), (p25 4), (p25 9), (p25 7), (p25 2), (p25 1), (p25 11), (p25 10)] },
  { start := p25 15, finish := p25 5, path := [(p25 15), (p25 5), (p25 10), (p25 11), (p25 1), (p25 2), (p25 7), (p25 9), (p25 4), (p25 14), (p25 19), (p25 17), (p25 16)] },
  { start := p25 7, finish := p25 9, path := [(p25 7), (p25 9), (p25 4), (p25 14), (p25 19), (p25 17), (p25 16), (p25 15), (p25 5), (p25 10), (p25 11), (p25 1), (p25 2)] },
  { start := p25 17, finish := p25 2, path := [(p25 17), (p25 2), (p25 1), (p25 11), (p25 10), (p25 5), (p25 7), (p25 9), (p25 14), (p25 4), (p25 19), (p25 15), (p25 16)] },
  { start := p25 4, finish := p25 19, path := [(p25 4), (p25 19), (p25 15), (p25 16), (p25 17), (p25 2), (p25 1), (p25 11), (p25 10), (p25 5), (p25 7), (p25 9), (p25 14)] },
  { start := p25 19, finish := p25 15, path := [(p25 19), (p25 15), (p25 16), (p25 17), (p25 2), (p25 1), (p25 11), (p25 10), (p25 5), (p25 7), (p25 9), (p25 14), (p25 4)] },
  { start := p25 15, finish := p25 19, path := [(p25 15), (p25 19), (p25 4), (p25 14), (p25 9), (p25 7), (p25 5), (p25 10), (p25 11), (p25 1), (p25 2), (p25 17), (p25 16)] },
  { start := p25 19, finish := p25 4, path := [(p25 19), (p25 4), (p25 14), (p25 9), (p25 7), (p25 5), (p25 10), (p25 11), (p25 1), (p25 2), (p25 17), (p25 16), (p25 15)] },
  { start := p25 2, finish := p25 17, path := [(p25 2), (p25 17), (p25 16), (p25 15), (p25 19), (p25 4), (p25 14), (p25 9), (p25 7), (p25 5), (p25 10), (p25 11), (p25 1)] },
  { start := p25 14, finish := p25 10, path := [(p25 14), (p25 10), (p25 5), (p25 7), (p25 2), (p25 1), (p25 11), (p25 16), (p25 17), (p25 15), (p25 19), (p25 4), (p25 9)] },
  { start := p25 10, finish := p25 14, path := [(p25 10), (p25 14), (p25 9), (p25 4), (p25 19), (p25 15), (p25 17), (p25 16), (p25 11), (p25 1), (p25 2), (p25 7), (p25 5)] },
  { start := p25 5, finish := p25 9, path := [(p25 5), (p25 9), (p25 4), (p25 14), (p25 19), (p25 17), (p25 16), (p25 15), (p25 10), (p25 11), (p25 1), (p25 2), (p25 7)] },
  { start := p25 9, finish := p25 5, path := [(p25 9), (p25 5), (p25 7), (p25 2), (p25 1), (p25 11), (p25 10), (p25 15), (p25 16), (p25 17), (p25 19), (p25 14), (p25 4)] },
  { start := p25 1, finish := p25 16, path := [(p25 1), (p25 16), (p25 15), (p25 17), (p25 19), (p25 14), (p25 9), (p25 4), (p25 2), (p25 7), (p25 5), (p25 10), (p25 11)] },
  { start := p25 16, finish := p25 1, path := [(p25 16), (p25 1), (p25 11), (p25 10), (p25 5), (p25 7), (p25 2), (p25 4), (p25 9), (p25 14), (p25 19), (p25 17), (p25 15)] },
]
def pairFiveCycle444 : List PairFiveEntry := [
  { start := p25 13, finish := p25 11, path := [(p25 13), (p25 11), (p25 10), (p25 5), (p25 7), (p25 2), (p25 17), (p25 15), (p25 16), (p25 1), (p25 3), (p25 8)] },
  { start := p25 11, finish := p25 10, path := [(p25 11), (p25 10), (p25 5), (p25 7), (p25 2), (p25 17), (p25 15), (p25 16), (p25 1), (p25 3), (p25 8), (p25 13)] },
  { start := p25 10, finish := p25 5, path := [(p25 10), (p25 5), (p25 7), (p25 2), (p25 17), (p25 15), (p25 16), (p25 1), (p25 3), (p25 8), (p25 13), (p25 11)] },
  { start := p25 5, finish := p25 7, path := [(p25 5), (p25 7), (p25 2), (p25 17), (p25 15), (p25 16), (p25 1), (p25 3), (p25 8), (p25 13), (p25 11), (p25 10)] },
  { start := p25 7, finish := p25 2, path := [(p25 7), (p25 2), (p25 17), (p25 15), (p25 16), (p25 1), (p25 3), (p25 8), (p25 13), (p25 11), (p25 10), (p25 5)] },
  { start := p25 2, finish := p25 17, path := [(p25 2), (p25 17), (p25 15), (p25 16), (p25 1), (p25 3), (p25 8), (p25 13), (p25 11), (p25 10), (p25 5), (p25 7)] },
  { start := p25 17, finish := p25 15, path := [(p25 17), (p25 15), (p25 16), (p25 1), (p25 3), (p25 8), (p25 13), (p25 11), (p25 10), (p25 5), (p25 7), (p25 2)] },
  { start := p25 15, finish := p25 16, path := [(p25 15), (p25 16), (p25 1), (p25 3), (p25 8), (p25 13), (p25 11), (p25 10), (p25 5), (p25 7), (p25 2), (p25 17)] },
  { start := p25 16, finish := p25 1, path := [(p25 16), (p25 1), (p25 3), (p25 8), (p25 13), (p25 11), (p25 10), (p25 5), (p25 7), (p25 2), (p25 17), (p25 15)] },
  { start := p25 1, finish := p25 3, path := [(p25 1), (p25 3), (p25 8), (p25 13), (p25 11), (p25 10), (p25 5), (p25 7), (p25 2), (p25 17), (p25 15), (p25 16)] },
  { start := p25 3, finish := p25 8, path := [(p25 3), (p25 8), (p25 13), (p25 11), (p25 10), (p25 5), (p25 7), (p25 2), (p25 17), (p25 15), (p25 16), (p25 1)] },
  { start := p25 8, finish := p25 13, path := [(p25 8), (p25 13), (p25 11), (p25 10), (p25 5), (p25 7), (p25 2), (p25 17), (p25 15), (p25 16), (p25 1), (p25 3)] },
  { start := p25 8, finish := p25 3, path := [(p25 8), (p25 3), (p25 1), (p25 16), (p25 15), (p25 17), (p25 2), (p25 7), (p25 5), (p25 10), (p25 11), (p25 13)] },
  { start := p25 3, finish := p25 1, path := [(p25 3), (p25 1), (p25 16), (p25 15), (p25 17), (p25 2), (p25 7), (p25 5), (p25 10), (p25 11), (p25 13), (p25 8)] },
  { start := p25 1, finish := p25 16, path := [(p25 1), (p25 16), (p25 15), (p25 17), (p25 2), (p25 7), (p25 5), (p25 10), (p25 11), (p25 13), (p25 8), (p25 3)] },
  { start := p25 16, finish := p25 15, path := [(p25 16), (p25 15), (p25 17), (p25 2), (p25 7), (p25 5), (p25 10), (p25 11), (p25 13), (p25 8), (p25 3), (p25 1)] },
  { start := p25 15, finish := p25 17, path := [(p25 15), (p25 17), (p25 2), (p25 7), (p25 5), (p25 10), (p25 11), (p25 13), (p25 8), (p25 3), (p25 1), (p25 16)] },
  { start := p25 17, finish := p25 2, path := [(p25 17), (p25 2), (p25 7), (p25 5), (p25 10), (p25 11), (p25 13), (p25 8), (p25 3), (p25 1), (p25 16), (p25 15)] },
  { start := p25 2, finish := p25 7, path := [(p25 2), (p25 7), (p25 5), (p25 10), (p25 11), (p25 13), (p25 8), (p25 3), (p25 1), (p25 16), (p25 15), (p25 17)] },
  { start := p25 7, finish := p25 5, path := [(p25 7), (p25 5), (p25 10), (p25 11), (p25 13), (p25 8), (p25 3), (p25 1), (p25 16), (p25 15), (p25 17), (p25 2)] },
  { start := p25 5, finish := p25 10, path := [(p25 5), (p25 10), (p25 11), (p25 13), (p25 8), (p25 3), (p25 1), (p25 16), (p25 15), (p25 17), (p25 2), (p25 7)] },
  { start := p25 10, finish := p25 11, path := [(p25 10), (p25 11), (p25 13), (p25 8), (p25 3), (p25 1), (p25 16), (p25 15), (p25 17), (p25 2), (p25 7), (p25 5)] },
  { start := p25 11, finish := p25 13, path := [(p25 11), (p25 13), (p25 8), (p25 3), (p25 1), (p25 16), (p25 15), (p25 17), (p25 2), (p25 7), (p25 5), (p25 10)] },
  { start := p25 13, finish := p25 8, path := [(p25 13), (p25 8), (p25 3), (p25 1), (p25 16), (p25 15), (p25 17), (p25 2), (p25 7), (p25 5), (p25 10), (p25 11)] },
  { start := p25 17, finish := p25 7, path := [(p25 17), (p25 7), (p25 2), (p25 1), (p25 11), (p25 10), (p25 13), (p25 3), (p25 8), (p25 5), (p25 15), (p25 16)] },
  { start := p25 2, finish := p25 1, path := [(p25 2), (p25 1), (p25 11), (p25 10), (p25 13), (p25 3), (p25 8), (p25 5), (p25 15), (p25 16), (p25 17), (p25 7)] },
  { start := p25 1, finish := p25 11, path := [(p25 1), (p25 11), (p25 10), (p25 13), (p25 3), (p25 8), (p25 5), (p25 15), (p25 16), (p25 17), (p25 7), (p25 2)] },
  { start := p25 10, finish := p25 13, path := [(p25 10), (p25 13), (p25 3), (p25 8), (p25 5), (p25 15), (p25 16), (p25 17), (p25 7), (p25 2), (p25 1), (p25 11)] },
  { start := p25 13, finish := p25 3, path := [(p25 13), (p25 3), (p25 8), (p25 5), (p25 15), (p25 16), (p25 17), (p25 7), (p25 2), (p25 1), (p25 11), (p25 10)] },
  { start := p25 8, finish := p25 5, path := [(p25 8), (p25 5), (p25 15), (p25 16), (p25 17), (p25 7), (p25 2), (p25 1), (p25 11), (p25 10), (p25 13), (p25 3)] },
  { start := p25 5, finish := p25 15, path := [(p25 5), (p25 15), (p25 16), (p25 17), (p25 7), (p25 2), (p25 1), (p25 11), (p25 10), (p25 13), (p25 3), (p25 8)] },
  { start := p25 16, finish := p25 17, path := [(p25 16), (p25 17), (p25 7), (p25 2), (p25 1), (p25 11), (p25 10), (p25 13), (p25 3), (p25 8), (p25 5), (p25 15)] },
  { start := p25 15, finish := p25 5, path := [(p25 15), (p25 5), (p25 8), (p25 3), (p25 13), (p25 10), (p25 11), (p25 1), (p25 2), (p25 7), (p25 17), (p25 16)] },
  { start := p25 5, finish := p25 8, path := [(p25 5), (p25 8), (p25 3), (p25 13), (p25 10), (p25 11), (p25 1), (p25 2), (p25 7), (p25 17), (p25 16), (p25 15)] },
  { start := p25 3, finish := p25 13, path := [(p25 3), (p25 13), (p25 10), (p25 11), (p25 1), (p25 2), (p25 7), (p25 17), (p25 16), (p25 15), (p25 5), (p25 8)] },
  { start := p25 13, finish := p25 10, path := [(p25 13), (p25 10), (p25 11), (p25 1), (p25 2), (p25 7), (p25 17), (p25 16), (p25 15), (p25 5), (p25 8), (p25 3)] },
  { start := p25 11, finish := p25 1, path := [(p25 11), (p25 1), (p25 2), (p25 7), (p25 17), (p25 16), (p25 15), (p25 5), (p25 8), (p25 3), (p25 13), (p25 10)] },
  { start := p25 1, finish := p25 2, path := [(p25 1), (p25 2), (p25 7), (p25 17), (p25 16), (p25 15), (p25 5), (p25 8), (p25 3), (p25 13), (p25 10), (p25 11)] },
  { start := p25 7, finish := p25 17, path := [(p25 7), (p25 17), (p25 16), (p25 15), (p25 5), (p25 8), (p25 3), (p25 13), (p25 10), (p25 11), (p25 1), (p25 2)] },
  { start := p25 17, finish := p25 16, path := [(p25 17), (p25 16), (p25 15), (p25 5), (p25 8), (p25 3), (p25 13), (p25 10), (p25 11), (p25 1), (p25 2), (p25 7)] },
  { start := p25 8, finish := p25 7, path := [(p25 8), (p25 7), (p25 5), (p25 10), (p25 11), (p25 1), (p25 16), (p25 15), (p25 17), (p25 2), (p25 3), (p25 13)] },
  { start := p25 2, finish := p25 3, path := [(p25 2), (p25 3), (p25 13), (p25 8), (p25 7), (p25 5), (p25 10), (p25 11), (p25 1), (p25 16), (p25 15), (p25 17)] },
  { start := p25 3, finish := p25 2, path := [(p25 3), (p25 2), (p25 17), (p25 15), (p25 16), (p25 1), (p25 11), (p25 10), (p25 5), (p25 7), (p25 8), (p25 13)] },
  { start := p25 7, finish := p25 8, path := [(p25 7), (p25 8), (p25 13), (p25 3), (p25 2), (p25 17), (p25 15), (p25 16), (p25 1), (p25 11), (p25 10), (p25 5)] },
  { start := p25 16, finish := p25 11, path := [(p25 16), (p25 11), (p25 1), (p25 2), (p25 7), (p25 5), (p25 8), (p25 3), (p25 13), (p25 10), (p25 15), (p25 17)] },
  { start := p25 10, finish := p25 15, path := [(p25 10), (p25 15), (p25 17), (p25 16), (p25 11), (p25 1), (p25 2), (p25 7), (p25 5), (p25 8), (p25 3), (p25 13)] },
  { start := p25 15, finish := p25 10, path := [(p25 15), (p25 10), (p25 13), (p25 3), (p25 8), (p25 5), (p25 7), (p25 2), (p25 1), (p25 11), (p25 16), (p25 17)] },
  { start := p25 11, finish := p25 16, path := [(p25 11), (p25 16), (p25 17), (p25 15), (p25 10), (p25 13), (p25 3), (p25 8), (p25 5), (p25 7), (p25 2), (p25 1)] },
]
def pairFivePath331 : List PairFiveEntry := [
  { start := p25 3, finish := p25 4, path := [(p25 3), (p25 8), (p25 13), (p25 14), (p25 10), (p25 5), (p25 9), (p25 4)] },
  { start := p25 4, finish := p25 3, path := [(p25 4), (p25 9), (p25 5), (p25 10), (p25 14), (p25 13), (p25 8), (p25 3)] },
  { start := p25 5, finish := p25 10, path := [(p25 5), (p25 8), (p25 9), (p25 14), (p25 4), (p25 3), (p25 13), (p25 10)] },
  { start := p25 10, finish := p25 5, path := [(p25 10), (p25 13), (p25 3), (p25 4), (p25 14), (p25 9), (p25 8), (p25 5)] },
  { start := p25 3, finish := p25 5, path := [(p25 3), (p25 13), (p25 10), (p25 14), (p25 4), (p25 9), (p25 8), (p25 5)] },
  { start := p25 5, finish := p25 3, path := [(p25 5), (p25 8), (p25 9), (p25 4), (p25 14), (p25 10), (p25 13), (p25 3)] },
  { start := p25 4, finish := p25 5, path := [(p25 4), (p25 14), (p25 10), (p25 13), (p25 3), (p25 8), (p25 9), (p25 5)] },
  { start := p25 5, finish := p25 4, path := [(p25 5), (p25 9), (p25 8), (p25 3), (p25 13), (p25 10), (p25 14), (p25 4)] },
  { start := p25 3, finish := p25 10, path := [(p25 3), (p25 8), (p25 5), (p25 9), (p25 4), (p25 14), (p25 13), (p25 10)] },
  { start := p25 10, finish := p25 3, path := [(p25 10), (p25 13), (p25 14), (p25 4), (p25 9), (p25 5), (p25 8), (p25 3)] },
  { start := p25 4, finish := p25 10, path := [(p25 4), (p25 9), (p25 5), (p25 8), (p25 3), (p25 13), (p25 14), (p25 10)] },
  { start := p25 10, finish := p25 4, path := [(p25 10), (p25 14), (p25 13), (p25 3), (p25 8), (p25 5), (p25 9), (p25 4)] },
  { start := p25 3, finish := p25 8, path := [(p25 3), (p25 13), (p25 10), (p25 14), (p25 4), (p25 9), (p25 5), (p25 8)] },
  { start := p25 8, finish := p25 3, path := [(p25 8), (p25 5), (p25 9), (p25 4), (p25 14), (p25 10), (p25 13), (p25 3)] },
  { start := p25 4, finish := p25 9, path := [(p25 4), (p25 14), (p25 10), (p25 13), (p25 3), (p25 8), (p25 5), (p25 9)] },
  { start := p25 9, finish := p25 4, path := [(p25 9), (p25 5), (p25 8), (p25 3), (p25 13), (p25 10), (p25 14), (p25 4)] },
  { start := p25 3, finish := p25 13, path := [(p25 3), (p25 8), (p25 5), (p25 9), (p25 4), (p25 14), (p25 10), (p25 13)] },
  { start := p25 13, finish := p25 3, path := [(p25 13), (p25 10), (p25 14), (p25 4), (p25 9), (p25 5), (p25 8), (p25 3)] },
  { start := p25 4, finish := p25 14, path := [(p25 4), (p25 9), (p25 5), (p25 8), (p25 3), (p25 13), (p25 10), (p25 14)] },
  { start := p25 14, finish := p25 4, path := [(p25 14), (p25 10), (p25 13), (p25 3), (p25 8), (p25 5), (p25 9), (p25 4)] },
  { start := p25 5, finish := p25 8, path := [(p25 5), (p25 9), (p25 4), (p25 14), (p25 10), (p25 13), (p25 3), (p25 8)] },
  { start := p25 8, finish := p25 5, path := [(p25 8), (p25 3), (p25 13), (p25 10), (p25 14), (p25 4), (p25 9), (p25 5)] },
  { start := p25 10, finish := p25 13, path := [(p25 10), (p25 14), (p25 4), (p25 9), (p25 5), (p25 8), (p25 3), (p25 13)] },
  { start := p25 13, finish := p25 10, path := [(p25 13), (p25 3), (p25 8), (p25 5), (p25 9), (p25 4), (p25 14), (p25 10)] },
  { start := p25 5, finish := p25 9, path := [(p25 5), (p25 8), (p25 3), (p25 13), (p25 10), (p25 14), (p25 4), (p25 9)] },
  { start := p25 9, finish := p25 5, path := [(p25 9), (p25 4), (p25 14), (p25 10), (p25 13), (p25 3), (p25 8), (p25 5)] },
  { start := p25 10, finish := p25 14, path := [(p25 10), (p25 13), (p25 3), (p25 8), (p25 5), (p25 9), (p25 4), (p25 14)] },
  { start := p25 14, finish := p25 10, path := [(p25 14), (p25 4), (p25 9), (p25 5), (p25 8), (p25 3), (p25 13), (p25 10)] },
  { start := p25 3, finish := p25 9, path := [(p25 3), (p25 13), (p25 8), (p25 5), (p25 10), (p25 14), (p25 4), (p25 9)] },
  { start := p25 9, finish := p25 3, path := [(p25 9), (p25 4), (p25 14), (p25 10), (p25 5), (p25 8), (p25 13), (p25 3)] },
  { start := p25 4, finish := p25 8, path := [(p25 4), (p25 14), (p25 9), (p25 5), (p25 10), (p25 13), (p25 3), (p25 8)] },
  { start := p25 8, finish := p25 4, path := [(p25 8), (p25 3), (p25 13), (p25 10), (p25 5), (p25 9), (p25 14), (p25 4)] },
  { start := p25 3, finish := p25 14, path := [(p25 3), (p25 8), (p25 13), (p25 10), (p25 5), (p25 9), (p25 4), (p25 14)] },
  { start := p25 14, finish := p25 3, path := [(p25 14), (p25 4), (p25 9), (p25 5), (p25 10), (p25 13), (p25 8), (p25 3)] },
  { start := p25 4, finish := p25 13, path := [(p25 4), (p25 9), (p25 14), (p25 10), (p25 5), (p25 8), (p25 3), (p25 13)] },
  { start := p25 13, finish := p25 4, path := [(p25 13), (p25 3), (p25 8), (p25 5), (p25 10), (p25 14), (p25 9), (p25 4)] },
  { start := p25 5, finish := p25 13, path := [(p25 5), (p25 9), (p25 8), (p25 3), (p25 4), (p25 14), (p25 10), (p25 13)] },
  { start := p25 13, finish := p25 5, path := [(p25 13), (p25 10), (p25 14), (p25 4), (p25 3), (p25 8), (p25 9), (p25 5)] },
  { start := p25 10, finish := p25 8, path := [(p25 10), (p25 14), (p25 13), (p25 3), (p25 4), (p25 9), (p25 5), (p25 8)] },
  { start := p25 8, finish := p25 10, path := [(p25 8), (p25 5), (p25 9), (p25 4), (p25 3), (p25 13), (p25 14), (p25 10)] },
  { start := p25 5, finish := p25 14, path := [(p25 5), (p25 8), (p25 9), (p25 4), (p25 3), (p25 13), (p25 10), (p25 14)] },
  { start := p25 14, finish := p25 5, path := [(p25 14), (p25 10), (p25 13), (p25 3), (p25 4), (p25 9), (p25 8), (p25 5)] },
  { start := p25 10, finish := p25 9, path := [(p25 10), (p25 13), (p25 14), (p25 4), (p25 3), (p25 8), (p25 5), (p25 9)] },
  { start := p25 9, finish := p25 10, path := [(p25 9), (p25 5), (p25 8), (p25 3), (p25 4), (p25 14), (p25 13), (p25 10)] },
  { start := p25 8, finish := p25 9, path := [(p25 8), (p25 5), (p25 10), (p25 14), (p25 13), (p25 3), (p25 4), (p25 9)] },
  { start := p25 9, finish := p25 8, path := [(p25 9), (p25 4), (p25 3), (p25 13), (p25 14), (p25 10), (p25 5), (p25 8)] },
  { start := p25 13, finish := p25 14, path := [(p25 13), (p25 10), (p25 5), (p25 9), (p25 8), (p25 3), (p25 4), (p25 14)] },
  { start := p25 14, finish := p25 13, path := [(p25 14), (p25 4), (p25 3), (p25 8), (p25 9), (p25 5), (p25 10), (p25 13)] },
  { start := p25 8, finish := p25 13, path := [(p25 8), (p25 3), (p25 4), (p25 14), (p25 9), (p25 5), (p25 10), (p25 13)] },
  { start := p25 13, finish := p25 8, path := [(p25 13), (p25 10), (p25 5), (p25 9), (p25 14), (p25 4), (p25 3), (p25 8)] },
  { start := p25 9, finish := p25 14, path := [(p25 9), (p25 4), (p25 3), (p25 13), (p25 8), (p25 5), (p25 10), (p25 14)] },
  { start := p25 14, finish := p25 9, path := [(p25 14), (p25 10), (p25 5), (p25 8), (p25 13), (p25 3), (p25 4), (p25 9)] },
  { start := p25 8, finish := p25 14, path := [(p25 8), (p25 9), (p25 5), (p25 10), (p25 13), (p25 3), (p25 4), (p25 14)] },
  { start := p25 14, finish := p25 8, path := [(p25 14), (p25 4), (p25 3), (p25 13), (p25 10), (p25 5), (p25 9), (p25 8)] },
  { start := p25 9, finish := p25 13, path := [(p25 9), (p25 8), (p25 5), (p25 10), (p25 14), (p25 4), (p25 3), (p25 13)] },
  { start := p25 13, finish := p25 9, path := [(p25 13), (p25 3), (p25 4), (p25 14), (p25 10), (p25 5), (p25 8), (p25 9)] },
]
def pairFivePath332 : List PairFiveEntry := [
  { start := p25 1, finish := p25 3, path := [(p25 1), (p25 11), (p25 13), (p25 10), (p25 5), (p25 8), (p25 3)] },
  { start := p25 3, finish := p25 1, path := [(p25 3), (p25 8), (p25 5), (p25 10), (p25 13), (p25 11), (p25 1)] },
  { start := p25 5, finish := p25 10, path := [(p25 5), (p25 8), (p25 13), (p25 3), (p25 1), (p25 11), (p25 10)] },
  { start := p25 10, finish := p25 5, path := [(p25 10), (p25 11), (p25 1), (p25 3), (p25 13), (p25 8), (p25 5)] },
  { start := p25 5, finish := p25 8, path := [(p25 5), (p25 10), (p25 13), (p25 11), (p25 1), (p25 3), (p25 8)] },
  { start := p25 8, finish := p25 5, path := [(p25 8), (p25 3), (p25 1), (p25 11), (p25 13), (p25 10), (p25 5)] },
  { start := p25 1, finish := p25 11, path := [(p25 1), (p25 3), (p25 13), (p25 8), (p25 5), (p25 10), (p25 11)] },
  { start := p25 11, finish := p25 1, path := [(p25 11), (p25 10), (p25 5), (p25 8), (p25 13), (p25 3), (p25 1)] },
  { start := p25 1, finish := p25 5, path := [(p25 1), (p25 11), (p25 10), (p25 13), (p25 3), (p25 8), (p25 5)] },
  { start := p25 5, finish := p25 1, path := [(p25 5), (p25 8), (p25 3), (p25 13), (p25 10), (p25 11), (p25 1)] },
  { start := p25 1, finish := p25 8, path := [(p25 1), (p25 3), (p25 13), (p25 11), (p25 10), (p25 5), (p25 8)] },
  { start := p25 8, finish := p25 1, path := [(p25 8), (p25 5), (p25 10), (p25 11), (p25 13), (p25 3), (p25 1)] },
  { start := p25 5, finish := p25 11, path := [(p25 5), (p25 10), (p25 13), (p25 8), (p25 3), (p25 1), (p25 11)] },
  { start := p25 11, finish := p25 5, path := [(p25 11), (p25 1), (p25 3), (p25 8), (p25 13), (p25 10), (p25 5)] },
  { start := p25 5, finish := p25 3, path := [(p25 5), (p25 8), (p25 13), (p25 10), (p25 11), (p25 1), (p25 3)] },
  { start := p25 3, finish := p25 5, path := [(p25 3), (p25 1), (p25 11), (p25 10), (p25 13), (p25 8), (p25 5)] },
  { start := p25 1, finish := p25 10, path := [(p25 1), (p25 11), (p25 13), (p25 3), (p25 8), (p25 5), (p25 10)] },
  { start := p25 10, finish := p25 1, path := [(p25 10), (p25 5), (p25 8), (p25 3), (p25 13), (p25 11), (p25 1)] },
  { start := p25 1, finish := p25 13, path := [(p25 1), (p25 11), (p25 10), (p25 5), (p25 8), (p25 3), (p25 13)] },
  { start := p25 13, finish := p25 1, path := [(p25 13), (p25 3), (p25 8), (p25 5), (p25 10), (p25 11), (p25 1)] },
  { start := p25 5, finish := p25 13, path := [(p25 5), (p25 8), (p25 3), (p25 1), (p25 11), (p25 10), (p25 13)] },
  { start := p25 13, finish := p25 5, path := [(p25 13), (p25 10), (p25 11), (p25 1), (p25 3), (p25 8), (p25 5)] },
  { start := p25 3, finish := p25 8, path := [(p25 3), (p25 1), (p25 11), (p25 13), (p25 10), (p25 5), (p25 8)] },
  { start := p25 8, finish := p25 3, path := [(p25 8), (p25 5), (p25 10), (p25 13), (p25 11), (p25 1), (p25 3)] },
  { start := p25 10, finish := p25 11, path := [(p25 10), (p25 5), (p25 8), (p25 13), (p25 3), (p25 1), (p25 11)] },
  { start := p25 11, finish := p25 10, path := [(p25 11), (p25 1), (p25 3), (p25 13), (p25 8), (p25 5), (p25 10)] },
  { start := p25 3, finish := p25 10, path := [(p25 3), (p25 1), (p25 11), (p25 13), (p25 8), (p25 5), (p25 10)] },
  { start := p25 10, finish := p25 3, path := [(p25 10), (p25 5), (p25 8), (p25 13), (p25 11), (p25 1), (p25 3)] },
  { start := p25 8, finish := p25 11, path := [(p25 8), (p25 5), (p25 10), (p25 13), (p25 3), (p25 1), (p25 11)] },
  { start := p25 11, finish := p25 8, path := [(p25 11), (p25 1), (p25 3), (p25 13), (p25 10), (p25 5), (p25 8)] },
  { start := p25 3, finish := p25 13, path := [(p25 3), (p25 1), (p25 11), (p25 10), (p25 5), (p25 8), (p25 13)] },
  { start := p25 13, finish := p25 3, path := [(p25 13), (p25 8), (p25 5), (p25 10), (p25 11), (p25 1), (p25 3)] },
  { start := p25 10, finish := p25 13, path := [(p25 10), (p25 5), (p25 8), (p25 3), (p25 1), (p25 11), (p25 13)] },
  { start := p25 13, finish := p25 10, path := [(p25 13), (p25 11), (p25 1), (p25 3), (p25 8), (p25 5), (p25 10)] },
  { start := p25 8, finish := p25 13, path := [(p25 8), (p25 5), (p25 10), (p25 11), (p25 1), (p25 3), (p25 13)] },
  { start := p25 13, finish := p25 8, path := [(p25 13), (p25 3), (p25 1), (p25 11), (p25 10), (p25 5), (p25 8)] },
  { start := p25 11, finish := p25 13, path := [(p25 11), (p25 1), (p25 3), (p25 8), (p25 5), (p25 10), (p25 13)] },
  { start := p25 13, finish := p25 11, path := [(p25 13), (p25 10), (p25 5), (p25 8), (p25 3), (p25 1), (p25 11)] },
]
def pairFivePath333 : List PairFiveEntry := [
  { start := p25 1, finish := p25 2, path := [(p25 1), (p25 11), (p25 10), (p25 5), (p25 7), (p25 2)] },
  { start := p25 2, finish := p25 1, path := [(p25 2), (p25 7), (p25 5), (p25 10), (p25 11), (p25 1)] },
  { start := p25 5, finish := p25 10, path := [(p25 5), (p25 7), (p25 2), (p25 1), (p25 11), (p25 10)] },
  { start := p25 10, finish := p25 5, path := [(p25 10), (p25 11), (p25 1), (p25 2), (p25 7), (p25 5)] },
  { start := p25 5, finish := p25 7, path := [(p25 5), (p25 10), (p25 11), (p25 1), (p25 2), (p25 7)] },
  { start := p25 7, finish := p25 5, path := [(p25 7), (p25 2), (p25 1), (p25 11), (p25 10), (p25 5)] },
  { start := p25 1, finish := p25 11, path := [(p25 1), (p25 2), (p25 7), (p25 5), (p25 10), (p25 11)] },
  { start := p25 11, finish := p25 1, path := [(p25 11), (p25 10), (p25 5), (p25 7), (p25 2), (p25 1)] },
  { start := p25 10, finish := p25 11, path := [(p25 10), (p25 5), (p25 7), (p25 2), (p25 1), (p25 11)] },
  { start := p25 11, finish := p25 10, path := [(p25 11), (p25 1), (p25 2), (p25 7), (p25 5), (p25 10)] },
  { start := p25 2, finish := p25 7, path := [(p25 2), (p25 1), (p25 11), (p25 10), (p25 5), (p25 7)] },
  { start := p25 7, finish := p25 2, path := [(p25 7), (p25 5), (p25 10), (p25 11), (p25 1), (p25 2)] },
]
def pairFivePath342 : List PairFiveEntry := [
  { start := p25 1, finish := p25 3, path := [(p25 1), (p25 11), (p25 14), (p25 10), (p25 13), (p25 8), (p25 5), (p25 9), (p25 4), (p25 3)] },
  { start := p25 3, finish := p25 1, path := [(p25 3), (p25 4), (p25 9), (p25 5), (p25 8), (p25 13), (p25 10), (p25 14), (p25 11), (p25 1)] },
  { start := p25 1, finish := p25 4, path := [(p25 1), (p25 11), (p25 13), (p25 10), (p25 14), (p25 9), (p25 5), (p25 8), (p25 3), (p25 4)] },
  { start := p25 4, finish := p25 1, path := [(p25 4), (p25 3), (p25 8), (p25 5), (p25 9), (p25 14), (p25 10), (p25 13), (p25 11), (p25 1)] },
  { start := p25 5, finish := p25 8, path := [(p25 5), (p25 10), (p25 14), (p25 11), (p25 13), (p25 3), (p25 1), (p25 4), (p25 9), (p25 8)] },
  { start := p25 8, finish := p25 5, path := [(p25 8), (p25 9), (p25 4), (p25 1), (p25 3), (p25 13), (p25 11), (p25 14), (p25 10), (p25 5)] },
  { start := p25 5, finish := p25 9, path := [(p25 5), (p25 10), (p25 13), (p25 11), (p25 14), (p25 4), (p25 1), (p25 3), (p25 8), (p25 9)] },
  { start := p25 9, finish := p25 5, path := [(p25 9), (p25 8), (p25 3), (p25 1), (p25 4), (p25 14), (p25 11), (p25 13), (p25 10), (p25 5)] },
  { start := p25 1, finish := p25 5, path := [(p25 1), (p25 11), (p25 13), (p25 10), (p25 14), (p25 9), (p25 4), (p25 3), (p25 8), (p25 5)] },
  { start := p25 5, finish := p25 1, path := [(p25 5), (p25 8), (p25 3), (p25 4), (p25 9), (p25 14), (p25 10), (p25 13), (p25 11), (p25 1)] },
  { start := p25 1, finish := p25 8, path := [(p25 1), (p25 11), (p25 14), (p25 13), (p25 10), (p25 5), (p25 9), (p25 4), (p25 3), (p25 8)] },
  { start := p25 8, finish := p25 1, path := [(p25 8), (p25 3), (p25 4), (p25 9), (p25 5), (p25 10), (p25 13), (p25 14), (p25 11), (p25 1)] },
  { start := p25 1, finish := p25 9, path := [(p25 1), (p25 11), (p25 13), (p25 14), (p25 10), (p25 5), (p25 8), (p25 3), (p25 4), (p25 9)] },
  { start := p25 9, finish := p25 1, path := [(p25 9), (p25 4), (p25 3), (p25 8), (p25 5), (p25 10), (p25 14), (p25 13), (p25 11), (p25 1)] },
  { start := p25 5, finish := p25 3, path := [(p25 5), (p25 10), (p25 14), (p25 13), (p25 11), (p25 1), (p25 4), (p25 9), (p25 8), (p25 3)] },
  { start := p25 3, finish := p25 5, path := [(p25 3), (p25 8), (p25 9), (p25 4), (p25 1), (p25 11), (p25 13), (p25 14), (p25 10), (p25 5)] },
  { start := p25 5, finish := p25 4, path := [(p25 5), (p25 10), (p25 13), (p25 14), (p25 11), (p25 1), (p25 3), (p25 8), (p25 9), (p25 4)] },
  { start := p25 4, finish := p25 5, path := [(p25 4), (p25 9), (p25 8), (p25 3), (p25 1), (p25 11), (p25 14), (p25 13), (p25 10), (p25 5)] },
  { start := p25 1, finish := p25 10, path := [(p25 1), (p25 11), (p25 13), (p25 14), (p25 9), (p25 4), (p25 3), (p25 8), (p25 5), (p25 10)] },
  { start := p25 10, finish := p25 1, path := [(p25 10), (p25 5), (p25 8), (p25 3), (p25 4), (p25 9), (p25 14), (p25 13), (p25 11), (p25 1)] },
  { start := p25 5, finish := p25 11, path := [(p25 5), (p25 10), (p25 13), (p25 14), (p25 4), (p25 9), (p25 8), (p25 3), (p25 1), (p25 11)] },
  { start := p25 11, finish := p25 5, path := [(p25 11), (p25 1), (p25 3), (p25 8), (p25 9), (p25 4), (p25 14), (p25 13), (p25 10), (p25 5)] },
  { start := p25 1, finish := p25 11, path := [(p25 1), (p25 4), (p25 9), (p25 14), (p25 13), (p25 3), (p25 8), (p25 5), (p25 10), (p25 11)] },
  { start := p25 11, finish := p25 1, path := [(p25 11), (p25 10), (p25 5), (p25 8), (p25 3), (p25 13), (p25 14), (p25 9), (p25 4), (p25 1)] },
  { start := p25 5, finish := p25 10, path := [(p25 5), (p25 9), (p25 4), (p25 14), (p25 13), (p25 8), (p25 3), (p25 1), (p25 11), (p25 10)] },
  { start := p25 10, finish := p25 5, path := [(p25 10), (p25 11), (p25 1), (p25 3), (p25 8), (p25 13), (p25 14), (p25 4), (p25 9), (p25 5)] },
  { start := p25 1, finish := p25 13, path := [(p25 1), (p25 11), (p25 14), (p25 10), (p25 5), (p25 8), (p25 9), (p25 4), (p25 3), (p25 13)] },
  { start := p25 13, finish := p25 1, path := [(p25 13), (p25 3), (p25 4), (p25 9), (p25 8), (p25 5), (p25 10), (p25 14), (p25 11), (p25 1)] },
  { start := p25 1, finish := p25 14, path := [(p25 1), (p25 11), (p25 13), (p25 10), (p25 5), (p25 9), (p25 8), (p25 3), (p25 4), (p25 14)] },
  { start := p25 14, finish := p25 1, path := [(p25 14), (p25 4), (p25 3), (p25 8), (p25 9), (p25 5), (p25 10), (p25 13), (p25 11), (p25 1)] },
  { start := p25 5, finish := p25 13, path := [(p25 5), (p25 10), (p25 14), (p25 11), (p25 1), (p25 3), (p25 4), (p25 9), (p25 8), (p25 13)] },
  { start := p25 13, finish := p25 5, path := [(p25 13), (p25 8), (p25 9), (p25 4), (p25 3), (p25 1), (p25 11), (p25 14), (p25 10), (p25 5)] },
  { start := p25 5, finish := p25 14, path := [(p25 5), (p25 10), (p25 13), (p25 11), (p25 1), (p25 4), (p25 3), (p25 8), (p25 9), (p25 14)] },
  { start := p25 14, finish := p25 5, path := [(p25 14), (p25 9), (p25 8), (p25 3), (p25 4), (p25 1), (p25 11), (p25 13), (p25 10), (p25 5)] },
  { start := p25 3, finish := p25 4, path := [(p25 3), (p25 13), (p25 14), (p25 9), (p25 8), (p25 5), (p25 10), (p25 11), (p25 1), (p25 4)] },
  { start := p25 4, finish := p25 3, path := [(p25 4), (p25 1), (p25 11), (p25 10), (p25 5), (p25 8), (p25 9), (p25 14), (p25 13), (p25 3)] },
  { start := p25 8, finish := p25 9, path := [(p25 8), (p25 13), (p25 14), (p25 4), (p25 3), (p25 1), (p25 11), (p25 10), (p25 5), (p25 9)] },
  { start := p25 9, finish := p25 8, path := [(p25 9), (p25 5), (p25 10), (p25 11), (p25 1), (p25 3), (p25 4), (p25 14), (p25 13), (p25 8)] },
  { start := p25 3, finish := p25 8, path := [(p25 3), (p25 13), (p25 14), (p25 10), (p25 11), (p25 1), (p25 4), (p25 9), (p25 5), (p25 8)] },
  { start := p25 8, finish := p25 3, path := [(p25 8), (p25 5), (p25 9), (p25 4), (p25 1), (p25 11), (p25 10), (p25 14), (p25 13), (p25 3)] },
  { start := p25 4, finish := p25 9, path := [(p25 4), (p25 14), (p25 13), (p25 10), (p25 11), (p25 1), (p25 3), (p25 8), (p25 5), (p25 9)] },
  { start := p25 9, finish := p25 4, path := [(p25 9), (p25 5), (p25 8), (p25 3), (p25 1), (p25 11), (p25 10), (p25 13), (p25 14), (p25 4)] },
  { start := p25 3, finish := p25 9, path := [(p25 3), (p25 8), (p25 5), (p25 10), (p25 14), (p25 13), (p25 11), (p25 1), (p25 4), (p25 9)] },
  { start := p25 9, finish := p25 3, path := [(p25 9), (p25 4), (p25 1), (p25 11), (p25 13), (p25 14), (p25 10), (p25 5), (p25 8), (p25 3)] },
  { start := p25 4, finish := p25 8, path := [(p25 4), (p25 9), (p25 5), (p25 10), (p25 13), (p25 14), (p25 11), (p25 1), (p25 3), (p25 8)] },
  { start := p25 8, finish := p25 4, path := [(p25 8), (p25 3), (p25 1), (p25 11), (p25 14), (p25 13), (p25 10), (p25 5), (p25 9), (p25 4)] },
  { start := p25 3, finish := p25 10, path := [(p25 3), (p25 13), (p25 14), (p25 11), (p25 1), (p25 4), (p25 9), (p25 8), (p25 5), (p25 10)] },
  { start := p25 10, finish := p25 3, path := [(p25 10), (p25 5), (p25 8), (p25 9), (p25 4), (p25 1), (p25 11), (p25 14), (p25 13), (p25 3)] },
  { start := p25 4, finish := p25 10, path := [(p25 4), (p25 14), (p25 13), (p25 11), (p25 1), (p25 3), (p25 8), (p25 9), (p25 5), (p25 10)] },
  { start := p25 10, finish := p25 4, path := [(p25 10), (p25 5), (p25 9), (p25 8), (p25 3), (p25 1), (p25 11), (p25 13), (p25 14), (p25 4)] },
  { start := p25 8, finish := p25 11, path := [(p25 8), (p25 13), (p25 14), (p25 10), (p25 5), (p25 9), (p25 4), (p25 3), (p25 1), (p25 11)] },
  { start := p25 11, finish := p25 8, path := [(p25 11), (p25 1), (p25 3), (p25 4), (p25 9), (p25 5), (p25 10), (p25 14), (p25 13), (p25 8)] },
  { start := p25 9, finish := p25 11, path := [(p25 9), (p25 14), (p25 13), (p25 10), (p25 5), (p25 8), (p25 3), (p25 4), (p25 1), (p25 11)] },
  { start := p25 11, finish := p25 9, path := [(p25 11), (p25 1), (p25 4), (p25 3), (p25 8), (p25 5), (p25 10), (p25 13), (p25 14), (p25 9)] },
  { start := p25 3, finish := p25 11, path := [(p25 3), (p25 8), (p25 13), (p25 14), (p25 10), (p25 5), (p25 9), (p25 4), (p25 1), (p25 11)] },
  { start := p25 11, finish := p25 3, path := [(p25 11), (p25 1), (p25 4), (p25 9), (p25 5), (p25 10), (p25 14), (p25 13), (p25 8), (p25 3)] },
  { start := p25 4, finish := p25 11, path := [(p25 4), (p25 9), (p25 14), (p25 13), (p25 10), (p25 5), (p25 8), (p25 3), (p25 1), (p25 11)] },
  { start := p25 11, finish := p25 4, path := [(p25 11), (p25 1), (p25 3), (p25 8), (p25 5), (p25 10), (p25 13), (p25 14), (p25 9), (p25 4)] },
  { start := p25 8, finish := p25 10, path := [(p25 8), (p25 3), (p25 13), (p25 14), (p25 11), (p25 1), (p25 4), (p25 9), (p25 5), (p25 10)] },
  { start := p25 10, finish := p25 8, path := [(p25 10), (p25 5), (p25 9), (p25 4), (p25 1), (p25 11), (p25 14), (p25 13), (p25 3), (p25 8)] },
  { start := p25 9, finish := p25 10, path := [(p25 9), (p25 4), (p25 14), (p25 13), (p25 11), (p25 1), (p25 3), (p25 8), (p25 5), (p25 10)] },
  { start := p25 10, finish := p25 9, path := [(p25 10), (p25 5), (p25 8), (p25 3), (p25 1), (p25 11), (p25 13), (p25 14), (p25 4), (p25 9)] },
  { start := p25 3, finish := p25 13, path := [(p25 3), (p25 1), (p25 11), (p25 10), (p25 14), (p25 4), (p25 9), (p25 5), (p25 8), (p25 13)] },
  { start := p25 13, finish := p25 3, path := [(p25 13), (p25 8), (p25 5), (p25 9), (p25 4), (p25 14), (p25 10), (p25 11), (p25 1), (p25 3)] },
  { start := p25 4, finish := p25 14, path := [(p25 4), (p25 1), (p25 11), (p25 10), (p25 13), (p25 3), (p25 8), (p25 5), (p25 9), (p25 14)] },
  { start := p25 14, finish := p25 4, path := [(p25 14), (p25 9), (p25 5), (p25 8), (p25 3), (p25 13), (p25 10), (p25 11), (p25 1), (p25 4)] },
  { start := p25 8, finish := p25 13, path := [(p25 8), (p25 5), (p25 10), (p25 11), (p25 14), (p25 9), (p25 4), (p25 1), (p25 3), (p25 13)] },
  { start := p25 13, finish := p25 8, path := [(p25 13), (p25 3), (p25 1), (p25 4), (p25 9), (p25 14), (p25 11), (p25 10), (p25 5), (p25 8)] },
  { start := p25 9, finish := p25 14, path := [(p25 9), (p25 5), (p25 10), (p25 11), (p25 13), (p25 8), (p25 3), (p25 1), (p25 4), (p25 14)] },
  { start := p25 14, finish := p25 9, path := [(p25 14), (p25 4), (p25 1), (p25 3), (p25 8), (p25 13), (p25 11), (p25 10), (p25 5), (p25 9)] },
  { start := p25 3, finish := p25 14, path := [(p25 3), (p25 13), (p25 8), (p25 9), (p25 5), (p25 10), (p25 11), (p25 1), (p25 4), (p25 14)] },
  { start := p25 14, finish := p25 3, path := [(p25 14), (p25 4), (p25 1), (p25 11), (p25 10), (p25 5), (p25 9), (p25 8), (p25 13), (p25 3)] },
  { start := p25 4, finish := p25 13, path := [(p25 4), (p25 14), (p25 9), (p25 8), (p25 5), (p25 10), (p25 11), (p25 1), (p25 3), (p25 13)] },
  { start := p25 13, finish := p25 4, path := [(p25 13), (p25 3), (p25 1), (p25 11), (p25 10), (p25 5), (p25 8), (p25 9), (p25 14), (p25 4)] },
  { start := p25 8, finish := p25 14, path := [(p25 8), (p25 13), (p25 3), (p25 4), (p25 1), (p25 11), (p25 10), (p25 5), (p25 9), (p25 14)] },
  { start := p25 14, finish := p25 8, path := [(p25 14), (p25 9), (p25 5), (p25 10), (p25 11), (p25 1), (p25 4), (p25 3), (p25 13), (p25 8)] },
  { start := p25 9, finish := p25 13, path := [(p25 9), (p25 14), (p25 4), (p25 3), (p25 1), (p25 11), (p25 10), (p25 5), (p25 8), (p25 13)] },
  { start := p25 13, finish := p25 9, path := [(p25 13), (p25 8), (p25 5), (p25 10), (p25 11), (p25 1), (p25 3), (p25 4), (p25 14), (p25 9)] },
  { start := p25 10, finish := p25 11, path := [(p25 10), (p25 14), (p25 13), (p25 8), (p25 5), (p25 9), (p25 4), (p25 3), (p25 1), (p25 11)] },
  { start := p25 11, finish := p25 10, path := [(p25 11), (p25 1), (p25 3), (p25 4), (p25 9), (p25 5), (p25 8), (p25 13), (p25 14), (p25 10)] },
  { start := p25 10, finish := p25 13, path := [(p25 10), (p25 5), (p25 8), (p25 9), (p25 4), (p25 14), (p25 11), (p25 1), (p25 3), (p25 13)] },
  { start := p25 13, finish := p25 10, path := [(p25 13), (p25 3), (p25 1), (p25 11), (p25 14), (p25 4), (p25 9), (p25 8), (p25 5), (p25 10)] },
  { start := p25 10, finish := p25 14, path := [(p25 10), (p25 5), (p25 9), (p25 8), (p25 3), (p25 13), (p25 11), (p25 1), (p25 4), (p25 14)] },
  { start := p25 14, finish := p25 10, path := [(p25 14), (p25 4), (p25 1), (p25 11), (p25 13), (p25 3), (p25 8), (p25 9), (p25 5), (p25 10)] },
  { start := p25 11, finish := p25 13, path := [(p25 11), (p25 1), (p25 3), (p25 4), (p25 9), (p25 14), (p25 10), (p25 5), (p25 8), (p25 13)] },
  { start := p25 13, finish := p25 11, path := [(p25 13), (p25 8), (p25 5), (p25 10), (p25 14), (p25 9), (p25 4), (p25 3), (p25 1), (p25 11)] },
  { start := p25 11, finish := p25 14, path := [(p25 11), (p25 1), (p25 4), (p25 3), (p25 8), (p25 13), (p25 10), (p25 5), (p25 9), (p25 14)] },
  { start := p25 14, finish := p25 11, path := [(p25 14), (p25 9), (p25 5), (p25 10), (p25 13), (p25 8), (p25 3), (p25 4), (p25 1), (p25 11)] },
  { start := p25 13, finish := p25 14, path := [(p25 13), (p25 11), (p25 10), (p25 5), (p25 9), (p25 8), (p25 3), (p25 1), (p25 4), (p25 14)] },
  { start := p25 14, finish := p25 13, path := [(p25 14), (p25 4), (p25 1), (p25 3), (p25 8), (p25 9), (p25 5), (p25 10), (p25 11), (p25 13)] },
]
def pairFivePath343 : List PairFiveEntry := [
  { start := p25 1, finish := p25 2, path := [(p25 1), (p25 11), (p25 13), (p25 10), (p25 5), (p25 7), (p25 8), (p25 3), (p25 2)] },
  { start := p25 2, finish := p25 1, path := [(p25 2), (p25 3), (p25 8), (p25 7), (p25 5), (p25 10), (p25 13), (p25 11), (p25 1)] },
  { start := p25 5, finish := p25 7, path := [(p25 5), (p25 10), (p25 13), (p25 11), (p25 1), (p25 2), (p25 3), (p25 8), (p25 7)] },
  { start := p25 7, finish := p25 5, path := [(p25 7), (p25 8), (p25 3), (p25 2), (p25 1), (p25 11), (p25 13), (p25 10), (p25 5)] },
  { start := p25 10, finish := p25 11, path := [(p25 10), (p25 5), (p25 8), (p25 7), (p25 2), (p25 1), (p25 3), (p25 13), (p25 11)] },
  { start := p25 11, finish := p25 10, path := [(p25 11), (p25 13), (p25 3), (p25 1), (p25 2), (p25 7), (p25 8), (p25 5), (p25 10)] },
  { start := p25 1, finish := p25 3, path := [(p25 1), (p25 11), (p25 10), (p25 13), (p25 8), (p25 5), (p25 7), (p25 2), (p25 3)] },
  { start := p25 3, finish := p25 1, path := [(p25 3), (p25 2), (p25 7), (p25 5), (p25 8), (p25 13), (p25 10), (p25 11), (p25 1)] },
  { start := p25 2, finish := p25 3, path := [(p25 2), (p25 7), (p25 5), (p25 8), (p25 13), (p25 10), (p25 11), (p25 1), (p25 3)] },
  { start := p25 3, finish := p25 2, path := [(p25 3), (p25 1), (p25 11), (p25 10), (p25 13), (p25 8), (p25 5), (p25 7), (p25 2)] },
  { start := p25 5, finish := p25 8, path := [(p25 5), (p25 10), (p25 11), (p25 13), (p25 3), (p25 1), (p25 2), (p25 7), (p25 8)] },
  { start := p25 8, finish := p25 5, path := [(p25 8), (p25 7), (p25 2), (p25 1), (p25 3), (p25 13), (p25 11), (p25 10), (p25 5)] },
  { start := p25 7, finish := p25 8, path := [(p25 7), (p25 2), (p25 1), (p25 3), (p25 13), (p25 11), (p25 10), (p25 5), (p25 8)] },
  { start := p25 8, finish := p25 7, path := [(p25 8), (p25 5), (p25 10), (p25 11), (p25 13), (p25 3), (p25 1), (p25 2), (p25 7)] },
  { start := p25 10, finish := p25 13, path := [(p25 10), (p25 5), (p25 7), (p25 8), (p25 3), (p25 2), (p25 1), (p25 11), (p25 13)] },
  { start := p25 13, finish := p25 10, path := [(p25 13), (p25 11), (p25 1), (p25 2), (p25 3), (p25 8), (p25 7), (p25 5), (p25 10)] },
  { start := p25 11, finish := p25 13, path := [(p25 11), (p25 1), (p25 2), (p25 3), (p25 8), (p25 7), (p25 5), (p25 10), (p25 13)] },
  { start := p25 13, finish := p25 11, path := [(p25 13), (p25 10), (p25 5), (p25 7), (p25 8), (p25 3), (p25 2), (p25 1), (p25 11)] },
  { start := p25 1, finish := p25 5, path := [(p25 1), (p25 11), (p25 10), (p25 13), (p25 8), (p25 3), (p25 2), (p25 7), (p25 5)] },
  { start := p25 5, finish := p25 1, path := [(p25 5), (p25 7), (p25 2), (p25 3), (p25 8), (p25 13), (p25 10), (p25 11), (p25 1)] },
  { start := p25 2, finish := p25 10, path := [(p25 2), (p25 7), (p25 5), (p25 8), (p25 13), (p25 3), (p25 1), (p25 11), (p25 10)] },
  { start := p25 10, finish := p25 2, path := [(p25 10), (p25 11), (p25 1), (p25 3), (p25 13), (p25 8), (p25 5), (p25 7), (p25 2)] },
  { start := p25 7, finish := p25 11, path := [(p25 7), (p25 2), (p25 1), (p25 3), (p25 13), (p25 8), (p25 5), (p25 10), (p25 11)] },
  { start := p25 11, finish := p25 7, path := [(p25 11), (p25 10), (p25 5), (p25 8), (p25 13), (p25 3), (p25 1), (p25 2), (p25 7)] },
  { start := p25 1, finish := p25 7, path := [(p25 1), (p25 11), (p25 13), (p25 10), (p25 5), (p25 8), (p25 3), (p25 2), (p25 7)] },
  { start := p25 7, finish := p25 1, path := [(p25 7), (p25 2), (p25 3), (p25 8), (p25 5), (p25 10), (p25 13), (p25 11), (p25 1)] },
  { start := p25 2, finish := p25 11, path := [(p25 2), (p25 7), (p25 8), (p25 5), (p25 10), (p25 13), (p25 3), (p25 1), (p25 11)] },
  { start := p25 11, finish := p25 2, path := [(p25 11), (p25 1), (p25 3), (p25 13), (p25 10), (p25 5), (p25 8), (p25 7), (p25 2)] },
  { start := p25 5, finish := p25 2, path := [(p25 5), (p25 10), (p25 13), (p25 11), (p25 1), (p25 3), (p25 8), (p25 7), (p25 2)] },
  { start := p25 2, finish := p25 5, path := [(p25 2), (p25 7), (p25 8), (p25 3), (p25 1), (p25 11), (p25 13), (p25 10), (p25 5)] },
  { start := p25 7, finish := p25 10, path := [(p25 7), (p25 2), (p25 3), (p25 1), (p25 11), (p25 13), (p25 8), (p25 5), (p25 10)] },
  { start := p25 10, finish := p25 7, path := [(p25 10), (p25 5), (p25 8), (p25 13), (p25 11), (p25 1), (p25 3), (p25 2), (p25 7)] },
  { start := p25 10, finish := p25 1, path := [(p25 10), (p25 5), (p25 8), (p25 7), (p25 2), (p25 3), (p25 13), (p25 11), (p25 1)] },
  { start := p25 1, finish := p25 10, path := [(p25 1), (p25 11), (p25 13), (p25 3), (p25 2), (p25 7), (p25 8), (p25 5), (p25 10)] },
  { start := p25 11, finish := p25 5, path := [(p25 11), (p25 1), (p25 3), (p25 2), (p25 7), (p25 8), (p25 13), (p25 10), (p25 5)] },
  { start := p25 5, finish := p25 11, path := [(p25 5), (p25 10), (p25 13), (p25 8), (p25 7), (p25 2), (p25 3), (p25 1), (p25 11)] },
  { start := p25 1, finish := p25 8, path := [(p25 1), (p25 11), (p25 13), (p25 10), (p25 5), (p25 7), (p25 2), (p25 3), (p25 8)] },
  { start := p25 8, finish := p25 1, path := [(p25 8), (p25 3), (p25 2), (p25 7), (p25 5), (p25 10), (p25 13), (p25 11), (p25 1)] },
  { start := p25 2, finish := p25 13, path := [(p25 2), (p25 7), (p25 8), (p25 5), (p25 10), (p25 11), (p25 1), (p25 3), (p25 13)] },
  { start := p25 13, finish := p25 2, path := [(p25 13), (p25 3), (p25 1), (p25 11), (p25 10), (p25 5), (p25 8), (p25 7), (p25 2)] },
  { start := p25 5, finish := p25 3, path := [(p25 5), (p25 10), (p25 13), (p25 11), (p25 1), (p25 2), (p25 7), (p25 8), (p25 3)] },
  { start := p25 3, finish := p25 5, path := [(p25 3), (p25 8), (p25 7), (p25 2), (p25 1), (p25 11), (p25 13), (p25 10), (p25 5)] },
  { start := p25 7, finish := p25 13, path := [(p25 7), (p25 2), (p25 3), (p25 1), (p25 11), (p25 10), (p25 5), (p25 8), (p25 13)] },
  { start := p25 13, finish := p25 7, path := [(p25 13), (p25 8), (p25 5), (p25 10), (p25 11), (p25 1), (p25 3), (p25 2), (p25 7)] },
  { start := p25 10, finish := p25 3, path := [(p25 10), (p25 5), (p25 8), (p25 7), (p25 2), (p25 1), (p25 11), (p25 13), (p25 3)] },
  { start := p25 3, finish := p25 10, path := [(p25 3), (p25 13), (p25 11), (p25 1), (p25 2), (p25 7), (p25 8), (p25 5), (p25 10)] },
  { start := p25 11, finish := p25 8, path := [(p25 11), (p25 1), (p25 3), (p25 2), (p25 7), (p25 5), (p25 10), (p25 13), (p25 8)] },
  { start := p25 8, finish := p25 11, path := [(p25 8), (p25 13), (p25 10), (p25 5), (p25 7), (p25 2), (p25 3), (p25 1), (p25 11)] },
  { start := p25 1, finish := p25 11, path := [(p25 1), (p25 2), (p25 3), (p25 13), (p25 8), (p25 7), (p25 5), (p25 10), (p25 11)] },
  { start := p25 11, finish := p25 1, path := [(p25 11), (p25 10), (p25 5), (p25 7), (p25 8), (p25 13), (p25 3), (p25 2), (p25 1)] },
  { start := p25 2, finish := p25 7, path := [(p25 2), (p25 1), (p25 3), (p25 8), (p25 13), (p25 11), (p25 10), (p25 5), (p25 7)] },
  { start := p25 7, finish := p25 2, path := [(p25 7), (p25 5), (p25 10), (p25 11), (p25 13), (p25 8), (p25 3), (p25 1), (p25 2)] },
  { start := p25 5, finish := p25 10, path := [(p25 5), (p25 7), (p25 8), (p25 13), (p25 3), (p25 2), (p25 1), (p25 11), (p25 10)] },
  { start := p25 10, finish := p25 5, path := [(p25 10), (p25 11), (p25 1), (p25 2), (p25 3), (p25 13), (p25 8), (p25 7), (p25 5)] },
  { start := p25 1, finish := p25 13, path := [(p25 1), (p25 11), (p25 10), (p25 5), (p25 8), (p25 7), (p25 2), (p25 3), (p25 13)] },
  { start := p25 13, finish := p25 1, path := [(p25 13), (p25 3), (p25 2), (p25 7), (p25 8), (p25 5), (p25 10), (p25 11), (p25 1)] },
  { start := p25 2, finish := p25 8, path := [(p25 2), (p25 7), (p25 5), (p25 10), (p25 13), (p25 11), (p25 1), (p25 3), (p25 8)] },
  { start := p25 8, finish := p25 2, path := [(p25 8), (p25 3), (p25 1), (p25 11), (p25 13), (p25 10), (p25 5), (p25 7), (p25 2)] },
  { start := p25 5, finish := p25 13, path := [(p25 5), (p25 10), (p25 11), (p25 1), (p25 3), (p25 2), (p25 7), (p25 8), (p25 13)] },
  { start := p25 13, finish := p25 5, path := [(p25 13), (p25 8), (p25 7), (p25 2), (p25 3), (p25 1), (p25 11), (p25 10), (p25 5)] },
  { start := p25 7, finish := p25 3, path := [(p25 7), (p25 2), (p25 1), (p25 11), (p25 13), (p25 10), (p25 5), (p25 8), (p25 3)] },
  { start := p25 3, finish := p25 7, path := [(p25 3), (p25 8), (p25 5), (p25 10), (p25 13), (p25 11), (p25 1), (p25 2), (p25 7)] },
  { start := p25 10, finish := p25 8, path := [(p25 10), (p25 5), (p25 7), (p25 2), (p25 3), (p25 1), (p25 11), (p25 13), (p25 8)] },
  { start := p25 8, finish := p25 10, path := [(p25 8), (p25 13), (p25 11), (p25 1), (p25 3), (p25 2), (p25 7), (p25 5), (p25 10)] },
  { start := p25 11, finish := p25 3, path := [(p25 11), (p25 1), (p25 2), (p25 7), (p25 8), (p25 5), (p25 10), (p25 13), (p25 3)] },
  { start := p25 3, finish := p25 11, path := [(p25 3), (p25 13), (p25 10), (p25 5), (p25 8), (p25 7), (p25 2), (p25 1), (p25 11)] },
  { start := p25 3, finish := p25 8, path := [(p25 3), (p25 13), (p25 10), (p25 11), (p25 1), (p25 2), (p25 7), (p25 5), (p25 8)] },
  { start := p25 8, finish := p25 3, path := [(p25 8), (p25 5), (p25 7), (p25 2), (p25 1), (p25 11), (p25 10), (p25 13), (p25 3)] },
  { start := p25 3, finish := p25 13, path := [(p25 3), (p25 8), (p25 5), (p25 7), (p25 2), (p25 1), (p25 11), (p25 10), (p25 13)] },
  { start := p25 13, finish := p25 3, path := [(p25 13), (p25 10), (p25 11), (p25 1), (p25 2), (p25 7), (p25 5), (p25 8), (p25 3)] },
  { start := p25 8, finish := p25 13, path := [(p25 8), (p25 3), (p25 1), (p25 2), (p25 7), (p25 5), (p25 10), (p25 11), (p25 13)] },
  { start := p25 13, finish := p25 8, path := [(p25 13), (p25 11), (p25 10), (p25 5), (p25 7), (p25 2), (p25 1), (p25 3), (p25 8)] },
]
def pairFivePath443 : List PairFiveEntry := [
  { start := p25 1, finish := p25 2, path := [(p25 1), (p25 16), (p25 19), (p25 14), (p25 11), (p25 10), (p25 15), (p25 17), (p25 7), (p25 5), (p25 9), (p25 4), (p25 2)] },
  { start := p25 2, finish := p25 1, path := [(p25 2), (p25 4), (p25 9), (p25 5), (p25 7), (p25 17), (p25 15), (p25 10), (p25 11), (p25 14), (p25 19), (p25 16), (p25 1)] },
  { start := p25 5, finish := p25 10, path := [(p25 5), (p25 9), (p25 19), (p25 17), (p25 7), (p25 2), (p25 4), (p25 14), (p25 11), (p25 1), (p25 16), (p25 15), (p25 10)] },
  { start := p25 10, finish := p25 5, path := [(p25 10), (p25 15), (p25 16), (p25 1), (p25 11), (p25 14), (p25 4), (p25 2), (p25 7), (p25 17), (p25 19), (p25 9), (p25 5)] },
  { start := p25 5, finish := p25 7, path := [(p25 5), (p25 15), (p25 19), (p25 14), (p25 10), (p25 11), (p25 16), (p25 17), (p25 2), (p25 1), (p25 4), (p25 9), (p25 7)] },
  { start := p25 7, finish := p25 5, path := [(p25 7), (p25 9), (p25 4), (p25 1), (p25 2), (p25 17), (p25 16), (p25 11), (p25 10), (p25 14), (p25 19), (p25 15), (p25 5)] },
  { start := p25 1, finish := p25 11, path := [(p25 1), (p25 4), (p25 19), (p25 17), (p25 2), (p25 7), (p25 9), (p25 14), (p25 10), (p25 5), (p25 15), (p25 16), (p25 11)] },
  { start := p25 11, finish := p25 1, path := [(p25 11), (p25 16), (p25 15), (p25 5), (p25 10), (p25 14), (p25 9), (p25 7), (p25 2), (p25 17), (p25 19), (p25 4), (p25 1)] },
  { start := p25 10, finish := p25 11, path := [(p25 10), (p25 15), (p25 19), (p25 9), (p25 5), (p25 7), (p25 17), (p25 16), (p25 1), (p25 2), (p25 4), (p25 14), (p25 11)] },
  { start := p25 11, finish := p25 10, path := [(p25 11), (p25 14), (p25 4), (p25 2), (p25 1), (p25 16), (p25 17), (p25 7), (p25 5), (p25 9), (p25 19), (p25 15), (p25 10)] },
  { start := p25 2, finish := p25 7, path := [(p25 2), (p25 4), (p25 19), (p25 16), (p25 1), (p25 11), (p25 14), (p25 9), (p25 5), (p25 10), (p25 15), (p25 17), (p25 7)] },
  { start := p25 7, finish := p25 2, path := [(p25 7), (p25 17), (p25 15), (p25 10), (p25 5), (p25 9), (p25 14), (p25 11), (p25 1), (p25 16), (p25 19), (p25 4), (p25 2)] },
  { start := p25 1, finish := p25 4, path := [(p25 1), (p25 11), (p25 16), (p25 19), (p25 17), (p25 15), (p25 10), (p25 14), (p25 9), (p25 5), (p25 7), (p25 2), (p25 4)] },
  { start := p25 4, finish := p25 1, path := [(p25 4), (p25 2), (p25 7), (p25 5), (p25 9), (p25 14), (p25 10), (p25 15), (p25 17), (p25 19), (p25 16), (p25 11), (p25 1)] },
  { start := p25 5, finish := p25 15, path := [(p25 5), (p25 7), (p25 9), (p25 19), (p25 14), (p25 4), (p25 2), (p25 17), (p25 16), (p25 1), (p25 11), (p25 10), (p25 15)] },
  { start := p25 15, finish := p25 5, path := [(p25 15), (p25 10), (p25 11), (p25 1), (p25 16), (p25 17), (p25 2), (p25 4), (p25 14), (p25 19), (p25 9), (p25 7), (p25 5)] },
  { start := p25 2, finish := p25 4, path := [(p25 2), (p25 7), (p25 17), (p25 19), (p25 16), (p25 15), (p25 5), (p25 9), (p25 14), (p25 10), (p25 11), (p25 1), (p25 4)] },
  { start := p25 4, finish := p25 2, path := [(p25 4), (p25 1), (p25 11), (p25 10), (p25 14), (p25 9), (p25 5), (p25 15), (p25 16), (p25 19), (p25 17), (p25 7), (p25 2)] },
  { start := p25 10, finish := p25 15, path := [(p25 10), (p25 11), (p25 14), (p25 19), (p25 9), (p25 4), (p25 1), (p25 16), (p25 17), (p25 2), (p25 7), (p25 5), (p25 15)] },
  { start := p25 15, finish := p25 10, path := [(p25 15), (p25 5), (p25 7), (p25 2), (p25 17), (p25 16), (p25 1), (p25 4), (p25 9), (p25 19), (p25 14), (p25 11), (p25 10)] },
  { start := p25 5, finish := p25 9, path := [(p25 5), (p25 10), (p25 15), (p25 19), (p25 17), (p25 16), (p25 11), (p25 14), (p25 4), (p25 1), (p25 2), (p25 7), (p25 9)] },
  { start := p25 9, finish := p25 5, path := [(p25 9), (p25 7), (p25 2), (p25 1), (p25 4), (p25 14), (p25 11), (p25 16), (p25 17), (p25 19), (p25 15), (p25 10), (p25 5)] },
  { start := p25 1, finish := p25 16, path := [(p25 1), (p25 2), (p25 4), (p25 19), (p25 14), (p25 9), (p25 7), (p25 17), (p25 15), (p25 5), (p25 10), (p25 11), (p25 16)] },
  { start := p25 16, finish := p25 1, path := [(p25 16), (p25 11), (p25 10), (p25 5), (p25 15), (p25 17), (p25 7), (p25 9), (p25 14), (p25 19), (p25 4), (p25 2), (p25 1)] },
  { start := p25 7, finish := p25 9, path := [(p25 7), (p25 2), (p25 17), (p25 19), (p25 15), (p25 16), (p25 1), (p25 4), (p25 14), (p25 11), (p25 10), (p25 5), (p25 9)] },
  { start := p25 9, finish := p25 7, path := [(p25 9), (p25 5), (p25 10), (p25 11), (p25 14), (p25 4), (p25 1), (p25 16), (p25 15), (p25 19), (p25 17), (p25 2), (p25 7)] },
  { start := p25 11, finish := p25 16, path := [(p25 11), (p25 10), (p25 14), (p25 19), (p25 4), (p25 9), (p25 5), (p25 15), (p25 17), (p25 7), (p25 2), (p25 1), (p25 16)] },
  { start := p25 16, finish := p25 11, path := [(p25 16), (p25 1), (p25 2), (p25 7), (p25 17), (p25 15), (p25 5), (p25 9), (p25 4), (p25 19), (p25 14), (p25 10), (p25 11)] },
  { start := p25 10, finish := p25 14, path := [(p25 10), (p25 5), (p25 15), (p25 19), (p25 16), (p25 17), (p25 7), (p25 9), (p25 4), (p25 2), (p25 1), (p25 11), (p25 14)] },
  { start := p25 14, finish := p25 10, path := [(p25 14), (p25 11), (p25 1), (p25 2), (p25 4), (p25 9), (p25 7), (p25 17), (p25 16), (p25 19), (p25 15), (p25 5), (p25 10)] },
  { start := p25 2, finish := p25 17, path := [(p25 2), (p25 1), (p25 4), (p25 19), (p25 9), (p25 14), (p25 11), (p25 16), (p25 15), (p25 10), (p25 5), (p25 7), (p25 17)] },
  { start := p25 17, finish := p25 2, path := [(p25 17), (p25 7), (p25 5), (p25 10), (p25 15), (p25 16), (p25 11), (p25 14), (p25 9), (p25 19), (p25 4), (p25 1), (p25 2)] },
  { start := p25 11, finish := p25 14, path := [(p25 11), (p25 1), (p25 16), (p25 19), (p25 15), (p25 17), (p25 2), (p25 4), (p25 9), (p25 7), (p25 5), (p25 10), (p25 14)] },
  { start := p25 14, finish := p25 11, path := [(p25 14), (p25 10), (p25 5), (p25 7), (p25 9), (p25 4), (p25 2), (p25 17), (p25 15), (p25 19), (p25 16), (p25 1), (p25 11)] },
  { start := p25 7, finish := p25 17, path := [(p25 7), (p25 5), (p25 9), (p25 19), (p25 4), (p25 14), (p25 10), (p25 15), (p25 16), (p25 11), (p25 1), (p25 2), (p25 17)] },
  { start := p25 17, finish := p25 7, path := [(p25 17), (p25 2), (p25 1), (p25 11), (p25 16), (p25 15), (p25 10), (p25 14), (p25 4), (p25 19), (p25 9), (p25 5), (p25 7)] },
  { start := p25 1, finish := p25 5, path := [(p25 1), (p25 11), (p25 16), (p25 19), (p25 17), (p25 15), (p25 10), (p25 14), (p25 9), (p25 4), (p25 2), (p25 7), (p25 5)] },
  { start := p25 5, finish := p25 1, path := [(p25 5), (p25 7), (p25 2), (p25 4), (p25 9), (p25 14), (p25 10), (p25 15), (p25 17), (p25 19), (p25 16), (p25 11), (p25 1)] },
  { start := p25 2, finish := p25 10, path := [(p25 2), (p25 7), (p25 17), (p25 19), (p25 16), (p25 15), (p25 5), (p25 9), (p25 14), (p25 4), (p25 1), (p25 11), (p25 10)] },
  { start := p25 10, finish := p25 2, path := [(p25 10), (p25 11), (p25 1), (p25 4), (p25 14), (p25 9), (p25 5), (p25 15), (p25 16), (p25 19), (p25 17), (p25 7), (p25 2)] },
  { start := p25 7, finish := p25 11, path := [(p25 7), (p25 2), (p25 17), (p25 19), (p25 15), (p25 16), (p25 1), (p25 4), (p25 14), (p25 9), (p25 5), (p25 10), (p25 11)] },
  { start := p25 11, finish := p25 7, path := [(p25 11), (p25 10), (p25 5), (p25 9), (p25 14), (p25 4), (p25 1), (p25 16), (p25 15), (p25 19), (p25 17), (p25 2), (p25 7)] },
  { start := p25 1, finish := p25 7, path := [(p25 1), (p25 16), (p25 17), (p25 15), (p25 19), (p25 14), (p25 11), (p25 10), (p25 5), (p25 9), (p25 4), (p25 2), (p25 7)] },
  { start := p25 7, finish := p25 1, path := [(p25 7), (p25 2), (p25 4), (p25 9), (p25 5), (p25 10), (p25 11), (p25 14), (p25 19), (p25 15), (p25 17), (p25 16), (p25 1)] },
  { start := p25 5, finish := p25 11, path := [(p25 5), (p25 9), (p25 14), (p25 4), (p25 19), (p25 17), (p25 7), (p25 2), (p25 1), (p25 16), (p25 15), (p25 10), (p25 11)] },
  { start := p25 11, finish := p25 5, path := [(p25 11), (p25 10), (p25 15), (p25 16), (p25 1), (p25 2), (p25 7), (p25 17), (p25 19), (p25 4), (p25 14), (p25 9), (p25 5)] },
  { start := p25 2, finish := p25 11, path := [(p25 2), (p25 17), (p25 16), (p25 15), (p25 19), (p25 9), (p25 7), (p25 5), (p25 10), (p25 14), (p25 4), (p25 1), (p25 11)] },
  { start := p25 11, finish := p25 2, path := [(p25 11), (p25 1), (p25 4), (p25 14), (p25 10), (p25 5), (p25 7), (p25 9), (p25 19), (p25 15), (p25 16), (p25 17), (p25 2)] },
  { start := p25 10, finish := p25 7, path := [(p25 10), (p25 14), (p25 9), (p25 4), (p25 19), (p25 16), (p25 11), (p25 1), (p25 2), (p25 17), (p25 15), (p25 5), (p25 7)] },
  { start := p25 7, finish := p25 10, path := [(p25 7), (p25 5), (p25 15), (p25 17), (p25 2), (p25 1), (p25 11), (p25 16), (p25 19), (p25 4), (p25 9), (p25 14), (p25 10)] },
  { start := p25 5, finish := p25 2, path := [(p25 5), (p25 15), (p25 17), (p25 16), (p25 19), (p25 14), (p25 10), (p25 11), (p25 1), (p25 4), (p25 9), (p25 7), (p25 2)] },
  { start := p25 2, finish := p25 5, path := [(p25 2), (p25 7), (p25 9), (p25 4), (p25 1), (p25 11), (p25 10), (p25 14), (p25 19), (p25 16), (p25 17), (p25 15), (p25 5)] },
  { start := p25 1, finish := p25 10, path := [(p25 1), (p25 4), (p25 14), (p25 9), (p25 19), (p25 17), (p25 2), (p25 7), (p25 5), (p25 15), (p25 16), (p25 11), (p25 10)] },
  { start := p25 10, finish := p25 1, path := [(p25 10), (p25 11), (p25 16), (p25 15), (p25 5), (p25 7), (p25 2), (p25 17), (p25 19), (p25 9), (p25 14), (p25 4), (p25 1)] },
  { start := p25 1, finish := p25 9, path := [(p25 1), (p25 16), (p25 17), (p25 15), (p25 19), (p25 14), (p25 11), (p25 10), (p25 5), (p25 7), (p25 2), (p25 4), (p25 9)] },
  { start := p25 9, finish := p25 1, path := [(p25 9), (p25 4), (p25 2), (p25 7), (p25 5), (p25 10), (p25 11), (p25 14), (p25 19), (p25 15), (p25 17), (p25 16), (p25 1)] },
  { start := p25 5, finish := p25 16, path := [(p25 5), (p25 9), (p25 14), (p25 4), (p25 19), (p25 17), (p25 7), (p25 2), (p25 1), (p25 11), (p25 10), (p25 15), (p25 16)] },
  { start := p25 16, finish := p25 5, path := [(p25 16), (p25 15), (p25 10), (p25 11), (p25 1), (p25 2), (p25 7), (p25 17), (p25 19), (p25 4), (p25 14), (p25 9), (p25 5)] },
  { start := p25 2, finish := p25 14, path := [(p25 2), (p25 17), (p25 16), (p25 15), (p25 19), (p25 9), (p25 7), (p25 5), (p25 10), (p25 11), (p25 1), (p25 4), (p25 14)] },
  { start := p25 14, finish := p25 2, path := [(p25 14), (p25 4), (p25 1), (p25 11), (p25 10), (p25 5), (p25 7), (p25 9), (p25 19), (p25 15), (p25 16), (p25 17), (p25 2)] },
  { start := p25 10, finish := p25 17, path := [(p25 10), (p25 14), (p25 9), (p25 4), (p25 19), (p25 16), (p25 11), (p25 1), (p25 2), (p25 7), (p25 5), (p25 15), (p25 17)] },
  { start := p25 17, finish := p25 10, path := [(p25 17), (p25 15), (p25 5), (p25 7), (p25 2), (p25 1), (p25 11), (p25 16), (p25 19), (p25 4), (p25 9), (p25 14), (p25 10)] },
  { start := p25 5, finish := p25 4, path := [(p25 5), (p25 15), (p25 17), (p25 16), (p25 19), (p25 14), (p25 10), (p25 11), (p25 1), (p25 2), (p25 7), (p25 9), (p25 4)] },
  { start := p25 4, finish := p25 5, path := [(p25 4), (p25 9), (p25 7), (p25 2), (p25 1), (p25 11), (p25 10), (p25 14), (p25 19), (p25 16), (p25 17), (p25 15), (p25 5)] },
  { start := p25 1, finish := p25 15, path := [(p25 1), (p25 4), (p25 14), (p25 9), (p25 19), (p25 17), (p25 2), (p25 7), (p25 5), (p25 10), (p25 11), (p25 16), (p25 15)] },
  { start := p25 15, finish := p25 1, path := [(p25 15), (p25 16), (p25 11), (p25 10), (p25 5), (p25 7), (p25 2), (p25 17), (p25 19), (p25 9), (p25 14), (p25 4), (p25 1)] },
  { start := p25 7, finish := p25 14, path := [(p25 7), (p25 17), (p25 15), (p25 16), (p25 19), (p25 4), (p25 2), (p25 1), (p25 11), (p25 10), (p25 5), (p25 9), (p25 14)] },
  { start := p25 14, finish := p25 7, path := [(p25 14), (p25 9), (p25 5), (p25 10), (p25 11), (p25 1), (p25 2), (p25 4), (p25 19), (p25 16), (p25 15), (p25 17), (p25 7)] },
  { start := p25 11, finish := p25 17, path := [(p25 11), (p25 14), (p25 4), (p25 9), (p25 19), (p25 15), (p25 10), (p25 5), (p25 7), (p25 2), (p25 1), (p25 16), (p25 17)] },
  { start := p25 17, finish := p25 11, path := [(p25 17), (p25 16), (p25 1), (p25 2), (p25 7), (p25 5), (p25 10), (p25 15), (p25 19), (p25 9), (p25 4), (p25 14), (p25 11)] },
  { start := p25 10, finish := p25 4, path := [(p25 10), (p25 15), (p25 16), (p25 17), (p25 19), (p25 9), (p25 5), (p25 7), (p25 2), (p25 1), (p25 11), (p25 14), (p25 4)] },
  { start := p25 4, finish := p25 10, path := [(p25 4), (p25 14), (p25 11), (p25 1), (p25 2), (p25 7), (p25 5), (p25 9), (p25 19), (p25 17), (p25 16), (p25 15), (p25 10)] },
  { start := p25 2, finish := p25 15, path := [(p25 2), (p25 4), (p25 9), (p25 14), (p25 19), (p25 16), (p25 1), (p25 11), (p25 10), (p25 5), (p25 7), (p25 17), (p25 15)] },
  { start := p25 15, finish := p25 2, path := [(p25 15), (p25 17), (p25 7), (p25 5), (p25 10), (p25 11), (p25 1), (p25 16), (p25 19), (p25 14), (p25 9), (p25 4), (p25 2)] },
  { start := p25 11, finish := p25 9, path := [(p25 11), (p25 16), (p25 15), (p25 17), (p25 19), (p25 4), (p25 1), (p25 2), (p25 7), (p25 5), (p25 10), (p25 14), (p25 9)] },
  { start := p25 9, finish := p25 11, path := [(p25 9), (p25 14), (p25 10), (p25 5), (p25 7), (p25 2), (p25 1), (p25 4), (p25 19), (p25 17), (p25 15), (p25 16), (p25 11)] },
  { start := p25 7, finish := p25 16, path := [(p25 7), (p25 9), (p25 4), (p25 14), (p25 19), (p25 15), (p25 5), (p25 10), (p25 11), (p25 1), (p25 2), (p25 17), (p25 16)] },
  { start := p25 16, finish := p25 7, path := [(p25 16), (p25 17), (p25 2), (p25 1), (p25 11), (p25 10), (p25 5), (p25 15), (p25 19), (p25 14), (p25 4), (p25 9), (p25 7)] },
  { start := p25 1, finish := p25 14, path := [(p25 1), (p25 11), (p25 10), (p25 15), (p25 17), (p25 16), (p25 19), (p25 9), (p25 5), (p25 7), (p25 2), (p25 4), (p25 14)] },
  { start := p25 14, finish := p25 1, path := [(p25 14), (p25 4), (p25 2), (p25 7), (p25 5), (p25 9), (p25 19), (p25 16), (p25 17), (p25 15), (p25 10), (p25 11), (p25 1)] },
  { start := p25 5, finish := p25 17, path := [(p25 5), (p25 7), (p25 2), (p25 4), (p25 14), (p25 9), (p25 19), (p25 16), (p25 1), (p25 11), (p25 10), (p25 15), (p25 17)] },
  { start := p25 17, finish := p25 5, path := [(p25 17), (p25 15), (p25 10), (p25 11), (p25 1), (p25 16), (p25 19), (p25 9), (p25 14), (p25 4), (p25 2), (p25 7), (p25 5)] },
  { start := p25 2, finish := p25 9, path := [(p25 2), (p25 7), (p25 5), (p25 15), (p25 16), (p25 17), (p25 19), (p25 14), (p25 10), (p25 11), (p25 1), (p25 4), (p25 9)] },
  { start := p25 9, finish := p25 2, path := [(p25 9), (p25 4), (p25 1), (p25 11), (p25 10), (p25 14), (p25 19), (p25 17), (p25 16), (p25 15), (p25 5), (p25 7), (p25 2)] },
  { start := p25 10, finish := p25 16, path := [(p25 10), (p25 11), (p25 1), (p25 4), (p25 9), (p25 14), (p25 19), (p25 17), (p25 2), (p25 7), (p25 5), (p25 15), (p25 16)] },
  { start := p25 16, finish := p25 10, path := [(p25 16), (p25 15), (p25 5), (p25 7), (p25 2), (p25 17), (p25 19), (p25 14), (p25 9), (p25 4), (p25 1), (p25 11), (p25 10)] },
  { start := p25 5, finish := p25 14, path := [(p25 5), (p25 10), (p25 11), (p25 16), (p25 17), (p25 15), (p25 19), (p25 4), (p25 1), (p25 2), (p25 7), (p25 9), (p25 14)] },
  { start := p25 14, finish := p25 5, path := [(p25 14), (p25 9), (p25 7), (p25 2), (p25 1), (p25 4), (p25 19), (p25 15), (p25 17), (p25 16), (p25 11), (p25 10), (p25 5)] },
  { start := p25 1, finish := p25 17, path := [(p25 1), (p25 2), (p25 7), (p25 9), (p25 14), (p25 4), (p25 19), (p25 15), (p25 5), (p25 10), (p25 11), (p25 16), (p25 17)] },
  { start := p25 17, finish := p25 1, path := [(p25 17), (p25 16), (p25 11), (p25 10), (p25 5), (p25 15), (p25 19), (p25 4), (p25 14), (p25 9), (p25 7), (p25 2), (p25 1)] },
  { start := p25 7, finish := p25 4, path := [(p25 7), (p25 2), (p25 1), (p25 16), (p25 15), (p25 17), (p25 19), (p25 14), (p25 11), (p25 10), (p25 5), (p25 9), (p25 4)] },
  { start := p25 4, finish := p25 7, path := [(p25 4), (p25 9), (p25 5), (p25 10), (p25 11), (p25 14), (p25 19), (p25 17), (p25 15), (p25 16), (p25 1), (p25 2), (p25 7)] },
  { start := p25 11, finish := p25 15, path := [(p25 11), (p25 10), (p25 5), (p25 9), (p25 4), (p25 14), (p25 19), (p25 17), (p25 7), (p25 2), (p25 1), (p25 16), (p25 15)] },
  { start := p25 15, finish := p25 11, path := [(p25 15), (p25 16), (p25 1), (p25 2), (p25 7), (p25 17), (p25 19), (p25 14), (p25 4), (p25 9), (p25 5), (p25 10), (p25 11)] },
  { start := p25 10, finish := p25 9, path := [(p25 10), (p25 5), (p25 7), (p25 17), (p25 16), (p25 15), (p25 19), (p25 4), (p25 2), (p25 1), (p25 11), (p25 14), (p25 9)] },
  { start := p25 9, finish := p25 10, path := [(p25 9), (p25 14), (p25 11), (p25 1), (p25 2), (p25 4), (p25 19), (p25 15), (p25 16), (p25 17), (p25 7), (p25 5), (p25 10)] },
  { start := p25 2, finish := p25 16, path := [(p25 2), (p25 1), (p25 11), (p25 14), (p25 9), (p25 4), (p25 19), (p25 15), (p25 10), (p25 5), (p25 7), (p25 17), (p25 16)] },
  { start := p25 16, finish := p25 2, path := [(p25 16), (p25 17), (p25 7), (p25 5), (p25 10), (p25 15), (p25 19), (p25 4), (p25 9), (p25 14), (p25 11), (p25 1), (p25 2)] },
  { start := p25 11, finish := p25 4, path := [(p25 11), (p25 1), (p25 2), (p25 17), (p25 15), (p25 16), (p25 19), (p25 9), (p25 7), (p25 5), (p25 10), (p25 14), (p25 4)] },
  { start := p25 4, finish := p25 11, path := [(p25 4), (p25 14), (p25 10), (p25 5), (p25 7), (p25 9), (p25 19), (p25 16), (p25 15), (p25 17), (p25 2), (p25 1), (p25 11)] },
  { start := p25 7, finish := p25 15, path := [(p25 7), (p25 5), (p25 10), (p25 14), (p25 4), (p25 9), (p25 19), (p25 16), (p25 11), (p25 1), (p25 2), (p25 17), (p25 15)] },
  { start := p25 15, finish := p25 7, path := [(p25 15), (p25 17), (p25 2), (p25 1), (p25 11), (p25 16), (p25 19), (p25 9), (p25 4), (p25 14), (p25 10), (p25 5), (p25 7)] },
  { start := p25 1, finish := p25 19, path := [(p25 1), (p25 11), (p25 16), (p25 17), (p25 15), (p25 10), (p25 14), (p25 9), (p25 5), (p25 7), (p25 2), (p25 4), (p25 19)] },
  { start := p25 19, finish := p25 1, path := [(p25 19), (p25 4), (p25 2), (p25 7), (p25 5), (p25 9), (p25 14), (p25 10), (p25 15), (p25 17), (p25 16), (p25 11), (p25 1)] },
  { start := p25 5, finish := p25 19, path := [(p25 5), (p25 7), (p25 9), (p25 14), (p25 4), (p25 2), (p25 17), (p25 16), (p25 1), (p25 11), (p25 10), (p25 15), (p25 19)] },
  { start := p25 19, finish := p25 5, path := [(p25 19), (p25 15), (p25 10), (p25 11), (p25 1), (p25 16), (p25 17), (p25 2), (p25 4), (p25 14), (p25 9), (p25 7), (p25 5)] },
  { start := p25 2, finish := p25 19, path := [(p25 2), (p25 7), (p25 17), (p25 16), (p25 15), (p25 5), (p25 9), (p25 14), (p25 10), (p25 11), (p25 1), (p25 4), (p25 19)] },
  { start := p25 19, finish := p25 2, path := [(p25 19), (p25 4), (p25 1), (p25 11), (p25 10), (p25 14), (p25 9), (p25 5), (p25 15), (p25 16), (p25 17), (p25 7), (p25 2)] },
  { start := p25 10, finish := p25 19, path := [(p25 10), (p25 11), (p25 14), (p25 9), (p25 4), (p25 1), (p25 16), (p25 17), (p25 2), (p25 7), (p25 5), (p25 15), (p25 19)] },
  { start := p25 19, finish := p25 10, path := [(p25 19), (p25 15), (p25 5), (p25 7), (p25 2), (p25 17), (p25 16), (p25 1), (p25 4), (p25 9), (p25 14), (p25 11), (p25 10)] },
  { start := p25 7, finish := p25 19, path := [(p25 7), (p25 2), (p25 17), (p25 15), (p25 16), (p25 1), (p25 4), (p25 14), (p25 11), (p25 10), (p25 5), (p25 9), (p25 19)] },
  { start := p25 19, finish := p25 7, path := [(p25 19), (p25 9), (p25 5), (p25 10), (p25 11), (p25 14), (p25 4), (p25 1), (p25 16), (p25 15), (p25 17), (p25 2), (p25 7)] },
  { start := p25 11, finish := p25 19, path := [(p25 11), (p25 10), (p25 14), (p25 4), (p25 9), (p25 5), (p25 15), (p25 17), (p25 7), (p25 2), (p25 1), (p25 16), (p25 19)] },
  { start := p25 19, finish := p25 11, path := [(p25 19), (p25 16), (p25 1), (p25 2), (p25 7), (p25 17), (p25 15), (p25 5), (p25 9), (p25 4), (p25 14), (p25 10), (p25 11)] },
  { start := p25 4, finish := p25 9, path := [(p25 4), (p25 14), (p25 19), (p25 17), (p25 16), (p25 15), (p25 10), (p25 11), (p25 1), (p25 2), (p25 7), (p25 5), (p25 9)] },
  { start := p25 9, finish := p25 4, path := [(p25 9), (p25 5), (p25 7), (p25 2), (p25 1), (p25 11), (p25 10), (p25 15), (p25 16), (p25 17), (p25 19), (p25 14), (p25 4)] },
  { start := p25 15, finish := p25 16, path := [(p25 15), (p25 17), (p25 19), (p25 14), (p25 9), (p25 4), (p25 2), (p25 7), (p25 5), (p25 10), (p25 11), (p25 1), (p25 16)] },
  { start := p25 16, finish := p25 15, path := [(p25 16), (p25 1), (p25 11), (p25 10), (p25 5), (p25 7), (p25 2), (p25 4), (p25 9), (p25 14), (p25 19), (p25 17), (p25 15)] },
  { start := p25 4, finish := p25 14, path := [(p25 4), (p25 9), (p25 19), (p25 16), (p25 17), (p25 15), (p25 5), (p25 7), (p25 2), (p25 1), (p25 11), (p25 10), (p25 14)] },
  { start := p25 14, finish := p25 4, path := [(p25 14), (p25 10), (p25 11), (p25 1), (p25 2), (p25 7), (p25 5), (p25 15), (p25 17), (p25 16), (p25 19), (p25 9), (p25 4)] },
  { start := p25 15, finish := p25 17, path := [(p25 15), (p25 16), (p25 19), (p25 9), (p25 14), (p25 4), (p25 1), (p25 11), (p25 10), (p25 5), (p25 7), (p25 2), (p25 17)] },
  { start := p25 17, finish := p25 15, path := [(p25 17), (p25 2), (p25 7), (p25 5), (p25 10), (p25 11), (p25 1), (p25 4), (p25 14), (p25 9), (p25 19), (p25 16), (p25 15)] },
  { start := p25 9, finish := p25 14, path := [(p25 9), (p25 4), (p25 19), (p25 15), (p25 17), (p25 16), (p25 1), (p25 2), (p25 7), (p25 5), (p25 10), (p25 11), (p25 14)] },
  { start := p25 14, finish := p25 9, path := [(p25 14), (p25 11), (p25 10), (p25 5), (p25 7), (p25 2), (p25 1), (p25 16), (p25 17), (p25 15), (p25 19), (p25 4), (p25 9)] },
  { start := p25 16, finish := p25 17, path := [(p25 16), (p25 15), (p25 19), (p25 4), (p25 14), (p25 9), (p25 5), (p25 10), (p25 11), (p25 1), (p25 2), (p25 7), (p25 17)] },
  { start := p25 17, finish := p25 16, path := [(p25 17), (p25 7), (p25 2), (p25 1), (p25 11), (p25 10), (p25 5), (p25 9), (p25 14), (p25 4), (p25 19), (p25 15), (p25 16)] },
  { start := p25 4, finish := p25 15, path := [(p25 4), (p25 19), (p25 9), (p25 14), (p25 10), (p25 11), (p25 1), (p25 16), (p25 17), (p25 2), (p25 7), (p25 5), (p25 15)] },
  { start := p25 15, finish := p25 4, path := [(p25 15), (p25 5), (p25 7), (p25 2), (p25 17), (p25 16), (p25 1), (p25 11), (p25 10), (p25 14), (p25 9), (p25 19), (p25 4)] },
  { start := p25 9, finish := p25 16, path := [(p25 9), (p25 19), (p25 4), (p25 14), (p25 11), (p25 10), (p25 5), (p25 15), (p25 17), (p25 7), (p25 2), (p25 1), (p25 16)] },
  { start := p25 16, finish := p25 9, path := [(p25 16), (p25 1), (p25 2), (p25 7), (p25 17), (p25 15), (p25 5), (p25 10), (p25 11), (p25 14), (p25 4), (p25 19), (p25 9)] },
  { start := p25 14, finish := p25 17, path := [(p25 14), (p25 19), (p25 4), (p25 9), (p25 7), (p25 5), (p25 10), (p25 15), (p25 16), (p25 11), (p25 1), (p25 2), (p25 17)] },
  { start := p25 17, finish := p25 14, path := [(p25 17), (p25 2), (p25 1), (p25 11), (p25 16), (p25 15), (p25 10), (p25 5), (p25 7), (p25 9), (p25 4), (p25 19), (p25 14)] },
  { start := p25 4, finish := p25 16, path := [(p25 4), (p25 19), (p25 17), (p25 15), (p25 10), (p25 11), (p25 14), (p25 9), (p25 5), (p25 7), (p25 2), (p25 1), (p25 16)] },
  { start := p25 16, finish := p25 4, path := [(p25 16), (p25 1), (p25 2), (p25 7), (p25 5), (p25 9), (p25 14), (p25 11), (p25 10), (p25 15), (p25 17), (p25 19), (p25 4)] },
  { start := p25 15, finish := p25 9, path := [(p25 15), (p25 19), (p25 14), (p25 4), (p25 2), (p25 7), (p25 17), (p25 16), (p25 1), (p25 11), (p25 10), (p25 5), (p25 9)] },
  { start := p25 9, finish := p25 15, path := [(p25 9), (p25 5), (p25 10), (p25 11), (p25 1), (p25 16), (p25 17), (p25 7), (p25 2), (p25 4), (p25 14), (p25 19), (p25 15)] },
  { start := p25 4, finish := p25 17, path := [(p25 4), (p25 19), (p25 16), (p25 15), (p25 5), (p25 7), (p25 9), (p25 14), (p25 10), (p25 11), (p25 1), (p25 2), (p25 17)] },
  { start := p25 17, finish := p25 4, path := [(p25 17), (p25 2), (p25 1), (p25 11), (p25 10), (p25 14), (p25 9), (p25 7), (p25 5), (p25 15), (p25 16), (p25 19), (p25 4)] },
  { start := p25 15, finish := p25 14, path := [(p25 15), (p25 19), (p25 9), (p25 4), (p25 1), (p25 11), (p25 16), (p25 17), (p25 2), (p25 7), (p25 5), (p25 10), (p25 14)] },
  { start := p25 14, finish := p25 15, path := [(p25 14), (p25 10), (p25 5), (p25 7), (p25 2), (p25 17), (p25 16), (p25 11), (p25 1), (p25 4), (p25 9), (p25 19), (p25 15)] },
  { start := p25 9, finish := p25 17, path := [(p25 9), (p25 19), (p25 15), (p25 16), (p25 1), (p25 2), (p25 4), (p25 14), (p25 11), (p25 10), (p25 5), (p25 7), (p25 17)] },
  { start := p25 17, finish := p25 9, path := [(p25 17), (p25 7), (p25 5), (p25 10), (p25 11), (p25 14), (p25 4), (p25 2), (p25 1), (p25 16), (p25 15), (p25 19), (p25 9)] },
  { start := p25 16, finish := p25 14, path := [(p25 16), (p25 19), (p25 4), (p25 9), (p25 5), (p25 10), (p25 15), (p25 17), (p25 7), (p25 2), (p25 1), (p25 11), (p25 14)] },
  { start := p25 14, finish := p25 16, path := [(p25 14), (p25 11), (p25 1), (p25 2), (p25 7), (p25 17), (p25 15), (p25 10), (p25 5), (p25 9), (p25 4), (p25 19), (p25 16)] },
  { start := p25 4, finish := p25 19, path := [(p25 4), (p25 14), (p25 10), (p25 15), (p25 17), (p25 16), (p25 11), (p25 1), (p25 2), (p25 7), (p25 5), (p25 9), (p25 19)] },
  { start := p25 19, finish := p25 4, path := [(p25 19), (p25 9), (p25 5), (p25 7), (p25 2), (p25 1), (p25 11), (p25 16), (p25 17), (p25 15), (p25 10), (p25 14), (p25 4)] },
  { start := p25 15, finish := p25 19, path := [(p25 15), (p25 17), (p25 2), (p25 4), (p25 14), (p25 9), (p25 7), (p25 5), (p25 10), (p25 11), (p25 1), (p25 16), (p25 19)] },
  { start := p25 19, finish := p25 15, path := [(p25 19), (p25 16), (p25 1), (p25 11), (p25 10), (p25 5), (p25 7), (p25 9), (p25 14), (p25 4), (p25 2), (p25 17), (p25 15)] },
  { start := p25 9, finish := p25 19, path := [(p25 9), (p25 14), (p25 11), (p25 16), (p25 17), (p25 15), (p25 10), (p25 5), (p25 7), (p25 2), (p25 1), (p25 4), (p25 19)] },
  { start := p25 19, finish := p25 9, path := [(p25 19), (p25 4), (p25 1), (p25 2), (p25 7), (p25 5), (p25 10), (p25 15), (p25 17), (p25 16), (p25 11), (p25 14), (p25 9)] },
  { start := p25 16, finish := p25 19, path := [(p25 16), (p25 17), (p25 7), (p25 9), (p25 14), (p25 4), (p25 2), (p25 1), (p25 11), (p25 10), (p25 5), (p25 15), (p25 19)] },
  { start := p25 19, finish := p25 16, path := [(p25 19), (p25 15), (p25 5), (p25 10), (p25 11), (p25 1), (p25 2), (p25 4), (p25 14), (p25 9), (p25 7), (p25 17), (p25 16)] },
  { start := p25 14, finish := p25 19, path := [(p25 14), (p25 9), (p25 7), (p25 17), (p25 16), (p25 15), (p25 5), (p25 10), (p25 11), (p25 1), (p25 2), (p25 4), (p25 19)] },
  { start := p25 19, finish := p25 14, path := [(p25 19), (p25 4), (p25 2), (p25 1), (p25 11), (p25 10), (p25 5), (p25 15), (p25 16), (p25 17), (p25 7), (p25 9), (p25 14)] },
  { start := p25 17, finish := p25 19, path := [(p25 17), (p25 16), (p25 11), (p25 14), (p25 9), (p25 4), (p25 1), (p25 2), (p25 7), (p25 5), (p25 10), (p25 15), (p25 19)] },
  { start := p25 19, finish := p25 17, path := [(p25 19), (p25 15), (p25 10), (p25 5), (p25 7), (p25 2), (p25 1), (p25 4), (p25 9), (p25 14), (p25 11), (p25 16), (p25 17)] },
]
def pairFivePath444 : List PairFiveEntry := [
  { start := p25 1, finish := p25 2, path := [(p25 1), (p25 16), (p25 11), (p25 13), (p25 10), (p25 15), (p25 17), (p25 7), (p25 5), (p25 8), (p25 3), (p25 2)] },
  { start := p25 2, finish := p25 1, path := [(p25 2), (p25 3), (p25 8), (p25 5), (p25 7), (p25 17), (p25 15), (p25 10), (p25 13), (p25 11), (p25 16), (p25 1)] },
  { start := p25 5, finish := p25 10, path := [(p25 5), (p25 8), (p25 7), (p25 17), (p25 2), (p25 3), (p25 13), (p25 11), (p25 1), (p25 16), (p25 15), (p25 10)] },
  { start := p25 10, finish := p25 5, path := [(p25 10), (p25 15), (p25 16), (p25 1), (p25 11), (p25 13), (p25 3), (p25 2), (p25 17), (p25 7), (p25 8), (p25 5)] },
  { start := p25 1, finish := p25 3, path := [(p25 1), (p25 11), (p25 16), (p25 17), (p25 15), (p25 10), (p25 13), (p25 8), (p25 5), (p25 7), (p25 2), (p25 3)] },
  { start := p25 3, finish := p25 1, path := [(p25 3), (p25 2), (p25 7), (p25 5), (p25 8), (p25 13), (p25 10), (p25 15), (p25 17), (p25 16), (p25 11), (p25 1)] },
  { start := p25 5, finish := p25 15, path := [(p25 5), (p25 7), (p25 8), (p25 13), (p25 3), (p25 2), (p25 17), (p25 16), (p25 1), (p25 11), (p25 10), (p25 15)] },
  { start := p25 15, finish := p25 5, path := [(p25 15), (p25 10), (p25 11), (p25 1), (p25 16), (p25 17), (p25 2), (p25 3), (p25 13), (p25 8), (p25 7), (p25 5)] },
  { start := p25 2, finish := p25 3, path := [(p25 2), (p25 7), (p25 17), (p25 16), (p25 15), (p25 5), (p25 8), (p25 13), (p25 10), (p25 11), (p25 1), (p25 3)] },
  { start := p25 3, finish := p25 2, path := [(p25 3), (p25 1), (p25 11), (p25 10), (p25 13), (p25 8), (p25 5), (p25 15), (p25 16), (p25 17), (p25 7), (p25 2)] },
  { start := p25 10, finish := p25 15, path := [(p25 10), (p25 11), (p25 13), (p25 8), (p25 3), (p25 1), (p25 16), (p25 17), (p25 2), (p25 7), (p25 5), (p25 15)] },
  { start := p25 15, finish := p25 10, path := [(p25 15), (p25 5), (p25 7), (p25 2), (p25 17), (p25 16), (p25 1), (p25 3), (p25 8), (p25 13), (p25 11), (p25 10)] },
  { start := p25 5, finish := p25 7, path := [(p25 5), (p25 15), (p25 10), (p25 13), (p25 11), (p25 16), (p25 17), (p25 2), (p25 1), (p25 3), (p25 8), (p25 7)] },
  { start := p25 7, finish := p25 5, path := [(p25 7), (p25 8), (p25 3), (p25 1), (p25 2), (p25 17), (p25 16), (p25 11), (p25 13), (p25 10), (p25 15), (p25 5)] },
  { start := p25 1, finish := p25 11, path := [(p25 1), (p25 3), (p25 2), (p25 17), (p25 7), (p25 8), (p25 13), (p25 10), (p25 5), (p25 15), (p25 16), (p25 11)] },
  { start := p25 11, finish := p25 1, path := [(p25 11), (p25 16), (p25 15), (p25 5), (p25 10), (p25 13), (p25 8), (p25 7), (p25 17), (p25 2), (p25 3), (p25 1)] },
  { start := p25 5, finish := p25 8, path := [(p25 5), (p25 10), (p25 15), (p25 17), (p25 16), (p25 11), (p25 13), (p25 3), (p25 1), (p25 2), (p25 7), (p25 8)] },
  { start := p25 8, finish := p25 5, path := [(p25 8), (p25 7), (p25 2), (p25 1), (p25 3), (p25 13), (p25 11), (p25 16), (p25 17), (p25 15), (p25 10), (p25 5)] },
  { start := p25 1, finish := p25 16, path := [(p25 1), (p25 2), (p25 3), (p25 13), (p25 8), (p25 7), (p25 17), (p25 15), (p25 5), (p25 10), (p25 11), (p25 16)] },
  { start := p25 16, finish := p25 1, path := [(p25 16), (p25 11), (p25 10), (p25 5), (p25 15), (p25 17), (p25 7), (p25 8), (p25 13), (p25 3), (p25 2), (p25 1)] },
  { start := p25 7, finish := p25 8, path := [(p25 7), (p25 2), (p25 17), (p25 15), (p25 16), (p25 1), (p25 3), (p25 13), (p25 11), (p25 10), (p25 5), (p25 8)] },
  { start := p25 8, finish := p25 7, path := [(p25 8), (p25 5), (p25 10), (p25 11), (p25 13), (p25 3), (p25 1), (p25 16), (p25 15), (p25 17), (p25 2), (p25 7)] },
  { start := p25 11, finish := p25 16, path := [(p25 11), (p25 10), (p25 13), (p25 3), (p25 8), (p25 5), (p25 15), (p25 17), (p25 7), (p25 2), (p25 1), (p25 16)] },
  { start := p25 16, finish := p25 11, path := [(p25 16), (p25 1), (p25 2), (p25 7), (p25 17), (p25 15), (p25 5), (p25 8), (p25 3), (p25 13), (p25 10), (p25 11)] },
  { start := p25 10, finish := p25 11, path := [(p25 10), (p25 15), (p25 5), (p25 8), (p25 7), (p25 17), (p25 16), (p25 1), (p25 2), (p25 3), (p25 13), (p25 11)] },
  { start := p25 11, finish := p25 10, path := [(p25 11), (p25 13), (p25 3), (p25 2), (p25 1), (p25 16), (p25 17), (p25 7), (p25 8), (p25 5), (p25 15), (p25 10)] },
  { start := p25 2, finish := p25 7, path := [(p25 2), (p25 3), (p25 1), (p25 16), (p25 11), (p25 13), (p25 8), (p25 5), (p25 10), (p25 15), (p25 17), (p25 7)] },
  { start := p25 7, finish := p25 2, path := [(p25 7), (p25 17), (p25 15), (p25 10), (p25 5), (p25 8), (p25 13), (p25 11), (p25 16), (p25 1), (p25 3), (p25 2)] },
  { start := p25 10, finish := p25 13, path := [(p25 10), (p25 5), (p25 15), (p25 16), (p25 17), (p25 7), (p25 8), (p25 3), (p25 2), (p25 1), (p25 11), (p25 13)] },
  { start := p25 13, finish := p25 10, path := [(p25 13), (p25 11), (p25 1), (p25 2), (p25 3), (p25 8), (p25 7), (p25 17), (p25 16), (p25 15), (p25 5), (p25 10)] },
  { start := p25 2, finish := p25 17, path := [(p25 2), (p25 1), (p25 3), (p25 8), (p25 13), (p25 11), (p25 16), (p25 15), (p25 10), (p25 5), (p25 7), (p25 17)] },
  { start := p25 17, finish := p25 2, path := [(p25 17), (p25 7), (p25 5), (p25 10), (p25 15), (p25 16), (p25 11), (p25 13), (p25 8), (p25 3), (p25 1), (p25 2)] },
  { start := p25 11, finish := p25 13, path := [(p25 11), (p25 1), (p25 16), (p25 15), (p25 17), (p25 2), (p25 3), (p25 8), (p25 7), (p25 5), (p25 10), (p25 13)] },
  { start := p25 13, finish := p25 11, path := [(p25 13), (p25 10), (p25 5), (p25 7), (p25 8), (p25 3), (p25 2), (p25 17), (p25 15), (p25 16), (p25 1), (p25 11)] },
  { start := p25 7, finish := p25 17, path := [(p25 7), (p25 5), (p25 8), (p25 3), (p25 13), (p25 10), (p25 15), (p25 16), (p25 11), (p25 1), (p25 2), (p25 17)] },
  { start := p25 17, finish := p25 7, path := [(p25 17), (p25 2), (p25 1), (p25 11), (p25 16), (p25 15), (p25 10), (p25 13), (p25 3), (p25 8), (p25 5), (p25 7)] },
  { start := p25 15, finish := p25 16, path := [(p25 15), (p25 10), (p25 5), (p25 7), (p25 8), (p25 13), (p25 11), (p25 1), (p25 3), (p25 2), (p25 17), (p25 16)] },
  { start := p25 16, finish := p25 15, path := [(p25 16), (p25 17), (p25 2), (p25 3), (p25 1), (p25 11), (p25 13), (p25 8), (p25 7), (p25 5), (p25 10), (p25 15)] },
  { start := p25 3, finish := p25 8, path := [(p25 3), (p25 2), (p25 1), (p25 11), (p25 16), (p25 17), (p25 7), (p25 5), (p25 15), (p25 10), (p25 13), (p25 8)] },
  { start := p25 8, finish := p25 3, path := [(p25 8), (p25 13), (p25 10), (p25 15), (p25 5), (p25 7), (p25 17), (p25 16), (p25 11), (p25 1), (p25 2), (p25 3)] },
  { start := p25 15, finish := p25 17, path := [(p25 15), (p25 5), (p25 10), (p25 11), (p25 13), (p25 8), (p25 7), (p25 2), (p25 3), (p25 1), (p25 16), (p25 17)] },
  { start := p25 17, finish := p25 15, path := [(p25 17), (p25 16), (p25 1), (p25 3), (p25 2), (p25 7), (p25 8), (p25 13), (p25 11), (p25 10), (p25 5), (p25 15)] },
  { start := p25 3, finish := p25 13, path := [(p25 3), (p25 1), (p25 2), (p25 7), (p25 17), (p25 16), (p25 11), (p25 10), (p25 15), (p25 5), (p25 8), (p25 13)] },
  { start := p25 13, finish := p25 3, path := [(p25 13), (p25 8), (p25 5), (p25 15), (p25 10), (p25 11), (p25 16), (p25 17), (p25 7), (p25 2), (p25 1), (p25 3)] },
  { start := p25 16, finish := p25 17, path := [(p25 16), (p25 1), (p25 11), (p25 10), (p25 13), (p25 3), (p25 2), (p25 7), (p25 8), (p25 5), (p25 15), (p25 17)] },
  { start := p25 17, finish := p25 16, path := [(p25 17), (p25 15), (p25 5), (p25 8), (p25 7), (p25 2), (p25 3), (p25 13), (p25 10), (p25 11), (p25 1), (p25 16)] },
  { start := p25 8, finish := p25 13, path := [(p25 8), (p25 5), (p25 7), (p25 2), (p25 17), (p25 15), (p25 10), (p25 11), (p25 16), (p25 1), (p25 3), (p25 13)] },
  { start := p25 13, finish := p25 8, path := [(p25 13), (p25 3), (p25 1), (p25 16), (p25 11), (p25 10), (p25 15), (p25 17), (p25 2), (p25 7), (p25 5), (p25 8)] },
  { start := p25 1, finish := p25 5, path := [(p25 1), (p25 11), (p25 16), (p25 17), (p25 15), (p25 10), (p25 13), (p25 8), (p25 3), (p25 2), (p25 7), (p25 5)] },
  { start := p25 5, finish := p25 1, path := [(p25 5), (p25 7), (p25 2), (p25 3), (p25 8), (p25 13), (p25 10), (p25 15), (p25 17), (p25 16), (p25 11), (p25 1)] },
  { start := p25 2, finish := p25 10, path := [(p25 2), (p25 7), (p25 17), (p25 16), (p25 15), (p25 5), (p25 8), (p25 13), (p25 3), (p25 1), (p25 11), (p25 10)] },
  { start := p25 10, finish := p25 2, path := [(p25 10), (p25 11), (p25 1), (p25 3), (p25 13), (p25 8), (p25 5), (p25 15), (p25 16), (p25 17), (p25 7), (p25 2)] },
  { start := p25 3, finish := p25 15, path := [(p25 3), (p25 8), (p25 13), (p25 11), (p25 10), (p25 5), (p25 7), (p25 17), (p25 2), (p25 1), (p25 16), (p25 15)] },
  { start := p25 15, finish := p25 3, path := [(p25 15), (p25 16), (p25 1), (p25 2), (p25 17), (p25 7), (p25 5), (p25 10), (p25 11), (p25 13), (p25 8), (p25 3)] },
  { start := p25 7, finish := p25 11, path := [(p25 7), (p25 2), (p25 17), (p25 15), (p25 16), (p25 1), (p25 3), (p25 13), (p25 8), (p25 5), (p25 10), (p25 11)] },
  { start := p25 11, finish := p25 7, path := [(p25 11), (p25 10), (p25 5), (p25 8), (p25 13), (p25 3), (p25 1), (p25 16), (p25 15), (p25 17), (p25 2), (p25 7)] },
  { start := p25 8, finish := p25 16, path := [(p25 8), (p25 3), (p25 13), (p25 10), (p25 11), (p25 1), (p25 2), (p25 17), (p25 7), (p25 5), (p25 15), (p25 16)] },
  { start := p25 16, finish := p25 8, path := [(p25 16), (p25 15), (p25 5), (p25 7), (p25 17), (p25 2), (p25 1), (p25 11), (p25 10), (p25 13), (p25 3), (p25 8)] },
  { start := p25 13, finish := p25 17, path := [(p25 13), (p25 3), (p25 8), (p25 5), (p25 7), (p25 2), (p25 1), (p25 16), (p25 11), (p25 10), (p25 15), (p25 17)] },
  { start := p25 17, finish := p25 13, path := [(p25 17), (p25 15), (p25 10), (p25 11), (p25 16), (p25 1), (p25 2), (p25 7), (p25 5), (p25 8), (p25 3), (p25 13)] },
  { start := p25 1, finish := p25 7, path := [(p25 1), (p25 11), (p25 16), (p25 17), (p25 15), (p25 5), (p25 10), (p25 13), (p25 8), (p25 3), (p25 2), (p25 7)] },
  { start := p25 7, finish := p25 1, path := [(p25 7), (p25 2), (p25 3), (p25 8), (p25 13), (p25 10), (p25 5), (p25 15), (p25 17), (p25 16), (p25 11), (p25 1)] },
  { start := p25 5, finish := p25 11, path := [(p25 5), (p25 7), (p25 8), (p25 13), (p25 3), (p25 1), (p25 2), (p25 17), (p25 16), (p25 15), (p25 10), (p25 11)] },
  { start := p25 11, finish := p25 5, path := [(p25 11), (p25 10), (p25 15), (p25 16), (p25 17), (p25 2), (p25 1), (p25 3), (p25 13), (p25 8), (p25 7), (p25 5)] },
  { start := p25 1, finish := p25 8, path := [(p25 1), (p25 16), (p25 11), (p25 13), (p25 10), (p25 5), (p25 15), (p25 17), (p25 7), (p25 2), (p25 3), (p25 8)] },
  { start := p25 8, finish := p25 1, path := [(p25 8), (p25 3), (p25 2), (p25 7), (p25 17), (p25 15), (p25 5), (p25 10), (p25 13), (p25 11), (p25 16), (p25 1)] },
  { start := p25 5, finish := p25 16, path := [(p25 5), (p25 8), (p25 7), (p25 17), (p25 2), (p25 1), (p25 3), (p25 13), (p25 11), (p25 10), (p25 15), (p25 16)] },
  { start := p25 16, finish := p25 5, path := [(p25 16), (p25 15), (p25 10), (p25 11), (p25 13), (p25 3), (p25 1), (p25 2), (p25 17), (p25 7), (p25 8), (p25 5)] },
  { start := p25 2, finish := p25 11, path := [(p25 2), (p25 7), (p25 17), (p25 16), (p25 15), (p25 10), (p25 5), (p25 8), (p25 13), (p25 3), (p25 1), (p25 11)] },
  { start := p25 11, finish := p25 2, path := [(p25 11), (p25 1), (p25 3), (p25 13), (p25 8), (p25 5), (p25 10), (p25 15), (p25 16), (p25 17), (p25 7), (p25 2)] },
  { start := p25 10, finish := p25 7, path := [(p25 10), (p25 11), (p25 13), (p25 8), (p25 3), (p25 2), (p25 1), (p25 16), (p25 17), (p25 15), (p25 5), (p25 7)] },
  { start := p25 7, finish := p25 10, path := [(p25 7), (p25 5), (p25 15), (p25 17), (p25 16), (p25 1), (p25 2), (p25 3), (p25 8), (p25 13), (p25 11), (p25 10)] },
  { start := p25 2, finish := p25 13, path := [(p25 2), (p25 17), (p25 7), (p25 8), (p25 5), (p25 10), (p25 15), (p25 16), (p25 11), (p25 1), (p25 3), (p25 13)] },
  { start := p25 13, finish := p25 2, path := [(p25 13), (p25 3), (p25 1), (p25 11), (p25 16), (p25 15), (p25 10), (p25 5), (p25 8), (p25 7), (p25 17), (p25 2)] },
  { start := p25 10, finish := p25 17, path := [(p25 10), (p25 13), (p25 11), (p25 16), (p25 1), (p25 2), (p25 3), (p25 8), (p25 7), (p25 5), (p25 15), (p25 17)] },
  { start := p25 17, finish := p25 10, path := [(p25 17), (p25 15), (p25 5), (p25 7), (p25 8), (p25 3), (p25 2), (p25 1), (p25 16), (p25 11), (p25 13), (p25 10)] },
  { start := p25 3, finish := p25 16, path := [(p25 3), (p25 8), (p25 13), (p25 11), (p25 10), (p25 15), (p25 5), (p25 7), (p25 17), (p25 2), (p25 1), (p25 16)] },
  { start := p25 16, finish := p25 3, path := [(p25 16), (p25 1), (p25 2), (p25 17), (p25 7), (p25 5), (p25 15), (p25 10), (p25 11), (p25 13), (p25 8), (p25 3)] },
  { start := p25 15, finish := p25 8, path := [(p25 15), (p25 16), (p25 17), (p25 7), (p25 2), (p25 3), (p25 1), (p25 11), (p25 13), (p25 10), (p25 5), (p25 8)] },
  { start := p25 8, finish := p25 15, path := [(p25 8), (p25 5), (p25 10), (p25 13), (p25 11), (p25 1), (p25 3), (p25 2), (p25 7), (p25 17), (p25 16), (p25 15)] },
  { start := p25 3, finish := p25 17, path := [(p25 3), (p25 13), (p25 8), (p25 7), (p25 5), (p25 15), (p25 10), (p25 11), (p25 16), (p25 1), (p25 2), (p25 17)] },
  { start := p25 17, finish := p25 3, path := [(p25 17), (p25 2), (p25 1), (p25 16), (p25 11), (p25 10), (p25 15), (p25 5), (p25 7), (p25 8), (p25 13), (p25 3)] },
  { start := p25 15, finish := p25 13, path := [(p25 15), (p25 17), (p25 16), (p25 11), (p25 1), (p25 3), (p25 2), (p25 7), (p25 8), (p25 5), (p25 10), (p25 13)] },
  { start := p25 13, finish := p25 15, path := [(p25 13), (p25 10), (p25 5), (p25 8), (p25 7), (p25 2), (p25 3), (p25 1), (p25 11), (p25 16), (p25 17), (p25 15)] },
  { start := p25 5, finish := p25 2, path := [(p25 5), (p25 10), (p25 15), (p25 17), (p25 16), (p25 1), (p25 11), (p25 13), (p25 3), (p25 8), (p25 7), (p25 2)] },
  { start := p25 2, finish := p25 5, path := [(p25 2), (p25 7), (p25 8), (p25 3), (p25 13), (p25 11), (p25 1), (p25 16), (p25 17), (p25 15), (p25 10), (p25 5)] },
  { start := p25 1, finish := p25 10, path := [(p25 1), (p25 2), (p25 3), (p25 13), (p25 8), (p25 5), (p25 7), (p25 17), (p25 15), (p25 16), (p25 11), (p25 10)] },
  { start := p25 10, finish := p25 1, path := [(p25 10), (p25 11), (p25 16), (p25 15), (p25 17), (p25 7), (p25 5), (p25 8), (p25 13), (p25 3), (p25 2), (p25 1)] },
  { start := p25 5, finish := p25 3, path := [(p25 5), (p25 15), (p25 10), (p25 13), (p25 11), (p25 1), (p25 16), (p25 17), (p25 2), (p25 7), (p25 8), (p25 3)] },
  { start := p25 3, finish := p25 5, path := [(p25 3), (p25 8), (p25 7), (p25 2), (p25 17), (p25 16), (p25 1), (p25 11), (p25 13), (p25 10), (p25 15), (p25 5)] },
  { start := p25 1, finish := p25 15, path := [(p25 1), (p25 3), (p25 2), (p25 17), (p25 7), (p25 5), (p25 8), (p25 13), (p25 10), (p25 11), (p25 16), (p25 15)] },
  { start := p25 15, finish := p25 1, path := [(p25 15), (p25 16), (p25 11), (p25 10), (p25 13), (p25 8), (p25 5), (p25 7), (p25 17), (p25 2), (p25 3), (p25 1)] },
  { start := p25 7, finish := p25 13, path := [(p25 7), (p25 17), (p25 2), (p25 3), (p25 1), (p25 11), (p25 16), (p25 15), (p25 10), (p25 5), (p25 8), (p25 13)] },
  { start := p25 13, finish := p25 7, path := [(p25 13), (p25 8), (p25 5), (p25 10), (p25 15), (p25 16), (p25 11), (p25 1), (p25 3), (p25 2), (p25 17), (p25 7)] },
  { start := p25 11, finish := p25 17, path := [(p25 11), (p25 13), (p25 10), (p25 15), (p25 5), (p25 7), (p25 8), (p25 3), (p25 2), (p25 1), (p25 16), (p25 17)] },
  { start := p25 17, finish := p25 11, path := [(p25 17), (p25 16), (p25 1), (p25 2), (p25 3), (p25 8), (p25 7), (p25 5), (p25 15), (p25 10), (p25 13), (p25 11)] },
  { start := p25 8, finish := p25 17, path := [(p25 8), (p25 13), (p25 3), (p25 2), (p25 1), (p25 16), (p25 11), (p25 10), (p25 15), (p25 5), (p25 7), (p25 17)] },
  { start := p25 17, finish := p25 8, path := [(p25 17), (p25 7), (p25 5), (p25 15), (p25 10), (p25 11), (p25 16), (p25 1), (p25 2), (p25 3), (p25 13), (p25 8)] },
  { start := p25 16, finish := p25 13, path := [(p25 16), (p25 17), (p25 15), (p25 10), (p25 5), (p25 8), (p25 7), (p25 2), (p25 3), (p25 1), (p25 11), (p25 13)] },
  { start := p25 13, finish := p25 16, path := [(p25 13), (p25 11), (p25 1), (p25 3), (p25 2), (p25 7), (p25 8), (p25 5), (p25 10), (p25 15), (p25 17), (p25 16)] },
  { start := p25 10, finish := p25 3, path := [(p25 10), (p25 15), (p25 5), (p25 8), (p25 7), (p25 2), (p25 17), (p25 16), (p25 1), (p25 11), (p25 13), (p25 3)] },
  { start := p25 3, finish := p25 10, path := [(p25 3), (p25 13), (p25 11), (p25 1), (p25 16), (p25 17), (p25 2), (p25 7), (p25 8), (p25 5), (p25 15), (p25 10)] },
  { start := p25 2, finish := p25 15, path := [(p25 2), (p25 3), (p25 1), (p25 16), (p25 11), (p25 10), (p25 13), (p25 8), (p25 5), (p25 7), (p25 17), (p25 15)] },
  { start := p25 15, finish := p25 2, path := [(p25 15), (p25 17), (p25 7), (p25 5), (p25 8), (p25 13), (p25 10), (p25 11), (p25 16), (p25 1), (p25 3), (p25 2)] },
  { start := p25 11, finish := p25 8, path := [(p25 11), (p25 16), (p25 1), (p25 3), (p25 2), (p25 7), (p25 17), (p25 15), (p25 5), (p25 10), (p25 13), (p25 8)] },
  { start := p25 8, finish := p25 11, path := [(p25 8), (p25 13), (p25 10), (p25 5), (p25 15), (p25 17), (p25 7), (p25 2), (p25 3), (p25 1), (p25 16), (p25 11)] },
  { start := p25 7, finish := p25 16, path := [(p25 7), (p25 8), (p25 5), (p25 15), (p25 10), (p25 11), (p25 13), (p25 3), (p25 1), (p25 2), (p25 17), (p25 16)] },
  { start := p25 16, finish := p25 7, path := [(p25 16), (p25 17), (p25 2), (p25 1), (p25 3), (p25 13), (p25 11), (p25 10), (p25 15), (p25 5), (p25 8), (p25 7)] },
  { start := p25 1, finish := p25 13, path := [(p25 1), (p25 11), (p25 16), (p25 17), (p25 15), (p25 10), (p25 5), (p25 8), (p25 7), (p25 2), (p25 3), (p25 13)] },
  { start := p25 13, finish := p25 1, path := [(p25 13), (p25 3), (p25 2), (p25 7), (p25 8), (p25 5), (p25 10), (p25 15), (p25 17), (p25 16), (p25 11), (p25 1)] },
  { start := p25 5, finish := p25 17, path := [(p25 5), (p25 7), (p25 8), (p25 13), (p25 3), (p25 2), (p25 1), (p25 16), (p25 11), (p25 10), (p25 15), (p25 17)] },
  { start := p25 17, finish := p25 5, path := [(p25 17), (p25 15), (p25 10), (p25 11), (p25 16), (p25 1), (p25 2), (p25 3), (p25 13), (p25 8), (p25 7), (p25 5)] },
  { start := p25 1, finish := p25 17, path := [(p25 1), (p25 16), (p25 11), (p25 13), (p25 10), (p25 15), (p25 5), (p25 7), (p25 8), (p25 3), (p25 2), (p25 17)] },
  { start := p25 17, finish := p25 1, path := [(p25 17), (p25 2), (p25 3), (p25 8), (p25 7), (p25 5), (p25 15), (p25 10), (p25 13), (p25 11), (p25 16), (p25 1)] },
  { start := p25 5, finish := p25 13, path := [(p25 5), (p25 8), (p25 7), (p25 17), (p25 2), (p25 3), (p25 1), (p25 11), (p25 16), (p25 15), (p25 10), (p25 13)] },
  { start := p25 13, finish := p25 5, path := [(p25 13), (p25 10), (p25 15), (p25 16), (p25 11), (p25 1), (p25 3), (p25 2), (p25 17), (p25 7), (p25 8), (p25 5)] },
  { start := p25 2, finish := p25 8, path := [(p25 2), (p25 7), (p25 17), (p25 16), (p25 15), (p25 5), (p25 10), (p25 13), (p25 11), (p25 1), (p25 3), (p25 8)] },
  { start := p25 8, finish := p25 2, path := [(p25 8), (p25 3), (p25 1), (p25 11), (p25 13), (p25 10), (p25 5), (p25 15), (p25 16), (p25 17), (p25 7), (p25 2)] },
  { start := p25 10, finish := p25 16, path := [(p25 10), (p25 11), (p25 13), (p25 8), (p25 3), (p25 1), (p25 2), (p25 17), (p25 7), (p25 5), (p25 15), (p25 16)] },
  { start := p25 16, finish := p25 10, path := [(p25 16), (p25 15), (p25 5), (p25 7), (p25 17), (p25 2), (p25 1), (p25 3), (p25 8), (p25 13), (p25 11), (p25 10)] },
  { start := p25 2, finish := p25 16, path := [(p25 2), (p25 17), (p25 7), (p25 8), (p25 5), (p25 15), (p25 10), (p25 11), (p25 13), (p25 3), (p25 1), (p25 16)] },
  { start := p25 16, finish := p25 2, path := [(p25 16), (p25 1), (p25 3), (p25 13), (p25 11), (p25 10), (p25 15), (p25 5), (p25 8), (p25 7), (p25 17), (p25 2)] },
  { start := p25 10, finish := p25 8, path := [(p25 10), (p25 13), (p25 11), (p25 16), (p25 1), (p25 3), (p25 2), (p25 7), (p25 17), (p25 15), (p25 5), (p25 8)] },
  { start := p25 8, finish := p25 10, path := [(p25 8), (p25 5), (p25 15), (p25 17), (p25 7), (p25 2), (p25 3), (p25 1), (p25 16), (p25 11), (p25 13), (p25 10)] },
  { start := p25 3, finish := p25 7, path := [(p25 3), (p25 8), (p25 13), (p25 11), (p25 10), (p25 5), (p25 15), (p25 17), (p25 16), (p25 1), (p25 2), (p25 7)] },
  { start := p25 7, finish := p25 3, path := [(p25 7), (p25 2), (p25 1), (p25 16), (p25 17), (p25 15), (p25 5), (p25 10), (p25 11), (p25 13), (p25 8), (p25 3)] },
  { start := p25 15, finish := p25 11, path := [(p25 15), (p25 16), (p25 17), (p25 7), (p25 2), (p25 1), (p25 3), (p25 13), (p25 8), (p25 5), (p25 10), (p25 11)] },
  { start := p25 11, finish := p25 15, path := [(p25 11), (p25 10), (p25 5), (p25 8), (p25 13), (p25 3), (p25 1), (p25 2), (p25 7), (p25 17), (p25 16), (p25 15)] },
  { start := p25 3, finish := p25 11, path := [(p25 3), (p25 13), (p25 8), (p25 7), (p25 5), (p25 10), (p25 15), (p25 16), (p25 17), (p25 2), (p25 1), (p25 11)] },
  { start := p25 11, finish := p25 3, path := [(p25 11), (p25 1), (p25 2), (p25 17), (p25 16), (p25 15), (p25 10), (p25 5), (p25 7), (p25 8), (p25 13), (p25 3)] },
  { start := p25 15, finish := p25 7, path := [(p25 15), (p25 17), (p25 16), (p25 11), (p25 1), (p25 2), (p25 3), (p25 8), (p25 13), (p25 10), (p25 5), (p25 7)] },
  { start := p25 7, finish := p25 15, path := [(p25 7), (p25 5), (p25 10), (p25 13), (p25 8), (p25 3), (p25 2), (p25 1), (p25 11), (p25 16), (p25 17), (p25 15)] },
]

def pairFiveTable (kind : Nat) : List PairFiveEntry :=
  match kind with
  | 0 => pairFiveCycle331 | 1 => pairFiveCycle332 | 2 => pairFiveCycle333
  | 3 => pairFiveCycle342 | 4 => pairFiveCycle343 | 5 => pairFiveCycle443
  | _ => pairFiveCycle444
def pairFiveEndpointTable (kind : Nat) : List PairFiveEntry :=
  match kind with
  | 0 => pairFivePath331 | 1 => pairFivePath332 | 2 => pairFivePath333
  | 3 => pairFivePath342 | 4 => pairFivePath343 | 5 => pairFivePath443
  | _ => pairFivePath444

def pairFiveLookup (table : List PairFiveEntry) (s t : PairFiveState) : List PairFiveState :=
  match table with
  | [] => []
  | e :: es => if e.start = s ∧ e.finish = t then e.path else pairFiveLookup es s t

def pairFiveCanonA (kind : PairFiveKind) : PairFiveMask :=
  match kind.val with
  | 5 | 6 => p32 15
  | _ => p32 7
def pairFiveCanonB (kind : PairFiveKind) : PairFiveMask :=
  match kind.val with
  | 0 => p32 25 | 1 => p32 11 | 2 => p32 7 | 3 => p32 27
  | 4 => p32 15 | 5 => p32 23 | _ => p32 15

def pairFiveCanonicalCyclePath (kind : PairFiveKind)
    (s t : PairFiveState) : List PairFiveState :=
  pairFiveLookup (pairFiveTable kind.val) s t
def pairFiveCanonicalEndpointPath (kind : PairFiveKind)
    (s t : PairFiveState) : List PairFiveState :=
  pairFiveLookup (pairFiveEndpointTable kind.val) s t

def pairFiveCanonicalCycleCertificate (kind : PairFiveKind)
    (s t : PairFiveState) : Prop :=
  pairFiveCycleValid (pairFiveCanonA kind) (pairFiveCanonB kind)
      (pairFiveCanonicalCyclePath kind s t) ∧
    pairFiveEdgeIn s t (pairFiveCanonicalCyclePath kind s t)

def PairFiveCycleThrough (m n : PairFiveMask)
    (s t : PairFiveState) : Prop :=
  ∃ path : List PairFiveState,
    path.Nodup ∧
    CoversList (PairFiveStates m n) path ∧
    ClosedPathOn PairFiveAdjacent path ∧
    pairFiveEdgeIn s t path
def pairFiveCanonicalEndpointCertificate (kind : PairFiveKind)
    (s t : PairFiveState) : Prop :=
  pairFivePathValid (pairFiveCanonA kind) (pairFiveCanonB kind) s t
    (pairFiveCanonicalEndpointPath kind s t)


def pairFiveNorm (m n : PairFiveMask) : PairFiveNorm :=
  match m.val, n.val with
  | 7, 7 => { kind := 2, swap := false, p := [0, 1, 2, 3, 4], q := [0, 1, 2, 3, 4] }
  | 7, 11 => { kind := 1, swap := false, p := [0, 1, 2, 3, 4], q := [0, 1, 2, 3, 4] }
  | 7, 13 => { kind := 1, swap := false, p := [0, 2, 1, 3, 4], q := [0, 2, 1, 3, 4] }
  | 7, 14 => { kind := 1, swap := false, p := [1, 2, 0, 3, 4], q := [2, 0, 1, 3, 4] }
  | 7, 15 => { kind := 4, swap := false, p := [0, 1, 2, 3, 4], q := [0, 1, 2, 3, 4] }
  | 7, 19 => { kind := 1, swap := false, p := [0, 1, 2, 4, 3], q := [0, 1, 2, 4, 3] }
  | 7, 21 => { kind := 1, swap := false, p := [0, 2, 1, 4, 3], q := [0, 2, 1, 4, 3] }
  | 7, 22 => { kind := 1, swap := false, p := [1, 2, 0, 4, 3], q := [2, 0, 1, 4, 3] }
  | 7, 23 => { kind := 4, swap := false, p := [0, 1, 2, 4, 3], q := [0, 1, 2, 4, 3] }
  | 7, 25 => { kind := 0, swap := false, p := [0, 1, 2, 3, 4], q := [0, 1, 2, 3, 4] }
  | 7, 26 => { kind := 0, swap := false, p := [1, 0, 2, 3, 4], q := [1, 0, 2, 3, 4] }
  | 7, 27 => { kind := 3, swap := false, p := [0, 1, 2, 3, 4], q := [0, 1, 2, 3, 4] }
  | 7, 28 => { kind := 0, swap := false, p := [2, 0, 1, 3, 4], q := [1, 2, 0, 3, 4] }
  | 7, 29 => { kind := 3, swap := false, p := [0, 2, 1, 3, 4], q := [0, 2, 1, 3, 4] }
  | 7, 30 => { kind := 3, swap := false, p := [1, 2, 0, 3, 4], q := [2, 0, 1, 3, 4] }
  | 11, 7 => { kind := 1, swap := false, p := [0, 1, 3, 2, 4], q := [0, 1, 3, 2, 4] }
  | 11, 11 => { kind := 2, swap := false, p := [0, 1, 3, 2, 4], q := [0, 1, 3, 2, 4] }
  | 11, 13 => { kind := 1, swap := false, p := [0, 3, 1, 2, 4], q := [0, 2, 3, 1, 4] }
  | 11, 14 => { kind := 1, swap := false, p := [1, 3, 0, 2, 4], q := [2, 0, 3, 1, 4] }
  | 11, 15 => { kind := 4, swap := false, p := [0, 1, 3, 2, 4], q := [0, 1, 3, 2, 4] }
  | 11, 19 => { kind := 1, swap := false, p := [0, 1, 3, 4, 2], q := [0, 1, 4, 2, 3] }
  | 11, 21 => { kind := 0, swap := false, p := [0, 1, 3, 2, 4], q := [0, 1, 3, 2, 4] }
  | 11, 22 => { kind := 0, swap := false, p := [1, 0, 3, 2, 4], q := [1, 0, 3, 2, 4] }
  | 11, 23 => { kind := 3, swap := false, p := [0, 1, 3, 2, 4], q := [0, 1, 3, 2, 4] }
  | 11, 25 => { kind := 1, swap := false, p := [0, 3, 1, 4, 2], q := [0, 2, 4, 1, 3] }
  | 11, 26 => { kind := 1, swap := false, p := [1, 3, 0, 4, 2], q := [2, 0, 4, 1, 3] }
  | 11, 27 => { kind := 4, swap := false, p := [0, 1, 3, 4, 2], q := [0, 1, 4, 2, 3] }
  | 11, 28 => { kind := 0, swap := false, p := [3, 0, 1, 2, 4], q := [1, 2, 3, 0, 4] }
  | 11, 29 => { kind := 3, swap := false, p := [0, 3, 1, 2, 4], q := [0, 2, 3, 1, 4] }
  | 11, 30 => { kind := 3, swap := false, p := [1, 3, 0, 2, 4], q := [2, 0, 3, 1, 4] }
  | 13, 7 => { kind := 1, swap := false, p := [0, 2, 3, 1, 4], q := [0, 3, 1, 2, 4] }
  | 13, 11 => { kind := 1, swap := false, p := [0, 3, 2, 1, 4], q := [0, 3, 2, 1, 4] }
  | 13, 13 => { kind := 2, swap := false, p := [0, 2, 3, 1, 4], q := [0, 3, 1, 2, 4] }
  | 13, 14 => { kind := 1, swap := false, p := [2, 3, 0, 1, 4], q := [2, 3, 0, 1, 4] }
  | 13, 15 => { kind := 4, swap := false, p := [0, 2, 3, 1, 4], q := [0, 3, 1, 2, 4] }
  | 13, 19 => { kind := 0, swap := false, p := [0, 2, 3, 1, 4], q := [0, 3, 1, 2, 4] }
  | 13, 21 => { kind := 1, swap := false, p := [0, 2, 3, 4, 1], q := [0, 4, 1, 2, 3] }
  | 13, 22 => { kind := 0, swap := false, p := [2, 0, 3, 1, 4], q := [1, 3, 0, 2, 4] }
  | 13, 23 => { kind := 3, swap := false, p := [0, 2, 3, 1, 4], q := [0, 3, 1, 2, 4] }
  | 13, 25 => { kind := 1, swap := false, p := [0, 3, 2, 4, 1], q := [0, 4, 2, 1, 3] }
  | 13, 26 => { kind := 0, swap := false, p := [3, 0, 2, 1, 4], q := [1, 3, 2, 0, 4] }
  | 13, 27 => { kind := 3, swap := false, p := [0, 3, 2, 1, 4], q := [0, 3, 2, 1, 4] }
  | 13, 28 => { kind := 1, swap := false, p := [2, 3, 0, 4, 1], q := [2, 4, 0, 1, 3] }
  | 13, 29 => { kind := 4, swap := false, p := [0, 2, 3, 4, 1], q := [0, 4, 1, 2, 3] }
  | 13, 30 => { kind := 3, swap := false, p := [2, 3, 0, 1, 4], q := [2, 3, 0, 1, 4] }
  | 14, 7 => { kind := 1, swap := false, p := [1, 2, 3, 0, 4], q := [3, 0, 1, 2, 4] }
  | 14, 11 => { kind := 1, swap := false, p := [1, 3, 2, 0, 4], q := [3, 0, 2, 1, 4] }
  | 14, 13 => { kind := 1, swap := false, p := [2, 3, 1, 0, 4], q := [3, 2, 0, 1, 4] }
  | 14, 14 => { kind := 2, swap := false, p := [1, 2, 3, 0, 4], q := [3, 0, 1, 2, 4] }
  | 14, 15 => { kind := 4, swap := false, p := [1, 2, 3, 0, 4], q := [3, 0, 1, 2, 4] }
  | 14, 19 => { kind := 0, swap := false, p := [1, 2, 3, 0, 4], q := [3, 0, 1, 2, 4] }
  | 14, 21 => { kind := 0, swap := false, p := [2, 1, 3, 0, 4], q := [3, 1, 0, 2, 4] }
  | 14, 22 => { kind := 1, swap := false, p := [1, 2, 3, 4, 0], q := [4, 0, 1, 2, 3] }
  | 14, 23 => { kind := 3, swap := false, p := [1, 2, 3, 0, 4], q := [3, 0, 1, 2, 4] }
  | 14, 25 => { kind := 0, swap := false, p := [3, 1, 2, 0, 4], q := [3, 1, 2, 0, 4] }
  | 14, 26 => { kind := 1, swap := false, p := [1, 3, 2, 4, 0], q := [4, 0, 2, 1, 3] }
  | 14, 27 => { kind := 3, swap := false, p := [1, 3, 2, 0, 4], q := [3, 0, 2, 1, 4] }
  | 14, 28 => { kind := 1, swap := false, p := [2, 3, 1, 4, 0], q := [4, 2, 0, 1, 3] }
  | 14, 29 => { kind := 3, swap := false, p := [2, 3, 1, 0, 4], q := [3, 2, 0, 1, 4] }
  | 14, 30 => { kind := 4, swap := false, p := [1, 2, 3, 4, 0], q := [4, 0, 1, 2, 3] }
  | 15, 7 => { kind := 4, swap := true, p := [0, 1, 2, 3, 4], q := [0, 1, 2, 3, 4] }
  | 15, 11 => { kind := 4, swap := true, p := [0, 1, 3, 2, 4], q := [0, 1, 3, 2, 4] }
  | 15, 13 => { kind := 4, swap := true, p := [0, 2, 3, 1, 4], q := [0, 3, 1, 2, 4] }
  | 15, 14 => { kind := 4, swap := true, p := [1, 2, 3, 0, 4], q := [3, 0, 1, 2, 4] }
  | 15, 15 => { kind := 6, swap := false, p := [0, 1, 2, 3, 4], q := [0, 1, 2, 3, 4] }
  | 15, 19 => { kind := 3, swap := true, p := [0, 1, 4, 2, 3], q := [0, 1, 3, 4, 2] }
  | 15, 21 => { kind := 3, swap := true, p := [0, 2, 4, 1, 3], q := [0, 3, 1, 4, 2] }
  | 15, 22 => { kind := 3, swap := true, p := [1, 2, 4, 0, 3], q := [3, 0, 1, 4, 2] }
  | 15, 23 => { kind := 5, swap := false, p := [0, 1, 2, 3, 4], q := [0, 1, 2, 3, 4] }
  | 15, 25 => { kind := 3, swap := true, p := [0, 3, 4, 1, 2], q := [0, 3, 4, 1, 2] }
  | 15, 26 => { kind := 3, swap := true, p := [1, 3, 4, 0, 2], q := [3, 0, 4, 1, 2] }
  | 15, 27 => { kind := 5, swap := false, p := [0, 1, 3, 2, 4], q := [0, 1, 3, 2, 4] }
  | 15, 28 => { kind := 3, swap := true, p := [2, 3, 4, 0, 1], q := [3, 4, 0, 1, 2] }
  | 15, 29 => { kind := 5, swap := false, p := [0, 2, 3, 1, 4], q := [0, 3, 1, 2, 4] }
  | 15, 30 => { kind := 5, swap := false, p := [1, 2, 3, 0, 4], q := [3, 0, 1, 2, 4] }
  | 19, 7 => { kind := 1, swap := false, p := [0, 1, 4, 2, 3], q := [0, 1, 3, 4, 2] }
  | 19, 11 => { kind := 1, swap := false, p := [0, 1, 4, 3, 2], q := [0, 1, 4, 3, 2] }
  | 19, 13 => { kind := 0, swap := false, p := [0, 1, 4, 2, 3], q := [0, 1, 3, 4, 2] }
  | 19, 14 => { kind := 0, swap := false, p := [1, 0, 4, 2, 3], q := [1, 0, 3, 4, 2] }
  | 19, 15 => { kind := 3, swap := false, p := [0, 1, 4, 2, 3], q := [0, 1, 3, 4, 2] }
  | 19, 19 => { kind := 2, swap := false, p := [0, 1, 4, 2, 3], q := [0, 1, 3, 4, 2] }
  | 19, 21 => { kind := 1, swap := false, p := [0, 4, 1, 2, 3], q := [0, 2, 3, 4, 1] }
  | 19, 22 => { kind := 1, swap := false, p := [1, 4, 0, 2, 3], q := [2, 0, 3, 4, 1] }
  | 19, 23 => { kind := 4, swap := false, p := [0, 1, 4, 2, 3], q := [0, 1, 3, 4, 2] }
  | 19, 25 => { kind := 1, swap := false, p := [0, 4, 1, 3, 2], q := [0, 2, 4, 3, 1] }
  | 19, 26 => { kind := 1, swap := false, p := [1, 4, 0, 3, 2], q := [2, 0, 4, 3, 1] }
  | 19, 27 => { kind := 4, swap := false, p := [0, 1, 4, 3, 2], q := [0, 1, 4, 3, 2] }
  | 19, 28 => { kind := 0, swap := false, p := [4, 0, 1, 2, 3], q := [1, 2, 3, 4, 0] }
  | 19, 29 => { kind := 3, swap := false, p := [0, 4, 1, 2, 3], q := [0, 2, 3, 4, 1] }
  | 19, 30 => { kind := 3, swap := false, p := [1, 4, 0, 2, 3], q := [2, 0, 3, 4, 1] }
  | 21, 7 => { kind := 1, swap := false, p := [0, 2, 4, 1, 3], q := [0, 3, 1, 4, 2] }
  | 21, 11 => { kind := 0, swap := false, p := [0, 2, 4, 1, 3], q := [0, 3, 1, 4, 2] }
  | 21, 13 => { kind := 1, swap := false, p := [0, 2, 4, 3, 1], q := [0, 4, 1, 3, 2] }
  | 21, 14 => { kind := 0, swap := false, p := [2, 0, 4, 1, 3], q := [1, 3, 0, 4, 2] }
  | 21, 15 => { kind := 3, swap := false, p := [0, 2, 4, 1, 3], q := [0, 3, 1, 4, 2] }
  | 21, 19 => { kind := 1, swap := false, p := [0, 4, 2, 1, 3], q := [0, 3, 2, 4, 1] }
  | 21, 21 => { kind := 2, swap := false, p := [0, 2, 4, 1, 3], q := [0, 3, 1, 4, 2] }
  | 21, 22 => { kind := 1, swap := false, p := [2, 4, 0, 1, 3], q := [2, 3, 0, 4, 1] }
  | 21, 23 => { kind := 4, swap := false, p := [0, 2, 4, 1, 3], q := [0, 3, 1, 4, 2] }
  | 21, 25 => { kind := 1, swap := false, p := [0, 4, 2, 3, 1], q := [0, 4, 2, 3, 1] }
  | 21, 26 => { kind := 0, swap := false, p := [4, 0, 2, 1, 3], q := [1, 3, 2, 4, 0] }
  | 21, 27 => { kind := 3, swap := false, p := [0, 4, 2, 1, 3], q := [0, 3, 2, 4, 1] }
  | 21, 28 => { kind := 1, swap := false, p := [2, 4, 0, 3, 1], q := [2, 4, 0, 3, 1] }
  | 21, 29 => { kind := 4, swap := false, p := [0, 2, 4, 3, 1], q := [0, 4, 1, 3, 2] }
  | 21, 30 => { kind := 3, swap := false, p := [2, 4, 0, 1, 3], q := [2, 3, 0, 4, 1] }
  | 22, 7 => { kind := 1, swap := false, p := [1, 2, 4, 0, 3], q := [3, 0, 1, 4, 2] }
  | 22, 11 => { kind := 0, swap := false, p := [1, 2, 4, 0, 3], q := [3, 0, 1, 4, 2] }
  | 22, 13 => { kind := 0, swap := false, p := [2, 1, 4, 0, 3], q := [3, 1, 0, 4, 2] }
  | 22, 14 => { kind := 1, swap := false, p := [1, 2, 4, 3, 0], q := [4, 0, 1, 3, 2] }
  | 22, 15 => { kind := 3, swap := false, p := [1, 2, 4, 0, 3], q := [3, 0, 1, 4, 2] }
  | 22, 19 => { kind := 1, swap := false, p := [1, 4, 2, 0, 3], q := [3, 0, 2, 4, 1] }
  | 22, 21 => { kind := 1, swap := false, p := [2, 4, 1, 0, 3], q := [3, 2, 0, 4, 1] }
  | 22, 22 => { kind := 2, swap := false, p := [1, 2, 4, 0, 3], q := [3, 0, 1, 4, 2] }
  | 22, 23 => { kind := 4, swap := false, p := [1, 2, 4, 0, 3], q := [3, 0, 1, 4, 2] }
  | 22, 25 => { kind := 0, swap := false, p := [4, 1, 2, 0, 3], q := [3, 1, 2, 4, 0] }
  | 22, 26 => { kind := 1, swap := false, p := [1, 4, 2, 3, 0], q := [4, 0, 2, 3, 1] }
  | 22, 27 => { kind := 3, swap := false, p := [1, 4, 2, 0, 3], q := [3, 0, 2, 4, 1] }
  | 22, 28 => { kind := 1, swap := false, p := [2, 4, 1, 3, 0], q := [4, 2, 0, 3, 1] }
  | 22, 29 => { kind := 3, swap := false, p := [2, 4, 1, 0, 3], q := [3, 2, 0, 4, 1] }
  | 22, 30 => { kind := 4, swap := false, p := [1, 2, 4, 3, 0], q := [4, 0, 1, 3, 2] }
  | 23, 7 => { kind := 4, swap := true, p := [0, 1, 2, 4, 3], q := [0, 1, 2, 4, 3] }
  | 23, 11 => { kind := 3, swap := true, p := [0, 1, 3, 2, 4], q := [0, 1, 3, 2, 4] }
  | 23, 13 => { kind := 3, swap := true, p := [0, 2, 3, 1, 4], q := [0, 3, 1, 2, 4] }
  | 23, 14 => { kind := 3, swap := true, p := [1, 2, 3, 0, 4], q := [3, 0, 1, 2, 4] }
  | 23, 15 => { kind := 5, swap := false, p := [0, 1, 2, 4, 3], q := [0, 1, 2, 4, 3] }
  | 23, 19 => { kind := 4, swap := true, p := [0, 1, 4, 2, 3], q := [0, 1, 3, 4, 2] }
  | 23, 21 => { kind := 4, swap := true, p := [0, 2, 4, 1, 3], q := [0, 3, 1, 4, 2] }
  | 23, 22 => { kind := 4, swap := true, p := [1, 2, 4, 0, 3], q := [3, 0, 1, 4, 2] }
  | 23, 23 => { kind := 6, swap := false, p := [0, 1, 2, 4, 3], q := [0, 1, 2, 4, 3] }
  | 23, 25 => { kind := 3, swap := true, p := [0, 4, 3, 1, 2], q := [0, 3, 4, 2, 1] }
  | 23, 26 => { kind := 3, swap := true, p := [1, 4, 3, 0, 2], q := [3, 0, 4, 2, 1] }
  | 23, 27 => { kind := 5, swap := false, p := [0, 1, 4, 2, 3], q := [0, 1, 3, 4, 2] }
  | 23, 28 => { kind := 3, swap := true, p := [2, 4, 3, 0, 1], q := [3, 4, 0, 2, 1] }
  | 23, 29 => { kind := 5, swap := false, p := [0, 2, 4, 1, 3], q := [0, 3, 1, 4, 2] }
  | 23, 30 => { kind := 5, swap := false, p := [1, 2, 4, 0, 3], q := [3, 0, 1, 4, 2] }
  | 25, 7 => { kind := 0, swap := false, p := [0, 3, 4, 1, 2], q := [0, 3, 4, 1, 2] }
  | 25, 11 => { kind := 1, swap := false, p := [0, 3, 4, 1, 2], q := [0, 3, 4, 1, 2] }
  | 25, 13 => { kind := 1, swap := false, p := [0, 3, 4, 2, 1], q := [0, 4, 3, 1, 2] }
  | 25, 14 => { kind := 0, swap := false, p := [3, 0, 4, 1, 2], q := [1, 3, 4, 0, 2] }
  | 25, 15 => { kind := 3, swap := false, p := [0, 3, 4, 1, 2], q := [0, 3, 4, 1, 2] }
  | 25, 19 => { kind := 1, swap := false, p := [0, 4, 3, 1, 2], q := [0, 3, 4, 2, 1] }
  | 25, 21 => { kind := 1, swap := false, p := [0, 4, 3, 2, 1], q := [0, 4, 3, 2, 1] }
  | 25, 22 => { kind := 0, swap := false, p := [4, 0, 3, 1, 2], q := [1, 3, 4, 2, 0] }
  | 25, 23 => { kind := 3, swap := false, p := [0, 4, 3, 1, 2], q := [0, 3, 4, 2, 1] }
  | 25, 25 => { kind := 2, swap := false, p := [0, 3, 4, 1, 2], q := [0, 3, 4, 1, 2] }
  | 25, 26 => { kind := 1, swap := false, p := [3, 4, 0, 1, 2], q := [2, 3, 4, 0, 1] }
  | 25, 27 => { kind := 4, swap := false, p := [0, 3, 4, 1, 2], q := [0, 3, 4, 1, 2] }
  | 25, 28 => { kind := 1, swap := false, p := [3, 4, 0, 2, 1], q := [2, 4, 3, 0, 1] }
  | 25, 29 => { kind := 4, swap := false, p := [0, 3, 4, 2, 1], q := [0, 4, 3, 1, 2] }
  | 25, 30 => { kind := 3, swap := false, p := [3, 4, 0, 1, 2], q := [2, 3, 4, 0, 1] }
  | 26, 7 => { kind := 0, swap := false, p := [1, 3, 4, 0, 2], q := [3, 0, 4, 1, 2] }
  | 26, 11 => { kind := 1, swap := false, p := [1, 3, 4, 0, 2], q := [3, 0, 4, 1, 2] }
  | 26, 13 => { kind := 0, swap := false, p := [3, 1, 4, 0, 2], q := [3, 1, 4, 0, 2] }
  | 26, 14 => { kind := 1, swap := false, p := [1, 3, 4, 2, 0], q := [4, 0, 3, 1, 2] }
  | 26, 15 => { kind := 3, swap := false, p := [1, 3, 4, 0, 2], q := [3, 0, 4, 1, 2] }
  | 26, 19 => { kind := 1, swap := false, p := [1, 4, 3, 0, 2], q := [3, 0, 4, 2, 1] }
  | 26, 21 => { kind := 0, swap := false, p := [4, 1, 3, 0, 2], q := [3, 1, 4, 2, 0] }
  | 26, 22 => { kind := 1, swap := false, p := [1, 4, 3, 2, 0], q := [4, 0, 3, 2, 1] }
  | 26, 23 => { kind := 3, swap := false, p := [1, 4, 3, 0, 2], q := [3, 0, 4, 2, 1] }
  | 26, 25 => { kind := 1, swap := false, p := [3, 4, 1, 0, 2], q := [3, 2, 4, 0, 1] }
  | 26, 26 => { kind := 2, swap := false, p := [1, 3, 4, 0, 2], q := [3, 0, 4, 1, 2] }
  | 26, 27 => { kind := 4, swap := false, p := [1, 3, 4, 0, 2], q := [3, 0, 4, 1, 2] }
  | 26, 28 => { kind := 1, swap := false, p := [3, 4, 1, 2, 0], q := [4, 2, 3, 0, 1] }
  | 26, 29 => { kind := 3, swap := false, p := [3, 4, 1, 0, 2], q := [3, 2, 4, 0, 1] }
  | 26, 30 => { kind := 4, swap := false, p := [1, 3, 4, 2, 0], q := [4, 0, 3, 1, 2] }
  | 27, 7 => { kind := 3, swap := true, p := [0, 1, 2, 3, 4], q := [0, 1, 2, 3, 4] }
  | 27, 11 => { kind := 4, swap := true, p := [0, 1, 3, 4, 2], q := [0, 1, 4, 2, 3] }
  | 27, 13 => { kind := 3, swap := true, p := [0, 3, 2, 1, 4], q := [0, 3, 2, 1, 4] }
  | 27, 14 => { kind := 3, swap := true, p := [1, 3, 2, 0, 4], q := [3, 0, 2, 1, 4] }
  | 27, 15 => { kind := 5, swap := false, p := [0, 1, 3, 4, 2], q := [0, 1, 4, 2, 3] }
  | 27, 19 => { kind := 4, swap := true, p := [0, 1, 4, 3, 2], q := [0, 1, 4, 3, 2] }
  | 27, 21 => { kind := 3, swap := true, p := [0, 4, 2, 1, 3], q := [0, 3, 2, 4, 1] }
  | 27, 22 => { kind := 3, swap := true, p := [1, 4, 2, 0, 3], q := [3, 0, 2, 4, 1] }
  | 27, 23 => { kind := 5, swap := false, p := [0, 1, 4, 3, 2], q := [0, 1, 4, 3, 2] }
  | 27, 25 => { kind := 4, swap := true, p := [0, 3, 4, 1, 2], q := [0, 3, 4, 1, 2] }
  | 27, 26 => { kind := 4, swap := true, p := [1, 3, 4, 0, 2], q := [3, 0, 4, 1, 2] }
  | 27, 27 => { kind := 6, swap := false, p := [0, 1, 3, 4, 2], q := [0, 1, 4, 2, 3] }
  | 27, 28 => { kind := 3, swap := true, p := [3, 4, 2, 0, 1], q := [3, 4, 2, 0, 1] }
  | 27, 29 => { kind := 5, swap := false, p := [0, 3, 4, 1, 2], q := [0, 3, 4, 1, 2] }
  | 27, 30 => { kind := 5, swap := false, p := [1, 3, 4, 0, 2], q := [3, 0, 4, 1, 2] }
  | 28, 7 => { kind := 0, swap := false, p := [2, 3, 4, 0, 1], q := [3, 4, 0, 1, 2] }
  | 28, 11 => { kind := 0, swap := false, p := [3, 2, 4, 0, 1], q := [3, 4, 1, 0, 2] }
  | 28, 13 => { kind := 1, swap := false, p := [2, 3, 4, 0, 1], q := [3, 4, 0, 1, 2] }
  | 28, 14 => { kind := 1, swap := false, p := [2, 3, 4, 1, 0], q := [4, 3, 0, 1, 2] }
  | 28, 15 => { kind := 3, swap := false, p := [2, 3, 4, 0, 1], q := [3, 4, 0, 1, 2] }
  | 28, 19 => { kind := 0, swap := false, p := [4, 2, 3, 0, 1], q := [3, 4, 1, 2, 0] }
  | 28, 21 => { kind := 1, swap := false, p := [2, 4, 3, 0, 1], q := [3, 4, 0, 2, 1] }
  | 28, 22 => { kind := 1, swap := false, p := [2, 4, 3, 1, 0], q := [4, 3, 0, 2, 1] }
  | 28, 23 => { kind := 3, swap := false, p := [2, 4, 3, 0, 1], q := [3, 4, 0, 2, 1] }
  | 28, 25 => { kind := 1, swap := false, p := [3, 4, 2, 0, 1], q := [3, 4, 2, 0, 1] }
  | 28, 26 => { kind := 1, swap := false, p := [3, 4, 2, 1, 0], q := [4, 3, 2, 0, 1] }
  | 28, 27 => { kind := 3, swap := false, p := [3, 4, 2, 0, 1], q := [3, 4, 2, 0, 1] }
  | 28, 28 => { kind := 2, swap := false, p := [2, 3, 4, 0, 1], q := [3, 4, 0, 1, 2] }
  | 28, 29 => { kind := 4, swap := false, p := [2, 3, 4, 0, 1], q := [3, 4, 0, 1, 2] }
  | 28, 30 => { kind := 4, swap := false, p := [2, 3, 4, 1, 0], q := [4, 3, 0, 1, 2] }
  | 29, 7 => { kind := 3, swap := true, p := [0, 2, 1, 3, 4], q := [0, 2, 1, 3, 4] }
  | 29, 11 => { kind := 3, swap := true, p := [0, 3, 1, 2, 4], q := [0, 2, 3, 1, 4] }
  | 29, 13 => { kind := 4, swap := true, p := [0, 2, 3, 4, 1], q := [0, 4, 1, 2, 3] }
  | 29, 14 => { kind := 3, swap := true, p := [2, 3, 1, 0, 4], q := [3, 2, 0, 1, 4] }
  | 29, 15 => { kind := 5, swap := false, p := [0, 2, 3, 4, 1], q := [0, 4, 1, 2, 3] }
  | 29, 19 => { kind := 3, swap := true, p := [0, 4, 1, 2, 3], q := [0, 2, 3, 4, 1] }
  | 29, 21 => { kind := 4, swap := true, p := [0, 2, 4, 3, 1], q := [0, 4, 1, 3, 2] }
  | 29, 22 => { kind := 3, swap := true, p := [2, 4, 1, 0, 3], q := [3, 2, 0, 4, 1] }
  | 29, 23 => { kind := 5, swap := false, p := [0, 2, 4, 3, 1], q := [0, 4, 1, 3, 2] }
  | 29, 25 => { kind := 4, swap := true, p := [0, 3, 4, 2, 1], q := [0, 4, 3, 1, 2] }
  | 29, 26 => { kind := 3, swap := true, p := [3, 4, 1, 0, 2], q := [3, 2, 4, 0, 1] }
  | 29, 27 => { kind := 5, swap := false, p := [0, 3, 4, 2, 1], q := [0, 4, 3, 1, 2] }
  | 29, 28 => { kind := 4, swap := true, p := [2, 3, 4, 0, 1], q := [3, 4, 0, 1, 2] }
  | 29, 29 => { kind := 6, swap := false, p := [0, 2, 3, 4, 1], q := [0, 4, 1, 2, 3] }
  | 29, 30 => { kind := 5, swap := false, p := [2, 3, 4, 0, 1], q := [3, 4, 0, 1, 2] }
  | 30, 7 => { kind := 3, swap := true, p := [1, 2, 0, 3, 4], q := [2, 0, 1, 3, 4] }
  | 30, 11 => { kind := 3, swap := true, p := [1, 3, 0, 2, 4], q := [2, 0, 3, 1, 4] }
  | 30, 13 => { kind := 3, swap := true, p := [2, 3, 0, 1, 4], q := [2, 3, 0, 1, 4] }
  | 30, 14 => { kind := 4, swap := true, p := [1, 2, 3, 4, 0], q := [4, 0, 1, 2, 3] }
  | 30, 15 => { kind := 5, swap := false, p := [1, 2, 3, 4, 0], q := [4, 0, 1, 2, 3] }
  | 30, 19 => { kind := 3, swap := true, p := [1, 4, 0, 2, 3], q := [2, 0, 3, 4, 1] }
  | 30, 21 => { kind := 3, swap := true, p := [2, 4, 0, 1, 3], q := [2, 3, 0, 4, 1] }
  | 30, 22 => { kind := 4, swap := true, p := [1, 2, 4, 3, 0], q := [4, 0, 1, 3, 2] }
  | 30, 23 => { kind := 5, swap := false, p := [1, 2, 4, 3, 0], q := [4, 0, 1, 3, 2] }
  | 30, 25 => { kind := 3, swap := true, p := [3, 4, 0, 1, 2], q := [2, 3, 4, 0, 1] }
  | 30, 26 => { kind := 4, swap := true, p := [1, 3, 4, 2, 0], q := [4, 0, 3, 1, 2] }
  | 30, 27 => { kind := 5, swap := false, p := [1, 3, 4, 2, 0], q := [4, 0, 3, 1, 2] }
  | 30, 28 => { kind := 4, swap := true, p := [2, 3, 4, 1, 0], q := [4, 3, 0, 1, 2] }
  | 30, 29 => { kind := 5, swap := false, p := [2, 3, 4, 1, 0], q := [4, 3, 0, 1, 2] }
  | 30, 30 => { kind := 6, swap := false, p := [1, 2, 3, 4, 0], q := [4, 0, 1, 2, 3] }
  | _, _ => { kind := 0, swap := false, p := [0, 1, 2, 3, 4], q := [0, 1, 2, 3, 4] }



instance pairFiveAdjacentDecidable (s t : PairFiveState) : Decidable (PairFiveAdjacent s t) := by
  unfold PairFiveAdjacent
  infer_instance
instance pairFiveSmallDecidable (m : PairFiveMask) : Decidable (pairFiveSmall m) := by
  unfold pairFiveSmall pairFiveList
  infer_instance
instance pairFivePathValidDecidable (m n : PairFiveMask) (s t : PairFiveState)
    (path : List PairFiveState) : Decidable (pairFivePathValid m n s t path) := by
  unfold pairFivePathValid
  infer_instance
instance pairFiveCycleValidDecidable (m n : PairFiveMask)
    (path : List PairFiveState) : Decidable (pairFiveCycleValid m n path) := by
  unfold pairFiveCycleValid
  infer_instance
instance pairFiveEdgeInDecidable (s t : PairFiveState)
    (path : List PairFiveState) : Decidable (pairFiveEdgeIn s t path) := by
  unfold pairFiveEdgeIn
  infer_instance

instance pairFiveCanonicalCycleCertificateDecidable (kind : PairFiveKind)
    (s t : PairFiveState) : Decidable (pairFiveCanonicalCycleCertificate kind s t) := by
  unfold pairFiveCanonicalCycleCertificate
  infer_instance
instance pairFiveCanonicalEndpointCertificateDecidable (kind : PairFiveKind)
    (s t : PairFiveState) : Decidable (pairFiveCanonicalEndpointCertificate kind s t) := by
  unfold pairFiveCanonicalEndpointCertificate
  infer_instance

theorem pairFive_canonical_cycle :
    ∀ kind : PairFiveKind, ∀ s t : PairFiveState,
      s ∈ PairFiveStates (pairFiveCanonA kind) (pairFiveCanonB kind) →
      t ∈ PairFiveStates (pairFiveCanonA kind) (pairFiveCanonB kind) →
      PairFiveAdjacent s t → pairFiveCanonicalCycleCertificate kind s t := by
  decide

theorem pairFive_canonical_endpoint :
    ∀ kind : PairFiveKind, kind.val ≥ 3 →
      ∀ s t : PairFiveState,
      s ∈ PairFiveStates (pairFiveCanonA kind) (pairFiveCanonB kind) →
      t ∈ PairFiveStates (pairFiveCanonA kind) (pairFiveCanonB kind) →
      s ≠ t → pairFiveCanonicalEndpointCertificate kind s t := by
  decide



theorem pairFive_canonical_edge_endpoint :
    ∀ kind : PairFiveKind, ∀ s t : PairFiveState,
      s ∈ PairFiveStates (pairFiveCanonA kind) (pairFiveCanonB kind) →
      t ∈ PairFiveStates (pairFiveCanonA kind) (pairFiveCanonB kind) →
      PairFiveAdjacent s t → pairFiveCanonicalEndpointCertificate kind s t := by
  decide

theorem pairFive_consecutive_of_walk
    (path : List PairFiveState) (h : pairFiveWalkB path = true) :
    Consecutive PairFiveAdjacent path := by
  induction path with
  | nil => simp [Consecutive]
  | cons x xs ih =>
      cases xs with
      | nil => simp [Consecutive]
      | cons y ys =>
          simp only [pairFiveWalkB, Bool.and_eq_true] at h
          exact ⟨h.1, ih h.2⟩

private theorem pairFive_getLast_some {α : Type} :
    ∀ (path : List α), path ≠ [] → ∃ z, path.getLast? = some z := by
  intro path
  induction path with
  | nil =>
      intro h
      exact False.elim (h rfl)
  | cons x xs ih =>
      cases xs with
      | nil =>
          intro _
          exact ⟨x, rfl⟩
      | cons y ys =>
          intro _
          rcases ih (by simp) with ⟨z, hz⟩
          exact ⟨z, by simpa using hz⟩

private theorem pairFive_close_of_head_last
    {path : List PairFiveState} {a z : PairFiveState}
    (ha : path.head? = some a) (hz : path.getLast? = some z)
    (hc : pairFiveCloseB path = true) : PairFiveAdjacent z a := by
  cases path with
  | nil => simp at ha
  | cons x xs =>
      cases xs with
      | nil =>
          simp [pairFiveCloseB, pairFiveAdjB] at hc
      | cons y ys =>
          have hxa : x = a := by simpa using ha
          subst x
          have hlast : (y :: ys).getLast? = some z := by simpa using hz
          have hclose : pairFiveAdjB z a = true := by
            simpa [pairFiveCloseB, hlast] using hc
          exact hclose


private theorem pairFive_head_some {α : Type} {path : List α}
    (hne : path ≠ []) : ∃ a, path.head? = some a := by
  cases path with
  | nil => exact False.elim (hne rfl)
  | cons a as => exact ⟨a, rfl⟩

theorem pairFive_canonical_hamiltonPathOn
    {kind : PairFiveKind} {s t : PairFiveState}
    (h : pairFiveCanonicalEndpointCertificate kind s t) :
    HamiltonPathOn (PairFiveStates (pairFiveCanonA kind) (pairFiveCanonB kind))
      PairFiveAdjacent s t := by
  rcases h with ⟨hh, hl, hn, hc, hw⟩
  refine ⟨pairFiveCanonicalEndpointPath kind s t, hh, hl, hn, ?_,
    pairFive_consecutive_of_walk _ hw⟩
  intro q
  exact hc q

theorem pairFive_canonical_cycle_hamiltonCycleOn
    {kind : PairFiveKind} {s t : PairFiveState}
    (h : pairFiveCanonicalCycleCertificate kind s t) :
    HamiltonCycleOn (PairFiveStates (pairFiveCanonA kind) (pairFiveCanonB kind))
      PairFiveAdjacent := by
  rcases h with ⟨hcyc, hedge⟩
  let path := pairFiveCanonicalCyclePath kind s t
  have hne : path ≠ [] := by
    intro hnil
    have hedge' : pairFiveEdgeIn s t [] := by
      simpa [path, hnil] using hedge
    simp [pairFiveEdgeIn, pairFiveEdgeInB] at hedge'
  have hlast : ∃ z, path.getLast? = some z :=
    pairFive_getLast_some path hne
  rcases hlast with ⟨z, hz⟩
  rcases pairFive_head_some hne with ⟨a, ha⟩
  have hclose : PairFiveAdjacent z a :=
    pairFive_close_of_head_last ha hz hcyc.2.2.2
  have hwalk : Consecutive PairFiveAdjacent path :=
    pairFive_consecutive_of_walk path hcyc.2.2.1
  have hnodup : path.Nodup := hcyc.1
  have hcover : CoversList
      (PairFiveStates (pairFiveCanonA kind) (pairFiveCanonB kind)) path := by
    intro q
    exact hcyc.2.1 q
  refine ⟨path, hnodup, hcover, ?_⟩
  exact ⟨a, z, ha, hz, hwalk, hclose⟩

theorem pairFive_canonical_cycle_through
    {kind : PairFiveKind} {s t : PairFiveState}
    (h : pairFiveCanonicalCycleCertificate kind s t) :
    PairFiveCycleThrough (pairFiveCanonA kind) (pairFiveCanonB kind) s t := by
  rcases h with ⟨hcyc, hedge⟩
  let path := pairFiveCanonicalCyclePath kind s t
  have hne : path ≠ [] := by
    intro hnil
    have hedge' : pairFiveEdgeIn s t [] := by
      simpa [path, hnil] using hedge
    simp [pairFiveEdgeIn, pairFiveEdgeInB] at hedge'
  have hlast : ∃ z, path.getLast? = some z :=
    pairFive_getLast_some path hne
  rcases hlast with ⟨z, hz⟩
  rcases pairFive_head_some hne with ⟨a, ha⟩
  have hclose : PairFiveAdjacent z a :=
    pairFive_close_of_head_last ha hz hcyc.2.2.2
  have hwalk : Consecutive PairFiveAdjacent path :=
    pairFive_consecutive_of_walk path hcyc.2.2.1
  have hcover : CoversList
      (PairFiveStates (pairFiveCanonA kind) (pairFiveCanonB kind)) path := by
    intro q
    exact hcyc.2.1 q
  refine ⟨path, hcyc.1, hcover, ?_, hedge⟩
  exact ⟨a, z, ha, hz, hwalk, hclose⟩


def pairFiveSmallMasks : List PairFiveMask :=
  [p32 7, p32 11, p32 13, p32 14, p32 15,
   p32 19, p32 21, p32 22, p32 23, p32 25,
   p32 26, p32 27, p32 28, p32 29, p32 30]

def pairFiveSmallMask (i : Fin 15) : PairFiveMask :=
  pairFiveSmallMasks.getD i.val (p32 7)

def pairFiveSubsetB (m n : PairFiveMask) : Bool :=
  (List.finRange 5).all (fun c =>
    (!pairFiveHas m c) || pairFiveHas n c)

def pairFiveOneChangeB (m n : PairFiveMask) : Bool :=
  ((decide ((pairFiveList m).length = 3) &&
      decide ((pairFiveList n).length = 3) &&
      decide ((pairFiveList (p32 (Nat.xor m.val n.val))).length = 2)) ||
    (decide ((pairFiveList m).length = 3) &&
      decide ((pairFiveList n).length = 4) && pairFiveSubsetB m n) ||
    (decide ((pairFiveList m).length = 4) &&
      decide ((pairFiveList n).length = 3) && pairFiveSubsetB n m))

def pairFiveAllowedB (m n m' n' : PairFiveMask) : Bool :=
  (decide (m = m') && decide (n = n')) ||
    (decide (n = n') && pairFiveOneChangeB m m') ||
    (decide (m = m') && pairFiveOneChangeB n n')

def pairFiveExitB (m n m' n' : PairFiveMask) (s : PairFiveState) : Bool :=
  (List.finRange 25).any (fun q =>
    decide (q ∈ PairFiveStates m n) &&
      decide (q ∈ PairFiveStates m' n') && pairFiveAdjB s q)

theorem pairFive_small_mask_complete :
    ∀ m : PairFiveMask, pairFiveSmall m → m ∈ pairFiveSmallMasks := by
  decide

theorem pairFive_small_mask_index :
    ∀ m : PairFiveMask, pairFiveSmall m →
      ∃ i : Fin 15, pairFiveSmallMask i = m := by
  decide

set_option maxHeartbeats 100000000 in
theorem pairFive_interface_exit_indexed :
    ∀ i j i' j' : Fin 15,
      pairFiveAllowedB (pairFiveSmallMask i) (pairFiveSmallMask j)
        (pairFiveSmallMask i') (pairFiveSmallMask j') = true →
      ∀ s : PairFiveState,
        s ∈ PairFiveStates (pairFiveSmallMask i) (pairFiveSmallMask j) →
        pairFiveExitB (pairFiveSmallMask i) (pairFiveSmallMask j)
          (pairFiveSmallMask i') (pairFiveSmallMask j') s = true := by
  decide

theorem pairFive_interface_exit_of_certificate
    {m n m' n' : PairFiveMask} {s : PairFiveState}
    (hcert : pairFiveExitB m n m' n' s = true) :
    ∃ q, q ∈ PairFiveStates m n ∧ q ∈ PairFiveStates m' n' ∧
      PairFiveAdjacent s q := by
  unfold pairFiveExitB at hcert
  rw [List.any_eq_true] at hcert
  rcases hcert with ⟨q, _, hq⟩
  simp only [Bool.and_eq_true, decide_eq_true_eq] at hq
  exact ⟨q, hq.1.1, hq.1.2, hq.2⟩

end PlanarRecoloring
