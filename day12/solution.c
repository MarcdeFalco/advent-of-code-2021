#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

#define MAX_VTX 20

char vertices[MAX_VTX][100];
int nvertices;
int adj[MAX_VTX][MAX_VTX];

int get_vtx(char *s)
{
    for (int i = 0; i < nvertices; i++)
        if (strncmp(s, vertices[i], 100) == 0)
            return i;
    strcpy(vertices[nvertices], s);
    adj[nvertices][0] = -1;
    return nvertices++;
}

void add_edge(int v1, int v2)
{
    int *a = adj[v1];
    while(*a != -1) a++;
    *(a++) = v2;
    *a = -1;
}

int count[MAX_VTX];

bool small_cave(char *s)
{
    for(int i = 0; i < strlen(s); i++)
    {
        if(!islower(s[i])) return false;
    }
    return true;
}

int visit(int x, bool dbl)
{
    int n_paths = 0;
    int *a = adj[x];
    while(*a != -1)
    {
        int y = *(a++);
        char *v = vertices[y];
        if (strncmp(v, "start", 10) == 0)
            continue;
        if (strncmp(v, "end", 10) == 0)
        {
            n_paths++;
            continue;
        }
        if(small_cave(vertices[y]))
        {
            if (count[y] == 0)
            {
                count[y] = 1;
                n_paths += visit(y, dbl);
                count[y] = 0;
            } else if (count[y] == 1 && !dbl)
                n_paths += visit(y, true);
        } else
            n_paths += visit(y, dbl);
    }

    return n_paths;
}

int main(void)
{
    FILE *fp = fopen("input.txt", "r");
    char line[500];

    while (fgets(line, 500, fp) != NULL)
    {
        int j = 0;
        for (j = 0; j < 500; j++)
            if (line[j] == '-')
                break;
        line[j] = '\0';
        int v1 = get_vtx(line);
        char *l2 = line+j+1;
        l2[strlen(l2)-1] = '\0';
        int v2 = get_vtx(l2);
        add_edge(v1, v2);
        add_edge(v2, v1);
    }

    int start = get_vtx("start");
    memset(count, 0, sizeof(int) * nvertices);
    printf("Part 1 : %d\n", visit(start, true));
    memset(count, 0, sizeof(int) * nvertices);
    printf("Part 2 : %d\n", visit(start, false));
}
