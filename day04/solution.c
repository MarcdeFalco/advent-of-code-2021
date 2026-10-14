/* Advent of Code 2021, jour 4.
   Simulation du bingo : un numéro rayé est remplacé par -1 et, après chaque
   rayure, on teste les lignes et les colonnes. On retient la première et la
   dernière grille gagnante, avec le numéro qui les a fait gagner. */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>

#define BUFFER_LEN 1000
#define MAX_NUM 100
#define MAX_BOARDS 100

void strike(int board[5][5], int n)
{
    for (int i = 0; i < 5; i++)
        for (int j = 0; j < 5; j++)
            if (board[i][j] == n)
                board[i][j] = -1;
}

bool won(int board[5][5])
{
    for (int i = 0; i < 5; i++)
    {
        bool row = true;
        bool col = true;
        for (int j = 0; j < 5; j++)
        {
            row &= board[i][j] < 0;
            col &= board[j][i] < 0;
        }
        if (row || col)
            return true;
    }
    return false;
}

int score(int board[5][5], int trigger)
{
    int s = 0;
    for (int i = 0; i < 5; i++)
        for (int j = 0; j < 5; j++)
            if (board[i][j] >= 0)
                s += board[i][j];
    return s * trigger;
}

int numbers[MAX_NUM];
int nnumbers = 0;
int boards[MAX_BOARDS][5][5];
int nboards = 0;

void lire_entree(const char *nom)
{
    FILE *fp = fopen(nom, "r");
    char buf[BUFFER_LEN];

    fgets(buf, BUFFER_LEN, fp);
    char *p = strtok(buf, ",");
    while (p != NULL)
    {
        numbers[nnumbers++] = atoi(p);
        p = strtok(NULL, ",");
    }

    /* chaque grille est précédée d'une ligne vide */
    while (fgets(buf, BUFFER_LEN, fp) != NULL)
    {
        for (int i = 0; i < 5; i++)
        {
            fgets(buf, BUFFER_LEN, fp);
            char *q = strtok(buf, " ");
            int j = 0;
            while (q != NULL)
            {
                if (q[0] != '\n')
                    boards[nboards][i][j++] = atoi(q);
                q = strtok(NULL, " ");
            }
        }
        nboards++;
    }
    fclose(fp);
}

int main(void)
{
    lire_entree("input.txt");

    int first = -1;
    int first_trigger = -1;
    int last = -1;
    int last_trigger = -1;

    for (int i = 0; i < nnumbers; i++)
    {
        int n = numbers[i];
        for (int j = 0; j < nboards; j++)
        {
            if (!won(boards[j]))
            {
                strike(boards[j], n);
                if (won(boards[j]))
                {
                    if (first == -1)
                    {
                        first = j;
                        first_trigger = n;
                    }
                    last = j;
                    last_trigger = n;
                }
            }
        }
    }

    printf("Partie 1 : %d\n", score(boards[first], first_trigger));
    printf("Partie 2 : %d\n", score(boards[last], last_trigger));
    return 0;
}
