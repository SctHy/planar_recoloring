import PlanarRecoloring.BinaryHamilton

/-!
# Prescribed endpoints in binary products

The reflected Gray enumeration is used only to name the vertex set.  The
construction below proves Hamilton paths for arbitrary opposite-parity words,
by joining the two first-coordinate layers or inserting one layer into the
first edge of a path in the other layer.
-/

namespace PlanarRecoloring

theorem HamiltonPathOn.congr_vertices {α : Type u} {r : α → α → Prop}
    {v w : List α} {s t : α}
    (h : HamiltonPathOn v r s t) (hvw : ∀ x, x ∈ v ↔ x ∈ w) :
    HamiltonPathOn w r s t := by
  rcases h with ⟨p, hp, hq, hn, hc, hw⟩
  exact ⟨p, hp, hq, hn, fun x => (hvw x).symm.trans (hc x), hw⟩

theorem HamiltonPathOn.appendOn {α : Type u} {r : α → α → Prop}
    {v w : List α} {s a b t : α}
    (h₁ : HamiltonPathOn v r s a) (h₂ : HamiltonPathOn w r b t)
    (hdis : DisjointLists v w) (hab : r a b) :
    HamiltonPathOn (v ++ w) r s t := by
  rcases h₁ with ⟨p, hp, hq, hn, hc, hw⟩
  rcases h₂ with ⟨q, qp, qq, qn, qc, qw⟩
  have hpn : p ≠ [] := by intro h; subst p; simp at hp
  have hqn : q ≠ [] := by intro h; subst q; simp at qp
  have hdis' : DisjointLists p q := by
    intro z hz1 hz2
    exact hdis ((hc z).mpr hz1) ((qc z).mpr hz2)
  refine ⟨p ++ q, ?_, ?_, nodup_append_of_disjoint hn qn hdis', ?_,
    consecutive_append hw qw hpn hqn hq qp hab⟩
  · rw [head_append_of_ne_nil hpn, hp]
  · rw [getLast_append_of_ne_nil hqn, qq]
  · intro z
    simp only [List.mem_append]
    rw [hc z, qc z]

/-- Insert a disjoint Hamilton path in place of the first edge of a supplied
path.  Both joining edges are explicit; the deleted first edge is not reused. -/
theorem HamiltonPathOn.insertAtFirstEdge {α : Type u} {r : α → α → Prop}
    {v w : List α} {x y a b t : α} {tail : List α}
    (hn : (x :: y :: tail).Nodup)
    (hc : CoversList v (x :: y :: tail))
    (hlast : (x :: y :: tail).getLast? = some t)
    (hwalk : Consecutive r (x :: y :: tail))
    (hq : HamiltonPathOn w r a b)
    (hdis : DisjointLists v w) (hxa : r x a) (hby : r b y) :
    HamiltonPathOn (v ++ w) r x t := by
  rcases hq with ⟨q, qp, qq, qn, qc, qw⟩
  have hqn : q ≠ [] := by intro h; subst q; simp at qp
  have hxtail : x ∉ y :: tail := (List.nodup_cons.mp hn).1
  have htail : (y :: tail).Nodup := (List.nodup_cons.mp hn).2
  have hxq : x ∉ q := by
    intro hx
    exact hdis ((hc x).mpr (by simp)) ((qc x).mpr hx)
  have hdisq : DisjointLists q (y :: tail) := by
    intro z hz ht
    exact hdis ((hc z).mpr (by simp [ht])) ((qc z).mpr hz)
  have hqtail : (q ++ y :: tail).Nodup :=
    nodup_append_of_disjoint qn htail hdisq
  have hn' : (x :: q ++ y :: tail).Nodup := by
    apply List.nodup_cons.mpr
    exact ⟨by simpa using And.intro hxq hxtail, hqtail⟩
  have hwalk' : Consecutive r (x :: q ++ y :: tail) := by
    have hq' : Consecutive r (q ++ y :: tail) :=
      consecutive_append qw hwalk.2 hqn (by simp) qq rfl hby
    cases q with
    | nil => simp at qp
    | cons z zs =>
      have hz : z = a := by simpa using qp
      subst z
      exact ⟨hxa, hq'⟩
  refine ⟨x :: q ++ y :: tail, rfl, ?_, hn', ?_, hwalk'⟩
  · have ht : (y :: tail).getLast? = some t := by simpa using hlast
    simpa using (getLast_append_of_ne_nil (xs := x :: q)
      (ys := y :: tail) (by simp)).trans ht
  · intro z
    simp only [List.mem_append, List.mem_cons]
    change (z ∈ v ∨ z ∈ w) ↔ ((z = x ∨ z ∈ q) ∨ z = y ∨ z ∈ tail)
    rw [hc z, qc z]
    simp only [List.mem_cons]
    simp [or_assoc, or_left_comm, or_comm]

private theorem binary_layer_disjoint (b : Bool) (n : Nat) :
    DisjointLists ((grayWords n).map (fun x => b :: x))
      ((grayWords n).map (fun x => (!b) :: x)) := by
  intro x hx hy
  rcases List.mem_map.mp hx with ⟨u, hu, rfl⟩
  rcases List.mem_map.mp hy with ⟨v, hv, h⟩
  have hb := (List.cons.inj h).1
  cases b <;> simp at hb

private theorem binary_layer_cover (b : Bool) (n : Nat) (x : List Bool) :
    x ∈ (grayWords n).map (fun u => b :: u) ++
      (grayWords n).map (fun u => (!b) :: u) ↔ x ∈ grayWords (n + 1) := by
  rw [grayWords_mem_iff]
  simp only [List.mem_append, List.mem_map]
  constructor
  · rintro (⟨u, hu, rfl⟩ | ⟨u, hu, rfl⟩) <;>
      simp [grayWords_mem_iff.mp hu]
  · intro hx
    cases x with
    | nil => simp at hx
    | cons a u =>
      have hu : u ∈ grayWords n := grayWords_mem_iff.mpr (by simpa using hx)
      cases b <;> cases a <;> simp [hu]

private theorem binary_layer_map {b : Bool} {n : Nat} {x y : List Bool}
    (h : HamiltonPathOn (grayWords n) ProductAdj x y) :
    HamiltonPathOn ((grayWords n).map (fun u => b :: u)) ProductAdj
      (b :: x) (b :: y) := by
  exact h.map (fun u => b :: u)
    (fun _ _ h => (List.cons.inj h).2)
    (fun {u v} h => productAdj_cons_map_gray h)

private theorem binary_adj_head (b : Bool) (x : List Bool) :
    ProductAdj (b :: x) ((!b) :: x) :=
  ⟨[], x, b, rfl, rfl⟩

private theorem binary_opposite_witness {n : Nat} (hn : 0 < n)
    {x : List Bool} (hx : x.length = n) :
    ∃ z, z.length = n ∧ cubeParity x = !cubeParity z := by
  cases x with
  | nil => simp at hx; omega
  | cons a tail =>
    refine ⟨(!a) :: tail, by simpa using hx, ?_⟩
    exact productAdj_parity (⟨[], tail, a, rfl, rfl⟩ :
      ProductAdj (a :: tail) ((!a) :: tail))

/-- Every two opposite-parity vertices of a nonzero binary product have a
Hamilton path, with their actual coordinate words as its endpoints. -/
theorem binary_hamiltonPathOn {n : Nat} (hn : 0 < n)
    {x y : List Bool} (hx : x.length = n) (hy : y.length = n)
    (hpar : cubeParity x = !cubeParity y) :
    HamiltonPathOn (grayWords n) ProductAdj x y := by
  induction n generalizing x y with
  | zero => omega
  | succ n ih =>
    cases x with
    | nil => simp at hx
    | cons a xs =>
      cases y with
      | nil => simp at hy
      | cons b ys =>
        have hxs : xs.length = n := by simpa using hx
        have hys : ys.length = n := by simpa using hy
        by_cases hn0 : n = 0
        · have hxs0 : xs = [] :=
            List.length_eq_zero_iff.mp (hn0 ▸ hxs)
          have hys0 : ys = [] :=
            List.length_eq_zero_iff.mp (hn0 ▸ hys)
          subst n
          subst xs
          subst ys
          cases a <;> cases b <;> simp [cubeParity] at hpar
          · exact ⟨[[false], [true]], rfl, rfl, by decide,
              by intro z; simp [grayWords], ⟨binary_adj_head false [], trivial⟩⟩
          · exact ⟨[[true], [false]], rfl, rfl, by decide,
              by intro z; simp [grayWords, or_comm],
              ⟨binary_adj_head true [], trivial⟩⟩
        have hn' : 0 < n := by omega
        by_cases hab : a = b
        · subst b
          have htailpar : cubeParity xs = !cubeParity ys := by
            cases a <;> simpa [cubeParity] using hpar
          rcases ih hn' hxs hys htailpar with ⟨p, hp, hq, pn, pc, pw⟩
          cases p with
          | nil => simp at hp
          | cons z p =>
            have hz : z = xs := by simpa using hp
            subst z
            cases p with
            | nil =>
              have hysx : ys = xs := by simpa using hq.symm
              subst ys
              cases cubeParity xs <;> simp at htailpar
            | cons z tail =>
              have hzmem : z ∈ grayWords n := (pc z).mpr (by simp)
              have hzlen : z.length = n := grayWords_mem_iff.mp hzmem
              have hzpar : cubeParity xs = !cubeParity z := productAdj_parity pw.1
              have hother := binary_layer_map (b := !a) (ih hn' hxs hzlen hzpar)
              have mappedN : ((xs :: z :: tail).map (fun u => a :: u)).Nodup :=
                nodup_map_cons_bool a pn
              have mappedCover : CoversList
                  ((grayWords n).map (fun u => a :: u))
                  ((xs :: z :: tail).map (fun u => a :: u)) := by
                intro u
                simp only [List.mem_map]
                constructor
                · rintro ⟨v, hv, rfl⟩
                  exact ⟨v, (pc v).mp hv, rfl⟩
                · rintro ⟨v, hv, rfl⟩
                  exact ⟨v, (pc v).mpr hv, rfl⟩
              have mappedLast :
                  ((xs :: z :: tail).map (fun u => a :: u)).getLast? =
                    some (a :: ys) := by rw [List.getLast?_map, hq]; rfl
              have mappedWalk := consecutive_map_gray (h := a) pw
              have hinsert := HamiltonPathOn.insertAtFirstEdge
                mappedN mappedCover mappedLast mappedWalk hother
                (binary_layer_disjoint a n) (binary_adj_head a xs)
                (productAdj_symm (binary_adj_head a z))
              exact hinsert.congr_vertices (binary_layer_cover a n)
        · have hb : b = !a := by cases a <;> cases b <;> simp_all
          subst b
          have hsame : cubeParity xs = cubeParity ys := by
            cases a <;> simpa [cubeParity] using hpar
          rcases binary_opposite_witness hn' hxs with ⟨z, hz, hxz⟩
          have hzy : cubeParity z = !cubeParity ys := by
            calc
              cubeParity z = !cubeParity xs := by
                simpa using (congrArg (fun c : Bool => !c) hxz).symm
              _ = !cubeParity ys := by rw [hsame]
          have hleft := binary_layer_map (b := a) (ih hn' hxs hz hxz)
          have hright := binary_layer_map (b := !a) (ih hn' hz hys hzy)
          exact (hleft.appendOn hright (binary_layer_disjoint a n)
            (binary_adj_head a z)).congr_vertices (binary_layer_cover a n)

end PlanarRecoloring
