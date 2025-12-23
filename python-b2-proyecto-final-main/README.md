# Proyecto Final Python B2
Librerias
Para instalar las librerías necesarias para esta actividad debes ejecutar el siguiente comando en el terminal:

pip install -r requirements.txt
Nota: El archivo 'requirements.txt' no está dentro de ninguna carpeta.

📝 Enunciado. Modelado Tipos de Financiamientos con Open Banking 
### **Contexto**:
Este ejercicio se basa en el conjunto de datos GFT Open Finance, cuyo objetivo es fomentar la competencia entre proveedores financieros, impulsar la innovación digital y promover nuevos servicios basados en datos. Este conjunto de datos se centra en la banca abierta y ofrece una valiosa oportunidad de aprendizaje sobre datos y tecnologías abiertas en el sector financiero.

La actividad propuesta permitirá a los estudiantes enfrentar la nueva realidad del intercambio de información bancaria, confrontando bases de datos de diferentes instituciones financieras, incluidas dos bancos y una compañía de seguros.

El objetivo es practicar habilidades de ingeniería de datos y ciencia de datos al desarrollar un sistema que sugiera **la clasificación de los tipos de financiamiento para un cliente específico**. Esto contribuirá a mejorar la experiencia del cliente mediante el diseño de modelos que optimicen la oferta de tipos de financiamiento.

Open Finance representa la evolución de Open Banking y promete traer más transparencia y autonomía a los usuarios del sistema financiero. Los datos proporcionados corresponden a la implementación de Open Finance en Brasil, donde se permite el intercambio de datos sobre seguros, inversiones y fondos de pensiones. El conjunto de datos incluye información financiera de un banco minorista (RetailBankEFG) obtenida a través de financiamiento abierto, con el consentimiento de los clientes, así como datos de un banco de inversión (InvestmentBankCDE) y una compañía de seguros (InsuranceCompanyABC). Estos conjuntos de datos contienen datos de compras anteriores de clientes, así como algunos datos demográficos.

### **Problema:**
El reto consiste en concebir una solución que integre las bases de datos de estas instituciones financieras en el contexto emergente de Open Finance, procese los datos con eficacia y cree modelos de clasificación para tipos de financiamientos utilizando algoritmos de aprendizaje automático.

### **Preguntas:**
Durante el desarrollo del ejercicio encontrarás una o más secciones de preguntas. Por favor, responde de manera justificada y, si se solicita incluir código, investiga para responder adecuadamente.

**Nota:** Para algunas respuestas, debes proporcionar la solución mediante código en Python e implementarla justo debajo de la línea correspondiente.
`#Write your code here`

### **Restricciones:**
No puedes borrar los nombres de las variables propuestas para el desarrollo del ejercicio.

### **Actividades:**
Para elaborar una solución que consolide las bases de datos de estas instituciones financieras y genere modelos de clasificación de tipos de financiamiento mediante algoritmos de aprendizaje automático, podemos dividir el proceso en los siguientes pasos:

- **Preparación de datos:** Integrar y limpiar los datos de las bases de datos de las instituciones financieras, asegurando que estén en un formato adecuado para su análisis.
- **Exploración de datos:** Realizar un análisis exploratorio de los datos para comprender mejor su estructura, distribución y características. Esto puede incluir la visualización de datos y la identificación de posibles patrones o relaciones.
- **Ingesta de datos:** Integrar las bases de datos de las instituciones financieras en un único repositorio de datos, asegurando que la información se pueda acceder de manera eficiente y segura.
- **Procesamiento de datos:** Realizar transformaciones adicionales en los datos según sea necesario, como la codificación de variables categóricas, la normalización de características numéricas y la manipulación de valores faltantes.
- Claro, aquí tienes el texto corregido:
- **Desarrollo de modelos para clasificar los tipos de financiamiento:** Seleccionar y entrenar algoritmos de clasificación adecuados para el problema de clasificación de tipos de financiamiento. Esto puede incluir técnicas como algoritmos de clasificación supervisada, tales como Support Vector Machines, Random Forests o redes neuronales.
- **Validación del modelo:** Evaluar el rendimiento de los modelos utilizando métricas adecuadas, como precisión, recall, F1-score, etc. Utilizar técnicas como la validación cruzada para garantizar la generalización del modelo.
- **Optimización del modelo:** Ajustar hiperparámetros y realizar selección de características para optimizar el rendimiento de los modelos.

## **Origen de la fuente de datos**:

Los datos están ubicados en la carpeta "data" y constan de los siguientes archivos.

* InvestmentBankCDE.csv
* RetailBankEFG.csv
* InsuranceCompanyABC.csv

## Archivos para desarrollar el ejericio:
Puedes elegir entre desarrollar el ejercicio en formato de notebook (ipynb) o como archivo Python (py). Los archivos con los que trabajarás son los siguientes:

- python_b2_proyecto_final.ipynb
- python_b2_proyecto_final.py

Nota: Este ejercicio tiene una serie de pistas para que puedas desarrollar y generar una solución con todo lo visto durante el desarrollo del curso.

💻 Comandos
En la siguiente sección se presentan algunos comandos útiles para el desarrollo de la actividad.

Git
Con el fin de actualizar los repositorios locales con la última versión de código fuente, ejecute:

git pull
Para agregar los cambios realizados en los archivos, ejecute:

git add .
Para añadir un mensaje a los cambios realizados localmente, ejecute:

git commit -m "Mensaje"
Para sincronizar nuestras modificaciones con el repositorio remoto, ejecute:

git push
