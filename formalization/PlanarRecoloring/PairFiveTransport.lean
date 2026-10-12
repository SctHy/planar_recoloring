import PlanarRecoloring.PairFive

/-! Transport the finite Chapter 4 witnesses to every labelled list pair. -/
namespace PlanarRecoloring

set_option maxHeartbeats 100000000

private theorem pairFive_encode_fst :
    ∀ a b : Fin 5, pairFiveFst (pairFiveEncode a b) = a := by decide
private theorem pairFive_encode_snd :
    ∀ a b : Fin 5, pairFiveSnd (pairFiveEncode a b) = b := by decide
private theorem pairFive_encode_self :
    ∀ s : PairFiveState, pairFiveEncode (pairFiveFst s) (pairFiveSnd s) = s := by decide

theorem pairFive_norm_kind :
    ∀ m n : PairFiveMask, (pairFiveNorm m n).kind < 7 := by decide

def pairFiveKind (m n : PairFiveMask) : PairFiveKind :=
  ⟨(pairFiveNorm m n).kind, pairFive_norm_kind m n⟩

theorem pairFive_norm_membership :
    ∀ m n : PairFiveMask, pairFiveSmall m → pairFiveSmall n →
      ∀ s : PairFiveState,
        s ∈ PairFiveStates m n ↔
          pairFiveUnmap (pairFiveNorm m n) s ∈
            PairFiveStates (pairFiveCanonA (pairFiveKind m n))
              (pairFiveCanonB (pairFiveKind m n)) := by decide

theorem pairFive_norm_palette_inverse :
    ∀ m n : PairFiveMask, ∀ c : Fin 5,
      pairFivePerm (pairFiveNorm m n).q (pairFivePerm (pairFiveNorm m n).p c) = c ∧
      pairFivePerm (pairFiveNorm m n).p (pairFivePerm (pairFiveNorm m n).q c) = c := by
  decide

private theorem pairFive_map_unmap (d : PairFiveNorm)
    (hleft : ∀ c, pairFivePerm d.q (pairFivePerm d.p c) = c)
    (hright : ∀ c, pairFivePerm d.p (pairFivePerm d.q c) = c)
    (s : PairFiveState) :
    pairFiveMap d (pairFiveUnmap d s) = s ∧
      pairFiveUnmap d (pairFiveMap d s) = s := by
  cases hs : d.swap <;>
    simp [pairFiveMap, pairFiveUnmap, hs, pairFive_encode_fst,
      pairFive_encode_snd, hleft, hright, pairFive_encode_self]

theorem pairFive_norm_inverse (m n : PairFiveMask) (s : PairFiveState) :
    pairFiveMap (pairFiveNorm m n) (pairFiveUnmap (pairFiveNorm m n) s) = s ∧
      pairFiveUnmap (pairFiveNorm m n) (pairFiveMap (pairFiveNorm m n) s) = s :=
  pairFive_map_unmap _ (fun c => (pairFive_norm_palette_inverse m n c).1)
    (fun c => (pairFive_norm_palette_inverse m n c).2) s

private theorem pairFive_map_adjacent (d : PairFiveNorm)
    (hinj : Function.Injective (pairFivePerm d.p))
    {s t : PairFiveState} (h : PairFiveAdjacent s t) :
    PairFiveAdjacent (pairFiveMap d s) (pairFiveMap d t) := by
  have hpne : ∀ a b, a ≠ b → pairFivePerm d.p a ≠ pairFivePerm d.p b := by
    intro a b hab hpab
    exact hab (hinj hpab)
  unfold PairFiveAdjacent pairFiveAdjB at h ⊢
  simp only [Bool.or_eq_true, Bool.and_eq_true, decide_eq_true_eq] at h ⊢
  cases hs : d.swap <;>
    simp only [pairFiveMap, hs, Bool.false_eq_true, ite_false, ite_true,
      pairFive_encode_fst, pairFive_encode_snd] <;>
    rcases h with ⟨hne, heq⟩ | ⟨heq, hne⟩
  · exact Or.inl ⟨hpne _ _ hne, congrArg (pairFivePerm d.p) heq⟩
  · exact Or.inr ⟨congrArg (pairFivePerm d.p) heq, hpne _ _ hne⟩
  · exact Or.inr ⟨congrArg (pairFivePerm d.p) heq, hpne _ _ hne⟩
  · exact Or.inl ⟨hpne _ _ hne, congrArg (pairFivePerm d.p) heq⟩

theorem pairFive_norm_map_adjacent (m n : PairFiveMask)
    {s t : PairFiveState} (h : PairFiveAdjacent s t) :
    PairFiveAdjacent (pairFiveMap (pairFiveNorm m n) s)
      (pairFiveMap (pairFiveNorm m n) t) := by
  apply pairFive_map_adjacent _ ?_ h
  intro a b hab
  have hp := congrArg (pairFivePerm (pairFiveNorm m n).q) hab
  simpa only [(pairFive_norm_palette_inverse m n a).1,
    (pairFive_norm_palette_inverse m n b).1] using hp

theorem pairFive_norm_unmap_adjacent (m n : PairFiveMask)
    {s t : PairFiveState} (h : PairFiveAdjacent s t) :
    PairFiveAdjacent (pairFiveUnmap (pairFiveNorm m n) s)
      (pairFiveUnmap (pairFiveNorm m n) t) := by
  let d : PairFiveNorm :=
    { kind := 0
      swap := (pairFiveNorm m n).swap
      p := (pairFiveNorm m n).q
      q := (pairFiveNorm m n).p }
  have hinj : Function.Injective (pairFivePerm d.p) := by
    intro a b hab
    have hp := congrArg (pairFivePerm (pairFiveNorm m n).p) hab
    simpa only [d, (pairFive_norm_palette_inverse m n a).2,
      (pairFive_norm_palette_inverse m n b).2] using hp
  simpa only [pairFiveMap, pairFiveUnmap, d] using
    (pairFive_map_adjacent d hinj h)

private theorem consecutive_map_vertices {α : Type u} {β : Type v}
    {r : α → α → Prop} {r' : β → β → Prop} (f : α → β)
    (hrel : ∀ a b, r a b → r' (f a) (f b)) :
    ∀ {path : List α}, Consecutive r path → Consecutive r' (path.map f) := by
  intro path
  induction path with
  | nil => intro _; trivial
  | cons x xs ih =>
      cases xs with
      | nil => intro _; trivial
      | cons y ys =>
          intro h
          exact ⟨hrel _ _ h.1, ih h.2⟩

private theorem transport_nodup {α : Type u} {β : Type v}
    {f : α → β} (hinj : Function.Injective f) {path : List α}
    (h : path.Nodup) : (path.map f).Nodup := by
  rw [List.nodup_iff_pairwise_ne] at h ⊢
  apply List.Pairwise.map f ?_ h
  intro a b hab heq
  exact hab (hinj heq)

private theorem pairFive_edgeIn_map
    (f : PairFiveState → PairFiveState)
    {s t : PairFiveState} {path : List PairFiveState}
    (h : pairFiveEdgeIn s t path) :
    pairFiveEdgeIn (f s) (f t) (path.map f) := by
  unfold pairFiveEdgeIn at h ⊢
  unfold pairFiveEdgeInB at h ⊢
  cases path with
  | nil => simp at h
  | cons x xs =>
      simp only [Bool.or_eq_true, Bool.and_eq_true, decide_eq_true_eq] at h
      simp [List.map]
      rcases h with h | h
      · left
        have hxs : x = s := h.1
        have hxt : xs.head? = some t := h.2
        subst x
        refine ⟨rfl, ?_⟩
        exact ⟨t, hxt, rfl⟩
      · right
        have hxs : x = t := h.1
        have hxt : xs.head? = some s := h.2
        subst x
        refine ⟨rfl, ?_⟩
        exact ⟨s, hxt, rfl⟩

theorem HamiltonPathOn.transport {α : Type u} {β : Type v}
    {vertices : List α} {vertices' : List β}
    {r : α → α → Prop} {r' : β → β → Prop}
    (f : α → β) (g : β → α)
    (hleft : ∀ a, g (f a) = a) (hright : ∀ b, f (g b) = b)
    (hmem : ∀ b, b ∈ vertices' ↔ g b ∈ vertices)
    (hrel : ∀ a b, r a b → r' (f a) (f b))
    {s t : α} (h : HamiltonPathOn vertices r s t) :
    HamiltonPathOn vertices' r' (f s) (f t) := by
  rcases h with ⟨path, hh, hl, hn, hc, hw⟩
  refine ⟨path.map f, ?_, ?_, ?_, ?_, consecutive_map_vertices f hrel hw⟩
  · simp only [List.head?_map, hh, Option.map_some]
  · simp only [List.getLast?_map, hl, Option.map_some]
  · apply transport_nodup (path := path) ?_ hn
    intro a b hab
    have h' := congrArg g hab
    simpa only [hleft] using h'
  · intro b
    rw [hmem b, hc (g b), List.mem_map]
    constructor
    · intro hb
      exact ⟨g b, hb, hright b⟩
    · rintro ⟨a, ha, hab⟩
      have hgb : g b = a := by rw [← hab, hleft]
      simpa only [hgb] using ha

theorem HamiltonCycleOn.transport {α : Type u} {β : Type v}
    {vertices : List α} {vertices' : List β}
    {r : α → α → Prop} {r' : β → β → Prop}
    (f : α → β) (g : β → α)
    (hleft : ∀ a, g (f a) = a) (hright : ∀ b, f (g b) = b)
    (hmem : ∀ b, b ∈ vertices' ↔ g b ∈ vertices)
    (hrel : ∀ a b, r a b → r' (f a) (f b))
    (h : HamiltonCycleOn vertices r) :
    HamiltonCycleOn vertices' r' := by
  rcases h with ⟨path, hn, hc, hclosed⟩
  rcases hclosed with ⟨a, z, ha, hz, hw, hclose⟩
  refine ⟨path.map f, ?_, ?_, ?_⟩
  · apply transport_nodup (path := path) ?_ hn
    intro x y hxy
    have h' := congrArg g hxy
    simpa only [hleft] using h'
  · intro b
    rw [hmem b, hc (g b), List.mem_map]
    constructor
    · intro hb
      exact ⟨g b, hb, hright b⟩
    · rintro ⟨x, hx, hxb⟩
      have hgb : g b = x := by rw [← hxb, hleft]
      simpa only [hgb] using hx
  · refine ⟨f a, f z, ?_, ?_, ?_, ?_⟩
    · simpa only [List.head?_map, ha, Option.map_some]
    · simpa only [List.getLast?_map, hz, Option.map_some]
    · exact consecutive_map_vertices f hrel hw
    · exact hrel _ _ hclose

theorem pairFive_hamiltonConnected
    {m n : PairFiveMask} (hm : pairFiveSmall m) (hn : pairFiveSmall n)
    (hkind : 3 ≤ (pairFiveKind m n).val) :
    HamiltonConnectedOn (PairFiveStates m n) PairFiveAdjacent := by
  intro s t hs ht hst
  let d := pairFiveNorm m n
  let cs := pairFiveUnmap d s
  let ct := pairFiveUnmap d t
  have hcs := (pairFive_norm_membership m n hm hn s).mp hs
  have hct := (pairFive_norm_membership m n hm hn t).mp ht
  have hcst : cs ≠ ct := by
    intro h
    have h' := congrArg (pairFiveMap d) h
    exact hst (by simpa only [cs, ct, d,
      (pairFive_norm_inverse m n s).1, (pairFive_norm_inverse m n t).1] using h')
  have hp := pairFive_canonical_hamiltonPathOn
    (pairFive_canonical_endpoint (pairFiveKind m n) hkind cs ct hcs hct hcst)
  have h := hp.transport (pairFiveMap d) (pairFiveUnmap d)
    (fun a => (pairFive_norm_inverse m n a).2)
    (fun b => (pairFive_norm_inverse m n b).1)
    (fun b => pairFive_norm_membership m n hm hn b)
    (fun _ _ hab => pairFive_norm_map_adjacent m n hab)
  simpa only [cs, ct, d, (pairFive_norm_inverse m n s).1,
    (pairFive_norm_inverse m n t).1] using h

theorem pairFive_hamiltonPath_of_edge
    {m n : PairFiveMask} (hm : pairFiveSmall m) (hn : pairFiveSmall n)
    {s t : PairFiveState} (hs : s ∈ PairFiveStates m n)
    (ht : t ∈ PairFiveStates m n) (hst : PairFiveAdjacent s t) :
    HamiltonPathOn (PairFiveStates m n) PairFiveAdjacent s t := by
  let d := pairFiveNorm m n
  let cs := pairFiveUnmap d s
  let ct := pairFiveUnmap d t
  have hcs := (pairFive_norm_membership m n hm hn s).mp hs
  have hct := (pairFive_norm_membership m n hm hn t).mp ht
  have hcst : PairFiveAdjacent cs ct := pairFive_norm_unmap_adjacent m n hst
  have hp := pairFive_canonical_hamiltonPathOn
    (pairFive_canonical_edge_endpoint (pairFiveKind m n) cs ct hcs hct hcst)
  have h := hp.transport (pairFiveMap d) (pairFiveUnmap d)
    (fun a => (pairFive_norm_inverse m n a).2)
    (fun b => (pairFive_norm_inverse m n b).1)
    (fun b => pairFive_norm_membership m n hm hn b)
    (fun _ _ hab => pairFive_norm_map_adjacent m n hab)
  simpa only [cs, ct, d, (pairFive_norm_inverse m n s).1,
    (pairFive_norm_inverse m n t).1] using h

theorem pairFive_hamiltonCycle
    {m n : PairFiveMask} (hm : pairFiveSmall m) (hn : pairFiveSmall n)
    {s t : PairFiveState} (hs : s ∈ PairFiveStates m n)
    (ht : t ∈ PairFiveStates m n) (hst : PairFiveAdjacent s t) :
    HamiltonCycleOn (PairFiveStates m n) PairFiveAdjacent := by
  let d := pairFiveNorm m n
  let cs := pairFiveUnmap d s
  let ct := pairFiveUnmap d t
  have hcs := (pairFive_norm_membership m n hm hn s).mp hs
  have hct := (pairFive_norm_membership m n hm hn t).mp ht
  have hcst : PairFiveAdjacent cs ct := by
    exact pairFive_norm_unmap_adjacent m n hst
  have hc := pairFive_canonical_cycle (pairFiveKind m n) cs ct hcs hct hcst
  have h := (pairFive_canonical_cycle_hamiltonCycleOn hc).transport
    (pairFiveMap d) (pairFiveUnmap d)
    (fun a => (pairFive_norm_inverse m n a).2)
    (fun b => (pairFive_norm_inverse m n b).1)
    (fun b => pairFive_norm_membership m n hm hn b)
    (fun _ _ hab => pairFive_norm_map_adjacent m n hab)
  exact h

theorem pairFive_cycle_through
    {m n : PairFiveMask} (hm : pairFiveSmall m) (hn : pairFiveSmall n)
    {s t : PairFiveState} (hs : s ∈ PairFiveStates m n)
    (ht : t ∈ PairFiveStates m n) (hst : PairFiveAdjacent s t) :
    PairFiveCycleThrough m n s t := by
  let d := pairFiveNorm m n
  let cs := pairFiveUnmap d s
  let ct := pairFiveUnmap d t
  have hcs := (pairFive_norm_membership m n hm hn s).mp hs
  have hct := (pairFive_norm_membership m n hm hn t).mp ht
  have hcst : PairFiveAdjacent cs ct :=
    pairFive_norm_unmap_adjacent m n hst
  have hcanon := pairFive_canonical_cycle_through
    (pairFive_canonical_cycle (pairFiveKind m n) cs ct hcs hct hcst)
  rcases hcanon with ⟨path, hnpath, hcpath, hclosed, hedge⟩
  have hinj : Function.Injective (pairFiveMap d) := by
    intro a b hab
    have h' := congrArg (pairFiveUnmap d) hab
    simpa only [d, (pairFive_norm_inverse m n a).2,
      (pairFive_norm_inverse m n b).2] using h'
  refine ⟨path.map (pairFiveMap d), ?_, ?_, ?_, ?_⟩
  · exact transport_nodup hinj hnpath
  · intro q
    rw [pairFive_norm_membership m n hm hn q]
    change pairFiveUnmap d q ∈
        PairFiveStates (pairFiveCanonA (pairFiveKind m n))
          (pairFiveCanonB (pairFiveKind m n)) ↔
      q ∈ List.map (pairFiveMap d) path
    rw [List.mem_map]
    constructor
    · intro hq
      have hp := (hcpath (pairFiveUnmap d q)).mp hq
      exact ⟨pairFiveUnmap d q, hp,
        by simpa only [d, (pairFive_norm_inverse m n q).1]⟩
    · rintro ⟨a, ha, hqa⟩
      have hqa' : pairFiveUnmap d q = a := by
        have h' := congrArg (pairFiveUnmap d) hqa
        have haq : a = pairFiveUnmap d q := by
          simpa only [d, (pairFive_norm_inverse m n a).2] using h'
        exact haq.symm
      apply (hcpath (pairFiveUnmap d q)).mpr
      simpa only [hqa'] using ha
  · rcases hclosed with ⟨a, z, ha, hz, hw, hclose⟩
    refine ⟨pairFiveMap d a, pairFiveMap d z, ?_, ?_, ?_, ?_⟩
    · simpa only [List.head?_map, ha, Option.map_some]
    · simpa only [List.getLast?_map, hz, Option.map_some]
    · exact consecutive_map_vertices (pairFiveMap d)
        (fun _ _ h => pairFive_norm_map_adjacent m n h) hw
    · exact pairFive_norm_map_adjacent m n hclose
  · simpa only [cs, ct, d, (pairFive_norm_inverse m n s).1,
      (pairFive_norm_inverse m n t).1] using
      (pairFive_edgeIn_map (pairFiveMap d) hedge)

end PlanarRecoloring
