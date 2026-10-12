import PlanarRecoloring.Chapter4
import PlanarRecoloring.FibreHamilton

/-!
# Arbitrary-length adjacent-pair reset

The layers keep their actual assignments.  The reset argument below uses
only the Appendix A fibre paths and the permitted list transitions.  It
does not assume a Hamilton path of the layered graph as an input.
-/

namespace PlanarRecoloring

abbrev PairFiveLayer := PairFiveMask × PairFiveMask

def PairFiveLayerSmall (l : PairFiveLayer) : Prop :=
  pairFiveSmall l.1 ∧ pairFiveSmall l.2

def PairFiveLayerStates (l : PairFiveLayer) : List PairFiveState :=
  PairFiveStates l.1 l.2

def PairFiveLayerAllowed (l l' : PairFiveLayer) : Prop :=
  pairFiveAllowedB l.1 l.2 l'.1 l'.2 = true

def PairFiveCommonStates (l l' : PairFiveLayer) : List PairFiveState :=
  (PairFiveLayerStates l).filter (fun q => decide (q ∈ PairFiveLayerStates l'))

def PairFiveFirstMem (ls : List PairFiveLayer) (s : PairFiveState) : Prop :=
  ∃ l, ls.head? = some l ∧ s ∈ PairFiveLayerStates l

def PairFiveLastMem (ls : List PairFiveLayer) (t : PairFiveState) : Prop :=
  ∃ l, ls.getLast? = some l ∧ t ∈ PairFiveLayerStates l

/-- A full Hamilton path in each fibre, with equal assignments at interfaces. -/
def PairFiveChain : List PairFiveLayer → PairFiveState → PairFiveState → Prop
  | [], _, _ => False
  | [l], s, t => HamiltonPathOn (PairFiveLayerStates l) PairFiveAdjacent s t
  | l :: l' :: ls, s, t =>
      ∃ q, HamiltonPathOn (PairFiveLayerStates l) PairFiveAdjacent s q ∧
        q ∈ PairFiveLayerStates l' ∧ PairFiveChain (l' :: ls) q t

private theorem reset_hp_start {α : Type} {vs : List α} {r : α → α → Prop}
    {s t : α} (h : HamiltonPathOn vs r s t) : s ∈ vs := by
  rcases h with ⟨p, hh, _, _, hc, _⟩
  exact (hc s).mpr (List.mem_of_head? hh)

private theorem reset_hp_reverse {α : Type} {vs : List α} {r : α → α → Prop}
    (hsym : ∀ a b, r a b → r b a) {s t : α}
    (h : HamiltonPathOn vs r s t) : HamiltonPathOn vs r t s := by
  rcases h with ⟨p, hh, hl, hn, hc, hw⟩
  refine ⟨p.reverse, ?_, ?_, (List.reverse_perm p).symm.nodup hn, ?_,
    consecutive_reverse_of_symmetric hsym hw⟩
  · simpa only [List.head?_reverse] using hl
  · simpa only [List.getLast?_reverse] using hh
  · intro q
    rw [List.mem_reverse]
    exact hc q

private theorem reset_adjacent_symm :
    ∀ s t : PairFiveState, PairFiveAdjacent s t → PairFiveAdjacent t s := by
  decide

private theorem reset_allowed_symm_indexed :
    ∀ i j i' j' : Fin 15,
      pairFiveAllowedB (pairFiveSmallMask i) (pairFiveSmallMask j)
        (pairFiveSmallMask i') (pairFiveSmallMask j') =
      pairFiveAllowedB (pairFiveSmallMask i') (pairFiveSmallMask j')
        (pairFiveSmallMask i) (pairFiveSmallMask j) := by
  set_option maxHeartbeats 100000000 in decide

theorem pairFive_layer_allowed_symm {l l' : PairFiveLayer}
    (hl : PairFiveLayerSmall l) (hl' : PairFiveLayerSmall l')
    (h : PairFiveLayerAllowed l l') : PairFiveLayerAllowed l' l := by
  rcases l with ⟨m, n⟩
  rcases l' with ⟨m', n'⟩
  rcases pairFive_small_mask_index m hl.1 with ⟨i, rfl⟩
  rcases pairFive_small_mask_index n hl.2 with ⟨j, rfl⟩
  rcases pairFive_small_mask_index m' hl'.1 with ⟨i', rfl⟩
  rcases pairFive_small_mask_index n' hl'.2 with ⟨j', rfl⟩
  unfold PairFiveLayerAllowed at h ⊢
  rw [← reset_allowed_symm_indexed i j i' j']
  exact h

private theorem reset_interface_indexed :
    ∀ i j i' j' : Fin 15,
      (pairFiveList (pairFiveSmallMask i)).length = 4 →
      (pairFiveList (pairFiveSmallMask j)).length = 4 →
      pairFiveAllowedB (pairFiveSmallMask i) (pairFiveSmallMask j)
        (pairFiveSmallMask i') (pairFiveSmallMask j') = true →
      9 ≤ (PairFiveCommonStates
        (pairFiveSmallMask i, pairFiveSmallMask j)
        (pairFiveSmallMask i', pairFiveSmallMask j')).length ∧
      3 ≤ (pairFiveKind (pairFiveSmallMask i) (pairFiveSmallMask j)).val ∧
      3 ≤ (pairFiveKind (pairFiveSmallMask i') (pairFiveSmallMask j')).val := by
  set_option maxHeartbeats 100000000 in decide

theorem pairFive_reset_interface {l l' : PairFiveLayer}
    (hl : PairFiveLayerSmall l) (hl' : PairFiveLayerSmall l')
    (ha : (pairFiveList l.1).length = 4)
    (hb : (pairFiveList l.2).length = 4)
    (h : PairFiveLayerAllowed l l') :
    9 ≤ (PairFiveCommonStates l l').length ∧
      3 ≤ (pairFiveKind l.1 l.2).val ∧
      3 ≤ (pairFiveKind l'.1 l'.2).val := by
  rcases l with ⟨m, n⟩
  rcases l' with ⟨m', n'⟩
  rcases pairFive_small_mask_index m hl.1 with ⟨i, rfl⟩
  rcases pairFive_small_mask_index n hl.2 with ⟨j, rfl⟩
  rcases pairFive_small_mask_index m' hl'.1 with ⟨i', rfl⟩
  rcases pairFive_small_mask_index n' hl'.2 with ⟨j', rfl⟩
  exact reset_interface_indexed i j i' j' ha hb h

private theorem reset_common_nodup :
    ∀ m n m' n' : PairFiveMask,
      (PairFiveCommonStates (m, n) (m', n')).Nodup := by
  intro m n m' n'
  apply List.Nodup.sublist List.filter_sublist
  exact List.Nodup.sublist List.filter_sublist (List.nodup_finRange 25)

private theorem reset_avoid_two {α : Type} {xs : List α}
    (hn : xs.Nodup) (hlen : 3 ≤ xs.length) (a b : α) :
    ∃ c, c ∈ xs ∧ c ≠ a ∧ c ≠ b := by
  classical
  cases xs with
  | nil => simp at hlen
  | cons x xs =>
      cases xs with
      | nil => simp at hlen
      | cons y ys =>
          cases ys with
          | nil => simp at hlen
          | cons z zs =>
              have hxy : x ≠ y := by
                intro h
                exact (List.nodup_cons.mp hn).1 (by simp [h])
              have hxz : x ≠ z := by
                intro h
                exact (List.nodup_cons.mp hn).1 (by simp [h])
              have hyz : y ≠ z := by
                intro h
                exact (List.nodup_cons.mp (List.nodup_cons.mp hn).2).1 (by simp [h])
              by_cases hx : x ≠ a ∧ x ≠ b
              · exact ⟨x, by simp, hx⟩
              by_cases hy : y ≠ a ∧ y ≠ b
              · exact ⟨y, by simp, hy⟩
              by_cases hz : z ≠ a ∧ z ≠ b
              · exact ⟨z, by simp, hz⟩
              grind

private theorem reset_interface_path {l l' : PairFiveLayer}
    (hl : PairFiveLayerSmall l) (hl' : PairFiveLayerSmall l')
    (ha : PairFiveLayerAllowed l l') {s : PairFiveState}
    (hs : s ∈ PairFiveLayerStates l) :
    ∃ q, q ∈ PairFiveLayerStates l ∧ q ∈ PairFiveLayerStates l' ∧
      HamiltonPathOn (PairFiveLayerStates l) PairFiveAdjacent s q := by
  rcases pairFive_interface_path hl.1 hl.2 hl'.1 hl'.2 ha hs with
    ⟨q, hq, hq', _, hp⟩
  exact ⟨q, hq, hq', hp⟩

private theorem reset_last_cons {α : Type} (a b : α) (xs : List α) :
    (a :: b :: xs).getLast? = (b :: xs).getLast? := by
  simp

private theorem reset_consecutive_prefix {α : Type} {r : α → α → Prop}
    (xs ys : List α) (h : Consecutive r (xs ++ ys)) : Consecutive r xs := by
  induction xs with
  | nil => trivial
  | cons x xs ih =>
      cases xs with
      | nil => trivial
      | cons y ys' => exact ⟨h.1, ih h.2⟩

private theorem reset_consecutive_suffix {α : Type} {r : α → α → Prop}
    (xs ys : List α) (h : Consecutive r (xs ++ ys)) : Consecutive r ys := by
  induction xs with
  | nil => exact h
  | cons x xs ih =>
      apply ih
      cases hxs : xs ++ ys with
      | nil => simp only [Consecutive]
      | cons y zs =>
          have h' : Consecutive r (x :: y :: zs) := by
            simpa only [List.cons_append, hxs] using h
          simpa only [hxs] using h'.2

/-- Traverse a nonempty prefix and reach its next interface. -/
theorem pairFive_prefix_exit
    (ls : List PairFiveLayer) (next : PairFiveLayer)
    (hne : ls ≠ [])
    (hsmall : ∀ l, l ∈ ls ++ [next] → PairFiveLayerSmall l)
    (hallowed : Consecutive PairFiveLayerAllowed (ls ++ [next]))
    {s : PairFiveState} (hs : PairFiveFirstMem ls s) :
    ∃ q, q ∈ PairFiveLayerStates next ∧ PairFiveChain ls s q := by
  induction ls generalizing s with
  | nil => exact False.elim (hne rfl)
  | cons l ls ih =>
      have hsl : s ∈ PairFiveLayerStates l := by
        rcases hs with ⟨first, hf, hsf⟩
        have he : l = first := by simpa using hf
        simpa only [he] using hsf
      have hl := hsmall l (by simp)
      cases ls with
      | nil =>
          rcases reset_interface_path hl (hsmall next (by simp)) hallowed.1 hsl with
            ⟨q, _, hq, hp⟩
          exact ⟨q, hq, hp⟩
      | cons l' ls =>
          have hl' := hsmall l' (by simp)
          rcases reset_interface_path hl hl' hallowed.1 hsl with ⟨p, _, hp, hpath⟩
          rcases ih (by simp) (fun v hv => hsmall v (List.mem_cons_of_mem l hv))
            hallowed.2 ⟨l', rfl, hp⟩ with ⟨q, hq, hchain⟩
          exact ⟨q, hq, p, hpath, hp, hchain⟩

/-- Reverse propagation supplies an entrance from the preceding interface. -/
theorem pairFive_suffix_entry
    (ls : List PairFiveLayer) (prev : PairFiveLayer)
    (hsmall : ∀ l, l ∈ prev :: ls → PairFiveLayerSmall l)
    (hallowed : Consecutive PairFiveLayerAllowed (prev :: ls))
    {t : PairFiveState} (ht : PairFiveLastMem ls t) :
    ∃ q, q ∈ PairFiveLayerStates prev ∧ PairFiveFirstMem ls q ∧
      PairFiveChain ls q t := by
  induction ls generalizing prev with
  | nil => rcases ht with ⟨l, hl, _⟩; simp at hl
  | cons l ls ih =>
      have hprev := hsmall prev (by simp)
      have hl := hsmall l (by simp)
      have hback := pairFive_layer_allowed_symm hprev hl hallowed.1
      cases ls with
      | nil =>
          have htl : t ∈ PairFiveLayerStates l := by
            rcases ht with ⟨last, hh, htm⟩
            have he : l = last := by simpa using hh
            simpa only [he] using htm
          rcases reset_interface_path hl hprev hback htl with ⟨q, hq, hqp, hp⟩
          exact ⟨q, hqp, ⟨l, rfl, hq⟩, reset_hp_reverse reset_adjacent_symm hp⟩
      | cons l' ls =>
          have ht' : PairFiveLastMem (l' :: ls) t := by
            rcases ht with ⟨last, hh, htm⟩
            exact ⟨last, by simpa only [reset_last_cons] using hh, htm⟩
          rcases ih l (fun v hv => hsmall v (List.mem_cons_of_mem prev hv)) hallowed.2 ht' with
            ⟨p, hpl, hpfirst, htail⟩
          rcases hpfirst with ⟨first, hf, hpf⟩
          have he : l' = first := by simpa using hf
          have hpl' : p ∈ PairFiveLayerStates l' := by simpa only [he] using hpf
          rcases reset_interface_path hl hprev hback hpl with ⟨q, hql, hqp, hp⟩
          exact ⟨q, hqp, ⟨l, rfl, hql⟩,
            p, reset_hp_reverse reset_adjacent_symm hp, hpl', htail⟩

private theorem pairFive_chain_append
    {ls : List PairFiveLayer} {next : PairFiveLayer}
    {s q t : PairFiveState}
    (hchain : PairFiveChain ls s q)
    (hq : q ∈ PairFiveLayerStates next)
    (hnext : HamiltonPathOn (PairFiveLayerStates next)
      PairFiveAdjacent q t) :
    PairFiveChain (ls ++ [next]) s t := by
  cases ls with
  | nil => exact False.elim hchain
  | cons l ls =>
      cases ls with
      | nil =>
          simpa only [List.cons_append, List.nil_append] using
            (show PairFiveChain [l, next] s t from ⟨q, hchain, hq, hnext⟩)
      | cons l' ls =>
          rcases hchain with ⟨p, hp, hp', htail⟩
          have happ := pairFive_chain_append (ls := l' :: ls)
            (next := next) htail hq hnext
          exact ⟨p, hp, hp', by simpa [List.cons_append] using happ⟩

private theorem pairFive_chain_concat
    {ls rs : List PairFiveLayer} {s q t : PairFiveState}
    (hleft : PairFiveChain ls s q)
    (hright : PairFiveChain rs q t) :
    PairFiveChain (ls ++ rs) s t := by
  cases rs with
  | nil => exact False.elim hright
  | cons l rs =>
      cases rs with
      | nil =>
          have hq : q ∈ PairFiveLayerStates l := reset_hp_start hright
          exact pairFive_chain_append hleft hq hright
      | cons l' rs =>
          rcases hright with ⟨p, hp, hp', htail⟩
          have hleft' : PairFiveChain (ls ++ [l]) s p :=
            pairFive_chain_append hleft (reset_hp_start hp) hp
          have hrest : PairFiveChain ((l' :: rs)) p t := htail
          have hcat := pairFive_chain_concat hleft' hrest
          simpa [List.append_assoc] using hcat

private theorem pairFive_common_mem_left
    {l l' : PairFiveLayer} {q : PairFiveState}
    (hq : q ∈ PairFiveCommonStates l l') :
    q ∈ PairFiveLayerStates l := by
  exact (List.mem_filter.mp hq).1

private theorem pairFive_common_mem_right
    {l l' : PairFiveLayer} {q : PairFiveState}
    (hq : q ∈ PairFiveCommonStates l l') :
    q ∈ PairFiveLayerStates l' := by
  have h := (List.mem_filter.mp hq).2
  simpa only [decide_eq_true_eq] using h

theorem pairFive_reset_chain
    (pref : List PairFiveLayer) (middle next : PairFiveLayer)
    (suffix : List PairFiveLayer)
    (hprefix : pref ≠ [])
    (hsmall : ∀ l, l ∈ pref ++ middle :: next :: suffix →
      PairFiveLayerSmall l)
    (hallowed : Consecutive PairFiveLayerAllowed
      (pref ++ middle :: next :: suffix))
    {s t : PairFiveState}
    (hs : PairFiveFirstMem pref s)
    (ht : PairFiveLastMem (middle :: next :: suffix) t)
    (hmiddleA : (pairFiveList middle.1).length = 4)
    (hmiddleB : (pairFiveList middle.2).length = 4) :
    PairFiveChain (pref ++ middle :: next :: suffix) s t := by
  have hprefix_mid : Consecutive PairFiveLayerAllowed
      (pref ++ [middle]) := by
    apply reset_consecutive_prefix (xs := pref ++ [middle])
      (ys := next :: suffix)
    simpa [List.append_assoc] using hallowed
  have hsmall_prefix_mid : ∀ l, l ∈ pref ++ [middle] →
      PairFiveLayerSmall l := by
    intro l hl
    apply hsmall l
    have hl' : l ∈ pref ∨ l = middle := by simpa using hl
    simp only [List.mem_append, List.mem_cons]
    rcases hl' with hp | hm
    · exact Or.inl hp
    · exact Or.inr (Or.inl hm)
  rcases pairFive_prefix_exit pref middle hprefix hsmall_prefix_mid
      hprefix_mid hs with ⟨q, hqmiddle, hprefix_chain⟩
  have hmiddle_small := hsmall middle (by simp)
  have hnext_small := hsmall next (by simp)
  have hmiddle_next : PairFiveLayerAllowed middle next := by
    have htail := reset_consecutive_suffix pref
      (middle :: next :: suffix) hallowed
    exact htail.1
  have hinterface := pairFive_reset_interface hmiddle_small hnext_small
    hmiddleA hmiddleB hmiddle_next
  have hcommon_len := hinterface.1
  have hmiddle_hc : HamiltonConnectedOn (PairFiveLayerStates middle)
      PairFiveAdjacent :=
    pairFive_hamiltonConnected hmiddle_small.1 hmiddle_small.2 hinterface.2.1
  have hnext_hc : HamiltonConnectedOn (PairFiveLayerStates next)
      PairFiveAdjacent :=
    pairFive_hamiltonConnected hnext_small.1 hnext_small.2 hinterface.2.2
  have hnext_suffix_small : ∀ l, l ∈ next :: suffix →
      PairFiveLayerSmall l := by
    intro l hl
    apply hsmall l
    have hl' : l = next ∨ l ∈ suffix := by simpa using hl
    simp only [List.mem_append, List.mem_cons]
    rcases hl' with hn | hsuf
    · exact Or.inr (Or.inr (Or.inl hn))
    · exact Or.inr (Or.inr (Or.inr hsuf))
  have hnext_suffix_allowed : Consecutive PairFiveLayerAllowed
      (next :: suffix) := by
    have htail := reset_consecutive_suffix pref
      (middle :: next :: suffix) hallowed
    exact htail.2
  cases suffix with
  | nil =>
      have ht_next : t ∈ PairFiveLayerStates next := by
        rcases ht with ⟨last, hlast, htm⟩
        have he : next = last := by simpa using hlast
        simpa only [he] using htm
      have hchoose : ∃ c, c ∈ PairFiveCommonStates middle next ∧
          c ≠ q ∧ c ≠ t :=
        reset_avoid_two (xs := PairFiveCommonStates middle next)
          (by simpa [PairFiveCommonStates, PairFiveLayerStates] using
            reset_common_nodup middle.1 middle.2 next.1 next.2)
          (by omega : 3 ≤ (PairFiveCommonStates middle next).length) q t
      rcases hchoose with ⟨c, hc, hcq, hct⟩
      have hcm := pairFive_common_mem_left hc
      have hcn := pairFive_common_mem_right hc
      have hmiddle_path := hmiddle_hc q c hqmiddle hcm hcq.symm
      have hnext_path := hnext_hc c t hcn ht_next hct
      have hnext_chain : PairFiveChain [next] c t := hnext_path
      have hmiddle_chain : PairFiveChain (middle :: next :: []) q t :=
        ⟨c, hmiddle_path, hcn, hnext_chain⟩
      have hcat := pairFive_chain_concat hprefix_chain hmiddle_chain
      simpa only [List.append_assoc, List.nil_append] using hcat
  | cons first rest =>
      have ht_suffix : PairFiveLastMem (first :: rest) t := by
        rcases ht with ⟨last, hlast, htm⟩
        exact ⟨last, by simpa [reset_last_cons] using hlast, htm⟩
      rcases pairFive_suffix_entry (first :: rest) next
          hnext_suffix_small hnext_suffix_allowed ht_suffix with
        ⟨r, hrnext, hrfirst, hsuffix_chain⟩
      have hchoose : ∃ c, c ∈ PairFiveCommonStates middle next ∧
          c ≠ q ∧ c ≠ r :=
        reset_avoid_two (xs := PairFiveCommonStates middle next)
          (by simpa [PairFiveCommonStates, PairFiveLayerStates] using
            reset_common_nodup middle.1 middle.2 next.1 next.2)
          (by omega : 3 ≤ (PairFiveCommonStates middle next).length) q r
      rcases hchoose with ⟨c, hc, hcq, hcr⟩
      have hcm := pairFive_common_mem_left hc
      have hcn := pairFive_common_mem_right hc
      have hmiddle_path := hmiddle_hc q c hqmiddle hcm hcq.symm
      have hrfirst' : r ∈ PairFiveLayerStates first := by
        rcases hrfirst with ⟨l, hl, hrl⟩
        have he : first = l := by simpa using hl
        simpa only [he] using hrl
      have hnext_path := hnext_hc c r hcn hrnext hcr
      have hnext_chain : PairFiveChain (next :: first :: rest) c t :=
        ⟨r, hnext_path, hrfirst', hsuffix_chain⟩
      have hmiddle_chain : PairFiveChain
          (middle :: next :: first :: rest) q t :=
        ⟨c, hmiddle_path, hcn, hnext_chain⟩
      have hcat := pairFive_chain_concat hprefix_chain hmiddle_chain
      simpa only [List.append_assoc] using hcat

/-- Layer-tagged states keep equal assignments in different fibres distinct. -/
abbrev PairFiveTaggedState := Nat × PairFiveState

def PairFiveTaggedInside (x y : PairFiveTaggedState) : Prop :=
  x.1 = y.1 ∧ PairFiveAdjacent x.2 y.2

def PairFiveTaggedBridge (x y : PairFiveTaggedState) : Prop :=
  x.1 + 1 = y.1 ∧ x.2 = y.2

def PairFiveTaggedLayer (i : Nat) (l : PairFiveLayer) :
    List PairFiveTaggedState :=
  (PairFiveLayerStates l).map (fun q => (i, q))

def PairFiveTaggedVertices : Nat → List PairFiveLayer →
    List PairFiveTaggedState
  | _, [] => []
  | i, l :: ls => PairFiveTaggedLayer i l ++
      PairFiveTaggedVertices (i + 1) ls

private theorem pairFive_tagged_layer_tag {i : Nat} {l : PairFiveLayer}
    {x : PairFiveTaggedState} (hx : x ∈ PairFiveTaggedLayer i l) :
    x.1 = i := by
  rcases List.mem_map.mp hx with ⟨q, _, rfl⟩
  rfl

private theorem pairFive_tagged_vertices_lower {i : Nat}
    {ls : List PairFiveLayer} {x : PairFiveTaggedState}
    (hx : x ∈ PairFiveTaggedVertices i ls) : i ≤ x.1 := by
  induction ls generalizing i with
  | nil => simp [PairFiveTaggedVertices] at hx
  | cons l ls ih =>
      simp only [PairFiveTaggedVertices, List.mem_append] at hx
      rcases hx with hx | hx
      · have hi := pairFive_tagged_layer_tag hx
        omega
      · exact Nat.le_trans (Nat.le_add_right i 1) (ih (i := i + 1) hx)

private theorem pairFive_tagged_disjoint {i : Nat} {l : PairFiveLayer}
    {ls : List PairFiveLayer} :
    DisjointLists (PairFiveTaggedLayer i l)
      (PairFiveTaggedVertices (i + 1) ls) := by
  intro x hx htail
  have hi : x.1 = i := pairFive_tagged_layer_tag hx
  have hge : i + 1 ≤ x.1 := pairFive_tagged_vertices_lower htail
  omega

private theorem hamiltonPathOn_append_layer
    {α : Type} {r : α → α → Prop}
    {v₁ v₂ : List α} {s q u t : α}
    (h₁ : HamiltonPathOn v₁ r s q)
    (h₂ : HamiltonPathOn v₂ r u t)
    (hdis : DisjointLists v₁ v₂)
    (hbridge : r q u) :
    HamiltonPathOn (v₁ ++ v₂) r s t := by
  rcases h₁ with ⟨p₁, hh₁, hl₁, hn₁, hc₁, hw₁⟩
  rcases h₂ with ⟨p₂, hh₂, hl₂, hn₂, hc₂, hw₂⟩
  have hp₁ : p₁ ≠ [] := by
    intro hnil
    subst p₁
    simp at hh₁
  have hp₂ : p₂ ≠ [] := by
    intro hnil
    subst p₂
    simp at hh₂
  have hdis' : DisjointLists p₁ p₂ := by
    intro x hx₁ hx₂
    exact hdis ((hc₁ x).mpr hx₁) ((hc₂ x).mpr hx₂)
  refine ⟨p₁ ++ p₂, ?_, ?_, nodup_append_of_disjoint hn₁ hn₂ hdis', ?_, ?_⟩
  · rw [head_append_of_ne_nil hp₁, hh₁]
  · rw [getLast_append_of_ne_nil hp₂, hl₂]
  · intro x
    simp only [List.mem_append]
    rw [hc₁ x, hc₂ x]
  · apply consecutive_append hw₁ hw₂ hp₁ hp₂ hl₁ hh₂
    exact hbridge

private theorem pairFive_chain_tagged_hamilton
    (i : Nat) {ls : List PairFiveLayer} {s t : PairFiveState}
    (h : PairFiveChain ls s t) :
    HamiltonPathOn (PairFiveTaggedVertices i ls)
      (LayeredEdge PairFiveTaggedInside PairFiveTaggedBridge)
      (i, s) (i + (ls.length - 1), t) := by
  cases ls with
  | nil => exact False.elim h
  | cons l ls =>
      cases ls with
      | nil =>
          have hmap := HamiltonPathOn.map (fun q => (i, q))
            (fun a b hab => by exact congrArg Prod.snd hab)
            (fun {a b : PairFiveState} hab =>
              (show LayeredEdge PairFiveTaggedInside PairFiveTaggedBridge
                (i, a) (i, b) from Or.inl ⟨rfl, hab⟩)) h
          simpa [PairFiveTaggedVertices, PairFiveTaggedLayer] using hmap
      | cons l' ls =>
          rcases h with ⟨q, hp, hq, htail⟩
          have hleft := HamiltonPathOn.map (fun z => (i, z))
            (fun a b hab => by exact congrArg Prod.snd hab)
            (fun {a b : PairFiveState} hab =>
              (show LayeredEdge PairFiveTaggedInside PairFiveTaggedBridge
                (i, a) (i, b) from Or.inl ⟨rfl, hab⟩)) hp
          have hright := pairFive_chain_tagged_hamilton (i + 1) htail
          have hdis : DisjointLists (PairFiveTaggedLayer i l)
              (PairFiveTaggedVertices (i + 1) (l' :: ls)) :=
            pairFive_tagged_disjoint (i := i) (l := l) (ls := l' :: ls)
          have hbridge : LayeredEdge PairFiveTaggedInside PairFiveTaggedBridge
              (i, q) (i + 1, q) :=
            Or.inr ⟨by omega, rfl⟩
          have hcat := hamiltonPathOn_append_layer hleft hright
            hdis hbridge
          have hidx : i + 1 + ((l' :: ls).length - 1) =
              i + ((l :: l' :: ls).length - 1) := by
            simp
            omega
          rw [hidx] at hcat
          simpa [PairFiveTaggedVertices, PairFiveTaggedLayer,
            List.append_assoc] using hcat

theorem pairFive_reset_tagged_hamiltonPathOn
    (pref : List PairFiveLayer) (middle next : PairFiveLayer)
    (suffix : List PairFiveLayer)
    (hprefix : pref ≠ [])
    (hsmall : ∀ l, l ∈ pref ++ middle :: next :: suffix →
      PairFiveLayerSmall l)
    (hallowed : Consecutive PairFiveLayerAllowed
      (pref ++ middle :: next :: suffix))
    {s t : PairFiveState}
    (hs : PairFiveFirstMem pref s)
    (ht : PairFiveLastMem (middle :: next :: suffix) t)
    (hmiddleA : (pairFiveList middle.1).length = 4)
    (hmiddleB : (pairFiveList middle.2).length = 4) :
    HamiltonPathOn
      (PairFiveTaggedVertices 0 (pref ++ middle :: next :: suffix))
      (LayeredEdge PairFiveTaggedInside PairFiveTaggedBridge)
      (0, s) ((pref ++ middle :: next :: suffix).length - 1, t) := by
  have hchain := pairFive_reset_chain pref middle next suffix hprefix hsmall
    hallowed hs ht hmiddleA hmiddleB
  simpa using pairFive_chain_tagged_hamilton 0 hchain

end PlanarRecoloring
