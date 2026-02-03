#SEGUNDA INTEGRAL
#By: Angel A. Higuera

#Librerías y modulos
#Importa modulos del sistema para manejo de rutas y ejecucion.
import sys
import os
#Importa libreria numerica para calculos matematicos.
import numpy as np
#Importa pandas para manejo de datos (aunque no nos enfocamos en excel aqui).
import pandas as pd
#Importa la funcion 'quad' de scipy para realizar integracion numerica.
from scipy.integrate import quad

#Importa los componentes necesarios de la interfaz grafica PyQt6.
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton,
                             QMessageBox, QFrame, QStackedLayout, QSizePolicy,
                             QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
                             QFileDialog)
#Importa clases para manejo de eventos, geometria y animaciones.
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect
#Importa clases para manejo de fuentes e imagenes.
from PyQt6.QtGui import QFont, QPixmap, QIcon


# ------------------------------------------------
# FUNCIÓN PARA PYINSTALLER
# ------------------------------------------------
def resource_path(relative_path):
    #Intenta obtener la ruta base temporal si se ejecuta como empaquetado.
    try:
        base_path = sys._MEIPASS
    #Si falla (ejecucion normal), usa la ruta absoluta actual.
    except Exception:
        base_path = os.path.abspath(".")
    #Devuelve la ruta completa al recurso.
    return os.path.join(base_path, relative_path)


# ------------------------------------------------
# FUNCIÓN MATEMÁTICA
# ------------------------------------------------
def normal_estandar(z):
    #Calcula el coeficiente de la funcion de densidad (1 sobre raiz de 2pi).
    coeficiente = 1 / (np.sqrt(2 * np.pi))
    #Calcula el exponente de la funcion (-z cuadrado sobre 2).
    exponente = -0.5 * (z ** 2)
    #Retorna el valor de la funcion evaluada en z.
    return coeficiente * np.exp(exponente)


class VentanaAzul(QMainWindow):
    def __init__(self):
        #Inicializa el constructor de la clase base QMainWindow.
        super().__init__()

        #Establece el titulo de la ventana.
        self.setWindowTitle("Segunda integral -Incremento B: By: Angel A. Higuera")

        #Define la geometria inicial de la ventana (posicion y tamano).
        self.rectangulo_delgado = QRect(555, 50, 380, 700)
        #Aplica la geometria a la ventana.
        self.setGeometry(self.rectangulo_delgado)

        # --- ANIMACIÓN ---
        self.animacion = QPropertyAnimation(self, b"geometry")
        self.animacion.setDuration(500)
        self.animacion.setEasingCurve(QEasingCurve.Type.InOutQuart)

        # --- ESTILOS (Omitidos comentarios de diseño por solicitud) ---
        self.setStyleSheet("""
            QMainWindow { 
                background-color: #E3F2FD; 
            }
            QFrame#ContenedorPrincipal {
                background-color: #ffffff;
                border: 4px solid #1565C0;
                border-radius: 20px;
            }
            QLabel {
                color: #0D47A1; font-family: 'Segoe UI', Arial; font-weight: bold; font-size: 14px;
            }
            QLabel#Titulo {
                font-size: 22px; color: #1565C0;
            }
            QLineEdit {
                padding: 8px; border: 2px solid #64B5F6; border-radius: 6px;
                background-color: #F1F8E9; color: #333; font-size: 14px;
            }
            QLineEdit:focus { border: 2px solid #1976D2; background-color: #fff; }

            QPushButton {
                background-color: #1976D2; color: white; border-radius: 10px;
                padding: 12px; font-weight: bold; font-size: 15px;
            }
            QPushButton:hover { background-color: #0D47A1; }

            QPushButton#BtnRegresar { 
                background-color: #546E7A; 
                margin-top: 10px;
            }

            /* ESTILO PARA EL BOTÓN EXCEL (VERDE) */
            QPushButton#BtnExcel {
                background-color: #2E7D32; /* Verde Excel */
                margin-top: 10px;
            }
            QPushButton#BtnExcel:hover {
                background-color: #1B5E20;
            }

            /* --- ESTILOS DE LA TABLA --- */
            QTableWidget {
                background-color: #FFFFFF;
                border: 1px solid #90CAF9;
                gridline-color: #E0E0E0;
                font-size: 14px;
                color: #333333; 
            }
            QTableWidget::item {
                padding: 5px;
                color: #333333; 
            }
            QTableWidget::item:selected {
                background-color: #BBDEFB;
                color: #000000;
            }
            QHeaderView::section {
                background-color: #1565C0;
                color: #FFFFFF; 
                font-weight: bold;
                padding: 6px;
                border: none;
            }

            /* Estilo del Footer */
            QLabel#FooterAlumno {
                color: #546E7A; font-size: 12px; font-weight: normal; margin-top: 5px;
            }
        """)

        # Widget central
        #Crea el widget central que contendra todo.
        widget_central = QWidget()
        #Establece el widget central en la ventana principal.
        self.setCentralWidget(widget_central)

        #Crea el layout principal vertical.
        layout_principal = QVBoxLayout(widget_central)
        layout_principal.setContentsMargins(15, 15, 15, 10)

        # 1. CONTENEDOR TIPO TARJETA
        #Crea el frame que actuara como contenedor visual.
        self.frame_contenido = QFrame()
        self.frame_contenido.setObjectName("ContenedorPrincipal")
        self.frame_contenido.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        #Anade el frame al layout principal.
        layout_principal.addWidget(self.frame_contenido)

        # 2. FOOTER (ALUMNO)
        lbl_alumno = QLabel("Alumno: Higuera Pineda Angel Abraham")
        lbl_alumno.setObjectName("FooterAlumno")
        lbl_alumno.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principal.addWidget(lbl_alumno)

        # --- STACK DE PÁGINAS ---
        #Crea un layout de tipo Stack para manejar multiples vistas (Input y Tabla).
        self.layout_stack = QStackedLayout(self.frame_contenido)
        self.layout_stack.setContentsMargins(20, 20, 20, 20)

        # ==========================================
        # PÁGINA 1: INPUT
        # ==========================================
        #Crea el widget para la pagina de entrada de datos.
        self.pag_input = QWidget()
        layout_input = QVBoxLayout(self.pag_input)
        layout_input.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        container_p1 = QWidget()
        container_p1.setFixedWidth(300)
        l_p1 = QVBoxLayout(container_p1)
        l_p1.setSpacing(15)

        lbl_titulo = QLabel("Segunda integral\nCon aumento")
        lbl_titulo.setObjectName("Titulo")
        lbl_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        l_p1.addWidget(lbl_titulo)

        # --- IMAGEN ---
        lbl_imagen = QLabel()
        lbl_imagen.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ruta_img = resource_path("assets/Integral2.png")
        pix = QPixmap(ruta_img)
        if not pix.isNull():
            pix = pix.scaled(250, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            lbl_imagen.setPixmap(pix)
        else:
            lbl_imagen.setText("No imagen")
        l_p1.addWidget(lbl_imagen)

        l_p1.addSpacing(20)
        l_p1.addWidget(QLabel("Ingrese aumento de 'b':"))

        #Crea el campo de texto para ingresar el paso (step).
        self.input_step = QLineEdit()
        self.input_step.setPlaceholderText("Ej. 0.02")
        self.input_step.setAlignment(Qt.AlignmentFlag.AlignCenter)
        l_p1.addWidget(self.input_step)

        l_p1.addSpacing(20)

        #Crea el boton para iniciar el calculo.
        self.btn_calcular = QPushButton("Calcular y Ver Tabla")
        #Conecta la senal clicked con el metodo de calculo.
        self.btn_calcular.clicked.connect(self.calcular_y_maximizar)
        l_p1.addWidget(self.btn_calcular)

        l_p1.addStretch()
        layout_input.addWidget(container_p1)

        # ==========================================
        # PÁGINA 2: TABLA DE RESULTADOS
        # ==========================================
        #Crea el widget para la pagina de resultados.
        self.pag_tabla = QWidget()
        layout_tabla = QVBoxLayout(self.pag_tabla)

        lbl_res_titulo = QLabel("Tabla de Resultados")
        lbl_res_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_tabla.addWidget(lbl_res_titulo)

        # Tabla
        #Inicializa la tabla para mostrar los datos.
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(2)
        #Define los encabezados de la tabla.
        self.tabla.setHorizontalHeaderLabels(["Valor de b (Límite Sup.)", "Probabilidad Acumulada"])
        header = self.tabla.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla.setAlternatingRowColors(True)
        self.tabla.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        layout_tabla.addWidget(self.tabla)

        # --- BOTONES INFERIORES ---
        container_btn = QWidget()
        l_btn = QHBoxLayout(container_btn)
        l_btn.setSpacing(10)  # Espacio entre botones

        # Botón Regresar
        #Crea boton para volver al inicio.
        self.btn_volver = QPushButton("← Regresar")
        self.btn_volver.setObjectName("BtnRegresar")
        #Conecta con el metodo para restaurar la vista.
        self.btn_volver.clicked.connect(self.regresar_y_restaurar)
        l_btn.addWidget(self.btn_volver)

        # --- NUEVO: BOTÓN EXCEL ---
        self.btn_excel = QPushButton("Obtener Excel")
        self.btn_excel.setObjectName("BtnExcel")  # ID para ponerlo verde en CSS
        self.btn_excel.clicked.connect(self.exportar_excel)
        l_btn.addWidget(self.btn_excel)

        layout_tabla.addWidget(container_btn)

        # Añadir páginas
        #Anade las paginas creadas al stack layout.
        self.layout_stack.addWidget(self.pag_input)
        self.layout_stack.addWidget(self.pag_tabla)

    def calcular_y_maximizar(self):
        #Inicia bloque de manejo de errores para validacion.
        try:
            #Obtiene el texto del input y reemplaza comas por puntos.
            step_txt = self.input_step.text().replace(',', '.')
            #Verifica si el campo esta vacio.
            if not step_txt:
                #Muestra advertencia si no hay datos.
                QMessageBox.warning(self, "Error", "Ingresa un valor.")
                return

            #Convierte el valor ingresado a flotante.
            step = float(step_txt)
            #Valida que el paso sea un numero positivo.
            if step <= 0:
                #Muestra advertencia si el valor es invalido.
                QMessageBox.warning(self, "Error", "El aumento debe ser mayor a 0.")
                return

            # CÁLCULOS
            #Inicializa la lista para los valores de 'b'.
            valores_b = []
            #Define el limite inferior de integracion.
            curr = -6.0
            #Define el limite superior maximo.
            end = 6.0

            #Genera la secuencia de valores desde -6 hasta 6 con el paso dado.
            while curr <= end + 0.0001:
                valores_b.append(curr)
                curr += step

            #Resetea las filas de la tabla.
            self.tabla.setRowCount(0)
            #Establece el numero de filas segun los datos generados.
            self.tabla.setRowCount(len(valores_b))

            row = 0
            #Itera sobre cada valor limite generado.
            for b_val in valores_b:
                #Calcula la integral definida usando 'quad' (metodo numerico).
                res, _ = quad(normal_estandar, -6, b_val)

                #Crea el item para la columna del valor b.
                item_b = QTableWidgetItem(f"{b_val:.2f}")
                #Crea el item con el resultado de la integral formateado a alta precision.
                item_res = QTableWidgetItem(f"{res:.15f}")

                item_b.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item_res.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                #Inserta los items en la tabla en la fila correspondiente.
                self.tabla.setItem(row, 0, item_b)
                self.tabla.setItem(row, 1, item_res)
                row += 1

            #Cambia la vista visible a la tabla de resultados.
            self.layout_stack.setCurrentIndex(1)

            # ANIMAR MAXIMIZACIÓN
            pos_actual = self.geometry()
            self.rectangulo_delgado = QRect(pos_actual.x(), pos_actual.y(), 380, 700)

            screen_geo = self.screen().availableGeometry()
            x_final = screen_geo.x() + 50
            y_final = screen_geo.y() + 50
            w_final = screen_geo.width() - 100
            h_final = screen_geo.height() - 100

            rect_grande = QRect(x_final, y_final, w_final, h_final)

            self.animacion.setStartValue(self.rectangulo_delgado)
            self.animacion.setEndValue(rect_grande)
            self.animacion.start()

        #Captura error si la conversion a float falla.
        except ValueError:
            QMessageBox.warning(self, "Error", "Ingresa un número válido.")

    def exportar_excel(self):
        # 1. Verificar si hay datos
        if self.tabla.rowCount() == 0:
            QMessageBox.warning(self, "Aviso", "No hay datos para exportar.")
            return

        # 2. Abrir cuadro de diálogo para guardar
        archivo, _ = QFileDialog.getSaveFileName(self, "Guardar Resultados", "", "Archivos Excel (*.xlsx)")

        if archivo:
            if not archivo.endswith('.xlsx'):
                archivo += '.xlsx'

            try:
                # 3. Recolectar datos de la tabla
                datos = []
                for row in range(self.tabla.rowCount()):
                    # Obtener textos de la tabla
                    valor_b = self.tabla.item(row, 0).text()
                    valor_res = self.tabla.item(row, 1).text()

                    # LÓGICA IMPORTANTE:
                    # 'No.': row + 1 crea la numeración 1, 2, 3...
                    # 'Probabilidad': NO usamos float(valor_res).
                    # Usamos el texto directo para que Excel muestre los 70 decimales
                    # y no los trunque a notación científica.

                    datos.append({
                        "No.": row + 1,  # <--- Agregado: Enumeración
                        "Límite Sup. (b)": float(valor_b),
                        "Probabilidad Acumulada": valor_res  # <--- Se guarda como STRING para mantener precisión visual
                    })

                # 4. Crear DataFrame y guardar con Pandas
                df = pd.DataFrame(datos)

                # Escribimos el Excel
                df.to_excel(archivo, index=False)

                QMessageBox.information(self, "Éxito", f"Archivo guardado correctamente en:\n{archivo}")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo guardar el archivo:\n{str(e)}")

    def regresar_y_restaurar(self):
        #Cambia el indice del stack para mostrar la pagina de input (0).
        self.layout_stack.setCurrentIndex(0)
        #Pone el foco en el campo de texto.
        self.input_step.setFocus()
        #Selecciona todo el texto para facilitar la reescritura.
        self.input_step.selectAll()

        #Prepara la animacion para volver al tamano original.
        self.animacion.setStartValue(self.geometry())
        self.animacion.setEndValue(self.rectangulo_delgado)
        #Inicia la animacion.
        self.animacion.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaAzul()
    ventana.show()
    sys.exit(app.exec())