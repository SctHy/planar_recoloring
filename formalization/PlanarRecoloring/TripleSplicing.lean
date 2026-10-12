import PlanarRecoloring.CycleSplicing

/-!
# Three-cycle splice interface

The bad-run proposition joins three centre-colour square strips.  This file
records the exact endpoint interface for that final operation: after cutting
one edge in each strip, three disjoint Hamilton paths can be concatenated
around a 3-cycle of cross edges.  The theorem is independent of the concrete
Appendix certificates and can be instantiated by any three explicit strip
families.
-/

namespace PlanarRecoloring

set_option maxHeartbeats 0
set_option maxRecDepth 100000

theorem HamiltonPathOn.splice_three
    {α : Type u} {r : α → α → Prop}
    {v₀ v₁ v₂ : List α}
    {a₀ b₀ a₁ b₁ a₂ b₂ : α}
    (h₀ : HamiltonPathOn v₀ r a₀ b₀)
    (h₁ : HamiltonPathOn v₁ r a₁ b₁)
    (h₂ : HamiltonPathOn v₂ r a₂ b₂)
    (hdis₀₁ : ∀ ⦃x⦄, x ∈ v₀ → x ∉ v₁)
    (hdis₀₂ : ∀ ⦃x⦄, x ∈ v₀ → x ∉ v₂)
    (hdis₁₂ : ∀ ⦃x⦄, x ∈ v₁ → x ∉ v₂)
    (h₀₁ : r b₀ a₁) (h₁₂ : r b₁ a₂) (h₂₀ : r b₂ a₀) :
    HamiltonCycleOn (v₀ ++ v₁ ++ v₂) r := by
  rcases h₀ with ⟨p₀, hp₀, hq₀, hn₀, hc₀, hw₀⟩
  rcases h₁ with ⟨p₁, hp₁, hq₁, hn₁, hc₁, hw₁⟩
  rcases h₂ with ⟨p₂, hp₂, hq₂, hn₂, hc₂, hw₂⟩
  have hp₀ne : p₀ ≠ [] := by intro h; subst p₀; simp at hp₀
  have hp₁ne : p₁ ≠ [] := by intro h; subst p₁; simp at hp₁
  have hp₂ne : p₂ ≠ [] := by intro h; subst p₂; simp at hp₂
  have hdis₀₁' : ∀ ⦃x⦄, x ∈ p₀ → x ∉ p₁ := by
    intro x hx₀ hx₁
    exact hdis₀₁ ((hc₀ x).mpr hx₀) ((hc₁ x).mpr hx₁)
  have hdis₀₂' : ∀ ⦃x⦄, x ∈ p₀ → x ∉ p₂ := by
    intro x hx₀ hx₂
    exact hdis₀₂ ((hc₀ x).mpr hx₀) ((hc₂ x).mpr hx₂)
  have hdis₁₂' : ∀ ⦃x⦄, x ∈ p₁ → x ∉ p₂ := by
    intro x hx₁ hx₂
    exact hdis₁₂ ((hc₁ x).mpr hx₁) ((hc₂ x).mpr hx₂)
  have hnodup₀₁ : (p₀ ++ p₁).Nodup := by
    apply List.nodup_append.mpr
    refine ⟨hn₀, hn₁, ?_⟩
    intro x hx₀ y hy₁ hxy
    exact hdis₀₁' hx₀ (hxy ▸ hy₁)
  have hnodup : ((p₀ ++ p₁) ++ p₂).Nodup := by
    apply List.nodup_append.mpr
    refine ⟨hnodup₀₁, hn₂, ?_⟩
    intro x hx₀₁ y hy₂ hxy
    rcases List.mem_append.mp hx₀₁ with hx₀ | hx₁
    · exact hdis₀₂' hx₀ (hxy ▸ hy₂)
    · exact hdis₁₂' hx₁ (hxy ▸ hy₂)
  have hcon₀₁ : Consecutive r (p₀ ++ p₁) := by
    exact consecutive_append hw₀ hw₁ hp₀ne hp₁ne hq₀ hp₁ h₀₁
  have hcon : Consecutive r ((p₀ ++ p₁) ++ p₂) := by
    have hlast₀₁ : (p₀ ++ p₁).getLast? = some b₁ := by
      rw [getLast_append_of_ne_nil hp₁ne]
      exact hq₁
    exact consecutive_append hcon₀₁ hw₂
      (by simp [hp₀ne]) hp₂ne hlast₀₁ hp₂ h₁₂
  have hhead : ((p₀ ++ p₁) ++ p₂).head? = some a₀ := by
    rw [head_append_of_ne_nil (by simp [hp₀ne, hp₁ne])]
    rw [head_append_of_ne_nil hp₀ne, hp₀]
  have hlast : ((p₀ ++ p₁) ++ p₂).getLast? = some b₂ := by
    rw [getLast_append_of_ne_nil hp₂ne, hq₂]
  refine ⟨(p₀ ++ p₁) ++ p₂, hnodup, ?_, ?_⟩
  · intro x
    simp only [List.mem_append]
    constructor
    · intro hx
      rcases hx with hx | hx
      · rcases hx with hx | hx
        · exact Or.inl (Or.inl ((hc₀ x).mp hx))
        · exact Or.inl (Or.inr ((hc₁ x).mp hx))
      · exact Or.inr ((hc₂ x).mp hx)
    · intro hx
      rcases hx with hx | hx
      · rcases hx with hx | hx
        · exact Or.inl (Or.inl ((hc₀ x).mpr hx))
        · exact Or.inl (Or.inr ((hc₁ x).mpr hx))
      · exact Or.inr ((hc₂ x).mpr hx)
  · exact ⟨a₀, b₂, hhead, hlast, hcon, h₂₀⟩

end PlanarRecoloring
