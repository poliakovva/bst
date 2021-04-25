import sys

from PyQt5.QtCore import QFileInfo, Qt
from PyQt5.QtGui import QTextDocument
from PyQt5.QtPrintSupport import QPrinter

from materials import MATERIALS
from table import html

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QGridLayout,
    QGroupBox,
    QWidget,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QFormLayout,
    QFileDialog,
    QCompleter
)


# Создание главного окна, содержащего все виджеты
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Расчет стоимости")
        # Создание объектов, которые группируют все слои для каждого типа материала
        self.calc_box_1 = CalculationBox("Плитные материалы", 1)
        self.calc_box_2 = CalculationBox("Фурнитура стандарт", 2)
        self.calc_box_3 = CalculationBox("Освещение", 3)
        self.calc_box_4 = CalculationBox("Фурнитура премиум", 4)
        self.calc_box_5 = CalculationBox("Столярные изделия", 5)
        # Создание таблицы с конечными результатами
        self.final_table = FinalTable()

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.general_layout = QGridLayout()
        self.central_widget.setLayout(self.general_layout)

        self.create_display()

    def create_display(self):
        self.general_layout.addWidget(self.calc_box_1, 0, 0)
        self.general_layout.addWidget(self.calc_box_2, 0, 1)
        self.general_layout.addWidget(self.calc_box_3, 0, 2)
        self.general_layout.addWidget(self.calc_box_4, 1, 0)
        self.general_layout.addWidget(self.calc_box_5, 1, 1)
        self.general_layout.addLayout(self.final_table, 1, 2)

    def get_final_table(self):
        return self.final_table

    def get_calc_box(self, n):
        if n == 1:
            return self.calc_box_1
        elif n == 2:
            return self.calc_box_2
        elif n == 3:
            return self.calc_box_3
        elif n == 4:
            return self.calc_box_4
        elif n == 5:
            return self.calc_box_5
        else:
            return None


# Создание виджета (области) для расчёта стоимостей определенного типа материала
class CalculationBox(QGroupBox):
    def __init__(self, title="", material_type=1):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.setTitle(title)
        self.calc_list = list()
        self.material_type = material_type
        self.create_display()
        self.full_cost = 0
        self.setMinimumWidth(450)

    def create_display(self, display_created=False):
        # Создание объекта строки расчета и добавление его в список
        calc_layout = CalculateMaterial(self.material_type)
        self.calc_list.append(calc_layout)
        # Если кнопки "Добавить материал" и "Рассчитать" уже созданы, то не создавать их
        if not display_created:
            layout_up = QHBoxLayout()
            add_btn = QPushButton("Добавить материал")
            add_btn.clicked.connect(lambda: self.create_display(True))
            layout_up.addWidget(add_btn)
            self.main_layout.addLayout(layout_up)

        self.main_layout.addLayout(calc_layout)

    def get_full_cost(self):
        self.full_cost = calculate(self.calc_list)
        return self.full_cost

    def clear_rows(self):
        for calc in self.calc_list:
            calc.self_clear()


# Создание виджета для расчёта стоимости конкретного материала
class CalculateMaterial(QVBoxLayout):
    def __init__(self, material_type=1):
        super().__init__()
        self.del_btn = QPushButton("Удалить")
        self.line = QLineEdit()

        self.line.setMinimumWidth(100)
        self.combo_box = QComboBox()
        self.combo_box.setCurrentText('')
        self.combo_box.setMaximumWidth(200)
        self.layout = QHBoxLayout()
        self.type = material_type
        self.materials = MATERIALS[material_type - 1]
        self.completer = QCompleter(self.materials)
        self.combo_box.setEditable(True)
        self.create_layout()

    def create_layout(self):
        self.combo_box.addItems(self.materials)
        self.combo_box.setCompleter(self.completer)
        self.completer.setFilterMode(Qt.MatchContains)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)

        self.combo_box.setCurrentText("")

        self.line.textChanged.connect(
            lambda: FinalTable.set_row(win.get_final_table(), CalculationBox.get_full_cost(win.get_calc_box(self.type)),
                                       self.type)
        )
        self.line.textChanged.connect(
            lambda: FinalTable.set_sum_row(win.get_final_table())
        )
        self.line.textChanged.connect(
            lambda: FinalTable.set_final_price_row(win.get_final_table())
        )
        self.line.textChanged.connect(lambda: input_check(self.line))
        self.combo_box.currentTextChanged.connect(
            lambda: FinalTable.set_row(win.get_final_table(), CalculationBox.get_full_cost(win.get_calc_box(self.type)),
                                       self.type)
        )
        self.combo_box.currentTextChanged.connect(
            lambda: FinalTable.set_sum_row(win.get_final_table())
        )
        self.combo_box.currentTextChanged.connect(
            lambda: FinalTable.set_final_price_row(win.get_final_table())
        )

        self.line.setPlaceholderText("Количество в м. кв. / шт.")
        # self.layout.addWidget(QLabel("Количество \n в м. кв. / шт."))
        self.layout.addWidget(self.line, 1)
        self.layout.addWidget(self.combo_box, 1)

        self.del_btn.setFixedSize(80, 20)
        self.del_btn.clicked.connect(lambda: clear_layout(self.layout))
        self.del_btn.clicked.connect(
            lambda: FinalTable.set_row(win.get_final_table(),
                                       (CalculationBox.get_full_cost(win.get_calc_box(self.type)) - calculate(
                                           [self])),
                                       self.type)
        )
        self.del_btn.clicked.connect(
            lambda: FinalTable.set_sum_row(win.get_final_table())
        )
        self.del_btn.clicked.connect(
            lambda: FinalTable.set_final_price_row(win.get_final_table())
        )
        self.layout.addWidget(self.del_btn, 0)

        self.addLayout(self.layout)

    def get_size(self):
        try:
            return self.line.text()
        except RuntimeError:
            return 0

    def get_material(self):
        try:
            return self.combo_box.currentText()
        except RuntimeError:
            return 0

    def get_materials_dict(self):
        try:
            return dict.copy(self.materials)
        except RuntimeError:
            return 0

    def self_clear(self):
        clear_layout(self.layout)



class FinalTable(QFormLayout):
    def __init__(self):
        super().__init__()
        # Создание строк в итоговой таблице для каждого типа материала и услуг
        self.p_row = QLineEdit()
        self.fs_row = QLineEdit()
        self.o_row = QLineEdit()
        self.fp_row = QLineEdit()
        self.s_row = QLineEdit()

        self.delivery_row = QLineEdit()
        self.delivery_row.textChanged.connect(self.set_final_price_row)
        self.lifting_row = QLineEdit()
        self.lifting_row.textChanged.connect(self.set_final_price_row)
        self.measurement_row = QLineEdit()
        self.measurement_row.textChanged.connect(self.set_final_price_row)
        self.project_row = QLineEdit()
        self.project_row.textChanged.connect(self.set_final_price_row)

        self.sum_row = QLineEdit()

        self.final_price_row = QLineEdit()

        self.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.row_dict = {
            1: self.p_row,
            2: self.fs_row,
            3: self.o_row,
            4: self.fp_row,
            5: self.s_row,
        }
        self.additional_row_dict = {
            1: self.delivery_row,
            2: self.lifting_row,
            3: self.measurement_row,
            4: self.project_row
        }
        # Делаем каждую строку неизменяемой
        for key in self.row_dict:
            self.row_set_read_only(key)
            row = self.row_dict.get(key)
            row.setText("0 руб.")

        self.sum_row.setText("0 руб.")
        self.sum_row.setReadOnly(True)
        self.set_sum_row()

        self.production_layout = QHBoxLayout()
        self.production_percent = QLineEdit()
        self.production_result = QLineEdit()
        self.production_result.setReadOnly(True)
        self.production_percent.setPlaceholderText("Введите %")
        self.production_percent.textChanged.connect(lambda: self.set_prod_result(self.production_percent.text()))
        self.production_percent.textChanged.connect(self.set_final_price_row)
        self.production_layout.addWidget(self.production_percent)
        self.production_layout.addWidget(self.production_result)

        self.final_price_row.setText("0 руб.")
        self.final_price_row.setReadOnly(True)

        self.clear_button = QPushButton("Отчистить")
        self.clear_button.clicked.connect(self.clear_final_table)
        self.clear_button.clicked.connect(clear_all)

        self.create_pdf = QPushButton("Сохранить в PDF")
        self.create_pdf.clicked.connect(self.set_pdf_table)
        self.create_pdf.clicked.connect(self.create_pdf_file)

        self.tech_rows_layout = QHBoxLayout()
        self.tech_rows_layout.addWidget(self.create_pdf)
        self.tech_rows_layout.addWidget(self.clear_button)

        self.text = QTextDocument()

        self.add_rows()

    def add_rows(self):
        self.addRow("Плитные материалы", self.p_row)
        self.addRow("Фурнитура стандарт", self.fs_row)
        self.addRow("Освещение", self.o_row)
        self.addRow("Фурнитура премиум", self.fp_row)
        self.addRow("Столярные изделия", self.s_row)
        self.addRow("Итоговая стоимость изделия", self.sum_row)
        self.addRow("Доставка", self.delivery_row)
        self.addRow("Подъем на этаж на лифте", self.lifting_row)
        self.addRow("Изготовление, сборка, монтаж", self.production_layout)
        self.addRow("Замер", self.measurement_row)
        self.addRow("Проект", self.project_row)
        self.addRow("Итоговая стоимость изделия и услуг", self.final_price_row)
        self.addRow(self.tech_rows_layout)

    def row_set_read_only(self, row_type=1):
        row = self.row_dict.get(row_type)
        row.setReadOnly(True)

    def set_row(self, calc=0, material_type=1):
        # Вывод в таблицу значения итоговой стоимости материала определенного типа
        row = self.row_dict.get(material_type)
        row.setText(str(int(calc)) + " руб.")

    # Вывод в таблицу значения итоговой стоимости только материалов, без учёта услуг
    def set_sum_row(self):
        total = 0
        for key in self.row_dict:
            row = self.row_dict.get(key).text()

            line = row.split(" ")
            total += float(line[0])
        self.sum_row.setText(str(total) + " руб.")

    # Вывод в таблицу значения итоговой стоимости всего изделия
    def set_final_price_row(self):
        final = 0
        for key in self.additional_row_dict:
            row_text = self.additional_row_dict.get(key).text()
            try:
                final += float(row_text)
            except ValueError:
                input_check(self.additional_row_dict.get(key))
        materials_sum = self.sum_row.text().split()
        final += float(materials_sum[0])
        f = self.production_result.text().split()
        try:
            final += float(f[0])
        except IndexError:
            pass
        except ValueError:
            pass
        self.final_price_row.setText(str(final) + " руб.")

    def set_prod_result(self, production_percent):
        try:
            # Обработка случая, когда пользователь пытается ввести дробное число через запятую, а не через точку
            percent_num = production_percent.split(',')
            if len(percent_num) > 1:
                percent_decimal = float(percent_num[1])
                while percent_decimal > 1:
                    percent_decimal = percent_decimal / 10
                production_percent = float(percent_num[0]) + percent_decimal
            percent = float(production_percent) / 100
            materials_sum = self.sum_row.text().split()
            self.production_result.setText(str("{0:.1f}".format(float(materials_sum[0]) * percent)))
            self.production_percent.setStyleSheet(stylesheet)
        except ValueError:
            if self.production_percent.text().strip() == "":
                self.production_percent.setStyleSheet(stylesheet)
            else:
                self.production_percent.setStyleSheet("border-style: solid; border-width: 2px; border-color: red")
            self.production_result.setText("")

    # Отчистить итоговую таблицу
    def clear_final_table(self):
        for key in self.row_dict:
            self.row_dict.get(key).setText("0 руб.")
        for key in self.additional_row_dict:
            self.additional_row_dict.get(key).setText("")
        self.production_percent.setText("")
        self.set_sum_row()
        self.set_final_price_row()

    # Создание pdf файла
    def create_pdf_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self.create_pdf, 'Сохранить в PDF', None)
        if file_name != '':
            if QFileInfo(file_name).suffix() == "":
                file_name += '.pdf'
        printer = QPrinter(QPrinter.HighResolution)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(file_name)
        self.text.print_(printer)

    # Заполнение HTML таблицы из файла table.py
    def set_pdf_table(self):
        html_format = html.format(
            p_row=self.p_row.text(),
            fs_row=self.fs_row.text(),
            o_row=self.o_row.text(),
            fp_row=self.fp_row.text(),
            s_row=self.s_row.text(),
            sum_row=self.sum_row.text(),
            delivery_row=self.delivery_row.text(),
            lifting_row=self.lifting_row.text(),
            production_result=self.production_result.text(),
            measurement_row=self.measurement_row.text(),
            project_row=self.project_row.text(),
            final_price_row=self.final_price_row.text()
        )
        self.html = html_format
        self.text.setHtml(self.html)


# Расчет стоимости определенного типа материала
def calculate(calc_list):
    total = 0
    for calc in calc_list:
        size = calc.get_size()
        material = calc.get_material()
        materials = calc.get_materials_dict()
        cost = materials.get(material)
        try:
            total = total + (float(size) * float(cost))
        except ValueError:
            total = 0
        except TypeError:
            total = 0

    return total


# Отчистка макета (layout) при нажатии кнопки "Удалить"
def clear_layout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()


def clear_all():
    for i in range(1, 6):
        print("i = " + str(i))
        calc_box = win.get_calc_box(i)
        calc_box.clear_rows()


def input_check(line):
    if line.text().isnumeric() or line.text() == '':
        line.setStyleSheet(None)
    else:
        line.setStyleSheet("border-style: solid; border-width: 2px; border-color: red")


stylesheet = """     
        QPushButton[text="Удалить"]{
            background-color: #dc143c;
            color: white;
            border-style: solid;
            border-width: 2px;
            border-radius: 10px;
            border-color: black;
        }
        QPushButton:pressed {
            border-radius: 10px;
            border-color: black;
            color: black;
        }
        QPushButton[text="Удалить"]:hover { 
            background-color:#ff2400 ;
            border-style: solid;
            }
        
        QGroupBox{
            background-color:  Lavender;
            border-style: solid;
            border-width: 4px;
            border-radius: 15px;
        }
        QMainWindow{
            background-color: #ffffff;
        }
        QLineEdit[readOnly="true"] {
            background-color: Lavender;
            font: 15px Arial, sans-serif;
            color: black;
            border-style: solid;
            border-radius: 15px;
        }
        """

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
