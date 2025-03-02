
import numpy as np
from scipy.optimize import minimize

# Define the basis state |0>
ket_0 = np.array([1, 0])

# Hadamard matrix U
H = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]])
# Define the 2x2 unitary matrix using the given decomposition
def unitary_matrix(rho, xi, zeta, sigma):
    U1 = np.array([[np.cos(rho), -np.sin(rho)], [np.sin(rho), np.cos(rho)]])
    U2 = np.diag([np.exp(1j * xi), np.exp(1j * zeta)])
    U3 = np.array([[np.cos(sigma), np.sin(sigma)], [-np.sin(sigma), np.cos(sigma)]])
    return U1 @ U2 @ U3

# Given error matrices A and B (assumed fixed)
rho_A, xi_A, zeta_A, sigma_A = np.random.uniform(-2*np.pi, 2*np.pi, 4)
rho_B, xi_B, zeta_B, sigma_B = np.random.uniform(-2*np.pi, 2*np.pi, 4)

A = np.eye(2)
B = np.eye(2)

# Define the function to optimize (find A† and B†)
def objective(params):
    rho_Ad, xi_Ad, zeta_Ad, sigma_Ad, rho_Bd, xi_Bd, zeta_Bd, sigma_Bd = params
    
    # Construct A† and B† using the unitary decomposition
    A_dagger = unitary_matrix(rho_Ad, xi_Ad, zeta_Ad, sigma_Ad).conj().T
    B_dagger = unitary_matrix(rho_Bd, xi_Bd, zeta_Bd, sigma_Bd).conj().T
    
    # Compute the expectation value
    expr = np.abs(ket_0.conj().T @ H.conj().T @ B_dagger @ B @ H @ A_dagger @ A @ ket_0)
    
    # Since we use minimize, return the negative value for maximization
    return -np.abs(expr)
# Initial guess: Random values for A† and B† parameters
initial_guess = np.random.uniform(-2*np.pi, 2*np.pi, 8)

# Bounds for all 8 parameters
bounds = [(-2*np.pi, 2*np.pi)] * 8

# Optimization using Nelder-Mead
result = minimize(objective, initial_guess, method='Nelder-Mead', bounds=bounds)


# Extract optimized parameters for A† and B†
optimized_params = result.x
optimized_A_dagger_params = optimized_params[:4]
optimized_B_dagger_params = optimized_params[4:]

# Construct optimized A† and B†
A_dagger_opt = unitary_matrix(*optimized_A_dagger_params).conj().T
B_dagger_opt = unitary_matrix(*optimized_B_dagger_params).conj().T

# Compute sanity checks
identity_A = A @ A_dagger_opt  # Should be close to identity
identity_B = B @ B_dagger_opt  # Should be close to identity

#identity_A = A @ A.conj().T  # Should be close to identity
#identity_B = B @ B.conj().T  # Should be close to identity


print("Optimized A† parameters (rho_Ad, xi_Ad, zeta_Ad, sigma_Ad):", optimized_A_dagger_params)
print("Optimized B† parameters (rho_Bd, xi_Bd, zeta_Bd, sigma_Bd):", optimized_B_dagger_params)
print("Maximized function value:", -result.fun)

# Print sanity checks
print("\nSanity Check: A * A† should be close to identity:")
print(identity_A)

print("\nSanity Check: B * B† should be close to identity:")
print(identity_B)

# Check closeness to identity
print("\nDeviation from Identity (Frobenius norm):")
print("||A * A† - I|| =", np.linalg.norm(identity_A - np.eye(2)))
print("||B * B† - I|| =", np.linalg.norm(identity_B - np.eye(2)))

