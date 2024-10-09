from DFA import *
from NFA import *
from er2nfa import *
from  helperFunctions import *
from typing import Deque, List

# -*- coding: utf-8 -*-

def main():
    file = input("Insira o nome do arquivo com o código fonte:\n")
    print("-=-=-=-=")
    #preparation
    tokensNres:Tuple[str,str]                           = read_er()
    NFAsNcurrentState:Tuple[List[NFA],int]              = thompsonConstructor(tokensNres[1])
    superNFA_finalStates:Tuple[NFA,List[List[int]]]     = uniter(NFAsNcurrentState[0],NFAsNcurrentState[1])
    superNFA:NFA                                        = superNFA_finalStates[0]
    finalStates:List[List[int]]                         = superNFA_finalStates[1]
    superDFA:[DFA]                                      = superNFA.nfa2dfa()
    finalStates_token:Dict[int,str]                     = dict(zip(finalStates,tokensNres[0]))
    #lexical analyser
    statements:List[str]                                = loadSourceCode(file)
    definitiveTokens = []
    
    for statement in statements :
        leximes:List[str] =  miniParser(statement)
        statementTokens = []
        for lexime in leximes:
            leximeTokens = []
            macroStateDFA = superDFA.accepts(lexime)[1]
            for microState in macroStateDFA:
                token = ""
                try:
                    token = finalStates_token[microState]
                except KeyError:
                    continue
                if token != "" :
                    leximeTokens.append(token)
            sizeLeximeTokens = len(leximeTokens)
            if sizeLeximeTokens == 0:
                #print("size 00:", leximeTokens)
                statementTokens.append('ERRO')
                #print("ERRO")
                #break
            elif sizeLeximeTokens == 1:
                #print("size 01:", leximeTokens)
                statementTokens.append(leximeTokens[0])
            elif (sizeLeximeTokens == 2):
                #print("size 02:", leximeTokens)
                if leximeTokens[0] == "ID":
                    statementTokens.append(leximeTokens[1])
                else :
                    statementTokens.append(leximeTokens[0])
        
        definitiveTokens.append(statementTokens)
        
    #print(definitiveTokens)
    for tokens in definitiveTokens:
        if "ERRO" in tokens:
            print("ERRO")
        else:
            for token in tokens:
                print(token, end=" ")
            print("\n", end="")
    


if __name__ == "__main__":
    main()
    
