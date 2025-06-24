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

def generar_dataset_prueba():
    """Genera un dataset de textos de prueba"""
    textos = [
        "En un lugar de la Mancha, de cuyo nombre no quiero acordarme, no ha mucho tiempo que vivía un hidalgo de los de lanza en astillero, adarga antigua, rocín flaco y galgo corredor.",
        "Había una vez en un reino muy lejano una princesa que vivía en un castillo encantado rodeado de dragones y criaturas mágicas que protegían un gran tesoro.",
        "La ciberseguridad es fundamental en el mundo moderno donde los datos personales y la información confidencial requieren protección constante contra amenazas digitales.",
        "Colombia es un país diverso con múltiples regiones geográficas que incluyen la costa Caribe, la región Pacífica, los Andes, la Amazonía y los Llanos Orientales.",
        "Los algoritmos de cifrado han evolucionado significativamente desde los métodos clásicos hasta los sistemas modernos que utilizan matemáticas complejas para garantizar la seguridad."
    ]
    
    # Generar textos de diferentes longitudes
    dataset = []
    for i, texto in enumerate(textos):
        dataset.append({
            'id': i + 1,
            'texto': texto,
            'longitud': len(texto),
            'tipo': f'Texto_{i+1}'
        })
    
    return dataset

def ejecutar_comparativa_completa():
    """Ejecuta la comparativa completa de todos los cifrados"""
    print("SIMULADOR DE CIFRADOS CLÁSICOS VS MODERNOS")
    print("=" * 60)
    
    # Generar dataset
    dataset = generar_dataset_prueba()
    analizador = AnalizadorSeguridad()
    
    # Configurar cifradores
    cesar = CifradorCesar(7)
    vigenere = CifradorVigenere("SEGURIDAD")
    aes = CifradorAES()
    
    resultados_comparativa = []
    
    for datos in dataset:
        texto = datos['texto']
        print(f"\nAnalizando: {datos['tipo']} ({datos['longitud']} caracteres)")
        
        # Análisis César
        inicio = time.time()
        texto_cesar = cesar.cifrar(texto)
        tiempo_cesar_cifrado = (time.time() - inicio) * 1000
        
        inicio = time.time()
        texto_cesar_descifrado = cesar.descifrar(texto_cesar)
        tiempo_cesar_descifrado = (time.time() - inicio) * 1000
        
        entropia_cesar = analizador.calcular_entropia(texto_cesar)
        
        # Análisis Vigenère
        inicio = time.time()
        texto_vigenere = vigenere.cifrar(texto)
        tiempo_vigenere_cifrado = (time.time() - inicio) * 1000
        
        inicio = time.time()
        texto_vigenere_descifrado = vigenere.descifrar(texto_vigenere)
        tiempo_vigenere_descifrado = (time.time() - inicio) * 1000
        
        entropia_vigenere = analizador.calcular_entropia(texto_vigenere)
        
        # Análisis AES
        inicio = time.time()
        texto_aes = aes.cifrar(texto)
        tiempo_aes_cifrado = (time.time() - inicio) * 1000
        
        inicio = time.time()
        texto_aes_descifrado = aes.descifrar(texto_aes)
        tiempo_aes_descifrado = (time.time() - inicio) * 1000
        
        entropia_aes = analizador.calcular_entropia(str(texto_aes))
        
        # Guardar resultados
        resultado = {
            'texto_id': datos['id'],
            'longitud': datos['longitud'],
            'cesar_cifrado_ms': tiempo_cesar_cifrado,
            'cesar_descifrado_ms': tiempo_cesar_descifrado,
            'cesar_entropia': entropia_cesar,
            'vigenere_cifrado_ms': tiempo_vigenere_cifrado,
            'vigenere_descifrado_ms': tiempo_vigenere_descifrado,
            'vigenere_entropia': entropia_vigenere,
            'aes_cifrado_ms': tiempo_aes_cifrado,
            'aes_descifrado_ms': tiempo_aes_descifrado,
            'aes_entropia': entropia_aes
        }
        
        resultados_comparativa.append(resultado)
        
        # Mostrar resultados parciales
        print(f"  César    - Cifrado: {tiempo_cesar_cifrado:.4f}ms | Entropía: {entropia_cesar:.2f}")
        print(f"  Vigenère - Cifrado: {tiempo_vigenere_cifrado:.4f}ms | Entropía: {entropia_vigenere:.2f}")
        print(f"  AES      - Cifrado: {tiempo_aes_cifrado:.4f}ms | Entropía: {entropia_aes:.2f}")
    
    return resultados_comparativa, dataset

def crear_visualizaciones(resultados):
    """Crea visualizaciones comparativas"""
    df = pd.DataFrame(resultados)
    
    # Configurar estilo
    sns.set_style("whitegrid")
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Comparativa de Cifrados: Clásicos vs Modernos', fontsize=16, fontweight='bold')
    
    # Gráfico 1: Tiempos de cifrado
    ax1 = axes[0, 0]
    longitudes = df['longitud']
    ax1.plot(longitudes, df['cesar_cifrado_ms'], 'o-', label='César', color='red', linewidth=2)
    ax1.plot(longitudes, df['vigenere_cifrado_ms'], 's-', label='Vigenère', color='blue', linewidth=2)
    ax1.plot(longitudes, df['aes_cifrado_ms'], '^-', label='AES', color='green', linewidth=2)
    ax1.set_xlabel('Longitud del texto (caracteres)')
    ax1.set_ylabel('Tiempo de cifrado (ms)')
    ax1.set_title('Rendimiento de Cifrado')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Gráfico 2: Entropía
    ax2 = axes[0, 1]
    metodos = ['César', 'Vigenère', 'AES']
    entropias_promedio = [
        df['cesar_entropia'].mean(),
        df['vigenere_entropia'].mean(),
        df['aes_entropia'].mean()
    ]
    colores = ['red', 'blue', 'green']
    bars = ax2.bar(metodos, entropias_promedio, color=colores, alpha=0.7)
    ax2.set_ylabel('Entropía promedio')
    ax2.set_title('Entropía de los Textos Cifrados')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Añadir valores en las barras
    for bar, valor in zip(bars, entropias_promedio):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                f'{valor:.2f}', ha='center', va='bottom')
    
    # Gráfico 3: Resistencia a fuerza bruta (escala logarítmica)
    ax3 = axes[1, 0]
    resistencias = [26, 26**5, 2**128]  # Simplificado para visualización
    resistencias_log = [np.log10(float(r)) for r in resistencias]
    bars3 = ax3.bar(metodos, resistencias_log, color=colores, alpha=0.7)
    ax3.set_ylabel('Log₁₀(Combinaciones posibles)')
    ax3.set_title('Resistencia a Fuerza Bruta')
    ax3.grid(True, alpha=0.3, axis='y')
    
    # Añadir valores en las barras
    for bar, valor in zip(bars3, resistencias_log):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{valor:.1f}', ha='center', va='bottom')
    
    # Gráfico 4: Comparativa general
    ax4 = axes[1, 1]
    categorias = ['Velocidad\n(menor=mejor)', 'Seguridad\n(mayor=mejor)', 'Simplicidad\n(mayor=mejor)']
    
    # Puntuaciones normalizadas (1-10)
    cesar_scores = [10, 1, 10]      # Muy rápido, muy inseguro, muy simple
    vigenere_scores = [8, 3, 6]    # Rápido, poco seguro, moderadamente simple
    aes_scores = [6, 10, 2]        # Moderado, muy seguro, complejo
    
    x = np.arange(len(categorias))
    width = 0.25
    
    ax4.bar(x - width, cesar_scores, width, label='César', color='red', alpha=0.7)
    ax4.bar(x, vigenere_scores, width, label='Vigenère', color='blue', alpha=0.7)
    ax4.bar(x + width, aes_scores, width, label='AES', color='green', alpha=0.7)
    
    ax4.set_ylabel('Puntuación (1-10)')
    ax4.set_title('Evaluación General')
    ax4.set_xticks(x)
    ax4.set_xticklabels(categorias)
    ax4.legend()
    ax4.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.show()

def demostrar_criptoanalisis():
    """Demuestra técnicas de criptoanálisis"""
    print("\nDEMOSTRACIÓN DE CRIPTOANÁLISIS")
    print("=" * 50)
    
    texto_original = "ESTE ES UN MENSAJE SECRETO MUY IMPORTANTE"
    print(f"Texto original: {texto_original}")
    
    # Demostrar vulnerabilidad del César
    cesar = CifradorCesar(5)
    texto_cesar = cesar.cifrar(texto_original)
    print(f"Texto cifrado con César: {texto_cesar}")
    
    print("\nAplicando fuerza bruta al cifrado César:")
    resultados_bruta = cesar.fuerza_bruta(texto_cesar)
    for i, (clave, descifrado) in enumerate(resultados_bruta[:10]):
        print(f"Clave {clave:2d}: {descifrado}")
    
    # Análisis de frecuencias para Vigenère
    print(f"\nAnálisis de frecuencias:")
    vigenere = CifradorVigenere("CLAVE")
    texto_vigenere = vigenere.cifrar(texto_original)
    print(f"Texto cifrado con Vigenère: {texto_vigenere}")
    
    frecuencias = vigenere.analisis_frecuencias(texto_vigenere)
    print("Frecuencias de letras en texto cifrado:")
    for letra, freq in frecuencias.most_common(5):
        print(f"  {letra}: {freq} veces")

if __name__ == "__main__":
    # Ejecutar análisis completo
    resultados, dataset = ejecutar_comparativa_completa()
    
    # Crear visualizaciones
    crear_visualizaciones(resultados)
    
    # Demostrar criptoanálisis
    demostrar_criptoanalisis()
    
    # Resumen final
    print("\nRESUMEN DE RESULTADOS")
    print("=" * 40)
    print("César: Muy rápido, pero extremadamente vulnerable")
    print("Vigenère: Rápido, vulnerable al análisis de frecuencias")
    print("AES: Más lento, pero criptográficamente seguro")
    print("\nConclusión: Los métodos modernos sacrifican velocidad por seguridad")