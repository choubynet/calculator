#!/usr/bin/env python3

from tkinter import *

# genération de la fenêtre
window = Tk()

# variable globale contenant la ligne des calculs affichés
calc_ongoing = ""

# variable globale contenant la ligne des résultats affichés
result_ongoing = ""

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
    result_ongoing = str(calcul())
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
    result_ongoing = str(calcul())
    result_text.set(result_ongoing)

    # affichage du nouveau calcul en cours
    calc_ongoing = calc_ongoing + "="
    calc_input_text.set(calc_ongoing)

# renvoie le résultat du calcul en cours
def calcul():
    result = 0
    additions = calc_ongoing.split("+")
    for value in additions:
        result = result + int(value)
    return result

# réinitialise la calculatrice
def reset():
    global calc_ongoing
    global result_ongoing
    global last_operation
    calc_ongoing = ""
    result_ongoing = ""
    last_operation = ""
    calc_input_text.set(calc_ongoing)

# affichage de l'interface graphique
Button(window, text="Fermer", command=window.quit).grid(row=0, column=3)
calc_input_text = StringVar()
Label(window, textvariable=calc_input_text).grid(row=1, columnspan=4)
result_text = StringVar()
Label(window, textvariable=result_text).grid(row=2, columnspan=4)
result_text.set(0)
Button(window, text=" 0 ", command=lambda: input_number("0")).grid(row=6, column=0)
Button(window, text=" 1 ", command=lambda: input_number("1")).grid(row=5, column=0)
Button(window, text=" 2 ", command=lambda: input_number("2")).grid(row=5, column=1)
Button(window, text=" 3 ", command=lambda: input_number("3")).grid(row=5, column=2)
Button(window, text=" 4 ", command=lambda: input_number("4")).grid(row=4, column=0)
Button(window, text=" 5 ", command=lambda: input_number("5")).grid(row=4, column=1)
Button(window, text=" 6 ", command=lambda: input_number("6")).grid(row=4, column=2)
Button(window, text=" 7 ", command=lambda: input_number("7")).grid(row=3, column=0)
Button(window, text=" 8 ", command=lambda: input_number("8")).grid(row=3, column=1)
Button(window, text=" 9 ", command=lambda: input_number("9")).grid(row=3, column=2)
Button(window, text=" + ", command=lambda: input_operation("+")).grid(row=3, column=3)
Button(window, text=" = ", command=lambda: equal()).grid(row=5, column=3)
window.mainloop()