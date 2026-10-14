/* Advent of Code 2021, jour 2.
   Simulation directe : on relit les commandes et on met à jour la position
   et la profondeur (partie 1), ou la position, la profondeur et la visée
   (partie 2). */

#include <stdio.h>

#define BUFFER_LEN 500

int partie1(FILE *fp)
{
    char buf[BUFFER_LEN];
    int depth = 0;
    int pos = 0;
    while (fgets(buf, BUFFER_LEN, fp) != NULL)
    {
        char dir[10];
        int amount;
        sscanf(buf, "%9s %d", dir, &amount);

        if (dir[0] == 'f')
            pos += amount;
        if (dir[0] == 'u')
            depth -= amount;
        if (dir[0] == 'd')
            depth += amount;
    }
    return depth * pos;
}

int partie2(FILE *fp)
{
    char buf[BUFFER_LEN];
    int depth = 0;
    int pos = 0;
    int aim = 0;
    while (fgets(buf, BUFFER_LEN, fp) != NULL)
    {
        char dir[10];
        int amount;
        sscanf(buf, "%9s %d", dir, &amount);

        if (dir[0] == 'f')
        {
            pos += amount;
            depth += aim * amount;
        }
        if (dir[0] == 'u')
            aim -= amount;
        if (dir[0] == 'd')
            aim += amount;
    }
    return depth * pos;
}

int main(void)
{
    FILE *fp = fopen("input.txt", "r");
    printf("Partie 1 : %d\n", partie1(fp));
    fclose(fp);

    fp = fopen("input.txt", "r");
    printf("Partie 2 : %d\n", partie2(fp));
    fclose(fp);
    return 0;
}
