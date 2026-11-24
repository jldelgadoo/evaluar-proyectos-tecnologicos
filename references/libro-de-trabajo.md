# Usar el libro de trabajo

La [plantilla Excel](../assets/evaluacion-tecnologica.xlsx) modela una alternativa frente a su referencia, con un horizonte de hasta 60 meses más el mes inicial. Se puede descargar y abrir directamente. Para que un agente entregue una planilla nueva, copiar el archivo a la ubicación solicitada y completar los campos autorizados. La orden `python3 scripts/proyectos.py plantilla RUTA_NUEVA.xlsx` crea una copia en blanco con las fórmulas y validaciones.

## Hojas y responsabilidades

| Hoja | Qué completar | Qué se obtiene |
|---|---|---|
| Resumen | Iniciativa, referencia, decisión solicitada, recursos requeridos y fundamento | Resultados del escenario seleccionado y estado del respaldo |
| Supuestos | Controles, valores de cada escenario y evidencia | Supuestos activos y validaciones por fila |
| Flujo mensual | Consultar el calendario calculado | Egresos, beneficios, caja acumulada, VAN, ROI, payback, déficit máximo y horas |
| Sensibilidad | Variaciones porcentuales de volumen elegible y costo variable unitario en los encabezados amarillos | Matriz de caja neta y umbrales de equilibrio |
| Viabilidad | Indicadores, riesgos, condiciones de prueba, acciones, responsables y fechas | Seguimiento de las condiciones de inversión y escalamiento |

## Completar Supuestos

Elegir escenario en B5 e indicar moneda y horizonte en B6 y B7. La tasa efectiva anual en B8 es opcional. Si se usa, respaldarla en F8:I8. En las filas 12 a 26, C, D y E corresponden a los tres escenarios. La columna B muestra el activo. Registrar fuente o método, fecha, responsable y estado en F:I. J y K muestran el control del valor y de la evidencia.

| Filas | Tratamiento |
|---|---|
| 12–14 | Desembolso inicial al mes 0 y un desembolso adicional en su mes de pago. El mes del adicional se requiere cuando su importe es positivo |
| 15–18 | Costo fijo operativo y gasto de referencia que realmente se retira, cada uno con su propio mes inicial. Ambos continúan hasta el cierre del horizonte |
| 19–22 | Volumen elegible mensual, proporción de adopción objetivo, primer mes de actividad y cantidad de meses hasta el objetivo. La adopción aumenta en tramos mensuales iguales y luego se estabiliza |
| 23–25 | Costo variable, ahorro efectivo y margen incremental por unidad adoptada. El margen admite valores negativos. Estas tres tasas se multiplican por el mismo volumen |
| 26 | Horas netas liberadas por unidad. Un valor ausente mantiene pendiente la capacidad. Un valor negativo representa carga adicional |

Completar con cero los importes monetarios que se haya determinado que no aplican. Un campo vacío conserva la incertidumbre. Para flujos puramente fijos pueden omitirse los parámetros de actividad cuando los tres importes por unidad son cero. Para cuantificar horas distintas de cero se necesita también el perfil de actividad. Las cuantías proyectadas pueden calcularse con respaldo aún pendiente y deben identificarse como estimaciones.

## Sensibilidad

La caja neta de la matriz es la caja fija neta más los beneficios por actividad, menos los costos variables, ajustados por las variaciones elegidas. Las filas cambian el volumen elegible y las columnas cambian el costo variable unitario. Cada efecto se aplica solo a sus componentes. El centro a variación cero concilia con la caja del escenario activo. El ahorro adicional por unidad indica la brecha para llegar a equilibrio con el volumen proyectado. La hoja diferencia volumen mínimo viable y límite superior cuando el margen de la actividad es negativo.

## Alcance y adaptación

La plantilla supone moneda única, flujos al cierre mensual, dos hitos de inversión como máximo, un perfil de adopción lineal y tasas unitarias constantes por escenario. Su perímetro básico es incremental, antes de impuestos y financiamiento. Cuando haya desembolsos por múltiples hitos, bandas de precios, capital de trabajo, impuestos, volatilidad de demanda o cobros con desfases materiales, explicitar la ampliación y modelar sus periodos en una serie detallada. El auditor de CSV admite calendarios mensuales irregulares en importes y cualquier horizonte mensual continuo.

## Auditar el Excel guardado

Ejecutar `python3 scripts/proyectos.py auditar-excel LIBRO_COMPLETADO.xlsx`. La orden lee el detalle mensual del escenario activo, reconstruye los indicadores y contrasta cada flujo y saldo, los resultados del resumen y el centro de sensibilidad. Devuelve un JSON con las diferencias y sus celdas. La tolerancia es media centésima en importes y horas, y 0,00000005 para el ROI en fracción decimal. El código de salida es 0 si concilia, 1 si localiza diferencias y 2 si faltan datos o el archivo requiere corrección.

Recalcular y guardar el libro después de editarlo. La auditoría utiliza los valores guardados por la aplicación de planillas. Para evaluar la credibilidad de las entradas o una fórmula del modelo de adopción, aplicar también los [controles de revisión](revision.md).

## Comprobación independiente con CSV

Usar [templates/flujos.csv](../templates/flujos.csv). Exportar una fila por mes, alternativa y escenario, incluido el mes cero. En cada fila, identificar alternativa, escenario y moneda. Las columnas D a I del detalle de Flujo mensual corresponden, en ese orden, a los seis componentes monetarios del CSV. La columna A es mes y M contiene horas. Los egresos son negativos o cero y los ahorros positivos o cero. Margen y horas admiten ambos signos. Incluir importes explícitos, incluso cuando sean cero. Para horas desconocidas dejar el campo vacío.

Guardar en UTF-8, con coma como separador de columnas y punto decimal sin separadores de miles. La orden `python3 scripts/proyectos.py auditar ARCHIVO.csv` emite un resumen JSON por alternativa y escenario. Añadir `--tasa-anual TASA_DECIMAL` para calcular el VAN. La tasa se aplica a todos los grupos de esa ejecución. Los importes se devuelven como cadenas decimales para conservar precisión. Un indicador indisponible queda en `null`. La herramienta rechaza series con meses faltantes, repetidos o cambios de moneda dentro de un mismo grupo.

Comparar los resultados con la misma versión y horizonte de la planilla. La salida por grupo permite contrastar escenarios calculados sin sobrescribir supuestos. No sumar importes entre grupos ni comparar valores presentes con distintas fechas base.
