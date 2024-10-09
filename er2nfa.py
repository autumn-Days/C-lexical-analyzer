# -*- coding: utf-8 -*-

from NFA import *

TOKENS = {
    'INT':'in.t.',
    'STRING':'st.r.i.n.g.',
    'ID':'_ab|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z||AB|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z||_ab|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z||AB|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z||01|2|3|4|5|6|7|8|9||^.',
    'EQ':'=',
    'NUM':'01|2|3|4|5|6|7|8|9|01|2|3|4|5|6|7|8|9|^.',
    'ADD':'+',
    'SUB':'-',
    'MULT':'*',
    'SEMICOLON':';',
    'GREATER':'>',
    'LESS':'<',
    'CONST':'"ab|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|0|1|2|3|4|5|6|7|8|9| |;|_|=|-|*|,|^.".'
    }

def isOperator(char:str) -> bool:
    return (char == "." or char == "|" or char == "^")

def isSymboll(char:str) -> bool:
    return (not isOperator(char))

def thompsonConstructor(res:List[str]) -> Tuple[List[NFA], int]:
    listNFAs:List[NFA] = []
    newLabel = 0
    for re in res:
        automataStack = deque()
        while re != "":
            char = re[0]
            if (isSymboll(char)):
                initState = newLabel
                finalState = newLabel+1
                states = set({initState,finalState})
                alphabet = set({char})
                initialStates = set({initState})
                finalStates = set({finalState})
                transiction = {}
                transiction[(initState,char)] = [finalState]
                newNFA = NFA(states,alphabet,transiction,initialStates,finalStates)
                automataStack.append(newNFA)
                newLabel += 2
            else:
                nfa = None
                #chapéu é o símbolo da estrela, pois estrela já é a multiplicaçaõ
                if char != "^":
                    secondOperand = automataStack.pop()
                    firstOperand = automataStack.pop()
                    if char == "|":
                        nfa = union(firstOperand,secondOperand)
                        #since I created two more states, I need to update
                        #the newLabel
                        newLabel += 2
                    elif char == ".":
                        nfa = cocatenation(firstOperand, secondOperand)
                elif char == "^":
                    onlyOperand = automataStack.pop()
                    nfa = star(onlyOperand)
                    #since I created two more states, I need to update
                    #the newLabel
                    newLabel += 2
                automataStack.append(nfa)
            re = re[1:]
        listNFAs.append(automataStack.pop())
    return (listNFAs, newLabel)