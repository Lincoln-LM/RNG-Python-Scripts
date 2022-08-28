"""
Functions that aid in recovering the state of PRNGs
"""
import numpy as np

def mat_inverse(mat):
    """Compute the inverse of a matrix via gauss jordan elimination"""
    height, width = mat.shape

    res = np.identity(height, np.uint8)
    pivot = 0
    for i in range(width):
        isfound = False
        for j in range(i, height):
            if mat[j, i]:
                if isfound:
                    mat[j] ^= mat[pivot]
                    res[j] ^= res[pivot]
                else:
                    isfound = True
                    mat[[j, pivot]] = mat[[pivot, j]]
                    res[[j, pivot]] = res[[pivot, j]]
        if isfound:
            pivot += 1

    for i in range(width):
        assert mat[i, i]

    for i in range(1, width)[::-1]:
        for j in range(i)[::-1]:
            if mat[j, i]:
                mat[j] ^= mat[i]
                res[j] ^= res[i]
    return res[:width]
