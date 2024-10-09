# -*- coding: utf-8 -*-

from typing import Set, Tuple, FrozenSet

class DFA:
    def __init__(self,setStates, alphabet, transiction, initialState:int, finalStates:Set[int]):
        self.setStates = setStates
        self.alphabet = alphabet
        self.transiction = transiction
        self.initialState = initialState
        self.finalStates = finalStates
    
    def accepts(self, word:str) -> Tuple[bool,FrozenSet[int]]:
        state = self.initialState
        while word != "":
            try :
                state = self.transiction[(state, word[0])]
            except KeyError :
                state = ""
            word = word[1:]
        return ((state in self.finalStates),state)
    