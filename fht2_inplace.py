Image = list[list[int]]


def shift(l1: list[int], n: int) -> list[int]:
    return l1[n:] + l1[:n]


def vecsum(l1: list[int], l2: list[int]) -> list[int]:
    from operator import add

    return list(map(add, l1, l2))


def ProcessPair(I_T: Image, k_T: int, I_B: Image, k_B: int, t_T: int):
    shift_val_a = t_T
    shift_val_b = t_T + 1
    a = I_T[k_T]
    b = I_B[k_B]
    assert shift_val_a >= 0
    assert shift_val_b >= 0
    a_copy = a.copy()
    assert len(a) == len(b), (len(a), len(b))
    a[:] = vecsum(a, shift(b, shift_val_a % len(a)))
    b[:] = vecsum(a_copy, shift(b, shift_val_b % len(b)))


def ProcessLine(I_T: Image, k_T: int, I_B: Image, k_B: int, t_T: int):
    a = I_T[k_T]
    b = I_B[k_B]
    b[:] = vecsum(a, shift(b, t_T % len(a)))


def fht2i(w: int, h: int, I: Image) -> tuple[Image, tuple[int]]:
    if h > 1:
        h_T = h // 2
        h_B = h - h_T
        I_T = I[:h_T]
        I_B = I[h_T:h]
        I_T, K_T = fht2i(w, h_T, I_T)
        I_B, K_B = fht2i(w, h_B, I_B)
        K: list[int | None] = [None] * h
        if h % 2 == 0:
            for t in range(0, h - 1, 2):
                t_B = t_T = t // 2
                k_T = K_T[t_T]
                k_B = K_B[t_B]
                ProcessPair(I_T, k_T, I_B, k_B, t_T)
                K[t] = k_T
                K[t + 1] = h_T + k_B
        elif h % 4 == 1:  # 5, 9, 13, 17, 21, 25
            t_C = h // 2
            t_T = t_C // 2
            t_B = t_T
            k_T = K_T[t_T]
            k_B = K_B[t_B]
            ProcessLine(I_T, k_T, I_B, k_B, t_T)
            K[t_C] = h_T + k_B
            for t in range(0, t_C, 2):
                t_B = t_T = t // 2
                k_T = K_T[t_T]
                k_B = K_B[t_B]
                ProcessPair(I_T, k_T, I_B, k_B, t_T)
                K[t] = k_T
                K[t + 1] = h_T + k_B
            for t in range(t_C + 1, h - 1, 2):
                t_T = t // 2
                t_B = t_T + 1
                k_T = K_T[t_T]
                k_B = K_B[t_B]
                ProcessPair(I_T, k_T, I_B, k_B, t_T)
                K[t] = k_T
                K[t + 1] = h_T + k_B
        else:  # 3, 7, 11, 15, 19, 23
            t_C = h // 2
            t_T = t_C // 2
            t_B = t_T
            k_T = K_T[t_T]
            k_B = K_B[t_B]
            ProcessLine(I_T, k_T, I_B, k_B, t_T)
            K[t_C - 1] = h_T + k_B
            for t in range(0, t_C - 2, 2):
                t_B = t_T = t // 2
                k_T = K_T[t_T]
                k_B = K_B[t_B]
                ProcessPair(I_T, k_T, I_B, k_B, t_T)
                K[t] = k_T
                K[t + 1] = h_T + k_B
            for t in range(t_C, h - 1, 2):
                t_T = t // 2
                t_B = t_T + 1
                k_T = K_T[t_T]
                k_B = K_B[t_B]
                ProcessPair(I_T, k_T, I_B, k_B, t_T)
                K[t] = k_T
                K[t + 1] = h_T + k_B
        return I, K
    else:
        return I, (0,)
