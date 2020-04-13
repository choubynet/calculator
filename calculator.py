#!/usr/bin/env python3

from tkinter import *
from decimal import *
from math import *

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
    global calc_ongoing
    global last_operation
    global result_ongoing

    # réinitialisation si on rentre un chiffre directement après un "="
    if last_operation == "=" or last_operation == 'error':
        reset()

    #saisie d'un chiffre immédiatement après une "opération instantannée" (log, fact, etc)
    elif last_operation == "instant":
        search_operation = 0
        for i in range(0, len(calc_ongoing)):
            if calc_ongoing[i] == "+" or calc_ongoing[i] == "-" or calc_ongoing[i] == "X" or calc_ongoing[i] == "/" or calc_ongoing[i] == "mod":
                search_operation = i + 1
        if search_operation == 0:
            calc_ongoing = ""
        else:
            calc_ongoing = calc_ongoing[:search_operation]
        calc_input_text.set(calc_ongoing)
        result_ongoing = ""

    # réinitialisation du nombre saisi si la dernière touche saisie était une opération
    elif last_operation != "":
        result_ongoing = ""

    if result_ongoing == "0":
        result_ongoing = ""

    last_operation = ""
    result_ongoing = result_ongoing + value

    # affichage du nouveau nombre
    result_text.set(result_ongoing)

# gestion de la saisie d'une opération "classique" (+ - / X)
def input_operation(value):
    global calc_ongoing
    global result_ongoing
    global last_operation

    if last_operation == "error":
        return

    if last_operation == "instant":
        last_operation = value
        try:
            result_ongoing = calcul(calc_ongoing)
        except:
            error()
            return
        result_text.set(result_ongoing)
        calc_ongoing = calc_ongoing + value
        calc_input_text.set(calc_ongoing)
        return

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
    if value != "mod":
        try:
            result_ongoing = calcul(calc_ongoing)
        except:
            error()
            return
        result_text.set(result_ongoing)

    # affichage du nouveau calcul en cours
    calc_ongoing = calc_ongoing + value
    calc_input_text.set(calc_ongoing)

def input_instant_operation(value):
    global calc_ongoing
    global result_ongoing
    global last_operation

    # gestion si un "=" a été saisi juste avant
    if last_operation == "=":
        calc_ongoing = ""

    try:
        if last_operation == "instant":
            search_operation = 0
            for i in range(0, len(calc_ongoing)):
                if calc_ongoing[i] == "+" or calc_ongoing[i] == "-" or calc_ongoing[i] == "X" or calc_ongoing[i] == "/" or calc_ongoing[i] == "mod":
                    search_operation = i + 1
            if search_operation == 0:
                calc_ongoing = value + "(" + calc_ongoing + ")"
            else:
                calc_ongoing = calc_ongoing[:search_operation] + value + "(" + calc_ongoing[-(len(calc_ongoing) - search_operation):]  + ")"
            
        else:
            calc_ongoing = calc_ongoing + value + "(" + result_ongoing + ")"
            
        calc_input_text.set(calc_ongoing)
        if value == "ln":
            result_ongoing = str(log(Decimal(result_ongoing))) 
        elif value == "log":
            result_ongoing = str(log(Decimal(result_ongoing), 10))
        result_text.set(result_ongoing)
        last_operation = "instant"

    except:
        error()
        return 

# gestion de la saisie du "="
def input_equal():
    global calc_ongoing
    global result_ongoing    
    global last_operation

    # gestion si la dernière opération saisie était "="
    if last_operation == "=" or last_operation == "error":
        return

    if last_operation == "instant":
        last_operation = "="
        try:
            result_ongoing = calcul(calc_ongoing)
        except:
            error()
            return
        result_text.set(result_ongoing)
        calc_ongoing = calc_ongoing + "="
        calc_input_text.set(calc_ongoing)
        return

    last_operation = "=" 

    # affichage du nouveau résultat
    calc_ongoing = calc_ongoing + result_ongoing
    try:
        result_ongoing = calcul(calc_ongoing)
    except:
        error()
        return
    result_text.set(result_ongoing)

    # affichage du nouveau calcul en cours
    calc_ongoing = calc_ongoing + "="
    calc_input_text.set(calc_ongoing)

# renvoie le résultat du calcul en cours
def calcul(calc):
    
    # transforme les soustractions en additions et les divisions en multiplications
    calc = calc.replace("-", "+-")
    calc = calc.replace("/", "X/")
    calc = calc.replace("mod", "Xmod")

    # transforme toutes les valeurs des "opérations instantannées" (log, fact, etc)
    search_start = calc.find("ln(")
    while search_start != -1:
        bracket_count = 1
        for i in range(search_start + 3, len(calc)):                        
            if calc[i] == "(":
                bracket_count = bracket_count + 1
            elif calc[i] == ")":
                bracket_count = bracket_count - 1
            if bracket_count == 0:
                search_end = i
                break
        if search_end == len(calc) - 1:
            calc = calc[:search_start] + str(log(Decimal(calcul(calc[(search_start + 3):-(len(calc) - search_end)]))))
        else:
            calc = calc[:search_start] + str(log(Decimal(calcul(calc[(search_start + 3):-(len(calc) - search_end)])))) + calc[-(len(calc) - search_end - 1):]
        search_start = calc.find("ln(")

    search_start = calc.find("log(")
    while search_start != -1:
        bracket_count = 1
        for i in range(search_start + 4, len(calc)):                        
            if calc[i] == "(":
                bracket_count = bracket_count + 1
            elif calc[i] == ")":
                bracket_count = bracket_count - 1
            if bracket_count == 0:
                search_end = i
                break
        if search_end == len(calc) - 1:
            calc = calc[:search_start] + str(log(Decimal(calcul(calc[(search_start + 4):-(len(calc) - search_end)])), 10))
        else:
            calc = calc[:search_start] + str(log(Decimal(calcul(calc[(search_start + 4):-(len(calc) - search_end)])), 10)) + calc[-(len(calc) - search_end - 1):]
        search_start = calc.find("log(")    

    # gestion des additions et soustractions
    result_add = 0    
    additions = calc.split("+")
    for value_add in additions:

        # gestion des multiplications et divisions
        result_mult = 1        
        multiplications = value_add.split("X")
        for value_mult in multiplications:
            if value_mult[0] == "m":
                result_mult = result_mult % Decimal(value_mult[3:])
            elif value_mult[0] == "/":
                value_mult = str(1 / Decimal(value_mult[1:]))
                result_mult = result_mult * Decimal(value_mult)
            else:
                result_mult = result_mult * Decimal(value_mult)

        result_add = result_add + result_mult

    result = str(result_add)

    return result

# gestion du bouton "clear"
def input_clear():
    global calc_ongoing
    global result_ongoing
    global last_operation
    
    if result_ongoing != "0":
        result_ongoing = "0"
        result_text.set(result_ongoing)
    else :
        reset()

# gestion du bouton "back"
def input_back():
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
    elif last_operation == "error":
        reset()

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

# bloque le programme en cas d'erreur
def error():
    global calc_ongoing
    global result_ongoing
    global last_operation
    calc_ongoing = ""
    result_ongoing = "ERREUR"
    last_operation = "error"
    calc_input_text.set(calc_ongoing)
    result_text.set(result_ongoing)

# affichage de l'interface graphique
window.configure(background="#e9f2ff")
window.title("Calculatrice")

Button(window, text="Fermer", command=window.quit).grid(row=0, column=4)

calc_input_text = StringVar()
Entry(window, textvariable=calc_input_text, font=('Digital dream', 12), justify="right", fg='black', bg="#83e879").grid(row=1, columnspan=5, ipadx=90, ipady=15)

result_text = StringVar()
Entry(window, textvariable=result_text, font=('Digital dream', 14, 'bold'), justify="right", fg='black', bg="#83e879").grid(row=2, columnspan=5, ipadx=70, ipady=15)
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
Button(window, text=" . ", font=('Helvetica', 12, 'bold'), fg='black', bg='white', command=lambda: input_number("."), height=2, width=7).grid(row=9, column=3)

Button(window, text=" mod ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_operation("mod"), height=2, width=7).grid(row=4, column=4)
Button(window, text=" / ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_operation("/"), height=2, width=7).grid(row=5, column=4)
Button(window, text=" X ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_operation("X"), height=2, width=7).grid(row=6, column=4)
Button(window, text=" - ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_operation("-"), height=2, width=7).grid(row=7, column=4)
Button(window, text=" + ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_operation("+"), height=2, width=7).grid(row=8, column=4)

Button(window, text=" log ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_instant_operation("log"), height=2, width=7).grid(row=8, column=0)
Button(window, text=" ln ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_instant_operation("ln"), height=2, width=7).grid(row=9, column=0)

Button(window, text=" <= ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_back(), height=2, width=7).grid(row=3, column=4)
Button(window, text=" C ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_clear(), height=2, width=7).grid(row=3, column=3)
Button(window, text=" = ", font=('Helvetica', 12), fg='black', bg='#5498f9', command=lambda: input_equal(), height=2, width=7).grid(row=9, column=4)

# lance le GUI
window.mainloop()