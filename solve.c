#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

bool is_valid(int **board, int boardSize, int row, int col, int number) {
    for (int i = 0; i < boardSize; i++) {
        if (board[row][i] == number || board[i][col] == number) {
            return false;
        }
    }
    int row_index = row - row % 3;
    int col_index = col - col % 3;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            if (board[i + row_index][j + col_index] == number) {
                return false;
            }
        }
    }
    return true;
}
bool solve(int **board, int boardSize, int row, int col) {
    if (row == boardSize - 1 && col == boardSize) {
        return true;
    } 
    if (col == boardSize) {
        row++;
        col = 0;
    }
    if (board[row][col] != 0) {
        return solve(board, boardSize, row, col + 1);
    }
    for (int i = 1; i <= boardSize; i++) {
        if (is_valid(board, boardSize, row, col, i)) {
            board[row][col] = i;
            if (solve(board, boardSize, row, col + 1)) {
                return true;
            }
            board[row][col] = 0;
        }
    }
    return false;
}
void print_board(int** board, int boardSize) {
    for (int i = 0; i < boardSize; i++) {
        for (int j = 0; j < boardSize; j++) {
            printf("%i ", board[i][j]);
        }
        printf("\n");
    }
}

void parse(int **board, int size) {
    FILE *file = fopen("board.txt", "r");
    if (file == NULL) {
        printf("not a valid file");
        exit(1);
    }

    int row = 0;
    char buffer[256];
    while (fgets(buffer, sizeof(buffer), file) != NULL) {
        if (strlen(buffer) != 10) {
            printf("Each row must have 9 numbers");
            exit(2);
        }
        for (int i = 0; i < size; i++) {
            int ascVal = buffer[i] - 48;
            board[row][i] = ascVal;
        }
        row++;
    }
    fclose(file);
}
int **execute() {
    int rows = 9;
    int cols = 9;
    int **board = (int **)malloc(rows * sizeof(int *));

    for (int i = 0; i < rows; i++) {
        board[i] = (int *)malloc(cols * sizeof(int));

        if (board[i] == NULL) {
            fprintf(stderr, "Memory allocation failed\n");
            exit(0);
        }
    }

    parse(board, 9);
    print_board(board, 9);
    printf("\n\n");
    solve(board, 9, 0, 0);
    print_board(board, 9);
    return board;
}

int free_board(int **board, int rows) {
    for (int i = 0; i < rows; i++) {
        free(board[i]);
    }
    free(board);

    return 0;
}
