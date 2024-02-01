import numpy as np
from functools import reduce
#Exercicio 4.1
impar = lambda x: x % 2 == 1

#Exercicio 4.2
positivo = lambda x: x > 0

#Exercicio 4.3
comparar_modulo = lambda x, y: abs(x) < abs(y)

#Exercicio 4.4
cart2pol = lambda x,y: (np.sqrt(x**2 + y**2), np.arctan2(y, x))

#Exercicio 4.5
ex5 = lambda f, g, h: lambda x, y, z: h(f(x,y),g(y,z))

#Exercicio 4.6
def quantificador_universal(lista, f):
    # if lista == []:
    #     return []
    # if f(lista[0]):
    #     return [lista[0], quantificador_universal(lista[1:], f)]
    # return quantificador_universal(lista[1:], f)

    ## OR return all(map(f, lista))
    return [e for e in lista if not f(e)] == []
    

#Exercicio 4.8
def subconjunto(lista1, lista2):
    ## OR return all(map(lambda x: x in lista2, lista1))
    return [a for a in lista1 if a not in lista2] == []
    ### OU return quantificador_universal(lista1, lambda x: x in lista2)


#Exercicio 4.9
def menor_ordem(lista, f):
    if lista == []:
        return None
    
    if len(lista) == 1:
        return lista[0]
    
    m = menor_ordem(lista[1:], f)

    return lista[0] if f(lista[0], m) else m

    ### OR return reduce(lambda x,y: x if f(x,y) else y, lista)


#Exercicio 4.10
def menor_e_resto_ordem(lista, f):
    if lista == []:
        return None, []
    if len(lista) == 1:
        return lista[0], []
    
    m, r = menor_e_resto_ordem(lista[1:], f)

    return (lista[0], [m] + r) if f(lista[0], m) else (m, [lista[0]] + r)
    

#Exercicio 5.2
def ordenar_seleccao(lista, ordem):
    pass

