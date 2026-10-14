/* Advent of Code 2021, jour 12.
   Les sommets sont numérotés au fil de la lecture (get_vtx) et les listes
   d'adjacence stockées dans adj, terminées par -1. Retour sur trace :
   count[y] marque les petites cavernes du chemin courant (mis à 1 avant
   l'appel récursif, remis à 0 après) et dbl indique si la seconde visite
   permise (partie 2) est déjà utilisée. */

#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

#define MAX_VTX 20

char vertices[MAX_VTX][100];
int nvertices;
int adj[MAX_VTX][MAX_VTX];

/* numéro du sommet de nom s, créé s'il n'existe pas encore */
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
    while (*a != -1)
        a++;
    *(a++) = v2;
    *a = -1;
}

/* count[y] = 1 si la petite caverne y est sur le chemin courant */
int count[MAX_VTX];

bool small_cave(char *s)
{
    for (size_t i = 0; i < strlen(s); i++)
    {
        if (!islower(s[i]))
            return false;
    }
    return true;
}

/* nombre de chemins de x à "end" */
int visit(int x, bool dbl)
{
    int n_paths = 0;
    int *a = adj[x];
    while (*a != -1)
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
        if (small_cave(vertices[y]))
        {
            if (count[y] == 0)
            {
                count[y] = 1;
                n_paths += visit(y, dbl);
                count[y] = 0;
            }
            else if (count[y] == 1 && !dbl)
                n_paths += visit(y, true);
        }
        else
            n_paths += visit(y, dbl);
    }

    return n_paths;
}

void lire_graphe(const char *nom)
{
    FILE *fp = fopen(nom, "r");
    char line[500];

    while (fgets(line, 500, fp) != NULL)
    {
        /* on coupe la ligne au tiret */
        int j = 0;
        for (j = 0; j < 500; j++)
            if (line[j] == '-')
                break;
        line[j] = '\0';
        int v1 = get_vtx(line);
        char *l2 = line + j + 1;
        l2[strlen(l2) - 1] = '\0'; /* retire le '\n' */
        int v2 = get_vtx(l2);
        add_edge(v1, v2);
        add_edge(v2, v1);
    }
    fclose(fp);
}

int partie1(void)
{
    memset(count, 0, sizeof(int) * nvertices);
    return visit(get_vtx("start"), true);
}

int partie2(void)
{
    memset(count, 0, sizeof(int) * nvertices);
    return visit(get_vtx("start"), false);
}

int main(void)
{
    lire_graphe("input.txt");
    printf("Partie 1 : %d\n", partie1());
    printf("Partie 2 : %d\n", partie2());
    return 0;
}
