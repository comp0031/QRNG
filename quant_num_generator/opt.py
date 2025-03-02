import numpy as np
from scipy.optimize import minimize

def matrix_from_params(params):
    """
    Converts an 8-element array of real numbers into a 2x2 complex matrix.
    We define:
      M = [ [p0 + i*p1, p2 + i*p3],
            [p4 + i*p5, p6 + i*p7] ]
    """
    return np.array([
        [params[0] + 1j*params[1], params[2] + 1j*params[3]],
        [params[4] + 1j*params[5], params[6] + 1j*params[7]]
    ])

def objective(x, U, ket0):
    """
    x: A length-16 vector, where:
       - x[0:8] parameterize A,
       - x[8:16] parameterize B.
    U: A given unitary (gate).
    ket0: The |0> state.
    
    Returns the negative absolute value of
      <0| U^\dagger (B^\dagger B) U (A^\dagger A) |0>
    so that minimizing this function maximizes our target.
    """
    A = matrix_from_params(x[:8])
    B = matrix_from_params(x[8:])
    
    # Compute A^\dagger A and B^\dagger B (which are positive semi-definite)
    A_daggerA = np.dot(A.conj().T, A)
    B_daggerB = np.dot(B.conj().T, B)
    
    # Compute the inner product <0| U^\dagger B^\daggerB U A^\daggerA |0>
    expr = np.vdot(ket0, np.dot(np.dot(U.conj().T, np.dot(B_daggerB, U)), np.dot(A_daggerA, ket0)))
    
    # Return the negative absolute value (since we maximize by minimizing its negative)
    return -np.abs(expr)

def sanity_checks(x, U, ket0):
    """
    Performs a series of sanity checks to verify that:
      - U is unitary.
      - ket0 is normalized.
      - Matrices A^\dagger A and B^\dagger B are Hermitian and positive semi-definite.
      - A A^\dagger and B B^\dagger are (approximately) the identity matrix.
    """
    tol = 1e-6

    # Check that U is unitary: U U^\dagger = I
    if not np.allclose(np.dot(U, U.conj().T), np.eye(U.shape[0]), atol=tol):
        raise ValueError("Gate U is not unitary.")
    else:
        print("Sanity check passed: U is unitary.")

    # Check that ket0 is normalized
    norm_ket0 = np.linalg.norm(ket0)
    if not np.allclose(norm_ket0, 1.0, atol=tol):
        raise ValueError("|0> state is not normalized. Norm = {:.6f}".format(norm_ket0))
    else:
        print("Sanity check passed: |0> is normalized.")

    # Build A and B from x
    A = matrix_from_params(x[:8])
    B = matrix_from_params(x[8:])
    
    # Check A^\dagger A and B^\dagger B for Hermiticity
    A_daggerA = np.dot(A.conj().T, A)
    B_daggerB = np.dot(B.conj().T, B)

    if not np.allclose(A_daggerA, A_daggerA.conj().T, atol=tol):
        raise ValueError("A^\dagger A is not Hermitian.")
    if not np.allclose(B_daggerB, B_daggerB.conj().T, atol=tol):
        raise ValueError("B^\dagger B is not Hermitian.")
    else:
        print("Sanity check passed: A^\dagger A and B^\dagger B are Hermitian.")

    # Check positive semi-definiteness by ensuring eigenvalues are >= -tol
    eigs_A = np.linalg.eigvalsh(A_daggerA)
    eigs_B = np.linalg.eigvalsh(B_daggerB)
    if np.any(eigs_A < -tol):
        raise ValueError("A^\dagger A is not positive semi-definite. Eigenvalues: {}".format(eigs_A))
    if np.any(eigs_B < -tol):
        raise ValueError("B^\dagger B is not positive semi-definite. Eigenvalues: {}".format(eigs_B))
    else:
        print("Sanity check passed: A^\dagger A and B^\dagger B are positive semi-definite.")

    # Additional check: Verify if A A^\dagger ~ I and B B^\dagger ~ I
    AA_dagger = np.dot(A, A.conj().T)
    BB_dagger = np.dot(B, B.conj().T)
    if not np.allclose(AA_dagger, np.eye(A.shape[0]), atol=tol):
        print("Warning: A A^\dagger is not the identity.\nComputed A A^\dagger:\n", AA_dagger)
    else:
        print("Sanity check passed: A A^\dagger is the identity.")
        
    if not np.allclose(BB_dagger, np.eye(B.shape[0]), atol=tol):
        print("Warning: B B^\dagger is not the identity.\nComputed B B^\dagger:\n", BB_dagger)
    else:
        print("Sanity check passed: B B^\dagger is the identity.")

    # Optionally, check the objective function value for the given x
    obj_val = -objective(x, U, ket0)
    print("Objective (absolute value): {:.6f}".format(obj_val))

# Define your gate U.
# For example, you might start with the identity:
U = np.array([[1, 0],
              [0, 1]], dtype=complex)
# Alternatively, for a Hadamard gate:
# U = 1/np.sqrt(2) * np.array([[1, 1],
#                              [1, -1]], dtype=complex)

# Define the |0> state.
ket0 = np.array([1, 0], dtype=complex)

# Choose an initial guess for the 16 parameters.
x0 = np.random.randn(16)

# Run sanity checks on the initial parameters and setup.
print("Running sanity checks on initial guess:")
sanity_checks(x0, U, ket0)

# Use an optimization routine; here we use Nelder-Mead.
result = minimize(objective, x0, args=(U, ket0), method='Nelder-Mead', options={'maxiter': 10000})

# Display the results.
print("\nOptimization completed.")
print("Optimal parameters:", result.x)
print("Maximum value of the expression:", -result.fun)

# Run sanity checks on the optimized parameters.
print("\nRunning sanity checks on optimized parameters:")
sanity_checks(result.x, U, ket0)
