#Primera integral
#By: Angel A. Higuera

#Librerías y modulos
import sys
import os
import numpy as np
#Importa la funcion quad de scipy para la integracioan numerica.
from scipy.integrate import quad
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QMessageBox, QFrame, QStackedLayout, QSizePolicy)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect
from PyQt6.QtGui import QFont, QPixmap


# ------------------------------------------------
# FUNCIÓN CLAVE PARA PYINSTALLER
# ------------------------------------------------
def resource_path(relative_path):
    """ Obtiene la ruta absoluta al recurso, funciona para dev y para PyInstaller """
    #Intenta obtener la ruta temporal de extraccion (_MEIPASS).
    try:
        # PyInstaller crea una carpeta temporal y guarda la ruta en _MEIPASS
        base_path = sys._MEIPASS
    #Si falla (modo desarrollo), usa la ruta absoluta actual.
    except Exception:
        base_path = os.path.abspath(".")

    #Retorna la ruta unida compatible con el OS.
    return os.path.join(base_path, relative_path)


# ------------------------------------------------

# Función matemática
def funcion_normal(x, u, f):
    #Calcula el coeficiente de normalizacion usando la desviacion (f).
    coeficiente = 1 / (f * np.sqrt(2 * np.pi))
    #Calcula el exponente cuadratico normalizado.
    exponente = -0.5 * ((x - u) / f) ** 2
    #Retorna el valor de la densidad de probabilidad.
    return coeficiente * np.exp(exponente)


class VentanaModerna(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Primera integral_con variables: By: Angel A Higuera")

        # Guardamos la geometría "Delgada" por defecto
        self.rectangulo_delgado = QRect(555, 50, 420, 700)
        self.setGeometry(self.rectangulo_delgado)

        # --- CONFIGURACIÓN DE ANIMACIÓN ---
        self.animacion = QPropertyAnimation(self, b"geometry")
        self.animacion.setDuration(400)
        self.animacion.setEasingCurve(QEasingCurve.Type.OutCubic)

        # --- ESTILOS (Omitidos comentarios de diseño) ---
        self.setStyleSheet("""
            QMainWindow { 
                background-color: #ef9a9a; 
            }
            QFrame#ContenedorPrincipal {
                background-color: #ffffff;
                border: 4px solid #c62828;
                border-radius: 20px;
            }
            QLabel {
                color: #b71c1c; font-family: 'Segoe UI', Arial; font-weight: bold; font-size: 13px;
            }
            QLineEdit {
                padding: 8px; border: 2px solid #ef5350; border-radius: 6px;
                background-color: #ffebee; color: #333; font-size: 14px;
            }
            QLineEdit:focus { border: 2px solid #d32f2f; background-color: #fff; }
            QPushButton {
                background-color: #d32f2f; color: white; border-radius: 10px;
                padding: 12px; font-weight: bold; font-size: 15px;
            }
            QPushButton:hover { background-color: #b71c1c; }
            QPushButton#BtnRegresar { 
                background-color: #555; 
                margin-top: 5px; 
            }
        """)

        widget_central = QWidget()
        self.setCentralWidget(widget_central)

        layout_principal = QVBoxLayout(widget_central)
        layout_principal.setContentsMargins(15, 15, 15, 15)

        # --- CONTENEDOR PRINCIPAL FLEXIBLE ---
        self.frame_contenido = QFrame()
        self.frame_contenido.setObjectName("ContenedorPrincipal")
        self.frame_contenido.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout_principal.addWidget(self.frame_contenido)

        #Inicializa el gestor de paginas (Stack) para navegacion.
        self.layout_stack = QStackedLayout(self.frame_contenido)
        self.layout_stack.setContentsMargins(20, 20, 20, 20)

        # ---------------------------------------------
        # PÁGINA 1: DATOS
        # ---------------------------------------------
        self.pagina_formulario = QWidget()
        layout_pag1_base = QVBoxLayout(self.pagina_formulario)
        layout_pag1_base.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout_pag1_base.setContentsMargins(0, 0, 0, 0)

        self.contenedor_inputs = QWidget()
        self.contenedor_inputs.setFixedWidth(320)

        layout_form = QVBoxLayout(self.contenedor_inputs)
        layout_form.setSpacing(10)
        layout_form.setContentsMargins(0, 0, 0, 0)

        lbl_titulo = QLabel("Operaciones")
        lbl_titulo.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        lbl_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_form.addWidget(lbl_titulo)

        # --- CARGAR IMAGEN DESDE ASSETS ---
        lbl_imagen = QLabel()
        lbl_imagen.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Usamos la función resource_path para encontrar el archivo
        # ya sea en la carpeta o dentro del .exe (logica de rutas).
        ruta_imagen = resource_path("assets/integral0.webp")

        #Carga la imagen en un objeto Pixmap.
        pixmap = QPixmap(ruta_imagen)

        #Verifica si la imagen se cargo correctamente.
        if not pixmap.isNull():
            pixmap = pixmap.scaled(300, 100, Qt.AspectRatioMode.KeepAspectRatio,
                                   Qt.TransformationMode.SmoothTransformation)
            lbl_imagen.setPixmap(pixmap)
        else:
            # Texto de respaldo si no encuentra la imagen
            lbl_imagen.setText("(Imagen no encontrada)")

        layout_form.addWidget(lbl_imagen)

        # Inputs
        layout_form.addWidget(QLabel("Media (u):"))
        self.input_u = QLineEdit()
        self.input_u.setPlaceholderText("Ej. 0")
        layout_form.addWidget(self.input_u)

        layout_form.addWidget(QLabel("Desviación Estándar (f):"))
        self.input_f = QLineEdit()
        self.input_f.setPlaceholderText("Ej. 1")
        layout_form.addWidget(self.input_f)

        layout_limites_lbl = QHBoxLayout()
        layout_limites_lbl.addWidget(QLabel("Límite Inferior (a):"))
        layout_limites_lbl.addWidget(QLabel("Límite Superior (b):"))
        layout_form.addLayout(layout_limites_lbl)

        layout_limites_input = QHBoxLayout()
        self.input_a = QLineEdit()
        self.input_a.setPlaceholderText("Ej. -1")
        self.input_b = QLineEdit()
        self.input_b.setPlaceholderText("Ej. 1")
        layout_limites_input.addWidget(self.input_a)
        layout_limites_input.addWidget(self.input_b)
        layout_form.addLayout(layout_limites_input)

        layout_form.addSpacing(10)

        #Conecta el boton con el metodo de calculo.
        self.btn_calcular = QPushButton("Calcular Integral")
        self.btn_calcular.clicked.connect(self.calcular)
        layout_form.addWidget(self.btn_calcular)

        self.lbl_resultado = QLabel("")
        self.lbl_resultado.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_resultado.setStyleSheet("font-size: 16px; color: #d32f2f; margin-top: 5px;")
        layout_form.addWidget(self.lbl_resultado)

        self.layout_botones_extra = QHBoxLayout()
        self.btn_ir_grafica = QPushButton("Ver Gráfica →")
        self.btn_ir_grafica.clicked.connect(self.cambiar_a_grafica)
        self.btn_ir_grafica.hide()

        self.btn_limpiar = QPushButton("Reiniciar")
        self.btn_limpiar.setStyleSheet("background-color: #757575;")
        self.btn_limpiar.clicked.connect(self.limpiar)
        self.btn_limpiar.hide()

        self.layout_botones_extra.addWidget(self.btn_limpiar)
        self.layout_botones_extra.addWidget(self.btn_ir_grafica)
        layout_form.addLayout(self.layout_botones_extra)

        layout_form.addStretch()

        lbl_alumno = QLabel("Alumno: Higuera Pineda Angel Abraham")
        lbl_alumno.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_alumno.setStyleSheet("font-size: 10px; color: #999; font-weight: normal;")
        layout_form.addWidget(lbl_alumno)

        layout_pag1_base.addWidget(self.contenedor_inputs)

        # ---------------------------------------------
        # PÁGINA 2: GRÁFICA
        # ---------------------------------------------
        self.pagina_grafica = QWidget()
        layout_graf = QVBoxLayout(self.pagina_grafica)
        layout_graf.setContentsMargins(0, 0, 0, 0)

        #Inicializa la figura de Matplotlib.
        self.figura = Figure(figsize=(5, 4), dpi=100)
        #Crea el canvas que conecta Matplotlib con Qt.
        self.canvas = FigureCanvas(self.figura)
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout_graf.addWidget(self.canvas, 1)

        self.btn_regresar = QPushButton("← Regresar a Datos")
        self.btn_regresar.setObjectName("BtnRegresar")
        self.btn_regresar.clicked.connect(self.regresar_a_form)
        layout_graf.addWidget(self.btn_regresar)

        self.layout_stack.addWidget(self.pagina_formulario)
        self.layout_stack.addWidget(self.pagina_grafica)

        #Variable para almacenar datos temporales entre calculo y grafica.
        self.datos_calculados = None

    def calcular(self):
        try:
            #Valida que todos los campos tengan texto.
            if not all([self.input_u.text(), self.input_f.text(), self.input_a.text(), self.input_b.text()]):
                QMessageBox.warning(self, "Atención", "Llena todos los campos.")
                return

            #Convierte los inputs a flotantes.
            u = float(self.input_u.text())
            f = float(self.input_f.text())
            a = float(self.input_a.text())
            b = float(self.input_b.text())

            #Valida que la desviacion estandar sea positiva.
            if f <= 0:
                QMessageBox.warning(self, "Error", "La desviación (f) debe ser mayor a 0.")
                return

            #Ejecuta la integracion numerica usando quad.
            res, err = quad(funcion_normal, a, b, args=(u, f))
            #Guarda los parametros para usarlos en la grafica.
            self.datos_calculados = (u, f, a, b, res)

            #Muestra el resultado en la etiqueta.
            self.lbl_resultado.setText(f"Resultado: {res:.5f}")
            #Muestra los botones de navegacion.
            self.btn_ir_grafica.show()
            self.btn_limpiar.show()
            self.btn_calcular.hide()

            #Bloquea los inputs para evitar edicion post-calculo.
            self.input_u.setEnabled(False)
            self.input_f.setEnabled(False)
            self.input_a.setEnabled(False)
            self.input_b.setEnabled(False)

        #Captura errores de conversion numerica.
        except ValueError:
            QMessageBox.warning(self, "Error", "Ingresa solo números válidos.")

    def cambiar_a_grafica(self):
        # 1. MAXIMIZAR VENTANA AUTOMÁTICAMENTE
        self.showMaximized()

        #Limpia la figura anterior para evitar sobreposicion.
        self.figura.clear()
        #Anade un subplot a la figura.
        ax = self.figura.add_subplot(111)

        #Desempaqueta los datos calculados previamente.
        u, f, a, b, res = self.datos_calculados

        #Define el rango X para la grafica (media +/- 4 desviaciones).
        x_min = min(u - 4 * f, a - f)
        x_max = max(u + 4 * f, b + f)
        #Genera 1000 puntos para la curva suave.
        x = np.linspace(x_min, x_max, 1000)
        #Evalua la funcion normal en esos puntos.
        y = funcion_normal(x, u, f)

        #Grafica la curva de la distribucion normal.
        ax.plot(x, y, color='#d32f2f', linewidth=2, label=f'Normal ($\\mu$={u}, $\\sigma$={f})')

        #Genera puntos especificos para el area sombreada (entre a y b).
        x_fill = np.linspace(a, b, 500)
        y_fill = funcion_normal(x_fill, u, f)
        #Rellena el area bajo la curva que representa la integral.
        ax.fill_between(x_fill, y_fill, color='#ef5350', alpha=0.3, label=f'Área = {res:.4f}')

        #Dibuja lineas verticales en los limites de integracion.
        ax.axvline(a, color='#b71c1c', linestyle='--')
        ax.axvline(b, color='#b71c1c', linestyle='--')

        #Configura titulos, leyenda y cuadricula.
        ax.set_title('Gráfica de la integral')
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)
        self.figura.tight_layout()

        #Redibuja el canvas con la nueva grafica.
        self.canvas.draw()
        #Cambia la vista a la pagina de la grafica.
        self.layout_stack.setCurrentIndex(1)

    def regresar_a_form(self):
        # 2. RESTAURAR TAMAÑO NORMAL (DELGADO)
        #Restaura la ventana al tamano original.
        self.showNormal()
        #Cambia la vista a la pagina del formulario.
        self.layout_stack.setCurrentIndex(0)

    def limpiar(self):
        #Limpia todos los campos de texto.
        self.input_u.clear();
        self.input_f.clear();
        self.input_a.clear();
        self.input_b.clear()
        #Resetea la etiqueta de resultado.
        self.lbl_resultado.setText("")
        #Habilita nuevamente los inputs para edicion.
        self.input_u.setEnabled(True);
        self.input_f.setEnabled(True)
        self.input_a.setEnabled(True);
        self.input_b.setEnabled(True)
        #Oculta los botones secundarios y muestra el de calcular.
        self.btn_ir_grafica.hide();
        self.btn_limpiar.hide();
        self.btn_calcular.show()
        #Pone el foco en el primer input.
        self.input_u.setFocus()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaModerna()
    ventana.show()
    sys.exit(app.exec())