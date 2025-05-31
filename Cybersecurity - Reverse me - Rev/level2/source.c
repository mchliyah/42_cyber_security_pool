#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

void ok() {
    printf("Good Jobe.\n");
    exit(0);
}

void no() {
    printf("Nope.\n");
    exit(1);
}

int main(void) {
    unsigned int counter;
    size_t target_len;
    int iVar3;
    bool boolean1;
    char input[24];
    char target[9];
    unsigned int J;
    int i;

    printf("Please enter key: ");
    int ret = scanf("%23s", input);
    if (ret != 1) {
        no();
    }

    if (input[0] != '0' || input[1] != '0') {
        no();
    }

    memset(target, 0, sizeof(target));
    target[0] = 'd';
    J = 2;
    i = 1;

    while (true) {
        target_len = strlen(target);
        counter = J;
        boolean1 = false;

        if (target_len < 8) {
            target_len = strlen(input);
            boolean1 = (counter < target_len);
        }

        if (!boolean1) {
            break;
        }

        char chunk[4] = {input[J], input[J + 1], input[J + 2], '\0'};
        iVar3 = atoi(chunk);
        target[i] = (char)iVar3;
        // printf("Converting '%s' to int: %d\n", chunk, iVar3);

        J += 3;
        i += 1;
    }

    target[i] = '\0';

    iVar3 = strcmp(target, "delabere");

    // ascii 
    // d = 100
    // e = 101
    // l = 108
    // a = 97
    // b = 98
    // e = 101
    // r = 114
    // e = 101
    // target = "delabere"
    if (iVar3 == 0) {
        ok();
    } else {
        no();
    }

    return 0;
}
