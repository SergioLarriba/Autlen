"""
Esta es la expresion regular para el ejercicio 0, que se facilita
a modo de ejemplo:
"""
RE0 = "[ab]*a" # (a+b)*a 



"""
Completa a continuacion las expresiones regulares para los
ejercicios 1-6:
"""

#NO BA -> PARECIDO AL EJERICIO 10 DE CLASE QUE PEDIA NO CONTENER 110  --> (0 + 10)∗1∗
#true -> a ab aab
#false -> ba aba
RE1 = "a*b*" # a*b* 


''' Diseña una expresión regular para el lenguaje sobre el alfabeto {a,b} que no contiene
2 símbolos idénticos y consecutivos, es decir, el símbolo en la posición i debe ser
diferente al símbolo en la posición i+1. Asigna la expresión regular a la variable RE2.
Nota: Se debe rechazar la cadena vacía 

Ejemplo de cadenas válidas: a, ab, aba
Ejemplo de cadenas inválidas: aa, bb, aaa
'''


RE2 = "(ab)*a|(ba)*b|a|b|(ab(ab)*)|(ba(ba)*)" # (ab)*a + (ba)*b + a + b + (ab)* + (ba)*



#L = {w ∈ {a,b}*: las subcadenas aa y bb son parte de w}
#Ejemplo de cadenas validas: aabb, abbaa  -> supongo q abbaa es una errata y es aabbaa
#Ejemplo de cadenas invalidas: ababaa, abbabb
# 
RE3 = "(aa[a+b]*bb)|(bb[a+b]*aa)|([a+b]*aabb)|([a+b]*bbaa)|(aabb[a+b]*)|(bbaa[a+b]*)|([a+b]*aabb[a+b]*)|([a+b]*bbaa[a+b]*)" # (aa?bb) + (bb?aa) + (?aabb) + (aabb?) + (?aabb?)   
         

#Diseña una expresión regular que acepte las cadenas no vacías que representan los
#números enteros del 0 al 255. La expresión regular debe rechazar las cadenas con
#las siguientes características:
#• Ceros innecesarios a la izquierda.
#• Símbolos que no están en el alfabeto.
#Ejemplo de cadenas validas: 0, 10, 255, 2, 20.
#Ejemplo de cadenas invalidas: -1, +1, 3.33, 007, 256.
RE4 = "[0-9]|([1-9][0-9])|(1[0-9][0-9])|(2[0-5][0-5])" 


''' Diseña una expresión regular para el siguiente lenguaje:
L = {w ∈ {a,b}*: w no contiene más de dos apariciones de la subcadena aa}
Ejemplo de cadenas validas: a, aa, abaa, abaab, abbaa
Ejemplo de cadenas invalidas: aabaaaa, bbaabaabaa '''
#COMO MUCHO 1 UNO -> 0*|0*10*
# b*|b|aab*
RE5 = "b*|ba|ab|aab*aab*|b*aab*aa|ab*aa|aab*|a|ab*aab*aab*|(b*aab*aab*)|b*aab*ab*aa" #  b* + ba + ab +  aab*aab* + b*aab*aa

# b* + aab* + b*aa + aab*aa +ab*a + ab* + b*a + b*a(ba)*b(ba|ab)*b*

''' Diseña una expresión regular para el siguiente lenguaje:
L = {w ∈ {1,0}*: w tiene como máximo un par de ceros consecutivos y como máximo
un par de unos consecutivos}
Ejemplo de cadenas validas: 0, 1, 00, 001, 0011, 00110,001010...,
Ejemplo de cadenas invalidas: 0000, 1111, 001100 '''

RE6 = "|0|1|01|10|(00(10)*11(01)*)|11|(0(10)*11(01)*)" 

#BASICOS --> 01 | 10 + 0 + 1 +
# 01(10)*1(01)*
# 0 + 1 + 00 + 11 + 01 + 10 + 000 + 001 + 010 + 011 + 100 +
#(00 + 0)[(10)*](1|11)[]
# 0011,

