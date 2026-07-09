## 🛣️ Caso de Prueba: [TC-TWN02-001]

![Recorrido de la ruta](./media/Town02/1-Town02.mp4)


### 1. Identificación y Resultado

| Métrica | Detalle |
| :--- | :--- |
| **Mapa (CARLA)** | `Town02` |
| **Resultado de la Prueba**| Llegada a destino sin colisión |
| **Dificultad ($M_{total}$)**| 🟢 **4.15** |

### 2. Condiciones del Escenario

* **Descripción del escenario:** Bloqueo simple en una calle de Town02 simulando una intervención por obras en la calzada. Se evalúa la capacidad base del VLM para detectar obstáculos estáticos comunes y activar la primera replanificación del sistema.



### 3. Métricas de Evaluación

**👁️ Percepción y Razonamiento (VLM)**
* **Falsos Positivos / Negativos:** 1 / 0

**⚙️ Planificación y Control (RouteManager & BehaviorAgent)**
* **Porcentaje de Ruta Completado:** 100%
* **Replanificaciones Activadas/Esperadas:** 1/1

### 4. Observaciones y Análisis Técnico

El obstáculo se encuentra posicionado profundamente en la vía; sin embargo, el crop izquierdo y la presencia de una valla adelantada permiten al modelo multimodal inferir el bloqueo con antelación suficiente para desencadenar la replanificación. Se registra, no obstante, un falso positivo puntual derivado de la segmentación espacial de las imágenes: el modelo clasifica erróneamente un soporte estructural ubicado en la acera como un obstáculo activo, al carecer de la precisión necesaria en ese frame para discernir el límite exacto del drivable path.

---

## 🛣️ Caso de Prueba: [TC-TWN02-002]

![Recorrido de la ruta](./media/Town02/2-Town02.mp4)


### 1. Identificación y Resultado

| Métrica | Detalle |
| :--- | :--- |
| **Mapa (CARLA)** | `Town02` |
| **Resultado de la Prueba**| Llegada a destino sin colisión |
| **Dificultad ($M_{total}$)**| 🟡 **6.24** |

### 2. Condiciones del Escenario

* **Descripción del escenario:** Bloqueo total de una vía transversal en Town02. A diferencia de un estrechamiento, el obstáculo cruza perpendicularmente todo el ancho de la calle, forzando un desvío absoluto e inmediato por vías adyacentes.



### 3. Métricas de Evaluación

**👁️ Percepción y Razonamiento (VLM)**
* **Falsos Positivos / Negativos:** 1 / 0

**⚙️ Planificación y Control (RouteManager & BehaviorAgent)**
* **Porcentaje de Ruta Completado:** 100%
* **Replanificaciones Activadas/Esperadas:** 1/1

### 4. Observaciones y Análisis Técnico

La detección del obstáculo frontal principal se realiza de manera robusta y con un margen de anticipación óptimo para el frenado. Se documenta la aparición de un falso positivo atribuible a la distorsión geométrica inherente a las esquinas del campo de visión tras el proceso de recorte de las imágenes. Esta deformación provoca que el modelo alucine un "large bowl-like object" en la calzada. A pesar de esta anomalía visual, el análisis de la trayectoria central se mantiene estable y las detecciones de los bloqueos reales se ejecutan exitosamente.

---

## 🛣️ Caso de Prueba: [TC-TWN02-003]

![Recorrido de la ruta](./media/Town02/3-Town02.mp4)


### 1. Identificación y Resultado

| Métrica | Detalle |
| :--- | :--- |
| **Mapa (CARLA)** | `Town02` |
| **Resultado de la Prueba**| Llegada a destino sin colisión |
| **Dificultad ($M_{total}$)**| 🔴 **10.91** |

### 2. Condiciones del Escenario

* **Descripción del escenario:** Escenario de alta densidad distribuido a lo largo de 3 calles en Town02. Combina zonas de obras con presencia policial, requiriendo que el RouteManager ejecute múltiples ciclos de replanificación consecutivos a lo largo del trayecto.



### 3. Métricas de Evaluación

**👁️ Percepción y Razonamiento (VLM)**
* **Falsos Positivos / Negativos:** 2 / 0

**⚙️ Planificación y Control (RouteManager & BehaviorAgent)**
* **Porcentaje de Ruta Completado:** 100%
* **Replanificaciones Activadas/Esperadas:** 0/0

### 4. Observaciones y Análisis Técnico

El sistema demuestra alta eficacia en la evaluación profunda del entorno, detectando con éxito los obstáculos ubicados al final de la trayectoria con amplia antelación. En cuanto al desempeño de la segmentación visual, se constatan dos falsos positivos: la clasificación de rocas cercanas y un soporte en la acera como elementos bloqueantes. Esto evidencia una sensibilidad excesiva del modelo ante objetos que, si bien son volumétricos, no invaden el espacio de conducción legal. A pesar de este ruido perceptual periférico, la gestión de los obstáculos reales de la ruta se completa de forma satisfactoria.

---

## 🛣️ Caso de Prueba: [TC-TWN02-004]

![Recorrido de la ruta](./media/Town02/4-Town02.mp4)


### 1. Identificación y Resultado

| Métrica | Detalle |
| :--- | :--- |
| **Mapa (CARLA)** | `Town02` |
| **Resultado de la Prueba**| Llegada a destino sin colisión |
| **Dificultad ($M_{total}$)**| 🔴 **10.14** |

### 2. Condiciones del Escenario

* **Descripción del escenario:** Variante topológica de la Ruta 3. Mantiene la misma densidad y tipología de obstáculos (obras y policía en 3 calles), pero ubicados en diferentes coordenadas geométricas de Town02. Diseñada para validar que la robustez del planificador es independiente de la intersección específica.



### 3. Métricas de Evaluación

**👁️ Percepción y Razonamiento (VLM)**
* **Falsos Positivos / Negativos:** 0 / 0

**⚙️ Planificación y Control (RouteManager & BehaviorAgent)**
* **Porcentaje de Ruta Completado:** 100%
* **Replanificaciones Activadas/Esperadas:** 3/3

### 4. Observaciones y Análisis Técnico

El módulo de navegación gestiona la presencia de múltiples obstáculos sucesivos manteniendo los márgenes de anticipación necesarios. Se observa un comportamiento perceptual oscilatorio durante la aproximación temprana al segundo obstáculo. En largas distancias, la resolución espacial genera ambigüedad semántica, provocando que la inferencia del modelo alterne entre "vía libre" y "vía bloqueada" en instantes consecutivos. Esta inestabilidad se resuelve de manera natural y determinista conforme el ego-vehículo reduce la distancia relativa al objetivo, consolidando la detección a tiempo.

---

## 🛣️ Caso de Prueba: [TC-TWN02-005]

![Recorrido de la ruta](./media/Town02/5-Town02.mp4)


### 1. Identificación y Resultado

| Métrica | Detalle |
| :--- | :--- |
| **Mapa (CARLA)** | `Town02` |
| **Resultado de la Prueba**| Llegada a destino sin colisión |
| **Dificultad ($M_{total}$)**| 🟢 **2.38** |

### 2. Condiciones del Escenario

* **Descripción del escenario:** Interrupción en una vía básica de Town02 ubicada en las proximidades del aparcamiento central. Este caso evalúa la navegación y percepción del modelo multimodal en zonas donde la geometría de la carretera interactúa con áreas de estacionamiento abiertas.



### 3. Métricas de Evaluación

**👁️ Percepción y Razonamiento (VLM)**
* **Falsos Positivos / Negativos:** 0 / 0

**⚙️ Planificación y Control (RouteManager & BehaviorAgent)**
* **Porcentaje de Ruta Completado:** 100%
* **Replanificaciones Activadas/Esperadas:** 1/1

### 4. Observaciones y Análisis Técnico

Se documenta un caso de detección tardía que resulta en una corrección cinemática abrupta. El agente inicia la maniobra de giro planificada hacia la vía interceptada debido a una falta de anticipación visual del obstáculo por parte del modelo multimodal. Al entrar el obstáculo en la zona de máxima visibilidad de la cámara, el sistema actualiza drásticamente su estado de percepción y el BehaviorAgent aplica una corrección de trayectoria de emergencia. Este evento demuestra una alta capacidad de respuesta reactiva del control vehicular, aunque evidencia limitaciones en la predicción topológica temprana bajo ciertas geometrías de intersección.

---

## 🛣️ Caso de Prueba: [TC-TWN02-006]

![Recorrido de la ruta](./media/Town02/6-Town02.mp4)


### 1. Identificación y Resultado

| Métrica | Detalle |
| :--- | :--- |
| **Mapa (CARLA)** | `Town02` |
| **Resultado de la Prueba**| Llegada a destino sin colisión |
| **Dificultad ($M_{total}$)**| 🟢 **2.42** |

### 2. Condiciones del Escenario

* **Descripción del escenario:** Obra de gran envergadura que bloquea ambos sentidos de circulación. Presenta un entorno visualmente rico y complejo para poner a prueba la atención del modelo multimodal frente a la superposición de múltiples texturas urbanas.



### 3. Métricas de Evaluación

**👁️ Percepción y Razonamiento (VLM)**
* **Falsos Positivos / Negativos:** 0 / 0

**⚙️ Planificación y Control (RouteManager & BehaviorAgent)**
* **Porcentaje de Ruta Completado:** 100%
* **Replanificaciones Activadas/Esperadas:** 1/1

### 4. Observaciones y Análisis Técnico

Durante el inicio de la ruta se presenta una alta densidad semántica en el campo de visión izquierdo (superposición de vegetación, infraestructura peatonal, mobiliario urbano y elementos de obra). Esta saturación contextual induce ruido en la inferencia del VLM, mermando su capacidad de atención y generando oscilaciones en la clasificación del estado de bloqueo (falsos negativos intermitentes). A pesar de la inestabilidad en la confirmación visual originada por la complejidad del entorno, el sistema logra integrar la detección en el momento crítico y la replanificación topológica se ejecuta correctamente.

---

## 🛣️ Caso de Prueba: [TC-TWN02-007]

![Recorrido de la ruta](./media/Town02/7-Town02.mp4)


### 1. Identificación y Resultado

| Métrica | Detalle |
| :--- | :--- |
| **Mapa (CARLA)** | `Town02` |
| **Resultado de la Prueba**| Llegada a destino sin colisión |
| **Dificultad ($M_{total}$)**| 🟢 **3.85** |

### 2. Condiciones del Escenario

* **Descripción del escenario:** Intervención en dos calles clave de Town02. Los bloqueos están colocados estratégicamente para afectar de forma crítica el flujo lógico del tráfico, forzando al algoritmo geométrico a calcular desvíos de larga distancia y evaluando su eficiencia computacional.



### 3. Métricas de Evaluación

**👁️ Percepción y Razonamiento (VLM)**
* **Falsos Positivos / Negativos:** 1 / 0

**⚙️ Planificación y Control (RouteManager & BehaviorAgent)**
* **Porcentaje de Ruta Completado:** 100%
* **Replanificaciones Activadas/Esperadas:** 2/2

### 4. Observaciones y Análisis Técnico

Durante la aproximación a una de las intersecciones finales, el módulo de percepción genera un falso positivo, reportando un bloqueo inexistente en la salida derecha. Como respuesta procedimental, el enrutador penaliza correctamente los pesos de los nodos correspondientes en el grafo de búsqueda. Sin embargo, dada la restricción topológica del mapa en esa área, no existía ninguna ruta alternativa conectada y viable para alcanzar el destino final. En consecuencia, el planificador se vio forzado a mantener la trayectoria original a pesar de la alta penalización de los nodos. Aunque el vehículo completó la ruta exitosamente (resultado empírico esperado), la consecución del objetivo no se dio mediante un procedimiento algorítmico adecuado: el sistema transitó de forma deliberada por un segmento que internamente consideraba intransitable debido a la falta de alternativas topológicas, constituyendo una resolución subóptima originada por un error perceptual.

---

## 🛣️ Caso de Prueba: [TC-TWN02-008]

![Recorrido de la ruta](./media/Town02/8-Town02.mp4)


### 1. Identificación y Resultado

| Métrica | Detalle |
| :--- | :--- |
| **Mapa (CARLA)** | `Town02` |
| **Resultado de la Prueba**| Llegada a destino sin colisión |
| **Dificultad ($M_{total}$)**| 🟢 **4.09** |

### 2. Condiciones del Escenario

* **Descripción del escenario:** Simulación de un retén policial. Evalúa la capacidad del sistema para gestionar un obstáculo de carácter institucional temporal y comprobar si el modelo multimodal extrae un contexto diferente al de una obra de construcción estándar.



### 3. Métricas de Evaluación

**👁️ Percepción y Razonamiento (VLM)**
* **Falsos Positivos / Negativos:** 2 / 0

**⚙️ Planificación y Control (RouteManager & BehaviorAgent)**
* **Porcentaje de Ruta Completado:** 100%
* **Replanificaciones Activadas/Esperadas:** 1/1

### 4. Observaciones y Análisis Técnico

El sistema exhibe un comportamiento nominal y seguro en cuanto a la anticipación visual. En las fases finales de la simulación, se produce un falso positivo en la inferencia del modelo multimodal, el cual reporta un bloqueo inexistente en la salida derecha de la intersección. Respondiendo de forma mecánicamente correcta a esta alerta perceptual, el planificador recalcula el grafo y desvía el vehículo hacia la izquierda. El agente logra alcanzar las coordenadas de destino de manera fluida a través de una ruta subóptima que no estaba contemplada en la topología inicial, validando la resiliencia algorítmica del planificador frente a "alucinaciones" aisladas del modelo visual.

---

## 🛣️ Caso de Prueba: [TC-TWN03-001]

![Recorrido de la ruta](./media/Town03/1-Town03.mp4)


### 1. Identificación y Resultado

| Métrica | Detalle |
| :--- | :--- |
| **Mapa (CARLA)** | `Town03` |
| **Resultado de la Prueba**| Llegada a destino sin colisión |
| **Dificultad ($M_{total}$)**| 🟢 **4.09** |

### 2. Condiciones del Escenario

* **Descripción del escenario:** Bloqueo estructural en una vía de pendiente ascendente dentro de Town03. La intervención consiste en una alineación continua de conos que conforman un único muro físico. Este escenario evalúa la robustez de percepción del modelo multimodal frente a obstáculos laterales, así como su capacidad para agrupar múltiples elementos individuales contiguos en una sola entidad semántica de bloqueo.



### 3. Métricas de Evaluación

**👁️ Percepción y Razonamiento (VLM)**
* **Falsos Positivos / Negativos:** 0 / 0

**⚙️ Planificación y Control (RouteManager & BehaviorAgent)**
* **Porcentaje de Ruta Completado:** 100%
* **Replanificaciones Activadas/Esperadas:** 1/1

### 4. Observaciones y Análisis Técnico

El sistema mantiene un margen lateral de seguridad adecuado durante toda la trayectoria. Resulta destacable la correcta desagregación semántica de las columnas estructurales del túnel, las cuales son clasificadas adecuadamente por el VLM como mobiliario urbano externo al área navegable, evitando falsos positivos. Asimismo, la agrupación de conos de balizamiento es inferida en su totalidad como una única entidad obstructiva, validando la eficacia del modelo para agrupar múltiples objetos contiguos bajo un mismo contexto de bloqueo.

---

## 🛣️ Caso de Prueba: [TC-TWN03-002]

![Recorrido de la ruta](./media/Town03/2-Town03.mp4)


### 1. Identificación y Resultado

| Métrica | Detalle |
| :--- | :--- |
| **Mapa (CARLA)** | `Town03` |
| **Resultado de la Prueba**| Llegada a destino sin colisión |
| **Dificultad ($M_{total}$)**| 🟢 **3.59** |

### 2. Condiciones del Escenario

* **Descripción del escenario:** Interrupción de una vía con pendiente ascendente cuya superficie presenta un estado de degradación simulado mediante la acumulación de tierra y sedimentos. El bloqueo se materializa combinando barreras estructurales con montículos de escombros no estructurados.



### 3. Métricas de Evaluación

**👁️ Percepción y Razonamiento (VLM)**
* **Falsos Positivos / Negativos:** 0 / 0

**⚙️ Planificación y Control (RouteManager & BehaviorAgent)**
* **Porcentaje de Ruta Completado:** 100%
* **Replanificaciones Activadas/Esperadas:** 1/1

### 4. Observaciones y Análisis Técnico

La detección de las barreras de construcción en el flanco derecho se ejecuta con alta precisión, desencadenando una redirección topológica exitosa. De especial relevancia en este escenario es la validación de la robustez del modelo multimodal frente a variaciones cinemáticas de inclinación (pitch). La alteración del horizonte visual originada por la pendiente geométrica de la vía no degrada el rendimiento de la percepción ni induce alucinaciones, manteniendo una operatividad estable y determinista.

---

## 🛣️ Caso de Prueba: [TC-TWN03-003]

![Recorrido de la ruta](./media/Town03/3-Town03.mp4)


### 1. Identificación y Resultado

| Métrica | Detalle |
| :--- | :--- |
| **Mapa (CARLA)** | `Town03` |
| **Resultado de la Prueba**| Llegada a destino sin colisión |
| **Dificultad ($M_{total}$)**| 🟡 **7.04** |

### 2. Condiciones del Escenario

* **Descripción del escenario:** Intervención multisectorial de alta complejidad simulando la concurrencia espacial de incidentes críticos: controles de seguridad, operaciones de emergencia (bomberos) y zonas de obras. La interrupción de las vías se ejecuta mediante una densa amalgama de entidades, incluyendo vehículos institucionales estacionarios (patrullas policiales y camiones de bomberos), señales de advertencia, barreras estructurales y contenedores de residuos urbanos. Este escenario somete a evaluación extrema la capacidad de desagregación semántica del modelo multimodal frente a entornos visualmente saturados, así como la resiliencia algorítmica del planificador geométrico para gestionar replanificaciones topológicas sucesivas en un nodo de alta conectividad.



### 3. Métricas de Evaluación

**👁️ Percepción y Razonamiento (VLM)**
* **Falsos Positivos / Negativos:** 1 / 0

**⚙️ Planificación y Control (RouteManager & BehaviorAgent)**
* **Porcentaje de Ruta Completado:** 100%
* **Replanificaciones Activadas/Esperadas:** 2/2

### 4. Observaciones y Análisis Técnico

En la intersección con bloqueo múltiple, el sistema demuestra una alta reactividad perceptiva al detectar secuencialmente la obstrucción frontal seguida de la lateral izquierda. Esta baja latencia de inferencia permite al RouteManager penalizar los pesos de ambas trayectorias en el grafo de búsqueda de forma casi simultánea. Cabe destacar que, debido a una escasez en la conectividad topológica del mapa Town03 en el sector de la rotonda, el planificador agota las opciones de enrutamiento por las salidas naturales y se ve forzado a calcular un itinerario alternativo de mayor escala. Pese a esta severa limitación del entorno, el agente logra converger hacia el destino bajo estrictos parámetros de seguridad.

---

## 🛣️ Caso de Prueba: [TC-TWN03-004]

![Recorrido de la ruta](./media/Town03/4-Town03.mp4)


### 1. Identificación y Resultado

| Métrica | Detalle |
| :--- | :--- |
| **Mapa (CARLA)** | `Town03` |
| **Resultado de la Prueba**| Colisión en salida de rotonda |
| **Dificultad ($M_{total}$)**| 🟡 **6.10** |

### 2. Condiciones del Escenario

* **Descripción del escenario:** Escenario de interrupción dual y espacialmente distribuida en Town03. El primer bloqueo se ubica en el anillo interior de la rotonda principal, empleando señalética de advertencia y barreras estructurales (intervención formal). El segundo se localiza en las inmediaciones de la estación de servicio, configurado mediante la agrupación de conos de tráfico y contenedores de residuos para emular una barricada de carácter improvisado o fortuito. Este caso de prueba evalúa la resiliencia de la percepción multimodal para inferir contextos de bloqueo dispares (estructurado frente a no estructurado) en una misma misión, así como la robustez del planificador para gestionar replanificaciones topológicas tanto en nodos circulares complejos como en transiciones hacia vías de servicio.



### 3. Métricas de Evaluación

**👁️ Percepción y Razonamiento (VLM)**
* **Falsos Positivos / Negativos:** 1 / 0

**⚙️ Planificación y Control (RouteManager & BehaviorAgent)**
* **Porcentaje de Ruta Completado:** 60%
* **Replanificaciones Activadas/Esperadas:** 1/2

### 4. Observaciones y Análisis Técnico

El modelo multimodal demuestra una notable comprensión del entorno al discriminar los depósitos de combustible de la estación de servicio como infraestructura adyacente, eludiendo falsos positivos pese a su proximidad. La incorporación a la vía y la detección de la barricada improvisada se resuelven de manera óptima. No obstante, el sistema reporta un falso positivo crítico al clasificar el monumento central de la rotonda como un obstáculo activo, inducido presumiblemente por su gran magnitud volumétrica. Esta anomalía perceptual, combinada con la ya mencionada topología restrictiva de la rotonda, desencadena una replanificación tardía que agota el margen espacial de maniobra, desembocando en una colisión contra las barreras físicas.

---

## 🛣️ Caso de Prueba: [TC-TWN03-005]

![Recorrido de la ruta](./media/Town03/5-Town03.mp4)


### 1. Identificación y Resultado

| Métrica | Detalle |
| :--- | :--- |
| **Mapa (CARLA)** | `Town03` |
| **Resultado de la Prueba**| Llegada a destino sin colisión |
| **Dificultad ($M_{total}$)**| 🔴 **11.30** |

### 2. Condiciones del Escenario

* **Descripción del escenario:** Interrupción simultánea de dos vías opuestas que genera un embudo topológico, restringiendo el flujo vehicular a una única trayectoria transitable. La composición de los bloqueos presenta una marcada asimetría volumétrica y semántica: un flanco se encuentra obstruido por vehículos de emergencia de gran envergadura (ambulancias y camión de bomberos), mientras que el flanco opuesto está delimitado por elementos de balizamiento de bajo perfil (conos de tráfico medianos).



### 3. Métricas de Evaluación

**👁️ Percepción y Razonamiento (VLM)**
* **Falsos Positivos / Negativos:** 2 / 0

**⚙️ Planificación y Control (RouteManager & BehaviorAgent)**
* **Porcentaje de Ruta Completado:** 100%
* **Replanificaciones Activadas/Esperadas:** 2/2

### 4. Observaciones y Análisis Técnico

La navegación inicial a través de la rotonda se ejecuta de forma nominal. Sin embargo, en la intersección con obstrucción bilateral, aparece una limitación arquitectónica que requiere ejecutar un evento manual (OVERRIDE) para forzar la percepción de ambos flancos. El análisis revela que la heurística actual de gestión temporal y espacial carece del refinamiento necesario para resolver concurrencias múltiples en un mismo nodo. El sistema de seguimiento exhibe deficiencias a la hora de discernir algorítmicamente cuándo una detección corresponde a un obstáculo previamente registrado que debe ignorarse y cuándo representa una entidad bloqueante nueva en la misma área de influencia, siendo este un aspecto crítico para investigaciones futuras.

---

## 🛣️ Caso de Prueba: [TC-TWN03-006]

![Recorrido de la ruta](./media/Town03/6-Town03.mp4)


### 1. Identificación y Resultado

| Métrica | Detalle |
| :--- | :--- |
| **Mapa (CARLA)** | `Town03` |
| **Resultado de la Prueba**| Llegada a destino sin colisión |
| **Dificultad ($M_{total}$)**| 🟡 **6.10** |

### 2. Condiciones del Escenario

* **Descripción del escenario:** Simulación de un retén policial. Evalúa la capacidad del sistema para gestionar un obstáculo de carácter institucional temporal y comprobar si el modelo multimodal extrae un contexto diferente al de una obra de construcción estándar.



### 3. Métricas de Evaluación

**👁️ Percepción y Razonamiento (VLM)**
* **Falsos Positivos / Negativos:** 1 / 1

**⚙️ Planificación y Control (RouteManager & BehaviorAgent)**
* **Porcentaje de Ruta Completado:** 100%
* **Replanificaciones Activadas/Esperadas:** 1/1

### 4. Observaciones y Análisis Técnico

Ante la presencia de un bloqueo frontal absoluto, el sistema cambia al carril izquierdo respetando el semáforo. Esto demuestra que cumple su objetivo principal: avanzar hacia su destino sin saltarse las normas de tráfico. Más adelante, al bajar una cuesta, el sistema comete un error y no detecta un obstáculo que hay delante. Aunque no sabemos exactamente por qué no lo vio (quizás por la inclinación de la calle o por un fallo puntual en el procesado de las imágenes), el vehículo logra mantener el control y llegar a su destino final sin problemas.

---

## 🛣️ Caso de Prueba: [TC-TWN03-007]

![Recorrido de la ruta](./media/Town03/7-Town03.mp4)


### 1. Identificación y Resultado

| Métrica | Detalle |
| :--- | :--- |
| **Mapa (CARLA)** | `Town03` |
| **Resultado de la Prueba**| Llegada a destino sin colisión |
| **Dificultad ($M_{total}$)**| 🟡 **7.30** |

### 2. Condiciones del Escenario

* **Descripción del escenario:** Intervención obstructiva en la salida diestra de una rotonda de tipología residencial. El bloqueo emula una operación logística de descarga de mercancías, materializado mediante la presencia de un vehículo de transporte pesado estacionado en la vía, flanqueado por elementos de carga dispersos (cajas) y balizado con conos de tráfico espaciados.



### 3. Métricas de Evaluación

**👁️ Percepción y Razonamiento (VLM)**
* **Falsos Positivos / Negativos:** 0 / 0

**⚙️ Planificación y Control (RouteManager & BehaviorAgent)**
* **Porcentaje de Ruta Completado:** 100%
* **Replanificaciones Activadas/Esperadas:** 1/1

### 4. Observaciones y Análisis Técnico

El módulo de percepción exhibe una excepcional agudeza visual periférica en este ensayo. El sistema logra detectar e interpretar correctamente la semántica del bloqueo en la salida derecha (reportando explícitamente la presencia de "conos y un camión"), a pesar de que los elementos obstructivos se encontraban en el límite lateral extremo del campo de visión con una ocupación de píxeles marginal. Esta inferencia temprana y precisa bajo condiciones de visibilidad geométrica reducida permite una ejecución fluida de la maniobra evasiva, validando la solidez del enrutamiento multimodal.

---

## 🛣️ Caso de Prueba: [TC-TWN03-008]

![Recorrido de la ruta](./media/Town03/8-Town03.mp4)


### 1. Identificación y Resultado

| Métrica | Detalle |
| :--- | :--- |
| **Mapa (CARLA)** | `Town03` |
| **Resultado de la Prueba**| Llegada a destino sin colisión |
| **Dificultad ($M_{total}$)**| 🟢 **4.09** |

### 2. Condiciones del Escenario

* **Descripción del escenario:** El recorrido comienza en un semáforo flanqueado por dos restricciones simultáneas: un control policial en la intersección izquierda y una calle completamente bloqueada en el lado derecho. En el tramo final, existe un bloqueo adicional en un cruce amplio cerca de la gasolinera que impide girar a la izquierda; sin embargo, las coordenadas de destino de la ruta están fijadas justo antes de llegar a dicha intersección.



### 3. Métricas de Evaluación

**👁️ Percepción y Razonamiento (VLM)**
* **Falsos Positivos / Negativos:** 0 / 0

**⚙️ Planificación y Control (RouteManager & BehaviorAgent)**
* **Porcentaje de Ruta Completado:** 100%
* **Replanificaciones Activadas/Esperadas:** 1/1

### 4. Observaciones y Análisis Técnico

El modelo multimodal (VLM) procesa y detecta correctamente los dos obstáculos iniciales. Resulta destacable observar cómo el sistema otorga prioridad de atención al bloqueo situado a la derecha, un comportamiento derivado de su mayor volumen y el gran espacio que ocupa en la imagen procesada. En cuanto al último obstáculo cercano a la gasolinera, este no llega a ser detectado; no obstante, se trata de un comportamiento lógico y esperado, ya que el vehículo alcanza su destino con éxito y la simulación termina antes de que dicho bloqueo entre en el rango de percepción efectivo de las cámaras.

---

## 🛣️ Caso de Prueba: [TC-TWN04-001]

![Recorrido de la ruta](./media/Town04/1-Town04.mp4)


### 1. Identificación y Resultado

| Métrica | Detalle |
| :--- | :--- |
| **Mapa (CARLA)** | `Town04` |
| **Resultado de la Prueba**| Llegada a destino sin colisión |
| **Dificultad ($M_{total}$)**| 🟢 **3.94** |

### 2. Condiciones del Escenario

* **Descripción del escenario:** Un obstáculo sencillo situado cerca de la gasolinera de Town04. Para cortar el paso, se han colocado unas barreras de obra normales atravesadas de lado a lado en la calle.



### 3. Métricas de Evaluación

**👁️ Percepción y Razonamiento (VLM)**
* **Falsos Positivos / Negativos:** 0 / 0

**⚙️ Planificación y Control (RouteManager & BehaviorAgent)**
* **Porcentaje de Ruta Completado:** 100%
* **Replanificaciones Activadas/Esperadas:** 1/1

### 4. Observaciones y Análisis Técnico

El sistema logra adelantarse y reaccionar a tiempo ante el obstáculo situado a la izquierda. Lo más destacado de esta prueba es un comportamiento inesperado pero muy positivo: el coche realiza un pequeño movimiento natural dentro de su carril que mejora el ángulo de visión de la cámara. Este ligero cambio de posición permite que el modelo visual capte perfectamente el obstáculo. La ruta finaliza de forma totalmente segura, demostrando que los pequeños ajustes dinámicos del coche sobre el asfalto ayudan enormemente a que la inteligencia artificial entienda mejor el entorno y reaccione con éxito.


---

## 🛣️ Caso de Prueba: [TC-TWN04-002]

![Recorrido de la ruta](./media/Town04/2-Town04.mp4)


### 1. Identificación y Resultado

| Métrica | Detalle |
| :--- | :--- |
| **Mapa (CARLA)** | `Town04` |
| **Resultado de la Prueba**| Llegada a destino sin colisión |
| **Dificultad ($M_{total}$)**| 🟢 **3.28** |

### 2. Condiciones del Escenario

* **Descripción del escenario:** El bloqueo se materializa exclusivamente mediante elementos de balizamiento de perfil medio (conos de tráfico), omitiendo el uso de barreras estructurales continuas. Este escenario evalúa la sensibilidad y agudeza del modelo multimodal para inferir restricciones camufladas en el entorno entre otros tipos de objetos urbanos.



### 3. Métricas de Evaluación

**👁️ Percepción y Razonamiento (VLM)**
* **Falsos Positivos / Negativos:** 0 / 0

**⚙️ Planificación y Control (RouteManager & BehaviorAgent)**
* **Porcentaje de Ruta Completado:** 100%
* **Replanificaciones Activadas/Esperadas:** 1/1

### 4. Observaciones y Análisis Técnico

El entorno de prueba presenta un alto grado de camuflaje visual debido a la densidad de mobiliario urbano y vegetación adyacente (farolas, contenedores, setos). Pese a este ruido de fondo, el modelo multimodal segmenta e identifica correctamente los conos de tráfico, apoyándose presumiblemente en la alta saturación cromática (naranja) de los mismos. La ejecución de la trayectoria se desarrolla sin incidencias, validando la robustez del modelo ante oclusiones parciales y texturas superpuestas.

---

## 🛣️ Caso de Prueba: [TC-TWN04-003]

![Recorrido de la ruta](./media/Town04/3-Town04.mp4)


### 1. Identificación y Resultado

| Métrica | Detalle |
| :--- | :--- |
| **Mapa (CARLA)** | `Town04` |
| **Resultado de la Prueba**| Llegada a destino sin colisión |
| **Dificultad ($M_{total}$)**| 🟡 **6.26** |

### 2. Condiciones del Escenario

* **Descripción del escenario:** Escenario con dos obstáculos situados en tipos de vías muy diferentes: el primero corta una salida clave de la autopista hacia la ciudad, y el segundo bloquea una calle normal del interior urbano. Para señalizarlos se emplean barreras, conos y señales. El objetivo es comprobar si el planificador de rutas es capaz de gestionar a la vez grandes desvíos (al perder un enlace importante de la autopista) y pequeños ajustes (calles cortadas), garantizando que el coche siempre encuentre una alternativa válida.



### 3. Métricas de Evaluación

**👁️ Percepción y Razonamiento (VLM)**
* **Falsos Positivos / Negativos:** 4 / 0

**⚙️ Planificación y Control (RouteManager & BehaviorAgent)**
* **Porcentaje de Ruta Completado:** 100%
* **Replanificaciones Activadas/Esperadas:** 2/2

### 4. Observaciones y Análisis Técnico

Durante la entrada a la autovía, el modelo visual comete un error importante (un falso positivo): confunde una gran roca del decorado ("large boulder") con un obstáculo que bloquea el paso. Esto demuestra que al VLM le cuesta distinguir entre cómo funciona un carril de aceleración y un cruce urbano normal. Además, el sistema se confunde varias veces con los barriles amarillos de protección de la autovía, creyendo que cortan la carretera. Estos errores indican que el modelo visual se fija demasiado en la forma y volumen de los objetos, fallando al no darse cuenta de que están colocados de forma inofensiva fuera de la calzada. A pesar de todo este "ruido" e inestabilidad visual, el planificador reacciona de manera excelente: calcula un desvío enorme y el coche llega a su destino con total éxito.

---

## 🛣️ Caso de Prueba: [TC-TWN04-004]

![Recorrido de la ruta](./media/Town04/4-Town04.mp4)


### 1. Identificación y Resultado

| Métrica | Detalle |
| :--- | :--- |
| **Mapa (CARLA)** | `Town04` |
| **Resultado de la Prueba**| Llegada a destino sin colisión |
| **Dificultad ($M_{total}$)**| 🟡 **6.31** |

### 2. Condiciones del Escenario

* **Descripción del escenario:** Escenario con dos obstáculos situados en las avenidas principales y rápidas de Town04. Ambos bloqueos utilizan barreras y conos cruzados en la calzada para simular cortes de tráfico por obras o incidentes temporales. El objetivo es comprobar si el planificador de rutas es capaz de recalcular el camino varias veces seguidas sin problemas en zonas de alta velocidad, y ver si el modelo visual se mantiene estable cuando se encuentra varios bloqueos parecidos en el mismo viaje.



### 3. Métricas de Evaluación

**👁️ Percepción y Razonamiento (VLM)**
* **Falsos Positivos / Negativos:** 2 / 0

**⚙️ Planificación y Control (RouteManager & BehaviorAgent)**
* **Porcentaje de Ruta Completado:** 100%
* **Replanificaciones Activadas/Esperadas:** 1/1

### 4. Observaciones y Análisis Técnico

El sistema detecta el bloqueo frontal principal con mucha antelación, lo que permite al coche acercarse y maniobrar de forma muy suave, segura y cómoda para los pasajeros. Además, el modelo identifica perfectamente los conos que cortan el paso en el cruce de la derecha. Sin embargo, se vuelve a confirmar el punto débil detectado en la prueba anterior: el sistema sufre falsos positivos al confundir de nuevo los barriles de protección de la autovía con obstáculos reales, creyendo que cortan el paso.

---

## 🛣️ Caso de Prueba: [TC-TWN04-005]

![Recorrido de la ruta](./media/Town04/5-Town04.mp4)


### 1. Identificación y Resultado

| Métrica | Detalle |
| :--- | :--- |
| **Mapa (CARLA)** | `Town04` |
| **Resultado de la Prueba**| Colisión con corredor balizado |
| **Dificultad ($M_{total}$)**| 🔴 **10.24** |

### 2. Condiciones del Escenario

* **Descripción del escenario:** Escenario complejo con obstáculos muy variados. Combina un corte importante en la salida de la autopista con zonas de obras en las calles interiores de la ciudad. Lo más destacado de esta prueba es la creación de un "pasillo" continuo hecho con conos cerca del aparcamiento, que obliga al vehículo a circular por un único camino estrecho. El objetivo es comprobar si el planificador sabe buscar desvíos largos cuando se corta una vía rápida, y si el coche es capaz de conducir con precisión dentro de un carril fuertemente delimitado por conos.


### 3. Métricas de Evaluación

**👁️ Percepción y Razonamiento (VLM)**
* **Falsos Positivos / Negativos:** 1 / 0

**⚙️ Planificación y Control (RouteManager & BehaviorAgent)**
* **Porcentaje de Ruta Completado:** 55%
* **Replanificaciones Activadas/Esperadas:** 3/4

### 4. Observaciones y Análisis Técnico

En la autovía, el vehículo logra esquivar con éxito, aunque dando un volantazo brusco, un obstáculo "ciego" que aparece de repente al salir de una curva. Más adelante, el modelo visual demuestra tener problemas de contraste o camuflaje: no logra detectar unos contenedores que bloquean el paso porque su color se confunde casi por completo con la vegetación del fondo, al estar situados en un desvío diagonal. En este punto, fue necesario intervenir usando el evento manual (OVERRIDE) para "avisar" al sistema del bloqueo y que recalculara la ruta. Finalmente, la prueba termina en colisión. El sistema falla por completo al intentar procesar un pasillo de conos curvo que bloquea a la vez la salida frontal y la de la izquierda. Este error revela una limitación importante: el modelo visual actual no es capaz de entender bien las barreras curvas o en forma de embudo, lo que hace que el coche se quede sin reacción y acabe chocando.

---

## 🛣️ Caso de Prueba: [TC-TWN04-006]

![Recorrido de la ruta](./media/Town04/6-Town04.mp4)


### 1. Identificación y Resultado

| Métrica | Detalle |
| :--- | :--- |
| **Mapa (CARLA)** | `Town04` |
| **Resultado de la Prueba**| Llegada a destino sin colisión |
| **Dificultad ($M_{total}$)**| 🔴 **10.40** |

### 2. Condiciones del Escenario

* **Descripción del escenario:** Corte total en la autopista utilizando conos de tráfico, paneles luminosos y un control policial. Al bloquear una vía rápida tan importante, el planificador de rutas se ve obligado a descartar su camino ideal y buscar un desvío enorme por otras zonas del mapa. Esta prueba sirve para comprobar si el sistema es rápido recalculando rutas a gran escala y si el modelo visual entiende correctamente los obstáculos cuando aparecen agrupados uno detrás de otro.



### 3. Métricas de Evaluación

**👁️ Percepción y Razonamiento (VLM)**
* **Falsos Positivos / Negativos:** 3 / 0

**⚙️ Planificación y Control (RouteManager & BehaviorAgent)**
* **Porcentaje de Ruta Completado:** 100%
* **Replanificaciones Activadas/Esperadas:** 1/1

### 4. Observaciones y Análisis Técnico

El vehículo demuestra una gran capacidad de anticipación al detectar el control policial en una de las salidas, lo que le permite cambiarse de carril de forma preventiva con mucho tiempo y espacio de sobra. Sin embargo, durante el tramo de alta velocidad, el sistema de visión sufre varias "alucinaciones": se confunde y cree que los elementos normales de la autopista (como los muros de contención laterales o los barriles de protección) son obstáculos que cortan el paso. A pesar de estos falsos positivos en la visión, el coche gestiona bien la situación, completa el recorrido y logra llegar a su destino de forma totalmente segura.

---

## 🛣️ Caso de Prueba: [TC-TWN04-007]

![Recorrido de la ruta](./media/Town04/7-Town04.mp4)


### 1. Identificación y Resultado

| Métrica | Detalle |
| :--- | :--- |
| **Mapa (CARLA)** | `Town04` |
| **Resultado de la Prueba**| Llegada a destino sin colisión |
| **Dificultad ($M_{total}$)**| 🟢 **1.00** |

### 2. Condiciones del Escenario

* **Descripción del escenario:** Sin obstáculos, preprarado para poner a prueba el modelo multimodal en la zona con mayor riqueza semántica de Town04.



### 3. Métricas de Evaluación

**👁️ Percepción y Razonamiento (VLM)**
* **Falsos Positivos / Negativos:** 0 / 0

**⚙️ Planificación y Control (RouteManager & BehaviorAgent)**
* **Porcentaje de Ruta Completado:** 100%
* **Replanificaciones Activadas/Esperadas:** 0/0

### 4. Observaciones y Análisis Técnico

A pesar de la elevada carga semántica y la diversidad arquitectónica propias del núcleo urbano de Town04, el modelo multimodal mantiene una tasa de falsos positivos nula.

---

## 🛣️ Caso de Prueba: [TC-TWN04-008]

![Recorrido de la ruta](./media/Town04/8-Town04.mp4)


### 1. Identificación y Resultado

| Métrica | Detalle |
| :--- | :--- |
| **Mapa (CARLA)** | `Town04` |
| **Resultado de la Prueba**| Colisión en corredor balizado |
| **Dificultad ($M_{total}$)**| 🔴 **10.37** |

### 2. Condiciones del Escenario

* **Descripción del escenario:** Restricción topológica severa a escala de ciudad, simulando un estado de emergencia generalizada con obstrucciones multifocales. El bloqueo es de alta complejidad semántica, empleando una flota de vehículos institucionales (policía, bomberos y ambulancias) distribuidos en vías clave. El escenario introduce cortes de balizamiento en disposición diagonal dentro del polígono de las intersecciones y bloqueos secundarios. Esta prueba somete a estrés extremo la capacidad del algoritmo de enrutamiento para hallar soluciones viables en un grafo masivamente penalizado, evaluando simultáneamente la robustez perceptual del VLM frente a contextos de emergencia.


### 3. Métricas de Evaluación

**👁️ Percepción y Razonamiento (VLM)**
* **Falsos Positivos / Negativos:** 1 / 0

**⚙️ Planificación y Control (RouteManager & BehaviorAgent)**
* **Porcentaje de Ruta Completado:** 40%
* **Replanificaciones Activadas/Esperadas:** 5/5

### 4. Observaciones y Análisis Técnico

En el primer cruce complejo, el coche detecta el bloqueo central a tiempo, pero tarda en ver el obstáculo de la izquierda. Esta falta de sincronización provoca que el vehículo dé un volantazo brusco y algo inestable para esquivarlo. Más adelante, al enfrentarse a la zona de emergencia más densa, el sistema se comporta de maravilla: logra interpretar correctamente los cortes diagonales y traza una maniobra de evasión bastante compleja hacia la izquierda. Sin embargo, igual que ocurrió en la Ruta 5, el vehículo acaba chocando en el tramo final al intentar atravesar un pasillo continuo delimitado por conos. Este choque confirma un patrón claro: el modelo visual falla al intentar interpretar barreras largas o "embudos" de conos que bloquean varias posibles salidas a la vez dentro de una misma imagen.

---

## 🛣️ Caso de Prueba: [TC-TWN04-009]

![Recorrido de la ruta](./media/Town04/9-Town04.mp4)


### 1. Identificación y Resultado

| Métrica | Detalle |
| :--- | :--- |
| **Mapa (CARLA)** | `Town04` |
| **Resultado de la Prueba**| Llegada a destino sin colisión |
| **Dificultad ($M_{total}$)**| 🔴 **13.33** |

### 2. Condiciones del Escenario

* **Descripción del escenario:** Escenario con varios obstáculos que simulan una zona afectada por obras o accidentes, señalizada con conos y carteles de advertencia. Lo más interesante de esta prueba es que crea una "trampa" en el mapa: la disposición de los bloqueos empuja al vehículo a tomar un desvío por la izquierda que acaba siendo un callejón sin salida. Esto obliga al coche a darse cuenta de que no puede avanzar por ahí, dar la vuelta y calcular una ruta completamente nueva usando el camino de la derecha. El objetivo es comprobar si el sistema es capaz de descartar calles bloqueadas sobre la marcha y corregir su propio rumbo tras haber tomado una decisión equivocada.



### 3. Métricas de Evaluación

**👁️ Percepción y Razonamiento (VLM)**
* **Falsos Positivos / Negativos:** 0 / 0

**⚙️ Planificación y Control (RouteManager & BehaviorAgent)**
* **Porcentaje de Ruta Completado:** 100%
* **Replanificaciones Activadas/Esperadas:** 3/3

### 4. Observaciones y Análisis Técnico

El sistema esquiva muy bien los obstáculos cuando están aislados. Sin embargo, en los cruces donde hay bloqueos complejos, el coche vuelve a detectar los peligros de forma un poco descoordinada, lo que provoca frenazos o correcciones de volante bruscas. Aun así, el gran éxito de esta prueba es cómo el sistema maneja la navegación: al esquivar un obstáculo, el coche se mete por un camino que resulta no tener salida. Lejos de quedarse atascado o chocar, el sistema demuestra ser resolutivo: frena, da la vuelta por sus propios medios y resuelve el problema recalculando toda la ruta para escapar por el camino correcto.

---

## 🛣️ Caso de Prueba: [TC-TWN04-010]

![Recorrido de la ruta](./media/Town04/10-Town04.mp4)


### 1. Identificación y Resultado

| Métrica | Detalle |
| :--- | :--- |
| **Mapa (CARLA)** | `Town04` |
| **Resultado de la Prueba**| Colisión con corredor balizado |
| **Dificultad ($M_{total}$)**| 🔴 **12.02** |

### 2. Condiciones del Escenario

* **Descripción del escenario:** Un escenario poblado de obstáculos repartidos por todo el centro urbano. Estos bloqueos son muy variados (incluyen barreras, conos, señales y vehículos) y están colocados estratégicamente en los cruces clave de las calles. El objetivo de esta prueba es llevar al planificador de rutas al límite al bloquear muchas calles importantes a la vez, obligando al sistema a recalcular el camino constantemente y a buscar grandes desvíos alternativos ante los continuos cortes de tráfico.



### 3. Métricas de Evaluación

**👁️ Percepción y Razonamiento (VLM)**
* **Falsos Positivos / Negativos:** 1 / 0

**⚙️ Planificación y Control (RouteManager & BehaviorAgent)**
* **Porcentaje de Ruta Completado:** 75%
* **Replanificaciones Activadas/Esperadas:** 5/6

### 4. Observaciones y Análisis Técnico

El vehículo detecta y esquiva adecuadamente los obstáculos cuando se presentan de forma aislada. Durante el trayecto en las vías rápidas, se vuelve a observar que el sistema se confunde con los elementos de protección de la autovía, marcando falsos positivos. Sin embargo, lo más importante de esta prueba es que confirma de forma definitiva un fallo repetitivo en el modelo visual: tal y como pasó en las Rutas 5 y 8, el sistema es incapaz de entender y gestionar los "pasillos" formados por conos que bloquean varias opciones a la vez (como el paso frontal y el derecho al mismo tiempo). Esta falta de comprensión espacial provoca que el vehículo se quede sin capacidad de reacción y acabe chocando.

---

## 🛣️ Caso de Prueba: [TC-TWN10HD-001]

![Recorrido de la ruta](./media/Town10HD/1-Town10HD.mp4)


### 1. Identificación y Resultado

| Métrica | Detalle |
| :--- | :--- |
| **Mapa (CARLA)** | `Town10HD` |
| **Resultado de la Prueba**| Llegada a destino sin colisión |
| **Dificultad ($M_{total}$)**| 🟢 **4.27** |

### 2. Condiciones del Escenario

* **Descripción del escenario:** Escenario con dos bloqueos distintos en las calles de Town10HD. El primero está formado por barreras de calle y un control policial reforzado con conos para asegurar el cierre total de la vía. Además, se ha bloqueado físicamente un paso de peatones para darle más realismo a la simulación. Este caso evalúa cómo responde el sistema cuando tiene que recalcular la ruta varias veces seguidas ante obstáculos de distinto tipo (obras y vehículos institucionales).



### 3. Métricas de Evaluación

**👁️ Percepción y Razonamiento (VLM)**
* **Falsos Positivos / Negativos:** 0 / 0

**⚙️ Planificación y Control (RouteManager & BehaviorAgent)**
* **Porcentaje de Ruta Completado:** 100%
* **Replanificaciones Activadas/Esperadas:** 2/2

### 4. Observaciones y Análisis Técnico

La percepción de los obstáculos funciona exitósamente y con buena anticipación. El modelo multimodal (VLM) procesa correctamente la división de las imágenes y detecta los coches de policía a través del crop derecho, entendiendo perfectamente que bloquean el paso. Gracias a esto, el sistema activa la replanificación de la ruta con tiempo y espacio suficiente para maniobrar. De igual manera, el vehículo gestiona sin problemas el segundo bloqueo situado en el cruce en cruz, demostrando que el algoritmo es robusto y capaz de resolver varios obstáculos seguidos sin generar falsos negativos en el camino.

---

## 🛣️ Caso de Prueba: [TC-TWN10HD-002]

![Recorrido de la ruta](./media/Town10HD/2-Town10HD.mp4)


### 1. Identificación y Resultado

| Métrica | Detalle |
| :--- | :--- |
| **Mapa (CARLA)** | `Town10HD` |
| **Resultado de la Prueba**| Llegada a destino sin colisión |
| **Dificultad ($M_{total}$)**| 🟢 **1.00** |

### 2. Condiciones del Escenario

* **Descripción del escenario:** Ruta de control sin ningún tipo de obstáculo, diseñada para realizar un recorrido estándar por la ciudad. El objetivo principal de esta prueba es evaluar la estabilidad del modelo multimodal (VLM) y comprobar que no genera falsos positivos al procesar la alta densidad de detalles, edificios y mobiliario urbano que caracteriza a Town10HD.



### 3. Métricas de Evaluación

**👁️ Percepción y Razonamiento (VLM)**
* **Falsos Positivos / Negativos:** 0 / 0

**⚙️ Planificación y Control (RouteManager & BehaviorAgent)**
* **Porcentaje de Ruta Completado:** 100%
* **Replanificaciones Activadas/Esperadas:** 0/0

### 4. Observaciones y Análisis Técnico

El vehículo completa la ruta de principio a fin de manera fluida y sin interrupciones. Durante todo el trayecto, el VLM analiza correctamente el entorno, indicando en sus razonamientos que la calzada (drivable path) se encuentra completamente despejada. Esto confirma que el modelo tiene una buena comprensión espacial y no se deja confundir por el ruido visual o la complejidad arquitectónica del mapa, manteniendo una tasa nula de falsos positivos en condiciones normales de conducción.

---

## 🛣️ Caso de Prueba: [TC-TWN10HD-003]

![Recorrido de la ruta](./media/Town10HD/3-Town10HD.mp4)


### 1. Identificación y Resultado

| Métrica | Detalle |
| :--- | :--- |
| **Mapa (CARLA)** | `Town10HD` |
| **Resultado de la Prueba**| Colisión en intersección con múltiples salidas bloqueadas |
| **Dificultad ($M_{total}$)**| 🟡 **6.03** |

### 2. Condiciones del Escenario

* **Descripción del escenario:** Escenario con múltiples bloqueos distribuidos en las calles principales, diseñados para forzar desvíos significativos en la ruta. Para recrear situaciones realistas de emergencia u obras complejas, las obstrucciones combinan barreras de tráfico, conos con luces, señales luminosas, contenedores y vehículos de servicio público.



### 3. Métricas de Evaluación

**👁️ Percepción y Razonamiento (VLM)**
* **Falsos Positivos / Negativos:** 0 / 0

**⚙️ Planificación y Control (RouteManager & BehaviorAgent)**
* **Porcentaje de Ruta Completado:** 40%
* **Replanificaciones Activadas/Esperadas:** 2/3

### 4. Observaciones y Análisis Técnico

El sistema gestiona con éxito el primer gran obstáculo del recorrido (formado por los vehículos de emergencia, barreras y contenedores). El VLM logra detectarlo correctamente a pesar de estar a una gran distancia frontal, lo que permite al planificador recalcular la ruta y esquivar este bloqueo compuesto de forma limpia.

Sin embargo, el sistema falla al llegar al segundo cruce, donde se presenta un bloqueo doble que corta tanto la salida frontal como la derecha. Aunque el VLM detecta la obstrucción frontal y el sistema penaliza esos nodos, el bloqueo de la salida derecha no se identifica con la antelación necesaria. Al no detectar el peligro a tiempo, el planificador no encuentra los nodos de la derecha para penalizarlos y decide tomar esa ruta, lo que termina desembocando en la colisión contra los obstáculos.

---

## 🛣️ Caso de Prueba: [TC-TWN10HD-004]

![Recorrido de la ruta](./media/Town10HD/4-Town10HD.mp4)


### 1. Identificación y Resultado

| Métrica | Detalle |
| :--- | :--- |
| **Mapa (CARLA)** | `Town10HD` |
| **Resultado de la Prueba**| Llegada a destino sin colisión |
| **Dificultad ($M_{total}$)**| 🟡 **6.15** |

### 2. Condiciones del Escenario

* **Descripción del escenario:** Escenario de triple bloqueo a lo largo del trayecto, con una configuración similar a la de la primera prueba (TC-TWN10HD-001), pero utilizando una variedad de elementos obstructivos diferentes. La principal complejidad geométrica de esta ruta radica en el primer bloqueo, que se encuentra muy retrasado en la calle y escondido en una esquina, lo que dificulta significativamente su visión directa desde la distancia.



### 3. Métricas de Evaluación

**👁️ Percepción y Razonamiento (VLM)**
* **Falsos Positivos / Negativos:** 0 / 0

**⚙️ Planificación y Control (RouteManager & BehaviorAgent)**
* **Porcentaje de Ruta Completado:** 100%
* **Replanificaciones Activadas/Esperadas:** 3/3

### 4. Observaciones y Análisis Técnico

El vehículo completa la ruta con total éxito, ejecutando todas las replanificaciones a la perfección y sin registrar ningún falso positivo. Resulta muy destacable el rendimiento del modelo multimodal (VLM) frente al primer obstáculo: a pesar de estar muy escorado y aparecer en el campo de visión de forma casi repentina al iniciar la curva, el sistema logra detectarlo con la antelación justa para que el RouteManager recalcule la trayectoria con seguridad. Los bloqueos restantes se superan de forma óptima y fluida, calcando la buena respuesta algorítmica y consistencia que ya se documentó en el TC-TWN10HD-001.

---

## 🛣️ Caso de Prueba: [TC-TWN10HD-005]

![Recorrido de la ruta](./media/Town10HD/5-Town10HD.mp4)


### 1. Identificación y Resultado

| Métrica | Detalle |
| :--- | :--- |
| **Mapa (CARLA)** | `Town10HD` |
| **Resultado de la Prueba**| Llegada a destino sin colisión |
| **Dificultad ($M_{total}$)**| 🟡 **7.17** |

### 2. Condiciones del Escenario

* **Descripción del escenario:** Escenario de doble bloqueo situado en el centro del mapa. Para cortar el paso, se agrupan varias barreras simulando un muro continuo de mayor tamaño. Además, se recrea una operación de descarga de un vehículo de transporte utilizando cajas de cartón, reforzando todo el perímetro obstructivo con conos de tráfico. Esta prueba evalúa cómo maneja el sistema una mezcla de obstáculos con características físicas y semánticas muy diferentes.



### 3. Métricas de Evaluación

**👁️ Percepción y Razonamiento (VLM)**
* **Falsos Positivos / Negativos:** 0 / 0

**⚙️ Planificación y Control (RouteManager & BehaviorAgent)**
* **Porcentaje de Ruta Completado:** 100%
* **Replanificaciones Activadas/Esperadas:** 1/1

### 4. Observaciones y Análisis Técnico

El vehículo completa el recorrido de forma impecable y gestiona sin problemas la gran variedad de elementos que bloquean la calle. Durante toda la ruta, el sistema se mantiene totalmente libre de falsos positivos y falsos negativos. El modelo multimodal (VLM) percibe los bloqueos con muy buena antelación, lo que permite al planificador (RouteManager) ejecutar las replanificaciones de manera fluida, segura y en el momento exacto.

---

## 🛣️ Caso de Prueba: [TC-TWN10HD-006]

![Recorrido de la ruta](./media/Town10HD/6-Town10HD.mp4)


### 1. Identificación y Resultado

| Métrica | Detalle |
| :--- | :--- |
| **Mapa (CARLA)** | `Town10HD` |
| **Resultado de la Prueba**| Llegada a destino sin colisión |
| **Dificultad ($M_{total}$)**| 🟢 **2.14** |

### 2. Condiciones del Escenario

* **Descripción del escenario:** Aunque la prueba se define como un bloqueo "simple", consiste realmente en una interrupción en una avenida principal de doble sentido y varios carriles, lo que impide el acceso directo a la zona central de Town10HD. La obstrucción se materializa alineando múltiples conos de tráfico con muy poca separación entre sí para formar una barrera transversal continua.



### 3. Métricas de Evaluación

**👁️ Percepción y Razonamiento (VLM)**
* **Falsos Positivos / Negativos:** 0 / 0

**⚙️ Planificación y Control (RouteManager & BehaviorAgent)**
* **Porcentaje de Ruta Completado:** 100%
* **Replanificaciones Activadas/Esperadas:** 1/1

### 4. Observaciones y Análisis Técnico

Al aproximarse a la intersección, el modelo multimodal (VLM) realiza una detección tardía del obstáculo situado en la salida izquierda. Esta demora perceptiva provoca que el vehículo inicie la maniobra planificada hacia esa calle, obligando al sistema a ejecutar una corrección cinemática brusca (un "cabeceo" o volantazo reactivo) en el momento en que se procesa el bloqueo. A pesar de este sobresalto dinámico, el control vehicular corrige la trayectoria con gran rapidez y eficacia, logrando esquivar la barrera y estabilizando el coche para reanudar la marcha. El resto de la ruta se completa de forma adecuada, segura y sin registrar ningún falso positivo.

---

## 🛣️ Caso de Prueba: [TC-TWN10HD-007]

![Recorrido de la ruta](./media/Town10HD/7-Town10HD.mp4)


### 1. Identificación y Resultado

| Métrica | Detalle |
| :--- | :--- |
| **Mapa (CARLA)** | `Town10HD` |
| **Resultado de la Prueba**| Colisión con obstáculo antes de llegar al destino |
| **Dificultad ($M_{total}$)**| 🟢 **3.74** |

### 2. Condiciones del Escenario

* **Descripción del escenario:** Bloqueo simple pero estratégicamente significativo, ya que corta una de las vías principales utilizadas para realizar cambios de sentido o cruzar de un lado a otro en Town10HD. Esta obstrucción se materializa instalando barreras de cadenas que cubren todo el ancho y el final de ambos carriles de circulación.



### 3. Métricas de Evaluación

**👁️ Percepción y Razonamiento (VLM)**
* **Falsos Positivos / Negativos:** 0 / 1

**⚙️ Planificación y Control (RouteManager & BehaviorAgent)**
* **Porcentaje de Ruta Completado:** 40%
* **Replanificaciones Activadas/Esperadas:** 0/1

### 4. Observaciones y Análisis Técnico

La prueba finaliza en colisión contra la barrera de cadenas. El modelo multimodal (VLM) no logra detectar el obstáculo, generando un falso negativo crítico. Este fallo de percepción se debe principalmente a dos factores concurrentes: un entorno de fondo visualmente muy sobrecargado (abundancia de árboles y mobiliario urbano) y el camuflaje cromático de la propia barrera, cuyo color se funde casi por completo con el tono del asfalto. Al no identificar la obstrucción en el análisis de los recortes visuales, el sistema no activa ninguna replanificación y el vehículo mantiene la trayectoria original a ciegas hasta el momento del impacto.

---

## 🛣️ Caso de Prueba: [TC-TWN10HD-008]

![Recorrido de la ruta](./media/Town10HD/8-Town10HD.mp4)


### 1. Identificación y Resultado

| Métrica | Detalle |
| :--- | :--- |
| **Mapa (CARLA)** | `Town10HD` |
| **Resultado de la Prueba**| Llegada a destino sin colisión |
| **Dificultad ($M_{total}$)**| 🟡 **5.12** |

### 2. Condiciones del Escenario

* **Descripción del escenario:** Bloqueo total en uno de los tramos viales que conecta las distintas secciones laterales de Town10HD. La interrupción se simula mediante el despliegue de conos de tráfico y varios vehículos policiales, recreando un escenario de intervención u operación de seguridad activa que restringe por completo el paso en esa calle específica.



### 3. Métricas de Evaluación

**👁️ Percepción y Razonamiento (VLM)**
* **Falsos Positivos / Negativos:** 0 / 0

**⚙️ Planificación y Control (RouteManager & BehaviorAgent)**
* **Porcentaje de Ruta Completado:** 100%
* **Replanificaciones Activadas/Esperadas:** 1/1

### 4. Observaciones y Análisis Técnico

El sistema demuestra una excelente capacidad de percepción bajo condiciones visuales adversas. A pesar de que la operación policial se encuentra ubicada en un entorno muy frondoso y oscurecido por las sombras de los árboles de la ciudad, el modelo multimodal (VLM) logra identificar correctamente los vehículos policiales y el balizamiento. Esta detección precisa, lograda en un escenario de baja iluminación natural y contraste reducido, permite al planificador ejecutar la replanificación topológica de manera totalmente exitosa y sin incurrir en colisiones.

---

## 🛣️ Caso de Prueba: [TC-TWN10HD-009]

![Recorrido de la ruta](./media/Town10HD/9-Town10HD.mp4)


### 1. Identificación y Resultado

| Métrica | Detalle |
| :--- | :--- |
| **Mapa (CARLA)** | `Town10HD` |
| **Resultado de la Prueba**| Llegada a destino sin colisión |
| **Dificultad ($M_{total}$)**| 🟡 **9.29** |

### 2. Condiciones del Escenario

* **Descripción del escenario:** Escenario con un bloqueo relativamente sencillo situado en una de las vías que conecta la sección urbana de Town10HD con la autovía periférica. La interrupción se configura utilizando únicamente un par de conos de tráfico y una señal luminosa de advertencia.



### 3. Métricas de Evaluación

**👁️ Percepción y Razonamiento (VLM)**
* **Falsos Positivos / Negativos:** 0 / 0

**⚙️ Planificación y Control (RouteManager & BehaviorAgent)**
* **Porcentaje de Ruta Completado:** 100%
* **Replanificaciones Activadas/Esperadas:** 1/1

### 4. Observaciones y Análisis Técnico

A pesar de tratarse de un obstáculo de escaso volumen y estar ubicado en una calle estrecha, el modelo multimodal (VLM) logra percibirlo con total claridad. Esta correcta identificación visual demuestra la buena sensibilidad del sistema ante bloqueos de menor escala, permitiendo al planificador ejecutar la replanificación de la ruta asociada de manera fluida y exitosa.

---

## 🛣️ Caso de Prueba: [TC-TWN10HD-010]

![Recorrido de la ruta](./media/Town10HD/10-Town10HD.mp4)


### 1. Identificación y Resultado

| Métrica | Detalle |
| :--- | :--- |
| **Mapa (CARLA)** | `Town10HD` |
| **Resultado de la Prueba**| Llegada a destino sin colisión |
| **Dificultad ($M_{total}$)**| 🟡 **9.79** |

### 2. Condiciones del Escenario

* **Descripción del escenario:** Escenario de doble bloqueo utilizando barreras de tráfico y conos. A diferencia de las interrupciones estándar, los obstáculos no se colocan de forma transversal en cada calle por separado, sino en diagonal a través de la intersección. Esta disposición crea una barrera geométricamente mucho más compleja, diseñada para someter al sistema a una prueba de percepción y evaluación de rutas más rigurosa.



### 3. Métricas de Evaluación

**👁️ Percepción y Razonamiento (VLM)**
* **Falsos Positivos / Negativos:** 0 / 0

**⚙️ Planificación y Control (RouteManager & BehaviorAgent)**
* **Porcentaje de Ruta Completado:** 100%
* **Replanificaciones Activadas/Esperadas:** 3/3

### 4. Observaciones y Análisis Técnico

Para lograr sortear este obstáculo diagonal, fue necesaria una intervención inicial utilizando la función de override (percepción manual). Gracias a la inyección de este evento, el sistema es capaz de penalizar algorítmicamente tanto la ruta frontal como la lateral, lo que permite al planificador recalcular la trayectoria y evitar la compleja disposición del bloqueo. Más adelante durante el trayecto, el vehículo vuelve a atravesar el mismo cruce conflictivo, pero abordándolo desde una dirección diferente, gestionando la situación sin incidencias hasta alcanzar el destino final con total éxito.

---