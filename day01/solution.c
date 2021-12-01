#include <stdio.h>
#include <stdlib.h>

#define BUFFER_LEN 500
#define MAX_DEPTHS 2000

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

    int increased = 0;
    for (int i = 1; i < ndepths; i++)
    {
        if (depths[i] > depths[i-1])
            increased++;
    }
    printf("Part 1 : %d\n", increased);

    increased = 0;
    int window = depths[0] + depths[1] + depths[2];
    for (int i = 3; i < ndepths; i++)
    {
        int new_window = window - depths[i-3] + depths[i];
        if (new_window > window)
            increased++;
        window = new_window;
    }
    printf("Part 2 : %d\n", increased);
}
