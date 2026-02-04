from app.controllers.app_controller import AppController
from app.ui.main_window import MainWindow
from shared.ui.components.float_menu import FloatFrame

if __name__ == "__main__" :
    main_window = MainWindow()
    app_controller = AppController(main_window)
    #
    main_window.mainloop()