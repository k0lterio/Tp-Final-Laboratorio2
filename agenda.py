import sqlite3
import sys 
import csv
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QListWidget, QVBoxLayout, QListWidgetItem,QMessageBox
from PyQt5 import uic 
  
class MiVentana(QMainWindow): 
    def __init__(self): 
        super().__init__()
        uic.loadUi("agenda.ui",self)
        self.setWindowTitle("Agenda")

        self.codigo = 0

        # conectar a la base de datos
        self.conexion = sqlite3.connect('base.db')
        self.cursor = self.conexion.cursor()

        # Botones 
        self.lista.itemClicked.connect(self.on_ver)
        self.nuevo.clicked.connect(self.on_nuevo)
        self.editar.clicked.connect(self.on_editar)
        self.guardar.clicked.connect(self.on_guardar)
        self.cancelar.clicked.connect(self.on_cancelar)
        self.eliminar.clicked.connect(self.on_eliminar)

        # Cargar contactos a la lista
        self.cursor.execute('select nombre from contactos')
        nombres = self.cursor.fetchall()
        for i in nombres:
            self.lista.addItem(i[0])

        # Botones deshabilitados
        self.editar.setEnabled(False)
        self.guardar.setEnabled(False)
        self.cancelar.setEnabled(False)
        self.eliminar.setEnabled(False)
    
    #Limpiar LineEdits
    def limpiar_Clear(self):
        self.nombre.clear()
        self.apellido.clear()
        self.email.clear()
        self.telefono.clear()
        self.direccion.clear()
        self.nacimiento.clear()
        self.altura.clear()
        self.peso.clear()

    #Deshabilitar LineEdit    
    def desac_lineEdit(self):
        self.nombre.setDisabled(True)
        self.apellido.setDisabled(True)
        self.email.setDisabled(True)
        self.telefono.setDisabled(True)
        self.direccion.setDisabled(True)
        self.nacimiento.setDisabled(True)
        self.altura.setDisabled(True)
        self.peso.setDisabled(True)

    def on_ver(self, actual):
        self.valor = actual.text()
        
        # Botones habilitados/deshabilitados
        self.nuevo.setEnabled(True)
        self.editar.setEnabled(True)
        self.guardar.setEnabled(False)
        self.cancelar.setEnabled(False)
        self.eliminar.setEnabled(True)
        
        #LineEdit deshabilitados
        MiVentana.desac_lineEdit(self)
        
        self.cursor.execute('select * from contactos')    
        contactos = self.cursor.fetchall()
        self.listar = []
        for contacto in contactos:
            self.listar = list(contacto)
            if self.listar[1] == self.valor:
                self.nombre.setText(self.listar[1])
                self.apellido.setText(self.listar[2])
                self.email.setText(self.listar[3])
                self.telefono.setText(self.listar[4])
                self.direccion.setText(self.listar[5])                        
                self.nacimiento.setText(self.listar[6])
                self.altura.setText(str(self.listar[7]))
                self.peso.setText(str(self.listar[8]))
        self.codigo = 0

    def on_editar(self):
        # Botones habilitados/deshabilitado
        self.nuevo.setEnabled(False)
        self.guardar.setEnabled(True)
        self.cancelar.setEnabled(True)
        self.eliminar.setEnabled(False)
        #Habilitar LineEdit
        self.nombre.setEnabled(True)
        self.apellido.setEnabled(True)
        self.email.setEnabled(True)
        self.telefono.setEnabled(True)
        self.direccion.setEnabled(True)
        self.nacimiento.setEnabled(True)
        self.altura.setEnabled(True)
        self.peso.setEnabled(True)
        self.codigo = 1

    def on_guardar(self):
        # Botones habilitados
        self.nuevo.setEnabled(True)
        self.editar.setEnabled(False)
        self.cancelar.setEnabled(False)
        self.guardar.setEnabled(False)

        if self.codigo == 0:
            self.nombre.setEnabled(True)
            self.apellido.setEnabled(True)
            self.email.setEnabled(True)
            self.telefono.setEnabled(True)
            self.direccion.setEnabled(True)
            self.nacimiento.setEnabled(True)
            self.altura.setEnabled(True)
            self.peso.setEnabled(True)
        
            nombre = self.nombre.text()
            apellido = self.apellido.text()
            email = self.email.text()
            telefono = self.telefono.text()
            direccion = self.direccion.text()
            nacimiento = self.nacimiento.text()
            altura = self.altura.text()
            peso = self.peso.text()

            self.cursor.execute('''
                insert into contactos(nombre,apellido,email,telefono,direccion,fecha_nacimiento,altura,peso)
                VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}')'''.format(nombre,apellido,email,telefono,direccion,nacimiento,altura,peso))
            self.conexion.commit()
            
            #Limpiar LineEdit
            MiVentana.limpiar_Clear(self)

            #Desactivar LineEdit
            MiVentana.desac_lineEdit(self) 
            # Actualizar lista
            self.lista.clear()
            self.cursor.execute('select nombre from contactos')
            nombres = self.cursor.fetchall()
            for i in nombres:
                self.lista.addItem(i[0])
        else:
            nombre = self.nombre.text()
            apellido = self.apellido.text()
            email = self.email.text()
            telefono = self.telefono.text()
            direccion = self.direccion.text()
            nacimiento = self.nacimiento.text()
            altura = self.altura.text()
            peso = self.peso.text()

            self.cursor.execute('select id_datos from contactos where nombre=?', (self.valor,))
            id = self.cursor.fetchall()
            id = list(id)
            self.cursor.execute(" update contactos set nombre='"+nombre+"', apellido='"+apellido+"', email='"+email+"', telefono='"+telefono+"', direccion='"+direccion+"', fecha_nacimiento='"+nacimiento+"', altura='"+altura+"', peso='"+peso+"' where id_datos = ?" ,(id[0][0],))          
            self.conexion.commit()

            #Deshabilitar LineEdit
            MiVentana.desac_lineEdit(self)

            #Limpiar LineEdit
            MiVentana.limpiar_Clear(self)
            
            #Actualizar lista
            self.lista.clear()    
            self.cursor.execute('select nombre from contactos')
            nombres = self.cursor.fetchall()
            for i in nombres:
                self.lista.addItem(i[0])

    def on_nuevo(self):
        # Botones habilitados/deshabilitados
        self.editar.setEnabled(False)
        self.eliminar.setEnabled(False)
        self.cancelar.setEnabled(True)
        self.guardar.setEnabled(True)
        # Limpiar LineEdit
        MiVentana.limpiar_Clear(self)
        
        # Habilitar LineEdit
        self.nombre.setEnabled(True)
        self.apellido.setEnabled(True)
        self.email.setEnabled(True)
        self.telefono.setEnabled(True)
        self.direccion.setEnabled(True)
        self.nacimiento.setEnabled(True)
        self.altura.setEnabled(True)
        self.peso.setEnabled(True)
        self.codigo = 0

    def on_eliminar(self):
        msg = QMessageBox()
        msg.setWindowTitle("Eliminar Contacto")
        msg.setText("¿Desea eliminar el contacto?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        resultado = msg.exec()
        if resultado == QMessageBox.Yes:
            self.cursor.execute('select nombre from contactos')
            dato = self.cursor.fetchall()
            for i in dato:
                if i[0] == self.valor:
                    self.cursor.execute('delete from contactos where nombre =? ', (i[0],))
            self.conexion.commit()
        #Actualizar lista
        self.lista.clear()    
        self.cursor.execute('select nombre from contactos')
        nombres = self.cursor.fetchall()
        for i in nombres:
            self.lista.addItem(i[0])
        #Limpiar LineEdit
        MiVentana.limpiar_Clear(self)
        
        #Botones habilitados/deshabilitados
        self.nuevo.setEnabled(True)
        self.editar.setEnabled(False)
        self.guardar.setEnabled(False)
        self.eliminar.setEnabled(False)

    def on_cancelar(self):
        #Limpiar LineEdit
        MiVentana.limpiar_Clear(self)
        
        #Deshabilitar LineEdit
        MiVentana.desac_lineEdit(self)
        self.nuevo.setEnabled(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MiVentana()
    window.desac_lineEdit()
    window.limpiar_Clear()
    window.show() 
    sys.exit(app.exec_()) 