#include <stdio.h>
#include <stdlib.h>

#define W 1000

void swap(int *x, int *y)
{
    int t = *x;
    *x = *y;
    *y = t;
}

int main(void)
{
    FILE *fp = fopen("input.txt", "r");
    int x1, y1, x2, y2;
    int m[W][W] = {};

    while(fscanf(fp, "%d,%d -> %d,%d\n", &x1, &y1, &x2, &y2) != EOF)
    {
        if (x1 == x2)
        {
            if (y1 > y2)
                swap(&y1, &y2);
            for(int y = y1; y <= y2; y++)
                m[x1][y]++;
        }
        else if (y1 == y2)
        {
            if (x1 > x2)
                swap(&x1, &x2);
            for(int x = x1; x <= x2; x++)
                m[x][y1]++;
        }
        else
        {
            float dx = x2 - x1;
            float dy = y2 - y1;
            float coeff = dx / dy;
            if (coeff == -1.0 || coeff == 1.0)
            {
                int c = (int) coeff;
                if (x1 > x2)
                {
                    swap(&x1, &x2);
                    swap(&y1, &y2);
                }
                for (int k = 0; k <= x2-x1; k++)
                    m[x1+k][y1+c*k]++;
            }
        }
    }

    fclose(fp);

    int count = 0;
    for(int j = 0; j < W; j++)
        for(int i = 0; i < W; i++)
            if (m[i][j] > 1)
                count++;

    printf("%d\n", count);
}
