#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

void fail() {
    printf("Nope.\n");
    exit(1);
}

void success() {
    printf("Good job!\n");
    exit(0);
}

int main() {

    char input[31];
    char buffer[9];
    int input_jump;
    int counter;
    bool breaking;

    memset(buffer, 0, sizeof(buffer));
    buffer[0] = '*';

    printf("Please enter key: ");
    
    if (scanf("%30s", input) != 1) {
        fail();
    }
    if (input[0] != '4') {
        fail();
    }
    if (input[1] != '2') {
        fail();
    }

    input_jump = 2; 
    counter = 1; 
    while (true) {
        size_t buf_len = strlen(buffer);
        breaking = false;

        if (buf_len < 8) {
            size_t input_len = strlen(input);
            breaking = (input_jump < input_len);
        }

        if (!breaking) break;

        char chunk[4] = {
            input[input_jump],
            input[input_jump + 1],
            input[input_jump + 2],
            '\0'
        };

        int val = atoi(chunk);
        buffer[counter] = (char)val;

        input_jump += 3;
        counter += 1;
    }
    bool all_asterisks = true;
    for (int i = 0; i < 8; i++) {
        if (buffer[i] != '*') {
            all_asterisks = false;
            break;
        }
    }
    if (all_asterisks) {
        success();
    } else {
        fail();
    }
    return 0;
}