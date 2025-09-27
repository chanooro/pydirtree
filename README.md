# pydirtree

🇮🇹 Leggi in Italiano | [🇬🇧 Read in English](README_en.md)

Albero directory CLI in Python: output testo/Markdown/JSON, filtri e profondità.

## Installazione
```bash
pip install -e .
```

### Uso base
```bash
# Stampa l’albero completo della cartella corrente
pydirtree
```

## Uso
```bash
# path
## Percorso di partenza (default = cartella corrente).
pydirtree ~/Documenti

# -d / --max-depth
## Limita la profondità dell’albero.
pydirtree -d 2

# --hidden
## Mostra file e cartelle nascosti.
pydirtree --hidden

# --ignore
## Ignora file/cartelle che combaciano con uno o più pattern glob.
pydirtree --ignore *.log build dist

# --only-dirs
## Mostra solo directory, escludendo i file.
pydirtree --only-dirs

# --format
## Formato di output (text, md, json).
pydirtree --format json

# -o / --output
## Scrive l’output su file.
pydirtree -o alberotree.txt

# --follow-symlinks
## Segui i symlink a directory.
pydirtree --follow-symlinks

# --size
## Mostra la dimensione dei file.
pydirtree --size

# --date
## Mostra la data di creazione dei file.
pydirtree --date

# --no-default-ignores
## Disabilita gli ignore predefiniti (.git, node_modules, __pycache__, .venv).
pydirtree --no-default-ignores

# --exclude-files
## Escludi file specifici con pattern glob.
pydirtree --exclude-files *.mp4 *.tmp

# --size-unit
## Unità di misura per le dimensioni (b, kb, mb, gb, tb). Default = b.
pydirtree --size --size-unit mb

# --space-between-lines
## Aggiunge una riga vuota dopo ogni file con informazioni, per maggiore leggibilità.
pydirtree --size --date --space-between-lines
```

#### Formati supportati
- text: output stile tree
- md: blocco Markdown
- json: struttura JSON navigabile

#### Esempio di output
```bash
# Cartella di test con due file e una sottocartella:
Demo/
├── file1.txt
│   (1.024 B - Created at: 2025/09/27 09:50:15)
│
├── file2.log
│   (2.825 B - Created at: 2025/09/26 15:22:01)
│
└── Subdir/
    └── file3.mp4
        (12.346.628 B - Created at: 2025/09/25 18:05:44)

# Con --only-dirs
Demo/
└── Subdir/

# Con --format json
{
  "name": "Demo",
  "type": "dir",
  "children": [
    {
      "name": "file1.txt",
      "type": "file",
      "size": 1024,
      "created": "2025/09/27 09:50:15"
    }
  ]
}
```

#### 🌐 Lingue disponibili
```bash
🇬🇧 Inglese (en.json)
🇮🇹 Italiano (it.json)
🇪🇸 Spagnolo (es.json)
🇨🇳 Cinese (zh.json)
🇷🇺 Russo (ru.json)
🇵🇹 Portoghese (pt.json)
🇯🇵 Giapponese (ja.json)
🇫🇷 Francese (fr.json)
🇩🇪 Tedesco (de.json)
🇳🇱 Olandese (nl.json)
🇩🇰 Danese (da.json)
🇸🇪 Svedese (sv.json)
🇷🇴 Rumeno (ro.json)
🇨🇿 Ceco (cs.json)
🇭🇷 Croato (hr.json)
🇵🇱 Polacco (pl.json)
🇸🇰 Slovacco (sk.json)
🇸🇮 Sloveno (sl.json)
🇱🇻 Lettone (lv.json)
🇱🇹 Lituano (lt.json)
🇮🇪 Irlandese (ga.json)
🇬🇷 Greco (el.json)
🇭🇺 Ungherese (hu.json)
🇫🇮 Finlandese (fi.json)
🇹🇷 Turco (tr.json)
🇦🇱 Albanese (sq.json)
🇷🇸 Serbo (sr.json)
🇰🇷 Coreano (ko.json)
```
