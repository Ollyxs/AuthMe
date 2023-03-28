import base64

text = input("Ingrese el texto a codificar en Base32: ")

# Codificar el texto en Base32
text_encoded = base64.b32encode(text.encode('ascii'))

# Decodificar el texto de Base32 de nuevo a texto
text_decoded = base64.b32decode(text_encoded).decode('ascii')

print("Texto original: ", text)
print("Texto codificado en Base32: ", text_encoded)