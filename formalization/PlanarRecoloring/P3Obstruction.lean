import PlanarRecoloring.Hamilton

/-!
# The finite forest obstruction

The three-colour recolouring graph of the path on three vertices has twelve
states. This file encodes those states as the six possible endpoint choices
for each middle-vertex colour and proves, by a kernel-checked finite search,
that no spanning cycle exists. The search is a bounded proof of the finite
obstruction used for the lower bound in Chapter 4; it does not assert the
forest upper bound.
-/

namespace PlanarRecoloring
set_option maxHeartbeats 0
set_option maxRecDepth 100000
abbrev P3State := Fin 12

def p3Other (b : Fin 3) (i : Fin 2) : Fin 3 :=
  match b.val, i.val with
  | 0, 0 => ⟨1, by omega⟩
  | 0, _ => ⟨2, by omega⟩
  | 1, 0 => ⟨0, by omega⟩
  | 1, _ => ⟨2, by omega⟩
  | _, 0 => ⟨0, by omega⟩
  | _, _ => ⟨1, by omega⟩

def p3Middle (s : P3State) : Fin 3 := ⟨s.val / 4, by omega⟩
def p3Left (s : P3State) : Fin 3 :=
  p3Other (p3Middle s) (Fin.ofNat 2 (s.val / 2))
def p3Right (s : P3State) : Fin 3 :=
  p3Other (p3Middle s) (Fin.ofNat 2 s.val)
def p3AdjacentB (s t : P3State) : Bool :=
  ((decide (p3Left s ≠ p3Left t) && decide (p3Middle s = p3Middle t) &&
      decide (p3Right s = p3Right t)) ||
   (decide (p3Left s = p3Left t) && decide (p3Middle s ≠ p3Middle t) &&
      decide (p3Right s = p3Right t)) ||
   (decide (p3Left s = p3Left t) && decide (p3Middle s = p3Middle t) &&
      decide (p3Right s ≠ p3Right t)))
def P3Adjacent (s t : P3State) : Prop := p3AdjacentB s t = true
def P3States : List P3State := List.finRange 12

instance p3AdjacentDecidable (s t : P3State) : Decidable (P3Adjacent s t) := by
  unfold P3Adjacent
  infer_instance

theorem p3_adj_symm : ∀ s t, P3Adjacent s t → P3Adjacent t s := by decide

def p3Search (start current : P3State) (visited : List P3State) : Nat → Bool
  | 0 => p3AdjacentB current start
  | fuel + 1 =>
      (List.finRange 12).any (fun q =>
        decide (q ∉ visited) && p3AdjacentB current q &&
          p3Search start q (q :: visited) fuel)

def p3CycleSearch : Bool :=
  (List.finRange 12).any (fun s => p3Search s s [s] 11)

set_option maxRecDepth 100000 in
theorem p3_cycle_search_false : p3CycleSearch = false := by decide

end PlanarRecoloring

namespace PlanarRecoloring

private theorem p3_search_follow (start current : P3State) :
    ∀ (visited rest : List P3State) (last : P3State) (fuel : Nat),
      rest.length = fuel →
      (current :: rest).Nodup →
      (∀ x, x ∈ rest → x ∉ visited) →
      Consecutive P3Adjacent (current :: rest) →
      (current :: rest).getLast? = some last →
      P3Adjacent last start →
      p3Search start current visited fuel = true := by
  intro visited rest last fuel
  induction fuel generalizing current visited rest last with
  | zero =>
      intro hlen hn hnot hcon hlast hclose
      have hrest : rest = [] := by
        cases rest with
        | nil => rfl
        | cons x xs => simp at hlen
      subst rest
      simp only [p3Search]
      have hcur : current = last := by simpa using hlast
      simpa [hcur, P3Adjacent] using hclose
  | succ fuel ih =>
      intro hlen hn hnot hcon hlast hclose
      cases rest with
      | nil => simp at hlen
      | cons q qs =>
          have hqnot : q ∉ visited := hnot q (by simp)
          have hqneq : q ≠ current := by
            intro heq
            subst q
            exact (List.nodup_cons.mp hn).1 (by simp)
          have htailnodup : (q :: qs).Nodup := (List.nodup_cons.mp hn).2
          have htailnot : ∀ x, x ∈ qs → x ∉ q :: visited := by
            intro x hx hmem
            simp only [List.mem_cons] at hmem
            rcases hmem with rfl | hmem
            · exact (List.nodup_cons.mp htailnodup).1 hx
            · exact hnot x (by simp [hx]) hmem
          have htailcon : Consecutive P3Adjacent (q :: qs) := hcon.2
          have htaillen : qs.length = fuel := by simpa using hlen
          have hlast' : (q :: qs).getLast? = some last := by
            simpa using hlast
          have hqadj : P3Adjacent current q := hcon.1
          have hrec := ih (current := q) (visited := q :: visited)
            (rest := qs) (last := last) htaillen htailnodup htailnot
            htailcon hlast' hclose
          rw [p3Search]
          rw [List.any_eq_true]
          refine ⟨q, List.mem_finRange q, ?_⟩
          simp only [Bool.and_eq_true, decide_eq_true_eq]
          exact ⟨⟨hqnot, hqadj⟩, hrec⟩

theorem p3_no_hamiltonCycleOn :
    ¬ HamiltonCycleOn P3States P3Adjacent := by
  intro h
  rcases h with ⟨path, hn, hc, hclosed⟩
  rcases hclosed with ⟨start, last, hhead, hlast, hcon, hclose⟩
  have hpath_to_states : path ⊆ P3States := by
    intro x hx
    exact List.mem_finRange x
  have hstates_to_path : P3States ⊆ path := by
    intro x hx
    exact (hc x).mp hx
  have hle : path.length ≤ P3States.length :=
    List.Nodup.length_le_of_subset hn hpath_to_states
  have hge : P3States.length ≤ path.length :=
    List.Nodup.length_le_of_subset (List.nodup_finRange 12) hstates_to_path
  have hlen : path.length = 12 := by
    unfold P3States at hle hge
    simp only [List.length_finRange] at hle hge
    omega
  rw [List.head?_eq_some_iff] at hhead
  rcases hhead with ⟨tail, rfl⟩
  have htail_len : tail.length = 11 := by simp_all
  have htail_not : ∀ x, x ∈ tail → x ∉ [start] := by
    intro x hx hmem
    simp only [List.mem_singleton] at hmem
    subst x
    exact (List.nodup_cons.mp hn).1 hx
  have hlast' : (start :: tail).getLast? = some last := hlast
  have hsearch := p3_search_follow start start [start] tail last 11
    htail_len hn htail_not hcon hlast' hclose
  have hglobal : p3CycleSearch = true := by
    unfold p3CycleSearch
    rw [List.any_eq_true]
    exact ⟨start, List.mem_finRange start, hsearch⟩
  rw [p3_cycle_search_false] at hglobal
  cases hglobal

end PlanarRecoloring
