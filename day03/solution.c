#include <stdio.h>
#include <stdbool.h>

#define NVALUES 1000
#define VALLEN 12

int search(char values[NVALUES][VALLEN+1], bool most)
{
    bool sel[NVALUES];
    
    for(int i = 0; i < NVALUES; i++)
        sel[i] = true;

    for(int i = 0; i < VALLEN; i++)
    {
        int nsel = 0;

        for(int j = 0; j < NVALUES; j++)
            if(sel[j])
                nsel++;

        printf("%d\n", nsel);

        if (nsel == 1)
            for(int j = 0; j < NVALUES; j++)
                if(sel[j])
                    return j;

        int n1 = 0;

        for(int j = 0; j < NVALUES; j++)
        {
            if(sel[j] && values[j][i] == '1')
                n1++;
        }
        for(int j = 0; j < NVALUES; j++)
        {
            if (most)
                sel[j] = sel[j] && values[j][i] == (n1 >= nsel/2 ? '1' : '0');
            else
                sel[j] = sel[j] && values[j][i] == (n1 < nsel/2 ? '1' : '0');
        }
    }

    return -1;
}

int main(void)
{
    FILE *fp = fopen("input.txt", "r");
    char values[NVALUES][VALLEN+1];
    for (int i = 0; i < NVALUES; i++)
        fscanf(fp, "%s\n", values[i]);
   
    int most = 0;
    for (int i = 0; i < VALLEN; i++)
    {
        int c1 = 0;
        for(int j = 0; j < NVALUES; j++)
            if (values[j][i] == '1')
                c1++;
        most = 2 * most + (c1>NVALUES/2 ? 1 : 0);
    }
    int least = (1 << 12) - most - 1;
    printf("Part 1 : %d\n", most * least);

    int i = search(values, true);
    printf("%d %s\n", i, values[i]);
    i = search(values, false);
    printf("%d %s\n", i, values[i]);
}
