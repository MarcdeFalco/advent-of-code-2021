/* Advent of Code 2021, jour 5.
   Chaque segment est tracé point par point dans un tableau W × W de
   compteurs ; on compte les cases couvertes au moins deux fois. La partie 1
   ignore les diagonales, la partie 2 trace aussi celles de pente ±1. */

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

#define W 1000

int m[W][W];

void swap(int *x, int *y)
{
    int t = *x;
    *x = *y;
    *y = t;
}

int recouvrements(const char *nom, bool diagonales)
{
    FILE *fp = fopen(nom, "r");
    int x1, y1, x2, y2;
    memset(m, 0, sizeof(m));

    while (fscanf(fp, "%d,%d -> %d,%d\n", &x1, &y1, &x2, &y2) == 4)
    {
        if (x1 == x2)
        {
            if (y1 > y2)
                swap(&y1, &y2);
            for (int y = y1; y <= y2; y++)
                m[x1][y]++;
        }
        else if (y1 == y2)
        {
            if (x1 > x2)
                swap(&x1, &x2);
            for (int x = x1; x <= x2; x++)
                m[x][y1]++;
        }
        else if (diagonales)
        {
            float dx = x2 - x1;
            float dy = y2 - y1;
            float coeff = dx / dy;
            if (coeff == -1.0 || coeff == 1.0)
            {
                int c = (int) coeff;
                /* on parcourt le segment de gauche à droite */
                if (x1 > x2)
                {
                    swap(&x1, &x2);
                    swap(&y1, &y2);
                }
                for (int k = 0; k <= x2 - x1; k++)
                    m[x1 + k][y1 + c * k]++;
            }
        }
    }
    fclose(fp);

    int count = 0;
    for (int j = 0; j < W; j++)
        for (int i = 0; i < W; i++)
            if (m[i][j] > 1)
                count++;
    return count;
}

int main(void)
{
    printf("Partie 1 : %d\n", recouvrements("input.txt", false));
    printf("Partie 2 : %d\n", recouvrements("input.txt", true));
    return 0;
}
