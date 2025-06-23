""" 
Simulador de cifrados clásicos vs modernos
"""

import time
import string
import random
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from collections import Counter
import numpy as np
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import hashlib

class CifradorCesar:
    """Implementación del cifrado César"""
    
    def __init__(self, desplazamiento=3):
        self.desplazamiento = desplazamiento
        
    def cifrar(self, texto):
        resultado = ""
        for char in texto:
            if char.isalpha():
                ascii_offset = 65 if char.isupper() else 97
                resultado += chr((ord(char) - ascii_offset + self.desplazamiento) % 26 + ascii_offset)
            else:
                resultado += char
        return resultado
    
    def descifrar(self, texto_cifrado):
        self.desplazamiento = -self.desplazamiento
        resultado = self.cifrar(texto_cifrado)
        self.desplazamiento = -self.desplazamiento
        return resultado
    
    def fuerza_bruta(self, texto_cifrado):
        """Ataque de fuerza bruta probando todas las claves posibles"""
        resultados = []
        for i in range(26):
            temp_cipher = CifradorCesar(i)
            descifrado = temp_cipher.descifrar(texto_cifrado)
            resultados.append((i, descifrado))
        return resultados

class CifradorVigenere:
    """Implementación del cifrado Vigenère"""
    
    def __init__(self, clave):
        self.clave = clave.upper()
        
    def cifrar(self, texto):
        resultado = ""
        clave_repetida = (self.clave * (len(texto) // len(self.clave) + 1))[:len(texto)]
        
        for i, char in enumerate(texto):
            if char.isalpha():
                ascii_offset = 65 if char.isupper() else 97
                desplazamiento = ord(clave_repetida[i]) - 65
                resultado += chr((ord(char) - ascii_offset + desplazamiento) % 26 + ascii_offset)
            else:
                resultado += char
        return resultado
    
    def descifrar(self, texto_cifrado):
        resultado = ""
        clave_repetida = (self.clave * (len(texto_cifrado) // len(self.clave) + 1))[:len(texto_cifrado)]
        
        for i, char in enumerate(texto_cifrado):
            if char.isalpha():
                ascii_offset = 65 if char.isupper() else 97
                desplazamiento = ord(clave_repetida[i]) - 65
                resultado += chr((ord(char) - ascii_offset - desplazamiento) % 26 + ascii_offset)
            else:
                resultado += char
        return resultado
    
    def analisis_frecuencias(self, texto):
        """Análisis de frecuencias para criptoanálisis"""
        texto_limpio = ''.join([c.upper() for c in texto if c.isalpha()])
        frecuencias = Counter(texto_limpio)
        return frecuencias

class CifradorAES:
    """Implementación de cifrado AES-256"""
    
    def __init__(self):
        self.key = None
        
    def generar_clave(self):
        """Genera una clave AES-256 aleatoria"""
        self.key = get_random_bytes(32)  # 256 bits
        return self.key
    
    def cifrar(self, texto):
        if not self.key:
            self.generar_clave()
            
        cipher = AES.new(self.key, AES.MODE_CBC)
        texto_bytes = texto.encode('utf-8')
        texto_padded = pad(texto_bytes, AES.block_size)
        texto_cifrado = cipher.encrypt(texto_padded)
        return cipher.iv + texto_cifrado  # IV + datos cifrados
    
    def descifrar(self, datos_cifrados):
        if not self.key:
            raise ValueError("No hay clave definida")
            
        iv = datos_cifrados[:16]  # Primeros 16 bytes son el IV
        datos = datos_cifrados[16:]
        
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        texto_descifrado = unpad(cipher.decrypt(datos), AES.block_size)
        return texto_descifrado.decode('utf-8')

class AnalizadorSeguridad:
    """Clase para analizar y comparar la seguridad de los cifrados"""
    
    def __init__(self):
        self.resultados = []
        
    def medir_tiempo_cifrado(self, cifrador, texto, repeticiones=1000):
        """Mide el tiempo de cifrado promedio"""
        tiempos = []
        for _ in range(repeticiones):
            inicio = time.time()
            cifrador.cifrar(texto)
            fin = time.time()
            tiempos.append(fin - inicio)
        return np.mean(tiempos) * 1000  # en milisegundos
    
    def medir_tiempo_descifrado(self, cifrador, texto_cifrado, repeticiones=1000):
        """Mide el tiempo de descifrado promedio"""
        tiempos = []
        for _ in range(repeticiones):
            inicio = time.time()
            if isinstance(cifrador, CifradorAES):
                cifrador.descifrar(texto_cifrado)
            else:
                cifrador.descifrar(texto_cifrado)
            fin = time.time()
            tiempos.append(fin - inicio)
        return np.mean(tiempos) * 1000  # en milisegundos
    
    def calcular_entropia(self, texto):
        """Calcula la entropía de Shannon del texto"""
        frecuencias = Counter(texto)
        longitud = len(texto)
        entropia = 0
        for freq in frecuencias.values():
            prob = freq / longitud
            if prob > 0:
                entropia -= prob * np.log2(prob)
        return entropia
    
    def analizar_resistencia_fuerza_bruta(self, tipo_cifrado):
        """Calcula la resistencia teórica a ataques de fuerza bruta"""
        if tipo_cifrado == "César":
            return 26  # 26 claves posibles
        elif tipo_cifrado == "Vigenère":
            return 26**5  # Asumiendo clave de 5 caracteres
        elif tipo_cifrado == "AES":
            return 2**256  # 256 bits de clave
        return 0