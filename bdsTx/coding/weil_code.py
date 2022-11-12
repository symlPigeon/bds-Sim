'''
Author: symlpigeon
Date: 2022-11-07 23:16:00
LastEditTime: 2022-11-08 15:22:50
LastEditors: symlpigeon
Description: 生成Weil码
FilePath: /sim_bds/python/coding/weil_code.py
'''

DATA_WEIL_CODE_LENGTH = 10243


def get_legendre_seq_k(k: int, n: int) -> int:
    """ 生成n对应的Legendre序列上的L(k)
        L(k) = 1, if k!=0 and exists x s.t. x^2 = k (mod n)
             = 0, else
    Args:
        k (int)
        n 

    Returns:
        st: k对应的L(k)
    """
    if pow(k, (n - 1) // 2, n) == 1:  # Legendre symbol is 1
        return 1
    return 0


def get_legendre_seq(n: int) -> bytes:
    """生成Legendre序列

    Args:
        n (int): 序列长度.

    Returns:
        bytes: Legendre序列
    """
    return bytes(get_legendre_seq_k(k, n) for k in range(n))


class legendre_seq():
    _seq = {}

    @classmethod
    def get(cls, length: int) -> bytes:
        if length in cls._seq:
            return cls._seq[length]
        else:
            cls._seq[length] = get_legendre_seq(length)
            return cls._seq[length]


def get_weil_code(legend_seq: bytes, w: int, sequence_length: int) -> bytes:
    """生成weil码，W(k;w)=L(k) xor L((k+w) mod N)

    Args:
        legend_seq (bytes): Legendre序列
        w(int): Legendre序列的相位差
        sequence_length(int): 序列的长度
    Returns:
        bytes: 
    """
    return bytes(legend_seq[k] ^ legend_seq[(k + w) % sequence_length]
                 for k in range(sequence_length))
