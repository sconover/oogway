import math

def add(u, v):
    return [a + b for a, b in zip(u, v)]

def subtract(u, v):
    return [a - b for a, b in zip(u, v)]

def equal(u, v):
    return all([a == b for a, b in zip(u, v)])
