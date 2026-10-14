/* Advent of Code 2021, jour 3.
   Partie 1 : comptage des '1' par colonne ; le mot des bits majoritaires
   donne m, celui des minoritaires est son complément 2^12 - 1 - m.
   Partie 2 : filtrage par bit successif, un tableau de booléens sel[]
   indiquant les mots encore candidats.
   L'entrée doit contenir exactement NVALUES mots de VALLEN bits. */

#include <stdio.h>
#include <stdbool.h>

#define NVALUES 1000
#define VALLEN 12

/* Indice du mot restant après filtrage selon le bit majoritaire (most)
   ou minoritaire (!most). */
int search(char values[NVALUES][VALLEN + 1], bool most)
{
    bool sel[NVALUES];

    for (int i = 0; i < NVALUES; i++)
        sel[i] = true;

    for (int i = 0; i <= VALLEN; i++)
    {
        int nsel = 0;
        for (int j = 0; j < NVALUES; j++)
            if (sel[j])
                nsel++;

        if (nsel == 1)
        {
            for (int j = 0; j < NVALUES; j++)
                if (sel[j])
                    return j;
        }

        int n1 = 0;
        for (int j = 0; j < NVALUES; j++)
        {
            if (sel[j] && values[j][i] == '1')
                n1++;
        }

        /* bit à garder : en cas d'égalité, '1' pour most, '0' sinon */
        char tgt = most ? (2 * n1 >= nsel ? '1' : '0')
                        : (2 * n1 < nsel ? '1' : '0');
        for (int j = 0; j < NVALUES; j++)
            sel[j] = sel[j] && values[j][i] == tgt;
    }

    return -1;
}

int value_to_bin(char val[VALLEN + 1])
{
    int n = 0;
    for (int i = 0; i < VALLEN; i++)
        n = 2 * n + (val[i] == '1' ? 1 : 0);
    return n;
}

int partie1(char values[NVALUES][VALLEN + 1])
{
    int most = 0;
    for (int i = 0; i < VALLEN; i++)
    {
        int c1 = 0;
        for (int j = 0; j < NVALUES; j++)
            if (values[j][i] == '1')
                c1++;
        most = 2 * most + (c1 > NVALUES / 2 ? 1 : 0);
    }
    int least = (1 << VALLEN) - most - 1;
    return most * least;
}

int partie2(char values[NVALUES][VALLEN + 1])
{
    int oxygen = value_to_bin(values[search(values, true)]);
    int co2 = value_to_bin(values[search(values, false)]);
    return oxygen * co2;
}

int main(void)
{
    FILE *fp = fopen("input.txt", "r");
    char values[NVALUES][VALLEN + 1];
    for (int i = 0; i < NVALUES; i++)
        fscanf(fp, "%12s", values[i]);
    fclose(fp);

    printf("Partie 1 : %d\n", partie1(values));
    printf("Partie 2 : %d\n", partie2(values));
    return 0;
}
