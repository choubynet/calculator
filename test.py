#!/usr/bin/env python3

from tkinter import *
from decimal import *

# genération de la fenêtre
window = Tk()

# variable globale contenant la ligne des calculs affichés
calc_ongoing = ""

# variable globale contenant la ligne des résultats affichés
result_ongoing = "0"

# variable globale contenant la dernière opération importante
last_operation = ""

# gestion de la saisie d'un chiffre
def input_number(value):
    global last_operation
    global result_ongoing

    # réinitialisation si on rentre un chiffre directement après un "="
    if last_operation == "=":
        reset()
    
    # réinitialisation du nombre saisi si la dernière touche saisie était une opération
    elif last_operation != "":
        result_ongoing = ""

    if result_ongoing == "0":
        result_ongoing = ""

    last_operation = ""
    result_ongoing = result_ongoing + value

    # affichage du nouveau nombre
    result_text.set(result_ongoing)

# gestion de la saisie d'une opération
def input_operation(value):
    global calc_ongoing
    global result_ongoing
    global last_operation

    # gestion si l'utilisateur saisit une opération juste après une autre opération
    if last_operation != "" and last_operation != "=":
        last_operation = value
        calc_ongoing = calc_ongoing[:-1] + value
        calc_input_text.set(calc_ongoing)
        return

    # gestion si un "=" a été saisi juste avant
    if last_operation == "=":
        last_operation = value
        calc_ongoing = result_ongoing + value
        calc_input_text.set(calc_ongoing)
        return

    last_operation = value

    # affichage du nouveau résultat
    calc_ongoing = calc_ongoing + result_ongoing
    result_ongoing = calcul(calc_ongoing)
    result_text.set(result_ongoing)

    # affichage du nouveau calcul en cours
    calc_ongoing = calc_ongoing + value
    calc_input_text.set(calc_ongoing)

# gestion de la saisie du "="
def equal():
    global calc_ongoing
    global result_ongoing    
    global last_operation

    # gestion si la dernière opération saisie était "="
    if last_operation == "=":
        return

    last_operation = "="

    # affichage du nouveau résultat
    calc_ongoing = calc_ongoing + result_ongoing
    result_ongoing = calcul(calc_ongoing)
    result_text.set(result_ongoing)

    # affichage du nouveau calcul en cours
    calc_ongoing = calc_ongoing + "="
    calc_input_text.set(calc_ongoing)

# renvoie le résultat du calcul en cours
def calcul(calc):

    # transforme les soustractions en additions et les divisions en multiplications
    calc = calc.replace("-", "+-")
    calc = calc.replace("/", "X/")

    # transforme les "," en "." pour les calculs
    calc = calc.replace(",", ".")

    # gestion des additions et soustractions
    result_add = 0    
    additions = calc.split("+")
    for value_add in additions:

        # gestion des multiplications et divisions
        result_mult = 1        
        multiplications = value_add.split("X")
        for value_mult in multiplications:
            if value_mult[0] == "/":
                value_mult = str(1 / Decimal(value_mult[1:]))
            result_mult = result_mult * Decimal(value_mult)

        result_add = result_add + result_mult

    result = str(result_add)
    result = result.replace(".", ",")

    return result

# gestion du bouton "clear"
def clear():
    global calc_ongoing
    global result_ongoing
    global last_operation
    
    if result_ongoing != "0":
        result_ongoing = "0"
        result_text.set(result_ongoing)
    else :
        reset()

# gestion du bouton "back"
def back():
    global calc_ongoing
    global result_ongoing
    global last_operation

    if last_operation == "":
        if result_ongoing != "0":
            result_ongoing = result_ongoing[:-1]
            if result_ongoing == "":
                result_ongoing = "0"
            result_text.set(result_ongoing)
    elif last_operation == "=":
        calc_ongoing = ""
        calc_input_text.set(calc_ongoing)

# réinitialise la calculatrice
def reset():
    global calc_ongoing
    global result_ongoing
    global last_operation
    calc_ongoing = ""
    result_ongoing = "0"
    last_operation = ""
    calc_input_text.set(calc_ongoing)
    result_text.set(result_ongoing)

# affichage de l'interface graphique
Button(window, text="Fermer", command=window.quit).grid(row=0, column=4)

calc_input_text = StringVar()
Label(window, textvariable=calc_input_text).grid(row=1, columnspan=5)

result_text = StringVar()
Label(window, textvariable=result_text).grid(row=2, columnspan=5)
result_text.set(result_ongoing)

Button(window, text=" 0 ", font=('Helvetica', 12, 'bold'), fg='black', bg='white', command=lambda: input_number("0"), height=2, width=7).grid(row=9, column=2)
Button(window, text=" 1 ", font=('Helvetica', 12, 'bold'), fg='black', bg='white', command=lambda: input_number("1"), height=2, width=7).grid(row=8, column=1)
Button(window, text=" 2 ", font=('Helvetica', 12, 'bold'), fg='black', bg='white', command=lambda: input_number("2"), height=2, width=7).grid(row=8, column=2)
Button(window, text=" 3 ", font=('Helvetica', 12, 'bold'), fg='black', bg='white', command=lambda: input_number("3"), height=2, width=7).grid(row=8, column=3)
Button(window, text=" 4 ", font=('Helvetica', 12, 'bold'), fg='black', bg='white', command=lambda: input_number("4"), height=2, width=7).grid(row=7, column=1)
Button(window, text=" 5 ", font=('Helvetica', 12, 'bold'), fg='black', bg='white', command=lambda: input_number("5"), height=2, width=7).grid(row=7, column=2)
Button(window, text=" 6 ", font=('Helvetica', 12, 'bold'), fg='black', bg='white', command=lambda: input_number("6"), height=2, width=7).grid(row=7, column=3)
Button(window, text=" 7 ", font=('Helvetica', 12, 'bold'), fg='black', bg='white', command=lambda: input_number("7"), height=2, width=7).grid(row=6, column=1)
Button(window, text=" 8 ", font=('Helvetica', 12, 'bold'), fg='black', bg='white', command=lambda: input_number("8"), height=2, width=7).grid(row=6, column=2)
Button(window, text=" 9 ", font=('Helvetica', 12, 'bold'), fg='black', bg='white', command=lambda: input_number("9"), height=2, width=7).grid(row=6, column=3)
Button(window, text=" , ", font=('Helvetica', 12, 'bold'), fg='black', bg='white', command=lambda: input_number(","), height=2, width=7).grid(row=9, column=3)

Button(window, text=" / ", font=('Helvetica', 12), fg='black', bg='grey', command=lambda: input_operation("/"), height=2, width=7).grid(row=5, column=4)
Button(window, text=" X ", font=('Helvetica', 12), fg='black', bg='grey', command=lambda: input_operation("X"), height=2, width=7).grid(row=6, column=4)
Button(window, text=" - ", font=('Helvetica', 12), fg='black', bg='grey', command=lambda: input_operation("-"), height=2, width=7).grid(row=7, column=4)
Button(window, text=" + ", font=('Helvetica', 12), fg='black', bg='grey', command=lambda: input_operation("+"), height=2, width=7).grid(row=8, column=4)

Button(window, text=" <= ", font=('Helvetica', 12), fg='black', bg='grey', command=lambda: back(), height=2, width=7).grid(row=3, column=4)

Button(window, text=" C ", font=('Helvetica', 12), fg='black', bg='grey', command=lambda: clear(), height=2, width=7).grid(row=3, column=3)

Button(window, text=" = ", font=('Helvetica', 12), fg='black', bg='blue', command=lambda: equal(), height=2, width=7).grid(row=9, column=4)

# lance le GUI
window.mainloop()