https://excalidraw.com/#json=TWjiIFeSkqoJ2u2RKpfwh,5FK50C3MYXvZ8oNvwIkyDw

Functions fo one thing

Typing always

Composition over inheritance 


A tokenizer just  such as words. Tokenizing into letters, syllables, sentences etc. is also possible.

A lexer or tokenizer splits text into smaller units lexem or token. It attachs extra information to each token. If we tokenize into words, a lexer would attach tags like number, word, punctuation etc.

A parser uses the output of a lexer and constucts a parse tree.

Create tests implementing the real functions from official libs (matlib, tensorflow etc.), comparing to be sure of result.


[craftinginterpreters](https://craftinginterpreters.com/contents.html)

tree-walk-interpreters


[improve error handling](https://craftinginterpreters.com/scanning.html#error-handling)

Adding EOF token ?

[Order_of_operations](https://en.wikipedia.org/wiki/Order_of_operations#Mnemonics)
"Please Excuse My Dear Aunt Sally"



Our Context-Free Grammar:

literal: Rational numbers | Complex numbers

variable: STRING

yyy : literal | variable
functions : STRING"(" ")"

xxx : yyy | functions

Polynomial

matrices: "[" xxx "]"
functions(var)

expression : xxx | Polynomial 

assignment : variable | functions "=" 
()
?

operators : Exponents > MulDiv > AddSub

expression : "+" | "−" 

Parentheses : "(" | ")"

Exponents : "^"

MulDiv : "∗" | "/" | "**"

AddSub : "+" | "−"

binary : expression operator expression ;

grouping : "(" yyy ")"