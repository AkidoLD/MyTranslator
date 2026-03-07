import webbrowser
from tkinter.ttk import Frame, Label, Separator, Style


class AboutFrame(Frame):

    _BG        = "white"
    _BG_HEADER = "#f0f0f0"
    _FG_MUTED  = "#666666"
    _ACCENT    = "#444444"
    _GITHUB    = "https://github.com/AkidoLD"

    def __init__(self, master, app_version: str, app_creator: str, **kwargs):
        super().__init__(master, **kwargs)
        #
        self._setup_styles()
        self.configure(style="About.TFrame")
        #
        self._build_header(app_version)
        self._build_separator()
        self._build_description()
        self._build_separator()
        self._build_info(app_version, app_creator)
        self._build_separator()
        self._build_footer()

    # ─── Setup ────────────────────────────────────────────────────────────────

    def _setup_styles(self):
        s = Style()
        s.configure("About.TFrame",          background=self._BG)
        s.configure("AboutHeader.TFrame",     background=self._BG_HEADER)
        s.configure("AboutSection.TFrame",    background=self._BG)
        s.configure("AboutTitle.TLabel",      background=self._BG_HEADER, font=("Ubuntu", 20, "bold"),  foreground=self._ACCENT)
        s.configure("AboutSubtitle.TLabel",   background=self._BG_HEADER, font=("Ubuntu", 11),          foreground=self._FG_MUTED)
        s.configure("AboutSectionTitle.TLabel", background=self._BG,      font=("Ubuntu", 12, "bold"),  foreground=self._ACCENT)
        s.configure("AboutBody.TLabel",       background=self._BG,        font=("Ubuntu", 11),          foreground="#333333")
        s.configure("AboutMuted.TLabel",      background=self._BG,        font=("Ubuntu", 10),          foreground=self._FG_MUTED)
        s.configure("AboutLink.TLabel",       background=self._BG,        font=("Ubuntu", 11, "underline"), foreground="#0078d4", cursor="hand2")
        s.configure("AboutTag.TLabel",        background="#e8e8e8",        font=("Ubuntu", 10),          foreground=self._ACCENT)
        s.configure("AboutInfo.TLabel",       background=self._BG,        font=("Ubuntu", 11),          foreground="#333333")

    # ─── Build ────────────────────────────────────────────────────────────────

    def _build_header(self, version: str):
        header = Frame(self, style="AboutHeader.TFrame", padding=(20, 15))
        header.pack(fill="x")
        #
        Label(header, text="MyTranslator", style="AboutTitle.TLabel").pack(anchor="w")
        Label(header, text=f"v{version}  —  Application de traduction modulaire", style="AboutSubtitle.TLabel").pack(anchor="w", pady=(2, 0))

    def _build_description(self):
        section = Frame(self, style="AboutSection.TFrame", padding=(20, 10))
        section.pack(fill="x")
        #
        Label(section, text="À propos", style="AboutSectionTitle.TLabel").pack(anchor="w", pady=(0, 6))
        #
        desc = (
            "MyTranslator est une application Python permettant d'effectuer des traductions "
            "à partir de plusieurs types de fournisseurs. Grâce à son système de providers, "
            "l'utilisateur choisit librement son fournisseur et personnalise son comportement."
        )
        self._desc_lb = Label(section, text=desc, style="AboutBody.TLabel", wraplength=400, justify="left")
        self._desc_lb.pack(anchor="w", pady=(0, 8))
        #
        Label(section, text="Objectif", style="AboutSectionTitle.TLabel").pack(anchor="w", pady=(4, 6))
        #
        goal = (
            "Ce projet a été développé à but éducatif, dans l'optique de maîtriser "
            "les concepts de Clean Architecture et d'améliorer la qualité du code au fil du temps. "
            "Le code reflète une progression — il n'est pas parfait, mais il évolue."
        )
        self._goal_lb = Label(section, text=goal, style="AboutBody.TLabel", wraplength=400, justify="left")
        self._goal_lb.pack(anchor="w")

    def _build_info(self, version: str, creator: str):
        section = Frame(self, style="AboutSection.TFrame", padding=(20, 10))
        section.pack(fill="x")
        #
        Label(section, text="Informations", style="AboutSectionTitle.TLabel").pack(anchor="w", pady=(0, 8))
        #
        infos = [
            ("Créateur",    creator),
            ("Version",     version),
            ("Langage",     "Python 3.13"),
            ("UI",          "Tkinter / TTK"),
            ("Architecture","Clean Architecture — Domain / Application / Infra / UI"),
            ("Licence",     "MIT"),
        ]
        for label, value in infos:
            row = Frame(section, style="AboutSection.TFrame")
            row.pack(fill="x", pady=2)
            Label(row, text=f"{label} :", style="AboutMuted.TLabel", width=14, anchor="w").pack(side="left")
            Label(row, text=value, style="AboutInfo.TLabel", anchor="w").pack(side="left")

        # Technologies
        Label(section, text="Technologies", style="AboutSectionTitle.TLabel").pack(anchor="w", pady=(12, 6))
        tags_frame = Frame(section, style="AboutSection.TFrame")
        tags_frame.pack(anchor="w")
        for tag in ["Python", "Tkinter", "TTK", "JSON", "Clean Arch", "MVC"]:
            Label(tags_frame, text=f" {tag} ", style="AboutTag.TLabel", padding=(4, 2)).pack(side="left", padx=(0, 4))

    def _build_footer(self):
        section = Frame(self, style="AboutSection.TFrame", padding=(20, 10))
        section.pack(fill="x")
        #
        Label(section, text="Liens", style="AboutSectionTitle.TLabel").pack(anchor="w", pady=(0, 6))
        #
        link = Label(section, text=self._GITHUB, style="AboutLink.TLabel")
        link.pack(anchor="w")
        link.bind("<Button-1>", lambda _: webbrowser.open(self._GITHUB))

    def _build_separator(self):
        Separator(self, orient="horizontal").pack(fill="x", padx=20, pady=2)

    # ─── Events ───────────────────────────────────────────────────────────────

        self.bind("<Configure>", self._on_resize)

    def _on_resize(self, event):
        wrap = event.width - 40
        self._desc_lb.configure(wraplength=wrap)
        self._goal_lb.configure(wraplength=wrap)


if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    root.geometry("600x700")
    root.title("À propos")
    AboutFrame(root, app_version="1.0.0", app_creator="AkidoLD").pack(fill="both", expand=True)
    root.mainloop()