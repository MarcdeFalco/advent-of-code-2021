/* Advent of Code 2021, jour 1.
   Partie 1 : on compte les mesures plus grandes que la précédente.
   Partie 2 : même chose sur une fenêtre glissante de trois mesures, dont la
   somme est mise à jour en O(1) à chaque pas. */

#include <stdio.h>
#include <stdlib.h>

#define BUFFER_LEN 500
#define MAX_DEPTHS 2000

int partie1(int depths[], int ndepths)
{
    int increased = 0;
    for (int i = 1; i < ndepths; i++)
    {
        if (depths[i] > depths[i - 1])
            increased++;
    }
    return increased;
}

int partie2(int depths[], int ndepths)
{
    int increased = 0;
    int window = depths[0] + depths[1] + depths[2];
    for (int i = 3; i < ndepths; i++)
    {
        int new_window = window - depths[i - 3] + depths[i];
        if (new_window > window)
            increased++;
        window = new_window;
    }
    return increased;
}

int main(void)
{
    char buffer[BUFFER_LEN];
    FILE *fp = fopen("input.txt", "r");
    int depths[MAX_DEPTHS];
    int ndepths = 0;

    while (fgets(buffer, BUFFER_LEN, fp) != NULL)
    {
        depths[ndepths] = atoi(buffer);
        ndepths++;
    }
    fclose(fp);

    printf("Partie 1 : %d\n", partie1(depths, ndepths));
    printf("Partie 2 : %d\n", partie2(depths, ndepths));
    return 0;
}
