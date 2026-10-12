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

end PlanarRecoloring
