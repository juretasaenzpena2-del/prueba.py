'''
Enunciado:
Crea una función llamada "count_vowels(text_chain)" que reciba como parámetro
una cadena de texto de tipo string llamada 'text_chain' y retorne el número
de vocales, ya sean mayúsculas o minúsculas, sin tilde que se encuentren en dicha 
cadena de texto.

Parámetros:
- text_chain: Este parámetro admite únicamente strings.

Ejemplo: 
    Entrada:
    count_vowels('Hello world, this is an example.')

    Salida:
    9

Enunciat:
Crea una funció anomenada "count_vowels(text_chain)" que rebi com a paràmetre
una cadena de text de tipus string anomenada 'text_chain' i retorni el número
de vocals, ja siguin majúscules o minúscules, sense accent, que es trobin en 
aquesta cadena de text.

Paràmetres:
- text_chain: Aquest paràmetre només admet strings.

Exemple:
     Entrada:
     count_vowels('Hello world, this is an example.')

     Sortida:
     9

'''

def count_vowels(text_chain):
    # Validar que el parametro sea un string
    if not isinstance(text_chain ,str):
        raise ValueError("El parametro debe ser una cadena de texto (string).")
    vowels= "aeiouAEIOU"
    count = 0 

    for char in text_chain:
        if char in vowels:
            count += 1
    
    return count
