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
# variable globale contenant la dernière opération importante (=, error, instant, constant_value, classic, bracket_open, bracket_close)
last_operation = ""



# gestion de la saisie d'un chiffre
def input_number(value):
    global calc_ongoing
    global last_operation
    global result_ongoing
    
    # réinitialisation si on rentre un chiffre directement après un "=", une erreur ou une parenthèse fermée
    if last_operation == "=" or last_operation == 'error' or last_operation == "bracket_close":
        reset()

    # saisie d'un chiffre immédiatement après une "opération instantanée" (log, fact, etc) annulant cette dernière
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

    # réinitialisation du nombre saisi si la dernière touche saisie était autre chose qu'un chiffre
    elif last_operation != "":
        result_ongoing = ""

    # disparition du "0" s'il était affiché seul
    if result_ongoing == "0":
        result_ongoing = ""

    last_operation = ""  

    # gestion des nombres spéciaux
    if value == "π":
        result_ongoing = str(pi)
        last_operation = "constant_value"
    elif value == "e":
        result_ongoing = str(e)
        last_operation = "constant_value"

    else:
        result_ongoing = result_ongoing + value
  
    # affichage du nouveau nombre
    result_text.set(result_ongoing)



# gestion de la saisie d'une opération "classique" (+, -, /, X et opérations telles que modulo)
def input_operation(value):
    global calc_ongoing
    global result_ongoing
    global last_operation

    # cas spécial si la dernière opération était une "opération instantanée"
    if last_operation == "instant":
        last_operation = "classic"
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
    if last_operation == "classic":
        if calc_ongoing[len(calc_ongoing) - 1] == "d" or calc_ongoing[len(calc_ongoing) - 1] == "p":
            calc_ongoing = calc_ongoing[:-3] + value
        else:
            calc_ongoing = calc_ongoing[:-1] + value
        calc_input_text.set(calc_ongoing)
        return

    # gestion si un "=" a été saisi juste avant
    if last_operation == "=":
        last_operation = "classic"
        calc_ongoing = result_ongoing + value
        calc_input_text.set(calc_ongoing)
        return

    # affichage du nouveau résultat
    if last_operation != "bracket_close":
        calc_ongoing = calc_ongoing + result_ongoing
    last_operation = "classic"
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



# gestion de la saisie d'une "opération instantanée" (ln, log, fact, etc)
def input_instant_operation(value):
    global calc_ongoing
    global result_ongoing
    global last_operation

    # gestion si un "=" a été saisi juste avant
    if last_operation == "=":
        calc_ongoing = ""

    # calcul et affichage de l'opération
    try:

        # recherche du point de modification si la dernière saisie était une parenthèse fermée ou une "opération instantanée"
        if last_operation == "bracket_close" or last_operation == "instant":
            bracket_count = 1
            for i in range (len(calc_ongoing) - 2, -1, -1):
                if calc_ongoing[i] == "(":
                    bracket_count = bracket_count - 1
                elif calc_ongoing[i] == ")":
                    bracket_count = bracket_count + 1
                if bracket_count == 0:
                    search_end = i
                    break
            search_operation = 0
            for i in range(0, search_end):
                if calc_ongoing[i] == "+" or calc_ongoing[i] == "-" or calc_ongoing[i] == "X" or calc_ongoing[i] == "/" or calc_ongoing[i] == "mod":
                    search_operation = i + 1
            if search_operation == 0:
                if calc_ongoing[0] == "(":
                    calc_ongoing = value + calc_ongoing
                else:
                    calc_ongoing = value + "(" + calc_ongoing + ")"
            else:
                if calc_ongoing[search_operation] == "(":
                    calc_ongoing = calc_ongoing[:search_operation] + value + calc_ongoing[-(len(calc_ongoing) - search_operation):]
                else:
                    calc_ongoing = calc_ongoing[:search_operation] + value + "(" + calc_ongoing[-(len(calc_ongoing) - search_operation):]  + ")"        
        
        # gestion du cas classique
        else:
            calc_ongoing = calc_ongoing + value + "(" + result_ongoing + ")"           
        
        calc_input_text.set(calc_ongoing)

        # calcul suivant l'opération souhaitée
        if value == "ln":
            result_ongoing = str(log(Decimal(result_ongoing))) 
        elif value == "log":
            result_ongoing = str(log(Decimal(result_ongoing), 10))
        elif value == "fact":
            result_ongoing = str(factorial(Decimal(result_ongoing)))
        elif value == "abs":
            result_ongoing = str(fabs(Decimal(result_ongoing)))
        elif value == "sqr":
            result_ongoing = str(pow(Decimal(result_ongoing), 2))
        elif value == "cube":
            result_ongoing = str(pow(Decimal(result_ongoing), 3))
        elif value == "10^":
            result_ongoing = str(pow(10, Decimal(result_ongoing)))
        elif value == "inv":
            result_ongoing = str(1 / Decimal(result_ongoing))
        elif value == "negate":
            result_ongoing = str((-1) * Decimal(result_ongoing))

        # affichage du résultat
        result_text.set(result_ongoing)

        last_operation = "instant"

    # gestion si un calcul renvoie une erreur
    except:
        error()
        return 



# gestion de la saisie du changement de signe
def input_change_sign():
    global calc_ongoing
    global result_ongoing
    global last_operation
    
    if last_operation != "":
        input_instant_operation("negate")
    else:
        try:
            result_ongoing = str((-1) * Decimal(result_ongoing))
            result_text.set(result_ongoing)
        except:
            error()
            return



# gestion de la saisie des parenthèses
def input_bracket(value):
    global calc_ongoing
    global result_ongoing
    global last_operation
    
    # gestion des cas spéciaux
    if (last_operation == "instant" and value == "(") or last_operation == "=":
        calc_ongoing = ""
        calc_input_text.set(calc_ongoing)

    if (calc_ongoing.count("(") <= calc_ongoing.count(")")) and (value == ")"):
        return
    else:
        if value == "(":
            if last_operation == "bracket_close":
                for i in range(len(calc_ongoing) - 1, -1, -1):
                    if calc_ongoing[i] == "(":
                        break
                calc_ongoing = calc_ongoing[:i + 1]
            else:                
                calc_ongoing = calc_ongoing + value
            last_operation = "bracket_open"
        else:
            if last_operation == "bracket_close":
                calc_ongoing = calc_ongoing + value
            else:
                if last_operation == "instant":
                    calc_ongoing = calc_ongoing + value
                else:
                    calc_ongoing = calc_ongoing + result_ongoing + value
                last_operation = "bracket_close"            
    calc_input_text.set(calc_ongoing)



# gestion du bouton "clear"
def input_clear():
    global calc_ongoing
    global result_ongoing
    global last_operation
    
    if last_operation == "error":
        reset()
    elif result_ongoing != "0":
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



# gestion de la saisie du "="
def input_equal():
    global calc_ongoing
    global result_ongoing    
    global last_operation

    # gestion si la dernière opération saisie était "="
    if last_operation == "=":
        return

    elif last_operation == "error":
        reset()
        return
        
    elif last_operation == "instant":
        last_operation = "="
        while calc_ongoing.count("(") != calc_ongoing.count(")"):
            calc_ongoing = calc_ongoing + ")"
        try:
            result_ongoing = calcul(calc_ongoing)
        except:
            error()
            return
        result_text.set(result_ongoing)
        calc_ongoing = calc_ongoing + "="
        calc_input_text.set(calc_ongoing)
        return    

    # affichage du nouveau résultat
    elif last_operation != "bracket_close":
        calc_ongoing = calc_ongoing + result_ongoing
    last_operation = "=" 
    while calc_ongoing.count("(") != calc_ongoing.count(")"):
            calc_ongoing = calc_ongoing + ")"
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

    while calc.count("(") != calc.count(")"):
        calc = calc + ")"
    
    # transforme les soustractions en additions et les divisions en multiplications
    calc = calc.replace("--", "+")
    calc = calc.replace("-", "+-")
    calc = calc.replace("/", "X/")
    calc = calc.replace("^", "X^")
    calc = calc.replace("mod", "Xmod")
    calc = calc.replace("exp", "Xexp")

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

    search_start = calc.find("fact(")
    while search_start != -1:
        bracket_count = 1
        for i in range(search_start + 5, len(calc)):                        
            if calc[i] == "(":
                bracket_count = bracket_count + 1
            elif calc[i] == ")":
                bracket_count = bracket_count - 1
            if bracket_count == 0:
                search_end = i
                break
        if search_end == len(calc) - 1:
            calc = calc[:search_start] + str(factorial(Decimal(calcul(calc[(search_start + 5):-(len(calc) - search_end)]))))
        else:
            calc = calc[:search_start] + str(factorial(Decimal(calcul(calc[(search_start + 5):-(len(calc) - search_end)])))) + calc[-(len(calc) - search_end - 1):]
        search_start = calc.find("fact(")

    search_start = calc.find("abs(")
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
            calc = calc[:search_start] + str(fabs(Decimal(calcul(calc[(search_start + 4):-(len(calc) - search_end)]))))
        else:
            calc = calc[:search_start] + str(fabs(Decimal(calcul(calc[(search_start + 4):-(len(calc) - search_end)])))) + calc[-(len(calc) - search_end - 1):]
        search_start = calc.find("abs(")

    search_start = calc.find("sqr(")
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
            calc = calc[:search_start] + str(pow(Decimal(calcul(calc[(search_start + 4):-(len(calc) - search_end)])), 2))
        else:
            calc = calc[:search_start] + str(pow(Decimal(calcul(calc[(search_start + 4):-(len(calc) - search_end)])), 2)) + calc[-(len(calc) - search_end - 1):]
        search_start = calc.find("sqr(")

    search_start = calc.find("cube(")
    while search_start != -1:
        bracket_count = 1
        for i in range(search_start + 5, len(calc)):                        
            if calc[i] == "(":
                bracket_count = bracket_count + 1
            elif calc[i] == ")":
                bracket_count = bracket_count - 1
            if bracket_count == 0:
                search_end = i
                break
        if search_end == len(calc) - 1:
            calc = calc[:search_start] + str(pow(Decimal(calcul(calc[(search_start + 5):-(len(calc) - search_end)])), 3))
        else:
            calc = calc[:search_start] + str(pow(Decimal(calcul(calc[(search_start + 5):-(len(calc) - search_end)])), 3)) + calc[-(len(calc) - search_end - 1):]
        search_start = calc.find("cube(")

    search_start = calc.find("ten(")
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
            calc = calc[:search_start] + str(pow(10, Decimal(calcul(calc[(search_start + 4):-(len(calc) - search_end)]))))
        else:
            calc = calc[:search_start] + str(pow(10, Decimal(calcul(calc[(search_start + 4):-(len(calc) - search_end)])))) + calc[-(len(calc) - search_end - 1):]
        search_start = calc.find("ten(")

    search_start = calc.find("inv(")
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
            calc = calc[:search_start] + str(1 / Decimal(calcul(calc[(search_start + 4):-(len(calc) - search_end)])))
        else:
            calc = calc[:search_start] + str(1 / Decimal(calcul(calc[(search_start + 4):-(len(calc) - search_end)]))) + calc[-(len(calc) - search_end - 1):]
        search_start = calc.find("inv(")  

    search_start = calc.find("negate(")
    while search_start != -1:
        bracket_count = 1
        for i in range(search_start + 7, len(calc)):                        
            if calc[i] == "(":
                bracket_count = bracket_count + 1
            elif calc[i] == ")":
                bracket_count = bracket_count - 1
            if bracket_count == 0:
                search_end = i
                break
        if search_end == len(calc) - 1:
            calc = calc[:search_start] + str((-1) * Decimal(calcul(calc[(search_start + 7):-(len(calc) - search_end)])))
        else:
            calc = calc[:search_start] + str((-1) * Decimal(calcul(calc[(search_start + 7):-(len(calc) - search_end)]))) + calc[-(len(calc) - search_end - 1):]
        search_start = calc.find("negate(")

    # gestion des parenthèses
    search_start = calc.find("(")
    while search_start != -1:
        bracket_count = 1
        for i in range(search_start + 1, len(calc)):                        
            if calc[i] == "(":
                bracket_count = bracket_count + 1
            elif calc[i] == ")":
                bracket_count = bracket_count - 1
            if bracket_count == 0:
                search_end = i
                break
        if search_end == len(calc) - 1:
            calc = calc[:search_start] + calcul(calc[(search_start + 1):-(len(calc) - search_end)])
        else:
            calc = calc[:search_start] + calcul(calc[(search_start + 1):-(len(calc) - search_end)]) + calc[-(len(calc) - search_end - 1):]
        search_start = calc.find("(")

    # gestion des additions et soustractions
    result_add = 0    
    additions = calc.split("+")
    i = 0
    length = len(additions)
    while i < length:
	    if additions[i] == "":
		    additions.remove(additions[i])
		    length = length -1  
		    continue
	    i = i + 1
    for value_add in additions:

        # gestion des multiplications et divisions
        result_mult = 1        
        multiplications = value_add.split("X")
        i = 0
        length = len(multiplications)
        while i < length:
	        if multiplications[i] == "":
		        multiplications.remove(multiplications[i])
		        length = length -1  
		        continue
	        i = i + 1
        for value_mult in multiplications:
            if value_mult[0] == "m":
                result_mult = result_mult % Decimal(value_mult[3:])
            elif value_mult[0] == "e":
                result_mult = result_mult * Decimal(str(pow(10, Decimal(value_mult[3:]))))
            elif value_mult[0] == "^":
                result_mult = Decimal(str((pow(result_mult, Decimal(value_mult[1:])))))
            elif value_mult[0] == "/":
                value_mult = str(1 / Decimal(value_mult[1:]))
                result_mult = result_mult * Decimal(value_mult)
            else:
                result_mult = result_mult * Decimal(value_mult)

        result_add = result_add + result_mult

    result = str(result_add)
    return result



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
    Button(window, text=" xʸ ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_operation("^"), height=2, width=7, borderwidth=2, relief="raised").grid(row=7, column=0)
    Button(window, text=" exp ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_operation("exp"), height=2, width=7, borderwidth=2, relief="raised").grid(row=5, column=3)
    Button(window, text=" . ", font=('Helvetica', 12, 'bold'), fg='black', bg='white', command=lambda: input_number("."), height=2, width=7, borderwidth=2, relief="raised").grid(row=10, column=3)
    Button(window, text=" π ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_number("π"), height=2, width=7, borderwidth=2, relief="raised").grid(row=4, column=1)
    Button(window, text=" e ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_number("e"), height=2, width=7, borderwidth=2, relief="raised").grid(row=4, column=2)
    Button(window, text=" mod ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_operation("mod"), height=2, width=7, borderwidth=2, relief="raised").grid(row=5, column=4)
    Button(window, text=" / ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_operation("/"), height=2, width=7, borderwidth=2, relief="raised").grid(row=6, column=4)
    Button(window, text=" X ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_operation("X"), height=2, width=7, borderwidth=2, relief="raised").grid(row=7, column=4)
    Button(window, text=" - ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_operation("-"), height=2, width=7, borderwidth=2, relief="raised").grid(row=8, column=4)
    Button(window, text=" + ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_operation("+"), height=2, width=7, borderwidth=2, relief="raised").grid(row=9, column=4)
    Button(window, text=" x² ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_instant_operation("sqr"), height=2, width=7, borderwidth=2, relief="raised").grid(row=5, column=0)
    Button(window, text=" x³ ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_instant_operation("cube"), height=2, width=7, borderwidth=2, relief="raised").grid(row=6, column=0)
    Button(window, text=" 10ˣ ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_instant_operation("10^"), height=2, width=7, borderwidth=2, relief="raised").grid(row=8, column=0)
    Button(window, text=" 1/x ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_instant_operation("inv"), height=2, width=7, borderwidth=2, relief="raised").grid(row=5, column=1)
    Button(window, text=" |x| ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_instant_operation("abs"), height=2, width=7, borderwidth=2, relief="raised").grid(row=5, column=2)
    Button(window, text=" n! ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_instant_operation("fact"), height=2, width=7, borderwidth=2, relief="raised").grid(row=6, column=3)
    Button(window, text=" log ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_instant_operation("log"), height=2, width=7, borderwidth=2, relief="raised").grid(row=9, column=0)
    Button(window, text=" ln ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_instant_operation("ln"), height=2, width=7, borderwidth=2, relief="raised").grid(row=10, column=0)
    Button(window, text=" ( ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_bracket("("), height=2, width=7, borderwidth=2, relief="raised").grid(row=6, column=1)
    Button(window, text=" ) ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_bracket(")"), height=2, width=7, borderwidth=2, relief="raised").grid(row=6, column=2)
    Button(window, text=" +/- ", font=('Helvetica', 12, 'bold'), fg='black', bg='white', command=lambda: input_change_sign(), height=2, width=7, borderwidth=2, relief="raised").grid(row=10, column=1)



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
    Button(window, text=" xʸ ", font=('Helvetica', 12), state='disabled', fg='#d7d5d5', bg='#ededed', height=2, width=7, borderwidth=2, relief="raised").grid(row=7, column=0)
    Button(window, text=" exp ", font=('Helvetica', 12), state='disabled', fg='#d7d5d5', bg='#ededed', height=2, width=7, borderwidth=2, relief="raised").grid(row=5, column=3)
    Button(window, text=" . ", font=('Helvetica', 12, 'bold'), state='disabled', fg='#d7d5d5', bg='#ededed', height=2, width=7, borderwidth=2, relief="raised").grid(row=10, column=3)
    Button(window, text=" π ", font=('Helvetica', 12), state='disabled', fg='#d7d5d5', bg='#ededed', height=2, width=7, borderwidth=2, relief="raised").grid(row=4, column=1)
    Button(window, text=" e ", font=('Helvetica', 12), state='disabled', fg='#d7d5d5', bg='#ededed', height=2, width=7, borderwidth=2, relief="raised").grid(row=4, column=2)
    Button(window, text=" mod ", font=('Helvetica', 12), state='disabled', fg='#d7d5d5', bg='#ededed', height=2, width=7, borderwidth=2, relief="raised").grid(row=5, column=4)
    Button(window, text=" / ", font=('Helvetica', 12), state='disabled', fg='#d7d5d5', bg='#ededed', height=2, width=7, borderwidth=2, relief="raised").grid(row=6, column=4)
    Button(window, text=" X ", font=('Helvetica', 12), state='disabled', fg='#d7d5d5', bg='#ededed', height=2, width=7, borderwidth=2, relief="raised").grid(row=7, column=4)
    Button(window, text=" - ", font=('Helvetica', 12), state='disabled', fg='#d7d5d5', bg='#ededed', height=2, width=7, borderwidth=2, relief="raised").grid(row=8, column=4)
    Button(window, text=" + ", font=('Helvetica', 12), state='disabled', fg='#d7d5d5', bg='#ededed', height=2, width=7, borderwidth=2, relief="raised").grid(row=9, column=4)
    Button(window, text=" x² ", font=('Helvetica', 12), state='disabled', fg='#d7d5d5', bg='#ededed', height=2, width=7, borderwidth=2, relief="raised").grid(row=5, column=0)
    Button(window, text=" x³ ", font=('Helvetica', 12), state='disabled', fg='#d7d5d5', bg='#ededed', height=2, width=7, borderwidth=2, relief="raised").grid(row=6, column=0)
    Button(window, text=" 10ˣ ", font=('Helvetica', 12), state='disabled', fg='#d7d5d5', bg='#ededed', height=2, width=7, borderwidth=2, relief="raised").grid(row=8, column=0)
    Button(window, text=" 1/x ", font=('Helvetica', 12), state='disabled', fg='#d7d5d5', bg='#ededed', height=2, width=7, borderwidth=2, relief="raised").grid(row=5, column=1)
    Button(window, text=" |x| ", font=('Helvetica', 12), state='disabled', fg='#d7d5d5', bg='#ededed', height=2, width=7, borderwidth=2, relief="raised").grid(row=5, column=2)
    Button(window, text=" n! ", font=('Helvetica', 12), state='disabled', fg='#d7d5d5', bg='#ededed', height=2, width=7, borderwidth=2, relief="raised").grid(row=6, column=3)
    Button(window, text=" log ", font=('Helvetica', 12), state='disabled', fg='#d7d5d5', bg='#ededed', height=2, width=7, borderwidth=2, relief="raised").grid(row=9, column=0)
    Button(window, text=" ln ", font=('Helvetica', 12), state='disabled', fg='#d7d5d5', bg='#ededed', height=2, width=7, borderwidth=2, relief="raised").grid(row=10, column=0)
    Button(window, text=" ( ", font=('Helvetica', 12), state='disabled', fg='#d7d5d5', bg='#ededed', height=2, width=7, borderwidth=2, relief="raised").grid(row=6, column=1)
    Button(window, text=" ) ", font=('Helvetica', 12), state='disabled', fg='#d7d5d5', bg='#ededed', height=2, width=7, borderwidth=2, relief="raised").grid(row=6, column=2)
    Button(window, text=" +/- ", font=('Helvetica', 12, 'bold'), state='disabled', fg='#d7d5d5', bg='#ededed', height=2, width=7, borderwidth=2, relief="raised").grid(row=10, column=1)
  


# affichage de l'interface graphique
window.configure(background="#0b0a13")
window.title("Calculatrice")

Label(window, bg="#0b0a13").grid(row=0, columnspan=6)
Label(window, bg="#0b0a13").grid(row=11, columnspan=6)
Label(window, bg="#0b0a13").grid(row=3, columnspan=6)

calc_input_text = StringVar()
Entry(window, textvariable=calc_input_text, font=('Digital dream', 12), justify="right", fg='black', bg="#83e879", highlightbackground='black').grid(row=1, columnspan=5, ipadx=90, ipady=15)

result_text = StringVar()
Entry(window, textvariable=result_text, font=('Digital dream', 14, 'bold'), justify="right", fg='black', bg="#83e879", highlightbackground='black').grid(row=2, columnspan=5, ipadx=70, ipady=15)
result_text.set(result_ongoing)

Button(window, text=" 0 ", font=('Helvetica', 12, 'bold'), fg='black', bg='white', command=lambda: input_number("0"), height=2, width=7, borderwidth=2, relief="raised").grid(row=10, column=2)
Button(window, text=" 1 ", font=('Helvetica', 12, 'bold'), fg='black', bg='white', command=lambda: input_number("1"), height=2, width=7, borderwidth=2, relief="raised").grid(row=9, column=1)
Button(window, text=" 2 ", font=('Helvetica', 12, 'bold'), fg='black', bg='white', command=lambda: input_number("2"), height=2, width=7, borderwidth=2, relief="raised").grid(row=9, column=2)
Button(window, text=" 3 ", font=('Helvetica', 12, 'bold'), fg='black', bg='white', command=lambda: input_number("3"), height=2, width=7, borderwidth=2, relief="raised").grid(row=9, column=3)
Button(window, text=" 4 ", font=('Helvetica', 12, 'bold'), fg='black', bg='white', command=lambda: input_number("4"), height=2, width=7, borderwidth=2, relief="raised").grid(row=8, column=1)
Button(window, text=" 5 ", font=('Helvetica', 12, 'bold'), fg='black', bg='white', command=lambda: input_number("5"), height=2, width=7, borderwidth=2, relief="raised").grid(row=8, column=2)
Button(window, text=" 6 ", font=('Helvetica', 12, 'bold'), fg='black', bg='white', command=lambda: input_number("6"), height=2, width=7, borderwidth=2, relief="raised").grid(row=8, column=3)
Button(window, text=" 7 ", font=('Helvetica', 12, 'bold'), fg='black', bg='white', command=lambda: input_number("7"), height=2, width=7, borderwidth=2, relief="raised").grid(row=7, column=1)
Button(window, text=" 8 ", font=('Helvetica', 12, 'bold'), fg='black', bg='white', command=lambda: input_number("8"), height=2, width=7, borderwidth=2, relief="raised").grid(row=7, column=2)
Button(window, text=" 9 ", font=('Helvetica', 12, 'bold'), fg='black', bg='white', command=lambda: input_number("9"), height=2, width=7, borderwidth=2, relief="raised").grid(row=7, column=3)
Button(window, text=" . ", font=('Helvetica', 12, 'bold'), fg='black', bg='white', command=lambda: input_number("."), height=2, width=7, borderwidth=2, relief="raised").grid(row=10, column=3)

Button(window, text=" π ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_number("π"), height=2, width=7, borderwidth=2, relief="raised").grid(row=4, column=1)
Button(window, text=" e ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_number("e"), height=2, width=7, borderwidth=2, relief="raised").grid(row=4, column=2)

Button(window, text=" exp ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_operation("exp"), height=2, width=7, borderwidth=2, relief="raised").grid(row=5, column=3)
Button(window, text=" mod ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_operation("mod"), height=2, width=7, borderwidth=2, relief="raised").grid(row=5, column=4)
Button(window, text=" xʸ ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_operation("^"), height=2, width=7, borderwidth=2, relief="raised").grid(row=7, column=0)
Button(window, text=" / ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_operation("/"), height=2, width=7, borderwidth=2, relief="raised").grid(row=6, column=4)
Button(window, text=" X ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_operation("X"), height=2, width=7, borderwidth=2, relief="raised").grid(row=7, column=4)
Button(window, text=" - ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_operation("-"), height=2, width=7, borderwidth=2, relief="raised").grid(row=8, column=4)
Button(window, text=" + ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_operation("+"), height=2, width=7, borderwidth=2, relief="raised").grid(row=9, column=4)

Button(window, text=" x² ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_instant_operation("sqr"), height=2, width=7, borderwidth=2, relief="raised").grid(row=5, column=0)
Button(window, text=" x³ ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_instant_operation("cube"), height=2, width=7, borderwidth=2, relief="raised").grid(row=6, column=0)
Button(window, text=" 10ˣ ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_instant_operation("10^"), height=2, width=7, borderwidth=2, relief="raised").grid(row=8, column=0)
Button(window, text=" 1/x ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_instant_operation("inv"), height=2, width=7, borderwidth=2, relief="raised").grid(row=5, column=1)
Button(window, text=" |x| ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_instant_operation("abs"), height=2, width=7, borderwidth=2, relief="raised").grid(row=5, column=2)
Button(window, text=" n! ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_instant_operation("fact"), height=2, width=7, borderwidth=2, relief="raised").grid(row=6, column=3)
Button(window, text=" log ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_instant_operation("log"), height=2, width=7, borderwidth=2, relief="raised").grid(row=9, column=0)
Button(window, text=" ln ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_instant_operation("ln"), height=2, width=7, borderwidth=2, relief="raised").grid(row=10, column=0)
Button(window, text=" ( ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_bracket("("), height=2, width=7, borderwidth=2, relief="raised").grid(row=6, column=1)
Button(window, text=" ) ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_bracket(")"), height=2, width=7, borderwidth=2, relief="raised").grid(row=6, column=2)

Button(window, text="  ", font=('Helvetica', 12), state='disabled', fg='black', bg='#e4edf2', height=2, width=7, borderwidth=2, relief="raised").grid(row=4, column=0)

Button(window, text=" +/- ", font=('Helvetica', 12, 'bold'), fg='black', bg='white', command=lambda: input_change_sign(), height=2, width=7, borderwidth=2, relief="raised").grid(row=10, column=1)
Button(window, text=" <= ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_back(), height=2, width=7, borderwidth=2, relief="raised").grid(row=4, column=4)
Button(window, text=" C ", font=('Helvetica', 12), fg='black', bg='#e4edf2', command=lambda: input_clear(), height=2, width=7, borderwidth=2, relief="raised").grid(row=4, column=3)
Button(window, text=" = ", font=('Helvetica', 12, 'bold'), fg='white', bg='#f8250c', command=lambda: input_equal(), height=2, width=7, borderwidth=2, relief="raised").grid(row=10, column=4)



# lance le GUI
window.mainloop()