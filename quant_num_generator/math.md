# Quantum Error correction math

## Types of Errors
1. Qubit Generation Error.
    - i.e try to generate $|0\rangle$ actually generate $A|0\rangle$,
        - where $\mathbf{A}$ is a unitary representing some error
        - note that on q.computer asking for qubit $|0\rangle$, actually get us $A|0\rangle$
        - known
2. Gate Error
    - i.e try to apply $\mathbf{U}|\phi\rangle$ but apply $\mathbf{B}\mathbf{U}|\phi\rangle$
        - where $\mathbf{U}$ is a unitary repr gate we wish to apply and $\mathbf{B}$ is error matrix
        - similar to above q.computer $U$ is actually $BU$
        - known
3. Measurement error
    - can't do sht

## How to fix

1. instead of $A|0\rangle$ do $A^\dagger A|0\rangle$ 

2. instead of  $\mathbf{B}\mathbf{U}|\phi\rangle$ do $\mathbf{B}^\dagger \mathbf{B}\mathbf{U}|\phi\rangle$

## Put it together

Ideal circuit:
    
$|0\rangle$ --- $U$---|measurement| ${[1]}$

Actual circuit:

$|0\rangle$ --- $A$ --- $A^\dagger$ --- $U$ --- $B$ ---$B^\dagger$ --- |measurement| $[2]$

Circuit we give to q. computer

$|0\rangle$ --- $A^\dagger$ --- $U$---$B^\dagger$ --- |measurement|

## Maths:

Ideally want $[1] = [2]$.

Formally want : $argmax_{A,B}|\langle0|U^\dagger B^\dagger B U A^\dagger A |0\rangle|^2$

Equivalently  $argmax_{A,B}|\langle0|U^\dagger B^\dagger B U A^\dagger A |0\rangle|$

Every $2\times2$ unitary can be repr. by $R_{V_1}R_UR_{V_2}$

${\displaystyle U={\begin{bmatrix}\cos \rho &-\sin \rho \\\sin \rho &\;\cos \rho \\\end{bmatrix}}{\begin{bmatrix}e^{i\xi }&0\\0&e^{i\zeta }\end{bmatrix}}{\begin{bmatrix}\;\cos \sigma &\sin \sigma \\-\sin \sigma &\cos \sigma \\\end{bmatrix}}~.}$


Try and optimize using [Nelder-Mead](https://en.m.wikipedia.org/wiki/Nelder%E2%80%93Mead_method)
-----------------------------------------------------------------------------------------------------

- start range $\rho,\xi,\zeta,\sigma \in [-2\pi,2\pi]$
