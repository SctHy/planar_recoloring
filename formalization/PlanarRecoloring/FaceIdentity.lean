import Std

namespace PlanarRecoloring

/-!
# Arithmetic core of the five-face identity

The article derives the identity from the face-length count, the degree-sum
count, and Euler's equation.  Planar embeddings and facial walks are not yet
objects of this Lean development, so this file isolates the exact integer
algebra that remains after those three structural equations have been supplied.
-/

theorem five_face_identity_arithmetic
    {p Q s D n e f : Int}
    (hface : 2 * e = 6 * f - p + Q)
    (hdegree : 2 * e = 3 * n - s + D)
    (heuler : n - e + f = 2) :
    p = 12 + Q + 2 * D - 2 * s := by
  omega

/-- The corresponding degree-at-most-three face count.  Here `p` and `q`
are the numbers of degree-one and degree-two vertices, and `L` is the sum
of `|F|-6` over faces of length at least seven.  The planar meaning of the
three equations remains an explicit structural input. -/
theorem subcubic_face_count_arithmetic
    {f5 L p q n e f : Int}
    (hface : 2 * e = 6 * f - f5 + L)
    (hdegree : 2 * e = 3 * n - 2 * p - q)
    (heuler : n - e + f = 2) :
    f5 = 12 - 4 * p - 2 * q + L := by
  omega

/-- With no degree-one or degree-two vertices, the same identity forces at
least twelve five-faces whenever the excess terms are nonnegative. -/
theorem five_face_count_at_least_twelve
    {p Q D : Int}
    (hidentity : p = 12 + Q + 2 * D)
    (hQ : 0 ≤ Q) (hD : 0 ≤ D) :
    12 ≤ p := by
  omega

end PlanarRecoloring
