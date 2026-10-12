import PlanarRecoloring.BinaryEndpoints
import PlanarRecoloring.CycleSplicing

/-!
# Recursive square strips

The bad-run proof in Chapter 4 first builds a strip for one of the four-cycle
components `Q_b`, then appends one fresh square layer at a time.  This file
formalizes that reusable strip step.  Layers use natural-number tags, which
keeps the recursive paths free of casts between `Fin n` and `Fin (n+1)`.

The main theorem is a kernel-checked Hamilton-cycle result for `C₄ □ Pₙ`, for
every `n ≥ 2`.  It is the square component used by `prop:badrun`; joining the
three centre-colour components using the actual cross-square recolouring edges
is a separate remaining interface.
-/

namespace PlanarRecoloring

set_option maxHeartbeats 0
set_option maxRecDepth 100000

abbrev SquareStripState := Fin 4 × Nat

def square4Adjacent (a b : Fin 4) : Prop :=
  (a = 0 ∧ b = 1) ∨ (a = 1 ∧ b = 0) ∨
    (a = 1 ∧ b = 2) ∨ (a = 2 ∧ b = 1) ∨
    (a = 2 ∧ b = 3) ∨ (a = 3 ∧ b = 2) ∨
    (a = 3 ∧ b = 0) ∨ (a = 0 ∧ b = 3)

def squareStripAdjacent (x y : SquareStripState) : Prop :=
  (x.2 = y.2 ∧ square4Adjacent x.1 y.1) ∨
    (x.1 = y.1 ∧ (x.2 + 1 = y.2 ∨ y.2 + 1 = x.2))

instance squareStripAdjacentDecidable (x y : SquareStripState) :
    Decidable (squareStripAdjacent x y) := by
  unfold squareStripAdjacent square4Adjacent
  infer_instance

def squareLayer (i : Nat) : List SquareStripState :=
  [(0, i), (1, i), (2, i), (3, i)]

def squareStripStates : Nat → List SquareStripState
  | 0 => []
  | n + 1 => squareStripStates n ++ squareLayer n

@[simp] theorem squareStripStates_zero : squareStripStates 0 = [] := rfl

@[simp] theorem squareStripStates_succ (n : Nat) :
    squareStripStates (n + 1) = squareStripStates n ++ squareLayer n := rfl

private theorem squareStrip_mem_layer_lt : ∀ {n} {x : SquareStripState},
    x ∈ squareStripStates n → x.2 < n
  | 0, x, hx => by simp [squareStripStates] at hx
  | n + 1, x, hx => by
      rw [squareStripStates_succ] at hx
      rcases List.mem_append.mp hx with h | h
      · exact Nat.lt_trans (squareStrip_mem_layer_lt h) (Nat.lt_succ_self n)
      · simp [squareLayer] at h
        rcases h with rfl | rfl | rfl | rfl <;> simp

private theorem squareLayer_mem_layer_eq {n : Nat} {x : SquareStripState}
    (h : x ∈ squareLayer n) : x.2 = n := by
  simp [squareLayer] at h
  rcases h with rfl | rfl | rfl | rfl <;> rfl

private theorem squareStripStates_nodup : ∀ n, (squareStripStates n).Nodup
  | 0 => by simp
  | n + 1 => by
      rw [squareStripStates_succ]
      apply List.nodup_append.mpr
      refine ⟨squareStripStates_nodup n, by simp [squareLayer], ?_⟩
      intro x hx y hy hxy
      have hx' := squareStrip_mem_layer_lt hx
      have hy' := squareLayer_mem_layer_eq hy
      have hxy' := congrArg Prod.snd hxy
      omega

private theorem squareStrip_layer_disjoint (n : Nat) :
    DisjointLists (squareStripStates n) (squareLayer n) := by
  intro x hx hy
  have hx' := squareStrip_mem_layer_lt hx
  have hy' := squareLayer_mem_layer_eq hy
  omega

private theorem squareStrip_states_cover_succ (n : Nat) (x : SquareStripState) :
    x ∈ squareStripStates (n + 1) ↔
      x ∈ squareStripStates n ∨ x ∈ squareLayer n := by
  rw [squareStripStates_succ]
  simp only [List.mem_append]

private theorem square_base_open :
    HamiltonPathOn (squareStripStates 2) squareStripAdjacent
      (1, 1) (0, 1) := by
  refine ⟨[(1, 1), (1, 0), (2, 0), (2, 1),
      (3, 1), (3, 0), (0, 0), (0, 1)], rfl, by simp,
      by decide, ?_, ?_⟩
  intro x
  · simp [squareStripStates, squareLayer, or_assoc, or_left_comm, or_comm]
  · simp only [Consecutive]
    decide

private theorem square_layer_path (o : Bool) (n : Nat) :
    HamiltonPathOn ([(0, n),
      (if o then 3 else 1, n),
      (2, n),
      (if o then 1 else 3, n)]) squareStripAdjacent
      (0, n) (if o then 1 else 3, n) := by
  cases o with
  | false =>
      refine ⟨[(0, n), (1, n), (2, n), (3, n)], rfl, by simp,
        by simp, ?_, ?_⟩
      · intro x; simp
      · simp only [Consecutive]
        simp [squareStripAdjacent, square4Adjacent]
  | true =>
      refine ⟨[(0, n), (3, n), (2, n), (1, n)], rfl, by simp,
        by simp, ?_, ?_⟩
      · intro x; simp
      · simp only [Consecutive]
        simp [squareStripAdjacent, square4Adjacent]

private theorem square_layer_tail (o : Bool) (n : Nat) :
    HamiltonPathOn ([(if o then 3 else 1, n),
      (2, n),
      (if o then 1 else 3, n)]) squareStripAdjacent
      (if o then 3 else 1, n) (if o then 1 else 3, n) := by
  cases o with
  | false =>
      refine ⟨[(1, n), (2, n), (3, n)], rfl, by simp,
        by simp, ?_, ?_⟩
      · intro x; simp
      · simp only [Consecutive]
        simp [squareStripAdjacent, square4Adjacent]
  | true =>
      refine ⟨[(3, n), (2, n), (1, n)], rfl, by simp,
        by simp, ?_, ?_⟩
      · intro x; simp
      · simp only [Consecutive]
        simp [squareStripAdjacent, square4Adjacent]

private theorem singleton_path (x : SquareStripState) :
    HamiltonPathOn [x] squareStripAdjacent x x := by
  refine ⟨[x], rfl, rfl, by simp, ?_, ?_⟩
  · intro y
    simp
  · trivial

private theorem square_strip_open_step {n : Nat} (hn : 2 ≤ n) (o : Bool)
    (hopen : HamiltonPathOn (squareStripStates n) squareStripAdjacent
      (if o then 1 else 3, n - 1) (0, n - 1)) :
    HamiltonPathOn (squareStripStates (n + 1)) squareStripAdjacent
      (if o then 3 else 1, n) (0, n) := by
  have htail := square_layer_tail o n
  have hdis₁ : DisjointLists
      [(if o then 3 else 1, n), (2, n), (if o then 1 else 3, n)]
      (squareStripStates n) := by
    intro x hx hy
    have hx' : x.2 = n := by
      simp [squareLayer] at hx
      rcases hx with rfl | rfl | rfl <;> rfl
    have hy' := squareStrip_mem_layer_lt hy
    omega
  have hbridge₁ : squareStripAdjacent
      (if o then 1 else 3, n) (if o then 1 else 3, n - 1) := by
    simp [squareStripAdjacent]
    omega
  have hfirst := htail.appendOn hopen hdis₁ hbridge₁
  have hsingle := singleton_path (0, n)
  have hdis₂ : DisjointLists
      ([(if o then 3 else 1, n), (2, n), (if o then 1 else 3, n)] ++
        squareStripStates n) [(0, n)] := by
    intro x hx hy
    have hx0 : x = (0, n) := by simpa using hy
    subst x
    rw [List.mem_append] at hx
    rcases hx with hx | hx
    · have hne₁ : (0 : Fin 4) ≠ (if o then 3 else 1) := by
        cases o <;> decide
      have hne₂ : (0 : Fin 4) ≠ (if o then 1 else 3) := by
        cases o <;> decide
      simp [squareLayer] at hx
      simp [hne₁, hne₂] at hx
    · have hx' := squareStrip_mem_layer_lt hx
      omega
  have hbridge₂ : squareStripAdjacent (0, n - 1) (0, n) := by
    simp [squareStripAdjacent]
    omega
  have hjoined := hfirst.appendOn hsingle hdis₂ hbridge₂
  apply hjoined.congr_vertices
  intro x
  rw [squareStrip_states_cover_succ]
  cases o <;>
    simp [List.mem_append, List.mem_cons, List.mem_singleton,
      squareLayer, or_assoc, or_left_comm, or_comm]

private theorem square_strip_cycle_step {n : Nat} (hn : 2 ≤ n) (o : Bool)
    (hopen : HamiltonPathOn (squareStripStates n) squareStripAdjacent
      (if o then 1 else 3, n - 1) (0, n - 1)) :
    HamiltonCycleOn (squareStripStates (n + 1)) squareStripAdjacent := by
  have htail := square_layer_path o n
  have hdis : DisjointLists (squareStripStates n)
      [(0, n), (if o then 3 else 1, n), (2, n),
        (if o then 1 else 3, n)] := by
    intro x hx hy
    have hx' := squareStrip_mem_layer_lt hx
    have hy' : x.2 = n := by
      simp [squareLayer] at hy
      rcases hy with rfl | rfl | rfl | rfl <;> rfl
    omega
  have hbridge₁ : squareStripAdjacent (0, n - 1) (0, n) := by
    simp [squareStripAdjacent]
    omega
  have hbridge₂ : squareStripAdjacent
      (if o then 1 else 3, n) (if o then 1 else 3, n - 1) := by
    simp [squareStripAdjacent]
    omega
  have hcycle := HamiltonPathOn.splice hopen htail hdis hbridge₁ hbridge₂
  rcases hcycle with ⟨path, hnodup, hcover, hclosed⟩
  refine ⟨path, hnodup, ?_, hclosed⟩
  intro x
  rw [squareStrip_states_cover_succ]
  cases o <;>
    simpa [squareLayer, List.mem_append, or_assoc, or_left_comm, or_comm]
      using hcover x

structure SquareStripCertificate (n : Nat) where
  orientation : Bool
  openProof : HamiltonPathOn (squareStripStates n) squareStripAdjacent
    (if orientation then 1 else 3, n - 1) (0, n - 1)

private def squareStripBaseCertificate : SquareStripCertificate 2 :=
  { orientation := true
    openProof := square_base_open }

private def squareStripCertificate_step {n : Nat}
    (hn : 2 ≤ n) (c : SquareStripCertificate n) :
    SquareStripCertificate (n + 1) := by
  cases ho : c.orientation with
  | false =>
      have hbase : HamiltonPathOn (squareStripStates n) squareStripAdjacent
          (if false then 1 else 3, n - 1) (0, n - 1) := by
        simpa [ho] using c.openProof
      have hopen := square_strip_open_step hn false hbase
      refine { orientation := true
               openProof := ?_ }
      simpa [ho] using hopen
  | true =>
      have hbase : HamiltonPathOn (squareStripStates n) squareStripAdjacent
          (if true then 1 else 3, n - 1) (0, n - 1) := by
        simpa [ho] using c.openProof
      have hopen := square_strip_open_step hn true hbase
      refine { orientation := false
               openProof := ?_ }
      simpa [ho] using hopen

private theorem squareStripCertificate_exists : ∀ n, 2 ≤ n →
    Nonempty (SquareStripCertificate n)
  | 0, hn => by omega
  | 1, hn => by omega
  | 2, hn => ⟨squareStripBaseCertificate⟩
  | n + 3, hn => by
      have hprev : 2 ≤ n + 2 := by omega
      rcases squareStripCertificate_exists (n + 2) hprev with ⟨c⟩
      exact ⟨squareStripCertificate_step hprev c⟩

/-- Each square component of the bad-run strip has a Hamilton cycle at every
length at least two.  The open-path certificate exposes the endpoint pair of
the newest-layer cut edge, which is the interface used by the next recursive
splice. -/
theorem square_strip_hamiltonCycle (n : Nat) (hn : 2 ≤ n) :
    HamiltonCycleOn (squareStripStates n) squareStripAdjacent := by
  cases n with
  | zero => omega
  | succ n =>
      cases n with
      | zero => omega
      | succ n =>
          cases n with
          | zero =>
              refine ⟨[(0, 0), (0, 1), (1, 1), (1, 0),
                (2, 0), (2, 1), (3, 1), (3, 0)], ?_, ?_, ?_⟩
              · decide
              · intro x
                simp [squareStripStates, squareLayer, or_assoc, or_left_comm, or_comm]
              · refine ⟨(0, 0), (3, 0), by simp, by simp, ?_, ?_⟩
                · simp only [Consecutive]
                  decide
                · decide
          | succ n =>
              have hprev : 2 ≤ n + 2 := by omega
              rcases squareStripCertificate_exists (n + 2) hprev with ⟨cprev⟩
              exact square_strip_cycle_step hprev cprev.orientation cprev.openProof

end PlanarRecoloring
