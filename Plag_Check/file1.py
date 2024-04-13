
%{
	/* header files */
	#include<stdio.h>
	#include<stdlib.h>
	#include<string.h>

	/* definitions of manifest constants*/
	#define _PROGRAM	1
	#define _VAR		2
	#define _BEGIN		3
	#define _END		4
	#define _END_DOT	5
	#define _INTEGER	6
	#define _FOR		7
	#define _READ		8
	#define _WRITE		9
	#define _TO		10
	#define _DO		11
	#define _SEMICOLON	12
	#define _COLON		13
	#define _COMMA		14
	#define _ASSIGN		15
	#define _ADD		16
	#define _SUB		17
	#define _MUL		18
	#define _DIV		19
	#define _OPEN_BRACE	20
	#define _CLOSE_BRACE	21
	#define _ID		22
	#define _INT		23

	/* hashtable implementation */
	#define SIZE 20

	typedef struct symbol {
		char* specifier;
		char type;
		struct symbol* next;
	} symbol;

	symbol* SYMTAB[SIZE];

	int hash_function(char* specifier) {
		int len = strlen(specifier);
		// simple hash function
		int hash = 0;
		for(int i = 0; i < len; i++) 
			hash += (int) specifier[i];
		return hash % SIZE;
	}

	void init() {
		// initialize all bucket to null
		for(int i = 0; i < SIZE; i++) 
			SYMTAB[i] = NULL;
	}

	symbol* search(char* specifier) {
		// compute the hash function for bucket index
		int i = hash_function(specifier);

		// search the linked list associated with the bucket
		symbol* temp = SYMTAB[i];
		while(temp != NULL && strcmp(temp -> specifier, specifier))
			temp = temp -> next;

		return temp;
	}

	symbol* insert(char* specifier, char type) {
		// compute the hash function for bucket index
		int i = hash_function(specifier);

		// create the new symbol
		symbol* new_symbol = (symbol *)malloc(sizeof(symbol));
		new_symbol -> specifier = (char *)strdup(specifier);
		new_symbol -> type = type;

		// insert it at the beginning of the bucket linked list
		new_symbol -> next = SYMTAB[i];
		SYMTAB[i] = new_symbol;

		return new_symbol;
	}

	void print() {
		// pretty printing of hash table
		printf("-------------------------------------\n");
		printf("SYMTAB\n");
		for(int i = 0; i < SIZE; i++) {
			printf("bucket [%d]: ", i);
			symbol* temp = SYMTAB[i];
			while(temp != NULL) {
				printf("%c%s -> ", temp -> type, temp -> specifier);
				temp = temp -> next;
			}
			printf("NULL\n");
		}
		printf("-------------------------------------\n");
	}

	


	/* declaration of useful functions and variables */
	void* yylval;
	void* install_id();
	void* install_num();
	int line = 0;
%}
