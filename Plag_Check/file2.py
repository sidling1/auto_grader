%{
    /* including the relevant header files */
    #include <stdio.h>
    #include <string.h>
    #include <stdlib.h>
 
    /* We define the size of table */
    #define SIZE 20
 
    /* we are defining the manifest constants below */
    #define _PROGRAM    1
    #define _VAR        2
    #define _BEGIN      3
    #define _END        4
    #define _END_DOT    5
    #define _INTEGER    6
    #define _FOR        7
    #define _READ       8
    #define _WRITE      9
    #define _TO         10
    #define _DO         11
    #define _SEMICOLON  12
    #define _COLON      13
    #define _COMMA      14
    #define _ASSIGN     15
    #define _ADD        16
    #define _SUB        17
    #define _MUL        18
    #define _DIV        19
    #define _OPEN_BRACE 20
    #define _CLOSE_BRACE    21
    #define _ID         22
    #define _INT        23
 
    /* Below is the implementation of the hashtable */
 
    /* The struct symbol contains the specifier string, type of symbol, and a pointer to the next symbol in the hash */
 
    typedef struct symbol {
        char* specifier;
        char type;
        struct symbol* next;
    } symbol;
 
    /* We will define a symbol table by creating an array of pointers to symbols */
    /* This will behave like an array of linked lists and is a hashtable */
    /* One linked list contains one hashed position */
 
    symbol* SYMTAB[SIZE];
 
    /* The below function is a simple hash function which hashes to the sum of the specifier value modulo SIZE */
 
    int hash_function(char* specifier) {
        int length = strlen(specifier);
        int sum = 0;
 
        for(int itr = 0; itr < length; itr++) {
            sum += (int) specifier[itr];
        }
 
        return sum % SIZE;
    }
 
    /* This function initializes the hashtable with all pointers pointing to null, indicating all linked lists are empty */
 
    void init() {
        for(int i = 0; i < SIZE; i++) {
            SYMTAB[i] = NULL;
        }
    }
 
   
 
    /* yylval is used to pass information about the identifiers and integers recognized by the lexer to the parser. When an identifier or integer token is recognized, yylval is set to hold a pointer to a structure containing the necessary information (such as the identifier string or integer value), and the corresponding token ID is returned by yylex(). */
    void* yylval;
 
    void* install_num();
 
    void* install_id();
 
    int line = 0;
%}
 
/* This section of your code defines the rules for matching tokens in your lexer. Here's a breakdown of what each part does: */
delim       [ \t\n]
letter      [A-Za-z]
digit       [0-9]
id      {letter}({letter}|{digit})*
int     {digit}+
er     {digit}({letter}|{digit})*
 
%%
 
\n      { line++; }
[ \t]       { }
PROGRAM     { return _PROGRAM; }
VAR     { return _VAR; }
BEGIN       { return _BEGIN; }
END     { return _END; }
END\.       { return _END_DOT; }
INTEGER     { return _INTEGER; }
FOR     { return _FOR; }
READ        { return _READ; }
WRITE       { return _WRITE; }
TO      { return _TO; }
DO      { return _DO; }
\;      { return _SEMICOLON; }
\:      { return _COLON; }
\,      { return _COMMA; }
\:\=       { return _ASSIGN; }
\+      { return _ADD; }
\-      { return _SUB; }
\*      { return _MUL; }
DIV     { return _DIV; }
\(      { return _OPEN_BRACE; }
\)      { return _CLOSE_BRACE; }
 
{id}        { yylval = (void*)install_id(); return _ID; }
{int}       { yylval = (void*)install_num(); return _INT; }
{er}    {
         fprintf(stderr, "Error: Unexpected character: token not found '%c'\n", yytext[0]);
         exit(1);      
       }
.    {
         fprintf(stderr, "Error: Unexpected character: token not found '%c'\n", yytext[0]);
         exit(1);      
       }
 
%%
 
/* we define the useful function here */
/* The function install_id searches yytext and if it doesn't find it then inserts with type being '^' */
 
void* install_id() {
    symbol* sym = search(yytext);
 
    if(sym == NULL) {
        sym = insert(yytext, '^');
    }
 
    return sym;
}
 
void* install_num() {
    symbol* sym = search(yytext);
 
    if(sym == NULL) {
        sym = insert(yytext, '#');
    }
 
    return sym;
}
 
int main() {
    init();
    int token;
    int prev_line = 0;
 
    token = yylex();
 
    while(token) {
        if(line != 0) {
            if(line == prev_line) {
                printf("%10c", ' ');
            }
            else {
                printf("%10d", line);
            }
        }
        else {
            line++;
            printf("%10d", line);
        }
 
        symbol* sym = NULL;
 
        if(token == 22 || token == 23) {
            sym = (symbol *)yylval;
        }
 
        if(sym == NULL) {
            printf("%10d \n", token);
        }
        else {
            printf("%10d %10c%s\n", token, sym -> type, sym -> specifier);
        }
 
        prev_line = line;
        token = yylex();
    }
 
    print();
    return 0;
}