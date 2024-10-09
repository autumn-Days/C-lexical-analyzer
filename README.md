# C lexical analyzer

## 1. General description

A lexical analyzer that recognizes the atribution statement of the C/C++ language. It was implemented as project of the "compilers" discipline of the Federal University of Ceará during 2024.2. It was both fun and stressful to implement it, but I could learn a lot with it😅. Here are some of the main features:

- Has the data types `int` and `string`;
- Has the operators `+`, `-`, `*`, `=`, `>`, and `<`;

## 2. General logic

Here are the general steps used to make it come to life:

1. Implementation of a set of regular expressions for each token.
    - All the regular expressions are converted from infix to post-fix notation with the use of the shunting-yard algorithm. Since this algorithm does not have much to do with the lexical analyzer itself, it was choosed to don't include it into the final version.
3. Implementation of an algorithm that takes as input all the regular expressions and return a single NFA
4. Implementation of an algorithm that receives as input a single NFA and returns a equivalent DFA 
5. Implementation of the lexical analyzer itself, which  the DFA for recognizing wheter or not a word is related with a TOKEN.

## 3. Example of possible inputs

|Inputs| Output |
|int a = 0 ;| INT VAR EQ ZERO SEMICOLON |
|in b = 5 + a ;| ERROR |
|string c = “teSte” ;| STRING VAR EQ CONST SEMICOLON |

