# Evaluar proyectos tecnológicos

Una skill en español para decidir si conviene financiar, pilotear, reformular, postergar o descartar una inversión en IA, software, infraestructura o modernización. La evaluación identifica la alternativa preferida, el supuesto que puede cambiar la decisión y la evidencia necesaria para comprometer recursos.

**[Descargar la plantilla Excel](https://raw.githubusercontent.com/jldelgadoo/evaluar-proyectos-tecnologicos/main/assets/evaluacion-tecnologica.xlsx)** · **[Leer la skill](SKILL.md)** · **[Abrir el dictamen de inversión](templates/dictamen.md)**

## Qué entrega

| Necesidad | Entregable |
|---|---|
| Priorizar una iniciativa | Decisión solicitada, línea base, alternativas viables y principal incertidumbre |
| Justificar una inversión | Modelo de caja incremental a tres escenarios, recuperación, VAN, ROI, déficit máximo y sensibilidad |
| Diseñar un piloto | Hipótesis comprobable, costo, alcance, métricas, umbrales y regla de salida |
| Comparar opciones o auditar cifras | Dictamen por alternativa y conciliación independiente de flujos mensuales |
| Seguir el beneficio | Métrica, responsable, acción de realización y fecha de revisión |

## Cómo utilizarla

**Con un agente.** En un proyecto de Codex, sitúa el contenido del repositorio en `.agents/skills/evaluar-proyectos-tecnologicos/` e invoca `$evaluar-proyectos-tecnologicos`. Indica qué decisión necesitas tomar, la situación actual y los datos disponibles. Si solicitas Excel, la skill parte del archivo incluido y puede completar los campos respaldados.

**En Excel.** Abre una copia de la plantilla por alternativa. Completa las celdas amarillas, selecciona el escenario y revisa el flujo y los umbrales de caja. El libro admite hasta 60 meses y lleva las horas liberadas fuera del flujo monetario. [Guía del libro](references/libro-de-trabajo.md)

**Con Python 3.10 o posterior.** La herramienta local utiliza la biblioteca estándar. Ejecuta los comandos desde la raíz del repositorio. La primera orden crea una copia en blanco. La segunda audita directamente un Excel completado y guardado. La tercera comprueba flujos mensuales externos en formato CSV.

```text
python3 scripts/proyectos.py plantilla RUTA_NUEVA.xlsx
python3 scripts/proyectos.py auditar-excel LIBRO_COMPLETADO.xlsx
python3 scripts/proyectos.py auditar ARCHIVO.csv [--tasa-anual TASA_DECIMAL]
```

## Recursos del método

| Recurso | Para qué consultarlo |
|---|---|
| [Alternativas y evidencia](references/alternativas-y-evidencia.md) | Construir la referencia y documentar la procedencia de cada supuesto |
| [Modelo financiero](references/modelo-financiero.md) | Convertir actividad en caja, mantener fechas coherentes y estimar umbrales |
| [Viabilidad tecnológica](references/viabilidad-tecnologica.md) | Evaluar calidad y costo de IA, integración, coexistencia y retiro tecnológico |
| [Piloto y beneficios](references/piloto-y-beneficios.md) | Acordar criterios de salida y verificar la captura posterior del beneficio |
| [Revisión del caso](references/revision.md) | Detectar dobles conteos, diferencias de alcance y resultados sin respaldo |
| [Formato de flujos](templates/flujos.csv) | Conciliar los resultados mensuales por alternativa, escenario y moneda |
| [Criterios de evaluación](evals/criterios.md) | Comprobar que el agente y la planilla responden correctamente a cambios y faltantes |

La decisión y la validación de los supuestos corresponden a las personas responsables de la iniciativa. La plantilla se entrega en blanco, con fórmulas y campos editables.
