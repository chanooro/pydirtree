import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import json
import pydirtree as pdt
import i18n

LANG = "it"  # default

def txt(k): return i18n.t(k, LANG)

def browse_dir():
    d = filedialog.askdirectory()
    if d: path_var.set(d)

def save_output():
    data = output_txt.get("1.0", "end-1c")
    if not data.strip():
        messagebox.showinfo("pydirtree", txt("no_output")); return
    f = filedialog.asksaveasfilename(defaultextension=".txt",
        filetypes=[("Text","*.txt"),("Markdown","*.md"),("JSON","*.json"),("All","*.*")])
    if f: Path(f).write_text(data, encoding="utf-8")

def generate():
    try:
        base = Path(path_var.get() or ".").resolve()
        if not base.exists():
            messagebox.showerror("pydirtree", f"{txt('err_path')} {base}"); return
        pdt.size_unit = size_unit_var.get()
        pdt.space_between = space_between_var.get()
        max_depth = int(depth_var.get()) if depth_var.get().strip() else None
        ignore = set(ignore_var.get().split()) if ignore_var.get().strip() else set()
        exclude_files = exclude_var.get().split() if exclude_var.get().strip() else []
        tree = pdt.build_tree(base, max_depth, hidden_var.get(), ignore, only_dirs_var.get(),
                              follow_symlinks_var.get(), size_var.get(), date_var.get(), exclude_files)
        fmt = format_var.get()
        out = json.dumps(tree, ensure_ascii=False, indent=2) if fmt=="json" else (pdt.render_md(tree) if fmt=="md" else pdt.render_text(tree))
        output_txt.delete("1.0", tk.END); output_txt.insert(tk.END, out)
    except Exception as e:
        messagebox.showerror("pydirtree", f"{txt('err_generic')}: {e}")

def on_lang_change(*_):
    global LANG
    LANG = lang_var.get().lower()
    i18n.load_lang(LANG)
    root.title(txt("title"))
    lbl_path.config(text=txt("path"))
    btn_browse.config(text=txt("browse"))
    lbl_depth.config(text=txt("depth"))
    lbl_format.config(text=txt("format"))
    lbl_unit.config(text=txt("size_unit"))
    lbl_ignore.config(text=txt("ignore"))
    lbl_exclude.config(text=txt("exclude"))
    chk_hidden.config(text=txt("hidden"))
    chk_onlydirs.config(text=txt("only_dirs"))
    chk_follow.config(text=txt("follow"))
    chk_size.config(text=txt("size"))
    chk_date.config(text=txt("date"))
    chk_space.config(text=txt("space"))
    btn_gen.config(text=txt("generate"))
    btn_save.config(text=txt("save"))

# ==== UI ====
root = tk.Tk()
i18n.load_lang(LANG)
root.title(txt("PyDirTree"))
root.iconbitmap("img/icon.ico")

# Vars
lang_var = tk.StringVar(value=LANG)
path_var = tk.StringVar(); depth_var = tk.StringVar()
ignore_var = tk.StringVar(); exclude_var = tk.StringVar()
format_var = tk.StringVar(value="text"); size_unit_var = tk.StringVar(value="B")
hidden_var = tk.BooleanVar(); only_dirs_var = tk.BooleanVar()
follow_symlinks_var = tk.BooleanVar(); size_var = tk.BooleanVar()
date_var = tk.BooleanVar(); space_between_var = tk.BooleanVar()

frm = ttk.Frame(root, padding=8); frm.grid(sticky="nsew")
root.columnconfigure(0, weight=1); root.rowconfigure(0, weight=1)

# Language selector
ttk.Label(frm, text="Lang:").grid(row=0, column=0, sticky="w")
ttk.Combobox(
    frm,
    textvariable=lang_var,
    values=[
        "en","it","es","zh","ru","pt","ja","fr","de","nl","da","sv",
        "ro","cs","hr","pl","sk","sl","lv","lt","ga","el","hu","fi",
        "tr","sq","sr","ko"
    ],
    width=10,
    state="readonly"
).grid(row=0, column=1, sticky="w")
lang_var.trace_add("write", on_lang_change)

# Path
lbl_path = ttk.Label(frm, text=txt("path")); lbl_path.grid(row=1, column=0, sticky="w")
ttk.Entry(frm, textvariable=path_var, width=60).grid(row=1, column=1, sticky="ew")
btn_browse = ttk.Button(frm, text=txt("browse"), command=browse_dir); btn_browse.grid(row=1, column=2, padx=4)
frm.columnconfigure(1, weight=1)

# Depth, Format, Unit
lbl_depth = ttk.Label(frm, text=txt("depth")); lbl_depth.grid(row=2, column=0, sticky="w")
ttk.Entry(frm, textvariable=depth_var, width=8).grid(row=2, column=1, sticky="w")
lbl_format = ttk.Label(frm, text=txt("format")); lbl_format.grid(row=2, column=1, padx=(140,0), sticky="w")
ttk.Combobox(frm, textvariable=format_var, values=["text","md","json"], width=8, state="readonly").grid(row=2, column=1, padx=(220,0), sticky="w")
lbl_unit = ttk.Label(frm, text=txt("size_unit")); lbl_unit.grid(row=2, column=2, sticky="w")
ttk.Combobox(frm, textvariable=size_unit_var, values=["B","KB","MB","GB","TB"], width=6, state="readonly").grid(row=2, column=2, padx=(130,0), sticky="w")

# Ignore / Exclude
lbl_ignore = ttk.Label(frm, text=txt("ignore")); lbl_ignore.grid(row=3, column=0, sticky="w")
ttk.Entry(frm, textvariable=ignore_var).grid(row=3, column=1, columnspan=2, sticky="ew")
lbl_exclude = ttk.Label(frm, text=txt("exclude")); lbl_exclude.grid(row=4, column=0, sticky="w")
ttk.Entry(frm, textvariable=exclude_var).grid(row=4, column=1, columnspan=2, sticky="ew")

# Flags
flags = ttk.Frame(frm); flags.grid(row=5, column=0, columnspan=3, sticky="w", pady=4)
chk_hidden = ttk.Checkbutton(flags, text=txt("hidden"), variable=hidden_var); chk_hidden.grid(row=0, column=0, padx=4, sticky="w")
chk_onlydirs = ttk.Checkbutton(flags, text=txt("only_dirs"), variable=only_dirs_var); chk_onlydirs.grid(row=0, column=1, padx=4, sticky="w")
chk_follow = ttk.Checkbutton(flags, text=txt("follow"), variable=follow_symlinks_var); chk_follow.grid(row=0, column=2, padx=4, sticky="w")
chk_size = ttk.Checkbutton(flags, text=txt("size"), variable=size_var); chk_size.grid(row=0, column=3, padx=4, sticky="w")
chk_date = ttk.Checkbutton(flags, text=txt("date"), variable=date_var); chk_date.grid(row=0, column=4, padx=4, sticky="w")
chk_space = ttk.Checkbutton(flags, text=txt("space"), variable=space_between_var); chk_space.grid(row=0, column=5, padx=4, sticky="w")

# Buttons
btns = ttk.Frame(frm); btns.grid(row=6, column=0, columnspan=3, sticky="e", pady=4)
btn_gen = ttk.Button(btns, text=txt("generate"), command=generate); btn_gen.grid(row=0, column=0, padx=4)
btn_save = ttk.Button(btns, text=txt("save"), command=save_output); btn_save.grid(row=0, column=1, padx=4)

# Output
output_txt = tk.Text(frm, wrap="none", height=24); output_txt.grid(row=7, column=0, columnspan=3, sticky="nsew", pady=(6,0))
frm.rowconfigure(7, weight=1)
try: output_txt.configure(font=("Consolas", 10))
except Exception: pass

root.mainloop()
