#include <stdio.h>
#include <string.h>

int main() {
    char expected_key[] = "__stack_check";
    char user_input[32] = {0};

    printf("Please enter key: ");
    
    scanf("%31s", user_input);
    
    if (strcmp(user_input, expected_key) == 0) {
        printf("Good job!\n");
    } else {
        printf("Nope!\n");
    }

    return 0;
}