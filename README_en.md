# pydirtree

[🇮🇹 Leggi in Italiano](README.md) | 🇬🇧 Read in English

Directory tree CLI in Python: text/Markdown/JSON output, filters and depth control.

## Installation
```bash
pip install -e .
```

### Basic usage
```bash
# Print the full directory tree of the current folder
pydirtree
```

## Usage
```bash
# path
## Starting path (default = current directory).
pydirtree ~/Documenti

# -d / --max-depth
## Limit the tree depth.
pydirtree -d 2

# --hidden
## Show hidden files and folders.
pydirtree --hidden

# --ignore
## Ignore files/folders matching one or more glob patterns.
pydirtree --ignore *.log build dist

# --only-dirs
## Show only directories, exclude files.
pydirtree --only-dirs

# --format
## Output format (text, md, json).
pydirtree --format json

# -o / --output
## Write the output to a file.
pydirtree -o alberotree.txt

# --follow-symlinks
## Follow symlinks to directories.
pydirtree --follow-symlinks

# --size
## Show file sizes.
pydirtree --size

# --date
## Show file creation date.
pydirtree --date

# --no-default-ignores
## Disable default ignores (.git, node_modules, __pycache__, .venv).
pydirtree --no-default-ignores

# --exclude-files
## Exclude specific files with glob patterns.
pydirtree --exclude-files *.mp4 *.tmp

# --size-unit
## Unit for file sizes (b, kb, mb, gb, tb). Default = b.
pydirtree --size --size-unit mb

# --space-between-lines
## Add a blank line after each file with info, for better readability.
pydirtree --size --date --space-between-lines
```

#### Supported formats
- text: tree-style output
- md: Markdown block
- json: JSON navigable structure

#### Output example
```bash
# Test folder with two files and a subfolder:
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

# With --only-dirs
Demo/
└── Subdir/

# With --format json
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

#### 🌐 Available languages
```bash
🇬🇧 English (en.json)
🇮🇹 Italian (it.json)
🇪🇸 Spanish (es.json)
🇨🇳 Chinese (zh.json)
🇷🇺 Russian (ru.json)
🇵🇹 Portuguese (pt.json)
🇯🇵 Japanese (ja.json)
🇫🇷 French (fr.json)
🇩🇪 German (de.json)
🇳🇱 Dutch (nl.json)
🇩🇰 Danish (da.json)
🇸🇪 Swedish (sv.json)
🇷🇴 Romanian (ro.json)
🇨🇿 Czech (cs.json)
🇭🇷 Croatian (hr.json)
🇵🇱 Polish (pl.json)
🇸🇰 Slovak (sk.json)
🇸🇮 Slovenian (sl.json)
🇱🇻 Latvian (lv.json)
🇱🇹 Lithuanian (lt.json)
🇮🇪 Irish (ga.json)
🇬🇷 Greek (el.json)
🇭🇺 Hungarian (hu.json)
🇫🇮 Finnish (fi.json)
🇹🇷 Turkish (tr.json)
🇦🇱 Albanian (sq.json)
🇷🇸 Serbian (sr.json)
🇰🇷 Korean (ko.json)
```
