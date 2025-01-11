
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

#define LEXBUF_SIZE 100
#define NUM 1
#define ID 2
#define NONE 0

// Example global variables
int lineno = 1;
int tokenval = NONE;
char lexbuf[LEXBUF_SIZE]; // Global lexbuf for keeping identifiers

// Token descriptions
const char *get_token_description(int token) {
    switch (token) {
        case NUM:
            return "Number";
        case ID:
            return "Identifier";
        case '=':
            return "Equal To";
        case '*':
            return "Multiplication";
        case '+':
            return "Plus";
        case '(':
            return "Left Parenthesis";
        case ')':
            return "Right Parenthesis";
        default:
            return "Special Symbol";
    }
}

// Example helper functions (you should implement these)
int lookup(const char *lexbuf) {
    // Dummy implementation; replace with actual lookup logic
    return 0; // Return 0 if not found
}

int insert(const char *lexbuf, int type) {
    // Dummy implementation; replace with actual insertion logic
    return 1; // Return a dummy token identifier
}

// Lexical analyzer function
int lexan(FILE *input) {
    int i = 0;
    char c;

    // Read the next character from the input
    c = fgetc(input);

    // Handle end of file
    if (c == EOF) {
        return EOF;
    }

    // Skip whitespace
    if (isspace(c)) {
        if (c == '\n') {
            lineno++;
        }
        return lexan(input);
    }

    // Handle digits
    if (isdigit(c)) {
        tokenval = 0;
        do {
            tokenval = tokenval * 10 + (c - '0');
            c = fgetc(input);
        } while (isdigit(c));
        ungetc(c, input); // Put back the last character
        snprintf(lexbuf, sizeof(lexbuf), "%d", tokenval);
        return NUM;
    }

    // Handle identifiers
    if (isalpha(c)) {
        lexbuf[i++] = c;
        while (isalnum(c = fgetc(input)) && i < LEXBUF_SIZE - 1) {
            lexbuf[i++] = c;
        }
        lexbuf[i] = '\0'; // Null-terminate the lexbuf
        ungetc(c, input); // Put back the last character

        tokenval = 1; // Dummy value for identifier
        return ID;
    }

    // Handle other characters
    lexbuf[0] = c;
    lexbuf[1] = '\0';
    tokenval = 0;
 return (int)c; // Return ASCII value of the character
}

// Main function to process input and print output
int main(void) {
    FILE *inputFile;
    FILE *outputFile;
    char inputFilename[100];
    char outputFilename[100] = "output.txt"; // Default output filename
    int token;

    // Prompt user for input filename
    printf("Enter the name of the input file: ");
    scanf("%99s", inputFilename);

    // Open the input file
    inputFile = fopen(inputFilename, "r");
    if (inputFile == NULL) {
        perror("Error opening input file");
        return 1;
    }

    // Open the output file
    outputFile = fopen(outputFilename, "w");
    if (outputFile == NULL) {
        perror("Error opening output file");
        fclose(inputFile);
        return 1;
    }

    // Process the input file and write output to the output file
    while ((token = lexan(inputFile)) != EOF) {
        const char *description = get_token_description(token);
        if (token == NUM || token == ID) {
            fprintf(outputFile, "Line %d, Token: %s, Token Value: %d, Description: %s\n",
                    lineno, lexbuf, tokenval, description);
        } else {
            fprintf(outputFile, "Line %d, Token: %s, Token Value: %d, Description: %s\n",
                    lineno, lexbuf, tokenval, description);
        }
    }

    // Clean up
    fclose(inputFile);
    fclose(outputFile);
     printf("Processing complete. Output written to %s\n", outputFilename);

    return 0;
}

