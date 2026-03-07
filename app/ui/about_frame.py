from tkinter.ttk import Frame, Label, Style


class AboutFrame(Frame):
    def __init__(
            self,
            master,
            app_version : str,
            app_creator: str,
            **kwargs
    ):
        super().__init__(master, padding=10,**kwargs)
        #
        Style().configure(
            "AboutFrame.TFrame",
            background="white",
        )
        #
        self.configure(style="AboutFrame.TFrame")
        #
        description = ("    MyTranslator est une application en python qui permet d'effectuer des traduction a partir de plusieurs type de fournisseur different.\n"
                       "    Avec son système de Fournisseur, c'est a l'utilisateur de choisir le provider qu'il veut utiliser un faire ca traduction, et de customiser son comportement comment bon lui semble.\n"
                       "    Cette app a ete créer a but eductif, afin de maitrise le concepte de clean architecture, et donc d'améliore la qualité de mes code.")
        #
        Label(self, text="A propos de MyTranslator", font=("Ubuntu", 18, 'bold'), background="white").pack(side='top', fill="x", pady=5)
        self._descript_lb = Label(self, text=description, font=("Ubuntu", 12), background="white")
        self._descript_lb.pack(side='top', fill="x", pady=2)
        #
        Label(self, text=f"Version : {app_version}", font=("Ubuntu", 11, 'bold'), background="white").pack(side='top', fill="x", pady=2)
        Label(self, text=f"Createur : {app_creator}", font=("Ubuntu", 11, 'bold'), background="white").pack(side='top', fill="x", pady=2)
        #
        self.bind("<Configure>", lambda e : self._descript_lb.config(wraplength=e.width))