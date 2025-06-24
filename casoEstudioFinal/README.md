# 🔐 Simulador de Cifrados Clásicos vs Modernos

## 📋 Descripción del Proyecto

Este proyecto académico implementa y compara la efectividad de diferentes algoritmos de cifrado, desde los métodos clásicos (César y Vigenère) hasta los sistemas modernos (AES-256). El objetivo es demostrar mediante análisis cuantitativo las diferencias en seguridad, rendimiento y resistencia a ataques entre estas técnicas criptográficas.

## 🎯 Objetivos

- **Implementar** algoritmos de cifrado César, Vigenère y AES-256
- **Comparar** rendimiento, seguridad y resistencia a ataques
- **Demostrar** técnicas de criptoanálisis (fuerza bruta, análisis de frecuencias)
- **Visualizar** métricas de comparación mediante gráficos
- **Analizar** la evolución de la criptografía a través del tiempo

## 🛠️ Tecnologías Utilizadas

- **Python 3.11+**
- **Librerías principales:**
  - `pycryptodome` - Implementación AES
  - `matplotlib` - Visualizaciones
  - `seaborn` - Gráficos estadísticos
  - `pandas` - Análisis de datos
  - `numpy` - Cálculos matemáticos

## 📦 Instalación

```bash
# Instalar dependencias
pip install pycryptodome matplotlib seaborn pandas numpy

# Clonar o descargar el proyecto
git clone [https://github.com/LopezCristhian/TalentoTech-Ciberseguridad.git]
```
### Funcionalidades Implementadas

1. **Cifrado César**
   - Cifrado y descifrado con desplazamiento configurable
   - Ataque de fuerza bruta automático
   - Análisis de vulnerabilidades

2. **Cifrado Vigenère**
   - Cifrado polialfabético con clave personalizable
   - Análisis de frecuencias para criptoanálisis
   - Demostración de vulnerabilidades

3. **Cifrado AES-256**
   - Implementación estándar con claves de 256 bits
   - Modo CBC con IV aleatorio
   - Máxima seguridad criptográfica actual

## 📊 Métricas Analizadas

### Rendimiento
- ⏱️ **Tiempo de cifrado** (milisegundos)
- ⏱️ **Tiempo de descifrado** (milisegundos)
- 📈 **Escalabilidad** según longitud del texto

### Seguridad
- 🔢 **Entropía de Shannon** del texto cifrado
- 🛡️ **Resistencia a fuerza bruta** (combinaciones posibles)
- 🔍 **Vulnerabilidad al análisis de frecuencias**

### Usabilidad
- 🎯 **Simplicidad de implementación**
- 🔧 **Facilidad de uso**
- 📚 **Complejidad del algoritmo**

## 📈 Resultados Esperados

### Comparativa de Rendimiento
| Algoritmo | Velocidad | Seguridad | Simplicidad |
|-----------|-----------|-----------|-------------|
| César     | ⭐⭐⭐⭐⭐ | ⭐        | ⭐⭐⭐⭐⭐   |
| Vigenère  | ⭐⭐⭐⭐   | ⭐⭐       | ⭐⭐⭐       |
| AES-256   | ⭐⭐⭐     | ⭐⭐⭐⭐⭐   | ⭐⭐         |

### Gráficos Generados
- 📊 Tiempos de cifrado vs longitud del texto
- 📈 Entropía promedio por algoritmo
- 📉 Resistencia a fuerza bruta (escala logarítmica)
- 🎯 Evaluación general comparativa

## 🔍 Demostraciones de Criptoanálisis

### Fuerza Bruta - César
```
Texto original: "MENSAJE SECRETO"
Texto cifrado: "PHQVDMH VHFUHWR"

Probando todas las claves posibles:
Clave  0: PHQVDMH VHFUHWR
Clave  1: OGPUCIG UGDTGSP
Clave  2: NFOTBHF TFCSFRP
Clave  3: MENSAJE SECRETO  ← ¡ENCONTRADO!
```

### Análisis de Frecuencias - Vigenère
- Identificación de patrones repetitivos
- Análisis estadístico de letras más frecuentes
- Correlación con frecuencias del idioma español

## 🧪 Dataset de Prueba

El programa incluye un dataset diverso de textos:
- 📚 Literatura clásica (Quijote)
- 🧚 Cuentos infantiles
- 💻 Textos técnicos de ciberseguridad
- 🇨🇴 Descripción geográfica de Colombia
- 🔐 Conceptos criptográficos

## 🔬 Análisis Científico

### Hipótesis
"Los algoritmos de cifrado modernos como AES ofrecen mayor seguridad que los métodos clásicos, pero a costa de mayor complejidad computacional"

### Metodología
1. **Implementación** de algoritmos desde cero
2. **Medición** de métricas cuantitativas
3. **Comparación** estadística de resultados
4. **Validación** mediante técnicas de ataque

### Conclusiones Esperadas
- Los cifrados clásicos son vulnerables a ataques sistemáticos
- AES proporciona seguridad práctica contra ataques actuales
- Existe un balance entre seguridad y eficiencia computacional

## 🎓 Valor Educativo

### Conceptos Demostrados
- **Criptografía simétrica** vs **asimétrica**
- **Evolución histórica** de la criptografía
- **Análisis de seguridad** cuantitativo
- **Técnicas de criptoanálisis**
- **Importancia de la entropía** en criptografía

### Aplicaciones Prácticas
- Evaluación de sistemas de seguridad
- Selección de algoritmos criptográficos
- Comprensión de vulnerabilidades históricas
- Fundamentos para ciberseguridad avanzada

## 🚀 Posibles Extensiones

1. **Cifrados adicionales:** RSA, Blowfish, DES
2. **Ataques avanzados:** Análisis diferencial, criptoanálisis lineal
3. **Implementación paralela:** Optimización con multiprocesamiento
4. **Interface gráfica:** GUI para facilitar uso educativo
5. **Análisis de redes:** Simulación de comunicaciones seguras

*"La seguridad de un sistema criptográfico no debe depender del secreto del algoritmo, sino únicamente del secreto de la clave"* - **Principio de Kerckhoffs**