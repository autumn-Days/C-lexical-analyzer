# -*- coding: utf-8 -*-

from er2nfa import *
from NFA import *

def read_er() -> Tuple[List[str],List[str]]:
    return (list(TOKENS.keys())),list(TOKENS.values())


def ers_2_nfas(res:List[str]) -> List[NFA]:
        thompsonConstructor(res)

def isFunnyToken(char):
    """A funny token is a token that can be next to
    another token without the need of spaces
    """
    return ((char == '=') or (char == '+') or (char == '-') or (char == "*") or (char == ";") or (char == "<") or char == (">"))

def parityQuotes(amountOfQuotes):
    """
    if it returns 1 you are inside a string
    if it returns 0 you are not inside a string
    """
    return amountOfQuotes%2

def prepareParsing(statement:str) -> str:
    spacelessStatement = ""
    isConst = 0
    quoteCounter = 0
    while statement != "":
        char = statement[0]
        if char == '"':
            quoteCounter +=1
            isConst = parityQuotes(quoteCounter) 
        if (isConst):
            spacelessStatement += char
        else:
            if (char != " "):
                #we are not inside a string and we are reading a funny token
                if isFunnyToken(char):
                    # We check a lot because of cases like these: @+=@ @+++++==><@
                    isPredecessorFunny = None
                    try :
                        isPredecessorFunny = isFunnyToken(spacelessStatement[-1])
                    except IndexError :
                        spacelessStatement += "@"
                        spacelessStatement += char
                        spacelessStatement = spacelessStatement[1:]
                        continue
                    if (isPredecessorFunny):
                        spacelessStatement += char
                    else:
                        spacelessStatement += "@"
                        spacelessStatement += char   
                else:
                    try :
                        if (isFunnyToken(spacelessStatement[-1])):
                            spacelessStatement += "@"
                    except IndexError:
                        spacelessStatement += char
                        statement = statement[1:]
                        continue
                    spacelessStatement += char
            else:
                #if the string is empty, we get InderError
                try :
                    if spacelessStatement[-1] != "|" :
                        spacelessStatement+= "|"
                except IndexError:
                        statement = statement[1:]
                        continue
        statement = statement[1:]
    return spacelessStatement

def miniParser(statement) -> List[str]:
    spacelessStatement = prepareParsing(statement)
    tokens = []
    lexime = ""
    while spacelessStatement != "":
        char = spacelessStatement[0]
        if char != '|' and char != '@':
            lexime += char
        else :
            if (lexime != '') :
                tokens.append(lexime)
                lexime = ""
                #I need to continue, otherwise it will delete my divisor for funny
                continue
        spacelessStatement = spacelessStatement[1:]
    if (lexime != ''):
        tokens.append(lexime)
    return tokens


def loadSourceCode(file) -> List[List[str]]:
    statements:List[List[str]] = []
    with open (file,'r') as f:
        lines = f.readlines()
        amountLines = len(lines)
        currentLine = 1
        for line in lines :
            #This condition is necessary for taking the
            #break line out
            if currentLine != amountLines:
                statements.append(line[:-1])
                currentLine+=1
            else:
                statements.append(line)
    return statements