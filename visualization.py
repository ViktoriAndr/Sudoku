from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.Qt import Qt, QSize

import solver
import copy
import sys

TITLE = "Sudoku"
ICON = "web.jpg"  # Лучше загрузить файл png(Поддерживает прозрачность)
STYLE_SHEET = "background-color:yellow;"
WIDTH = 855
HEIGHT = 880
GRID = "cell_1.txt"


class MainWindow(QMainWindow):
    """
    Класс главного окна
    Здесть происходит основная логика
    """
    RED = "background-color:red;"
    GREEN = "background-color:lime;"
    WHITE = "background-color:white;"
    YELLOW = "background-color:yellow;"

    def __init__(self):
        super().__init__()
        self.window = QFrame(self)
        self.init_settings()
        self.init_main_logic()

    def init_settings(self):
        """
        Иницализация настоек окна
        """
        self.setCentralWidget(self.window)
        self.setWindowTitle(TITLE)
        self.setWindowIcon(QIcon(ICON))
        self.window.setStyleSheet(STYLE_SHEET)
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)
        self.resize(WIDTH, HEIGHT)

        screen = QDesktopWidget().screenGeometry()
        x = (screen.width() - WIDTH) / 2
        y = (screen.height() - HEIGHT) / 2
        self.move(x, y)

    def _lambda(self, button, solver, x, y):
        """
        Возвращает фунцию которая
        создает меню по выбору числа
        :param button: Ссылка на экземляр кнопки
        :return: Функция,создающая меню кнопки
        """

        def _meth():
            menu = QMenu()
            action = []
            act_1 = QAction('.')
            act_1.triggered.connect(self._lambda_2(button, '.', solver, x, y))
            action.append(act_1)
            for e in range(1, self.len_grid + 1):
                act = QAction(str(e))
                act.triggered.connect(self._lambda_2(button, e, solver, x, y))
                action.append(act)
            menu.addActions(action)
            button.setMenu(menu)
            button.setStyleSheet(MainWindow.WHITE)
            button.showMenu()

        return _meth

    def _lambda_2(self, button, e, solver, x, y):
        """
        Возвращает фунцию, которая
        перекракшивает кнопку в красный цвет
        и устанавливает значение текста в кнопки 
        в параметр e
        :param button: Ссылка на экземляр кнопки
        :param e:     Значение устанавливое в поле текста кнопки
        :return:      Функция устанавливающее  в поле текста кнорки paran e
        """

        def _meth():
            button.setText(str(e))
            if str(e) == str(solver[x][y]):
                button.setStyleSheet(MainWindow.GREEN)
                button.blockSignals(True)
            elif str(e) == '.':
                button.setStyleSheet(MainWindow.WHITE)
            else:
                button.setStyleSheet(MainWindow.RED)
                button.blockSignals(True)

        return _meth

    def _lambda_3(self, button, grid, solve, x, y):
        """
        заполняет всю сетку
        :param grid: нерешённая сетка
        :param solve: решённая сетка
        :return: заполненное поле
        """

        def _meth():
            if grid[x][y] == '.':
                button.setText(str(solve[x][y]))
                button.setStyleSheet(MainWindow.GREEN)
                button.blockSignals(True)

        return _meth

    def init_main_logic(self):
        """
        Иницализация главной логики программы
        """
        created_grid = solver.creating_grid(GRID)
        created_grid_copy = copy.deepcopy(created_grid)

        self.grid = created_grid
        self.solver_grid = solver.all_solutions(created_grid_copy)[0]
        self.len_grid = len(self.grid)

        solve = QPushButton("Solve", self)
        solve.resize(WIDTH, HEIGHT // self.len_grid)
        solve.move(1, self.len_grid * HEIGHT // (self.len_grid + 1))
        solve.setStyleSheet(MainWindow.YELLOW)
        solve.show()

        for y in range(self.len_grid):
            for x in range(self.len_grid):
                button = QPushButton(str(self.grid[x][y]), self)
                button.resize(WIDTH // self.len_grid,
                              HEIGHT // (self.len_grid + 1))
                if str(self.grid[x][y]) == '.':
                    button.pressed.connect(self._lambda(button, self.solver_grid, x, y))
                    button.setStyleSheet(MainWindow.WHITE)
                else:
                    button.setStyleSheet(MainWindow.GREEN)
                button.move(y * WIDTH // self.len_grid, x * HEIGHT // (self.len_grid + 1))
                solve.pressed.connect(self._lambda_3(button, self.grid, self.solver_grid, x, y))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
