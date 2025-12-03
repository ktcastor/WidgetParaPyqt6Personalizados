"""
Módulo para agregar nuevos Widgets a tus
aplicaciones realizadas con pyqt6
"""

"""
importamos las librerias necesarias para el funcionamiento del
módulo
"""
from PyQt6.QtWidgets import (
    QWidget, QLineEdit, QListWidget, QVBoxLayout,QHBoxLayout,
    QApplication, QListWidgetItem, QLabel, QPushButton
)
from PyQt6.QtGui import QFont,QPixmap
from PyQt6.QtCore import Qt, pyqtSignal
import sys


"""
Widget que agrega un campo de busqueda personalizado y te muestra la lista de datos
que puedes selecionar

recibe como parametro datos en forma de lista o json

"""
class CassieSearch(QWidget):
    # Señal que emite el valor seleccionado
    # Si es lista → emite el texto
    # Si es dict → emite (key, value)
    itemSelected = pyqtSignal(object)

    def __init__(self, data=None, parent=None):
        super().__init__(parent)

        self.data = data if data else []

        # Campo de texto
        self.search_field = QLineEdit(self)
        self.search_field.setPlaceholderText("🔍 Escribe para buscar...")
        self.search_field.textChanged.connect(self.update_results)

        # Lista de resultados
        self.result_list = QListWidget(self)
        self.result_list.hide()
        self.result_list.itemClicked.connect(self.on_item_clicked)

        # Layout interno del widget
        layout = QVBoxLayout(self)
        layout.addWidget(self.search_field)
        layout.addWidget(self.result_list)
        self.setLayout(layout)

        # Estilo inicial pastel
        self.setStyleSheet("""
            QLineEdit {
                background-color: #ffe6f0;
                border: 2px solid #f5b8d1;
                border-radius: 10px;
                padding: 6px;
                font-size: 14px;
            }
            QListWidget {
                background-color: #fff0f6;
                border: 1px solid #f5b8d1;
                border-radius: 8px;
                font-size: 13px;
            }
        """)

    def update_results(self, text):
        """Actualiza la lista de resultados según lo escrito"""
        self.result_list.clear()
        if text:
            if isinstance(self.data, list):
                # Lista simple
                matches = [item for item in self.data if text.lower() in item.lower()]
                for item in matches:
                    self.result_list.addItem(item)

            elif isinstance(self.data, dict):
                # Diccionario JSON: mostrar key y value
                matches = [(k, v) for k, v in self.data.items() if text.lower() in v.lower()]
                for k, v in matches:
                    item = QListWidgetItem(f"{k} - {v}")
                    item.setData(Qt.ItemDataRole.UserRole, (k, v))
                    self.result_list.addItem(item)

            if self.result_list.count() > 0:
                self.result_list.show()
            else:
                self.result_list.hide()
        else:
            self.result_list.hide()

    def on_item_clicked(self, item):
        """Emite señal con el valor seleccionado"""
        if isinstance(self.data, list):
            self.itemSelected.emit(item.text())
            self.result_list.hide()
        elif isinstance(self.data, dict):
            key, value = item.data(Qt.ItemDataRole.UserRole)
            self.itemSelected.emit((key, value))
            self.result_list.hide()

    def setColors(self, field_color="#ffe6f0", border_color="#f5b8d1", list_color="#fff0f6"):
        """Permite cambiar colores del widget"""
        self.setStyleSheet(f"""
            QLineEdit {{
                background-color: {field_color};
                border: 2px solid {border_color};
                border-radius: 10px;
                padding: 6px;
                font-size: 14px;
            }}
            QListWidget {{
                background-color: {list_color};
                border: 1px solid {border_color};
                border-radius: 8px;
                font-size: 13px;
            }}
        """)


"""
Widget que agrega un CassieButton

"""

class CassieButton(QPushButton):
    def __init__(self, text="Cassie Button", parent=None):
        super().__init__(text, parent)

        # Estilo pastel por defecto
        self.setFont(QFont("Arial", 12))
        self.setStyleSheet("""
            QPushButton {
                background-color: #f8c8dc;
                border: 2px solid #e6a6c9;
                border-radius: 12px;
                padding: 8px 16px;
                color: #4a004a;
            }
            QPushButton:hover {
                background-color: #ffd6e7;
            }
            QPushButton:pressed {
                background-color: #f5b8d1;
            }
        """)

    def setStyleColors(self, bg_color="#f8c8dc", border_color="#e6a6c9",
                       text_color="#4a004a", hover_color="#ffd6e7", pressed_color="#f5b8d1"):
        """Permite cambiar colores del botón dinámicamente"""
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                border: 2px solid {border_color};
                border-radius: 12px;
                padding: 8px 16px;
                color: {text_color};
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {pressed_color};
            }}
        """)

    def setFontStyle(self, font_name="Arial", font_size=12, bold=False):
        """Permite cambiar tipografía del botón"""
        font = QFont(font_name, font_size)
        font.setBold(bold)
        self.setFont(font)



"""
    Ejemplo de como usar los componentes de cassieqt
"""

"""
Widget que crea un carrusel de imagenes

necesitas pasarle las rutas de la s imagenes en formato json

"""

#Creamos un QLabel personalizado que detecta doble clic
class CassieImageLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image_path = None  # Guardamos la ruta de la imagen

    #Método para asignar imagen y guardar la ruta
    def setImage(self, path, size=(200, 150)):
        self.image_path = path
        pixmap = QPixmap(path)
        self.setPixmap(pixmap.scaled(size[0], size[1], Qt.AspectRatioMode.KeepAspectRatio))

    #Evento de doble clic → abrir ventana con imagen grande
    def mouseDoubleClickEvent(self, event):
        if self.image_path:
            self.open_fullscreen()

    #Método para abrir una ventana nueva mostrando la imagen en grande
    def open_fullscreen(self):
        win = QWidget()
        win.setWindowTitle("Vista completa")
        layout = QVBoxLayout(win)

        lbl = QLabel()
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pixmap = QPixmap(self.image_path)
        lbl.setPixmap(pixmap.scaled(800, 600, Qt.AspectRatioMode.KeepAspectRatio))

        layout.addWidget(lbl)
        win.resize(820, 620)
        win.show()

        #Referencia para evitar que se destruya la ventana
        self._fullscreen_window = win


class CassieCarrusel(QWidget):

    #Constructor de la clase
    def __init__(self, data, parent=None):
        super().__init__(parent)

        #Almacenamos los datos y el indice actual
        self.data = data
        self.index = 0

        #Creamos los labels para las imágenes (clicables)
        self.label_prev = CassieImageLabel(self)
        self.label_center = CassieImageLabel(self)
        self.label_next = CassieImageLabel(self)

        # Agregamos bótones de Navegación para el carrusel
        self.btn_prev = CassieButton("⏪ Anterior")
        self.btn_next = CassieButton("Siguiente ⏩")

        # Definimos cuales serán las señales que recibirán los botones
        self.btn_prev.clicked.connect(self.show_prev)
        self.btn_next.clicked.connect(self.show_next)

        #Creamos un layout horizontal para las imágenes
        h_images = QHBoxLayout()
        h_images.addStretch()
        h_images.addWidget(self.label_prev)
        h_images.addWidget(self.label_center)
        h_images.addWidget(self.label_next)
        h_images.addStretch()

        #Creamos un layout horizontal y añadimos los botones
        h_buttons = QHBoxLayout()
        h_buttons.addStretch()
        h_buttons.addWidget(self.btn_prev)
        h_buttons.addWidget(self.btn_next)
        h_buttons.addStretch()

        #Creamos un layout vertical y añadimos el layout de imágenes y el de botones
        v_layout = QVBoxLayout()
        v_layout.addLayout(h_images)
        v_layout.addLayout(h_buttons)

        #Establecemos el layout principal en el Widget
        self.setLayout(v_layout)

        # Mostramos las imágenes iniciales
        self.update_images()

    #Método para actualizar las imágenes mostradas
    def update_images(self):
        if not self.data:
            self.label_center.setText("No hay imágenes")
            return

        #Calculamos los índices de la imagen previa y la siguiente
        prev_index = (self.index - 1) % len(self.data)
        next_index = (self.index + 1) % len(self.data)

        #Asignamos imágenes a los labels
        self.label_prev.setImage(self.data[prev_index], size=(120, 90))
        self.label_center.setImage(self.data[self.index], size=(400, 300))
        self.label_next.setImage(self.data[next_index], size=(120, 90))

    #Método para mostrar la imagen anterior
    def show_prev(self):
        self.index = (self.index - 1) % len(self.data)
        self.update_images()

    #Método para mostrar la imagen siguiente
    def show_next(self):
        self.index = (self.index + 1) % len(self.data)
        self.update_images()

    #Método para cambiar el color de los botones
    def setStyleColors(self, bg_color="#f8c8dc", border_color="#e6a6c9",
                       text_color="#4a004a", hover_color="#ffd6e7", pressed_color="#f5b8d1"):

        self.btn_prev.setStyleColors(bg_color=bg_color,border_color=border_color,text_color=text_color,hover_color=hover_color,pressed_color=pressed_color)
        self.btn_next.setStyleColors(bg_color=bg_color,border_color=border_color,text_color=text_color,hover_color=hover_color,pressed_color=pressed_color)




if __name__ == "__main__":

    #Creamos una aplicación de pyqt6
    app = QApplication(sys.argv)

    # Creamos una ventana principal con un layaut vertical central
    main = QWidget()
    main.setWindowTitle("Cassieqt widgets 🌸")
    layout = QVBoxLayout(main)

    

    #Creamos un carrusel de iḿagenes con CassieCarrusel

    imagesData = [

    "/home/cassie/Descargas/fondo cassie.png",
    "/home/cassie/Descargas/fondo.png",
    "/home/cassie/Descargas/micplay.png"

    ]

    cassieCarrusel = CassieCarrusel(imagesData)
    layout.addWidget(cassieCarrusel)



    #creammos un widget CassieSearch y le cargamos los datos

    data = {

        "001" : "Manzana",
        "002" : "Pera",
        "003" : "uva",
        "004" : "Fresa"

    }

    search = CassieSearch(data = data)

    #Creamos un label el cual mostrara el item seleccionado

    chooseOneItem = QLabel("Selecciona un elemento de la lista...")
    chooseOneItem.setStyleSheet("font-size: 14px; color: #a64d79;")

    #Cassie search necesita que le pases una funcion que recibira el valor corespondiente un texto o un diccinario json

    def on_selected(value):

        if isinstance(value, tuple):
            # Caso dict → (key, value)
            key, val = value
            chooseOneItem.setText(f"Seleccionaste: {key} → {val}")
        else:
            # Caso lista → texto
            chooseOneItem.setText(f"Seleccionaste: {value}")


    search.itemSelected.connect(on_selected)

   

    #Añadimos CassieSearch al layout y el label de texto seleccionado
    layout.addWidget(search)
    layout.addWidget(chooseOneItem)



    #Creamos un CassieButton y lo mostramos
    label = QLabel("CassieButton")
    label.setStyleSheet("font-size: 14px; color: #a64d79;")
    
    #Botón por defecto
    button = CassieButton("Botón por defecto")
    button.clicked.connect(lambda: label.setText("¡CassieButton rosa presionado!"))

    # Botón con estilo personalizado
    button2 = CassieButton("Botón personalizado")
    button2.setStyleColors(bg_color="#cce7ff", border_color="#99ccff",
                           text_color="#003366", hover_color="#b3d9ff", pressed_color="#80bfff")
    button2.setFontStyle("Verdana", 11, bold=True)
    button2.clicked.connect(lambda: label.setText("¡CassieButton azul fue presionado!"))

    # Añadir al layout
    layout.addWidget(button)
    layout.addWidget(button2)
    layout.addWidget(label)

    main.resize(500, 800)
    main.show()

    sys.exit(app.exec())
