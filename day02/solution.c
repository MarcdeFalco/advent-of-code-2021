#include <stdio.h>
#include <string.h>

#define BUFFER_LEN 500

int main(void)
{
    char buf[BUFFER_LEN];
    FILE *fp = fopen("input.txt", "r");

    int depth = 0;
    int pos = 0;
    while (fgets(buf, BUFFER_LEN, fp) != NULL)
    {
        char dir[10];
        int amount;
        sscanf(buf, "%s %d\n", dir, &amount);

        if (dir[0] == 'f')
            pos += amount;
        if (dir[0] == 'u')
            depth -= amount;
        if (dir[0] == 'd')
            depth += amount;
    }
    printf("Part 1 : %d\n", depth * pos);

    fclose(fp);

    fp = fopen("input.txt", "r");
    depth = 0;
    pos = 0;
    int aim = 0;
    while (fgets(buf, BUFFER_LEN, fp) != NULL)
    {
        char dir[10];
        int amount;
        sscanf(buf, "%s %d\n", dir, &amount);

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
    printf("Part 2 : %d\n", depth * pos);

    fclose(fp);
}
