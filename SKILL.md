---
name: evaluar-proyectos-tecnologicos
description: Construye, compara y audita casos de negocio para IA, software, automatización, infraestructura y modernización. Úsala para evaluar inversiones internas, dimensionar un piloto, revisar evidencia, estimar flujos mensuales, VAN o recuperación, o entregar un Excel editable y una recomendación en español.
---

# Evaluar proyectos tecnológicos

Responder primero qué decisión se propone, por qué y qué evidencia la cambiaría. Ajustar la profundidad al compromiso que se pide. Una priorización temprana puede resolverse con rangos y una prueba de valor. Una inversión requiere alternativas comparables, supuestos con respaldo y un plan de realización de beneficios.

## Elegir la ruta de trabajo

| Petición | Trabajo | Entregable |
|---|---|---|
| Calificar una idea | Precisar decisión, referencia, objetivo medible y dato decisivo que falta | Ficha preliminar y siguiente validación |
| Solicitar inversión o comparar opciones | Definir alternativas, construir caja por escenario, probar sensibilidad y revisar viabilidad | Dictamen ejecutivo y modelo editable |
| Decidir si pilotear o escalar | Diseñar una prueba capaz de cambiar la decisión, con límites, responsables y regla de salida | Protocolo de piloto y decisión condicionada |
| Revisar un caso existente | Conservar entradas originales, reconstruir los indicadores y contrastar el argumento con la evidencia | Hallazgos por impacto y cálculo corregido o pendiente |
| Generar una planilla | Partir de la plantilla incluida, rellenar solo datos suministrados o respaldados y verificar la copia | Archivo Excel utilizable con fórmulas y validaciones |

## Procedimiento

1. **Fijar la comparación.** Registrar quién decide, qué monto o autorización solicita el proponente, qué ocurre si se posterga y qué restricciones son obligatorias. Definir una referencia dinámica, horizonte, moneda y población común. Aplicar [Alternativas y evidencia](references/alternativas-y-evidencia.md).
2. **Explicar el mecanismo de valor.** Trazar la secuencia desde población elegible y adopción hasta actividad real, resultado operativo y efecto económico. Registrar fuente, fecha, responsable y nivel de validación de cada supuesto material. Identificar el gasto retirable, margen incremental, capacidad reutilizable y riesgo residual.
3. **Modelar las alternativas viables.** Estimar diferencias de caja respecto de la referencia. Asignar cada flujo al mes en que ocurre. Comparar escenarios coherentes y variar por separado los factores que pueden cambiar la decisión. Calcular el umbral de equilibrio cuando esté identificado. Usar [Modelo financiero](references/modelo-financiero.md).
4. **Probar condiciones de ejecución.** Elegir las revisiones específicas del tipo de proyecto en [Viabilidad tecnológica](references/viabilidad-tecnologica.md). Vincular cada impedimento material con una prueba verificable, una persona responsable y una fecha.
5. **Resolver la incertidumbre.** Si la evidencia disponible permite actuar, recomendar una alternativa. Si una prueba acotada puede resolver una duda material, definir su costo, métrica y regla de salida. Consultar [Piloto y realización del beneficio](references/piloto-y-beneficios.md).
6. **Revisar y entregar.** Aplicar los [controles de revisión](references/revision.md). Presentar la propuesta, el rango de resultados, el supuesto dominante, la condición que cambia la recomendación y el compromiso siguiente. Para comité, completar el [dictamen](templates/dictamen.md).

## Trabajar con archivos

- Para una solicitud de Excel, entregar una copia de [la plantilla](assets/evaluacion-tecnologica.xlsx). También se puede crear con la orden `plantilla` de [la herramienta local](scripts/proyectos.py). El [contrato del libro](references/libro-de-trabajo.md) indica qué celdas completar, cómo revisar las dependencias y cuándo ampliar el calendario. La plantilla puede usarse directamente en Excel.
- Para auditar una planilla completada y guardada, usar `auditar-excel`. Revisar las diferencias por celda en el flujo, el resumen y el centro de sensibilidad. Para contrastar otra serie mensual, usar `auditar` sobre el [CSV de flujos](templates/flujos.csv). Conciliar en la misma moneda y el mismo escenario. El cálculo es local y utiliza la biblioteca estándar de Python.
- Usar una copia por alternativa y conservar el mismo horizonte y moneda al comparar. En cada copia, el selector recalcula el caso activo. En el dictamen, identificar la versión y el escenario de cada resultado.
- Generar fichas y modelos en blanco cuando el usuario pida una plantilla. Conservar los datos faltantes como pendientes. Omitir cifras ficticias, casos de demostración y nombres de personas u organizaciones.
