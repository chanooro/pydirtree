# pydirtree

Albero directory CLI in Python: output testo/Markdown/JSON, filtri e profondità.

## Installazione
```bash
pip install -e .
```

## Uso
```bash
# Stampa l’albero completo della cartella corrente
pydirtree

# Solo cartelle fino a profondità 2
pydirtree -d 2 --only-dirs

# Includi file nascosti e dimensioni
pydirtree --hidden --size

# Esporta in Markdown
pydirtree --format md -o TREE.md
```

#### Formati supportati
- text: output stile tree
- md: blocco Markdown
- json: struttura JSON navigabile

#### Opzioni principali
- -d, --max-depth: profondità massima
- --hidden: includi file nascosti
- --ignore PATTERN ...: ignora pattern - (glob)
- --only-dirs: mostra solo directory
- --size: mostra dimensioni file
