# -*- coding: utf-8 -*-

from DFA import *
from collections import deque
from typing import Dict, List, Tuple, Deque

class NFA():
    def __init__(self, setStates, alphabet, transiction, initialStates, finalStates):
        self.setStates = setStates
        self.alphabet = alphabet
        self.transiction = transiction
        self.initialStates = initialStates
        self.finalStates = finalStates

    def __repr__(self):
        return f" setStates:{self.setStates}\n alphabet: {self.alphabet}\n transition: {self.transiction}\n finalStates: {self.finalStates}\n initStates: {self.initialStates}"

    def displayTransition(self):
        print("{")
        listKeys = list(self.transiction.keys())
        listValues = list(self.transiction.values())
        for key,value in zip(listKeys,listValues):
            print("\t"+str(key)+":\t"+str(value))
        print("}")

    def nextStates(self, state, character):
        try:
            return self.transiction[(state,character)]; #list
        except KeyError:
            return set({})#set

    def __epsilonClosure(self, states):
        totalClosure = set(states)
        statesToComputeClosure = list(states)
        
        while statesToComputeClosure:
            state = statesToComputeClosure.pop()
            # Check for epsilon transitions using the key (state, '')
            if (state, '') in self.transiction:  
                for nextState in self.transiction[(state, '')]:
                    if nextState not in totalClosure:
                        totalClosure.add(nextState)
                        statesToComputeClosure.append(nextState)                 
        return totalClosure


    def accepts(self, word):
        statesAlreadyVisited = self.__epsilonClosure(self.initialStates)
        while word != "":
            statesShouldGo = set({})
            for state in statesAlreadyVisited :
                statesShouldGo = statesShouldGo | self.__epsilonClosure(self.nextStates(state,word[0]))
            word = word[1:]
            statesAlreadyVisited = statesShouldGo
        return ((statesAlreadyVisited & self.finalStates) != set({}))


    def nfa2dfa(self):
        EPSILON_CLOSURE_INIT_STATES_NFA = self.__epsilonClosure(self.initialStates)#set
        initialStateDFA = frozenset(EPSILON_CLOSURE_INIT_STATES_NFA)#frozenset
        #begin basic structures of a DFA
        statesToVisit = deque()#deque[frozenset]
        statesToVisit.append(initialStateDFA)
        setDFAstates = set({frozenset(EPSILON_CLOSURE_INIT_STATES_NFA)})#list[frozenset]
        transictionDFA = {} #An empty dict
        finalStates= set({})#set
        #end basic structures of a DFA

        while statesToVisit :
            currentDfaMacroState = statesToVisit.popleft()#frozenset
            copyOneAlphabet = self.alphabet
            for inputSymboll in self.alphabet:#char
                OnGoingNextMacroState = set({})#set{frozenset}
                for stateNfa in list(currentDfaMacroState):
                    #the following line returns an empty set if the key was not found (state,key):[list]
                    setOutgoingStates = self.nextStates(stateNfa, inputSymboll)#list|set. If the return is not an empty set, it is a list. This variable name is confusing
                    if setOutgoingStates:
                        OnGoingNextMacroState.update(setOutgoingStates)
                definitiveNextMacroState = frozenset(self.__epsilonClosure(OnGoingNextMacroState))
            
                if definitiveNextMacroState not in setDFAstates:
                    setDFAstates.add(definitiveNextMacroState)
                    statesToVisit.append(definitiveNextMacroState)
                
                if definitiveNextMacroState & self.finalStates :
                    finalStates.add(definitiveNextMacroState)
                
                transictionDFA[(currentDfaMacroState,inputSymboll)] = definitiveNextMacroState   
        
        return DFA(setDFAstates,self.alphabet,transictionDFA,initialStateDFA,finalStates)

def cocatenation(nfa1:NFA, nfa2:NFA) -> NFA:
    OLD_FINAL_STATE_1 = list(nfa1.finalStates)[0]
    OLD_INIT_STATE_2  = list(nfa2.initialStates)[0]
    
    newStates =  nfa1.setStates | nfa2.setStates
    newAlphabet = nfa1.alphabet | nfa2.alphabet
    newInitState = nfa1.initialStates
    newFinalStates= nfa2.finalStates

    newTransictionFunction:Dict[Tuple[int,str],int] = {}
    
    for key in nfa1.transiction:
        newTransictionFunction[key] = nfa1.transiction[key]
    for key in nfa2.transiction:
        newTransictionFunction[key] = nfa2.transiction[key]
    
    LIST_OLD_INIT_STATE_2 = []
    LIST_OLD_INIT_STATE_2.append(OLD_INIT_STATE_2)
    newTransictionFunction[(OLD_FINAL_STATE_1,"")] = LIST_OLD_INIT_STATE_2
    
    #In this function I just modify the first automata
    del nfa2
    return NFA(newStates, newAlphabet, newTransictionFunction, newInitState, newFinalStates)

def union(nfa1, nfa2, newLabel=None) -> NFA:
    """   
    This function will create a brand new automata,
    not a rewrite of a previous given        
    """
    #union of two alphabets
    newAlphabet:Set[int] = nfa1.alphabet | nfa2.alphabet
    #create new initial state
    newStates:Set[int] = nfa1.setStates | nfa2.setStates
    newInit = -1
    if newLabel != None:
        newInit = newLabel
    else :
        newInit = (max(newStates)+1)
    newTransition = {(newInit,""):[]}
    oldInitStates = list(nfa1.initialStates | nfa2.initialStates)
    for oldInitState in oldInitStates:
        newTransition[(newInit,"")].append(oldInitState)
    #create new final state
    newFinal = -2
    if newLabel != None:
        newFinal = newLabel+1
    else :
        newFinal = newInit+1
    #add the new states to the set of states
    newStates.add(newInit)
    newStates.add(newFinal)
    #add transition from every olFinalState1-2 to newFinal
    oldFinalStates:Set[int] = nfa1.finalStates | nfa2.finalStates
    for oldFinalState in oldFinalStates :
        if (oldFinalState in oldInitStates):
            newTransition[(oldFinalState,"")].append(newFinal)    
        else:
            newTransition[(oldFinalState,"")] = [newFinal]
    newTransition.update(nfa1.transiction)
    newTransition.update(nfa2.transiction)    
    del nfa1, nfa2
    return NFA(newStates,newAlphabet,newTransition,set({newInit}),set({newFinal}))

def uniter(NFAs:List[NFA], newLabel:int) -> Tuple[NFA,List[List[int]]]:
    isFirstIteraction:bool = True
    listFinalStates = [] 
    while (len(NFAs) != 1):
        secondOperand = NFAs.pop()
        firstOperand = NFAs.pop()
        if (isFirstIteraction):
            listFinalStates.append(list(secondOperand.finalStates)[0])
            isFirstIteraction = False
        listFinalStates.append(list(firstOperand.finalStates)[0])
        newNFA = union(firstOperand,secondOperand,newLabel)
        NFAs.append(newNFA)
        newLabel +=2
    listFinalStates.reverse()
    return (NFAs.pop(), listFinalStates)


def star(nfa:NFA) -> NFA:
    #add epsilon from final state to initial to the transition list 
    epsilonTransitionsNewFinal = []
    epsilonTransitionsNewFinal.append(list(nfa.initialStates)[0])
    #add epsilon from old final to new final to the transition list
    oldFinalState = list(nfa.finalStates)[0]#it will only have one final state
    newFinalState = oldFinalState+1
    epsilonTransitionsNewFinal.append(newFinalState)
    nfa.transiction[(oldFinalState,"")] = epsilonTransitionsNewFinal
    #remove the old final state from the set of finals
    nfa.finalStates.remove(oldFinalState)
    nfa.finalStates.add(newFinalState)
    #creates a new initial state
    oldInitialState = list(nfa.initialStates)[0]
    newInitialState = (int(newFinalState)+1)
    #epsilon of the newInitital state
    epsilonTransitionsNewInit = [oldInitialState,newFinalState]
    nfa.transiction[newInitialState,""] = epsilonTransitionsNewInit
    #remove the old initial state
    nfa.initialStates.remove(oldInitialState)
    nfa.initialStates.add(newInitialState)
    #add the newInit and the new final to the states
    nfa.setStates.add(newFinalState)
    nfa.setStates.add(newInitialState)
    
    return nfa
