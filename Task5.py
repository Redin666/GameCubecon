import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QAction, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self, rows, columns, grid):
        super().__init__()
        self.rows = rows
        self.columns = columns
        self.grid = grid
        self.initUI()
        self.setFocusPolicy(Qt.StrongFocus)

    def initUI(self):
        self.setWindowTitle("Кубикон")
        self.setGeometry(100, 100, 22 * self.columns + 2, 22 * self.rows + 2)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        self.cube_labels = []

        for i in range(self.rows):
            row_layout = QHBoxLayout()
            for j in range(self.columns):
                cube_label = QLabel()
                cube_label.setStyleSheet("background-color: {};".format('gray' if i == 0 or j == 0 or i == self.rows - 1 or j == self.columns - 1 else self.grid[i][j]))
                cube_label.setFixedSize(100, 100)
                row_layout.addWidget(cube_label)
                self.cube_labels.append(cube_label)
            main_layout.addLayout(row_layout)

       
        for i in range(self.rows):
            for j in range(self.columns):
                if self.grid[i][j] == 'black':
                    self.current_position = [i, j]
                    break

        self.rules_button = QPushButton("Правила", self)
        self.rules_button.setWindowModality(Qt.WindowModal)
        self.rules_button.clicked.connect(self.show_rules)
        main_layout.addWidget(self.rules_button)

    def show_rules(self):
        rules_text = (
            "Цель игры: выстроить кубики в линии по цветам \n\n"
            "Управление: Игрок может управлять черным кубиком с помощью стрелок на клавиатуре.\nСтрелка вверх перемещает"
            "кубик вверх\nстрелка вниз - вниз\nстрелка влево - влево\nстрелка вправо - вправо.\n")

        QMessageBox.information(self, "Правила", rules_text)

    def keyPressEvent(self, event):
        key = event.key()
        if key in [Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down]:
            next_position = self.current_position.copy()

            if key == Qt.Key_Left:
                next_position[1] -= 1
            elif key == Qt.Key_Right:
                next_position[1] += 1
            elif key == Qt.Key_Up:
                next_position[0] -= 1
            elif key == Qt.Key_Down:
                next_position[0] += 1


            next_position[0] = max(1, min(next_position[0], self.rows - 2))
            next_position[1] = max(1, min(next_position[1], self.columns - 2))

            if (next_position[0] == 0 or next_position[0] == self.rows - 1 or
                next_position[1] == 0 or next_position[1] == self.columns - 1):
                return

            if self.grid[next_position[0]][next_position[1]] == 'none':
                self.grid[next_position[0]][next_position[1]] = 'black'
                self.grid[self.current_position[0]][self.current_position[1]] = 'none'
                self.current_position = next_position
            elif self.grid[next_position[0]][next_position[1]] in ['red', 'blue', 'green', 'yellow', 'pink']:
                next_position_cube = [next_position[0] + (next_position[0] - self.current_position[0]),
                                    next_position[1] + (next_position[1] - self.current_position[1])]
                if 1 <= next_position_cube[0] < self.rows - 1 and 1 <= next_position_cube[1] < self.columns - 1:
                    if self.grid[next_position_cube[0]][next_position_cube[1]] == 'none':
                        self.grid[next_position_cube[0]][next_position_cube[1]] = self.grid[next_position[0]][next_position[1]]
                        self.grid[next_position[0]][next_position[1]] = 'black'
                        self.grid[self.current_position[0]][self.current_position[1]] = 'none'
                        self.current_position = next_position

            self.update_cubes()

            if self.check_win_condition():
                QMessageBox.information(self, "Победа!", "Вы выиграли!")

    def update_cubes(self):
        for i, label in enumerate(self.cube_labels):
            row = i // self.columns
            col = i % self.columns
            if row == self.current_position[0] and col == self.current_position[1]:
                label.setStyleSheet("background-color: black;")
            else:
                label.setStyleSheet("background-color: {};".format('gray' if row == 0 or col == 0 or row == self.rows - 1 or col == self.columns - 1 else self.grid[row][col]))

    def check_win_condition(self):
        colors_to_check = {'red', 'blue', 'green', 'yellow', 'pink'}

        if all(self.grid[1][j] in colors_to_check for j in range(1, self.columns - 1)):
            if all(self.grid[self.rows - 2][j] in colors_to_check for j in range(1, self.columns - 1)):
                return True

        for i in range(1, self.rows - 1):
            if all(self.grid[i][1] in colors_to_check for i in range(1, self.rows - 1)):
                if all(self.grid[i][self.columns - 2] in colors_to_check for i in range(1, self.rows - 1)):
                    return True

        return False


class MenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Меню")
        self.setGeometry(100, 100, 300, 200)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        level1_button = QPushButton("Уровень 1", self)
        level1_button.clicked.connect(lambda: self.start_level("level1.txt"))
        layout.addWidget(level1_button)

        level2_button = QPushButton("Уровень 2", self)
        level2_button.clicked.connect(lambda: self.start_level("level2.txt"))
        layout.addWidget(level2_button)
    
        level3_button = QPushButton("Уровень 3", self)
        level3_button.clicked.connect(lambda: self.start_level("level3.txt"))
        layout.addWidget(level3_button)

    def start_level(self, filename):
        try:
            with open(filename, 'r') as file:
                rows = 0
                columns = 0
                grid = []
                colors = {
                    0: 'none',
                    1: 'gray',
                    2: 'black',
                    3: 'red',
                    4: 'blue',
                    5: 'green',
                    6: 'yellow',
                    7: 'pink'
                }
                for line in file:
                    row = [colors[int(num)] for num in line.split()]
                    if not columns:
                        columns = len(row)
                    else:
                        if len(row) != columns:
                            raise ValueError("Inconsistent number of columns")
                    rows += 1
                    grid.append(row)
                self.start_game(rows, columns, grid)
        except FileNotFoundError:
            QMessageBox.critical(self, "Ошибка", "Файл уровня не найден.")
        except ValueError as e:
            QMessageBox.critical(self, "Ошибка", str(e))
        except KeyError as e:
            QMessageBox.critical(self, "Ошибка", f"Неизвестный цвет: {e}")

    def start_game(self, rows, columns, grid):
        self.game_window = MainWindow(rows, columns, grid)
        self.game_window.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.game_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu_window = MenuWindow()
    menu_window.show()
    sys.exit(app.exec_())
