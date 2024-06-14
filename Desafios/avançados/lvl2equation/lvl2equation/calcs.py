import math
from typing import Union, List, Optional

def delta(a: Union[int, float], b: Union[int, float], c: Union[int, float]) -> Union[int, float]:
    """
    Recebe: coeficientes a, b e c de uma equação de segundo grau
    Retorna: valor de delta.
    """
    return b**2 - 4*a*c

def bhaskara(a: Union[int, float], b: Union[int, float], c: Union[int, float]) -> Optional[Union[List[float], float]]:
    """
    Recebe: coeficientes a, b e c de uma equação de segundo grau
    Retorna: os valores de x, ou None, se não houver raízes reais.
    """
    d = delta(a, b, c)
    if d > 0:
        x1 = (-b + math.sqrt(d)) / (2 * a)
        x2 = (-b - math.sqrt(d)) / (2 * a)
        return [x1, x2]
    elif d == 0:
        x = (-b + math.sqrt(d)) / (2 * a)
        return x
    else:
        print('Não possui raízes reais')
        return None
