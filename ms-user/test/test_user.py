import unittest

class TestCRUDUsuario(unittest.TestCase):

    def test_create(self):
        # Crear un nuevo usuario
        usuario = Usuario(name="Juan", last_name= "Juan", password= "1234", email="juan@example.com")

        # Guardar el usuario en la base de datos
        usuario.save()

        # Comprobar que el usuario se ha guardado correctamente
        self.assertEqual(usuario.id, 1) # El primer usuario tiene id=1

    

    def test_update(self):
        # Actualizar los datos de un usuario
        usuario = Usuario.objects.get(id=1)
        usuario.name = "Bruno"
        usuario.last_name = "Romero"
        usuario.save()

        # Comprobar que los datos se han actualizado correctamente
        usuario_actualizado = Usuario.objects.get(id=1)
        self.assertEqual(usuario_actualizado.nombre, "Bruno")

    def test_delete(self):
        # Eliminar un usuario
        usuario = Usuario.objects.get(id=1)
        usuario.delete()

        # Comprobar que el usuario se ha eliminado correctamente
        with self.assertRaises(Usuario.DoesNotExist):
            Usuario.objects.get(id=1)

if __name__ == '__main__':
    unittest.main()