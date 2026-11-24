# Criterios de evaluación de la skill

Aplicar estas pruebas a una copia desechable. Registrar versión, entrada modificada, resultado esperado, resultado obtenido y corrección. Las pruebas describen propiedades del método y pueden repetirse con datos autorizados del usuario.

| Prueba | Evidencia de aceptación |
|---|---|
| Entrega en blanco | La skill entrega un XLSX con fórmulas, escenarios y campos editables. Los indicadores permanecen pendientes hasta contar con las entradas necesarias |
| Ausencia de cifras comprobables | La respuesta identifica la incertidumbre material, su dueño y la evidencia necesaria para decidir. Se puede entregar la ficha preliminar |
| Cambio de escenario | Cambian los flujos y el resumen según las entradas del escenario elegido. Un valor ausente en otro escenario no contamina el activo |
| Ahorro frente a capacidad | Una variación en horas liberadas modifica el indicador de capacidad y conserva el flujo de caja si los demás parámetros quedan fijos |
| Coexistencia tecnológica | Posponer el retiro del legado mantiene el gasto de referencia durante el solapamiento y reduce el beneficio acumulado dentro del horizonte |
| Adopción de IA | Reducir adopción disminuye actividad, costos variables y beneficios variables. Los desembolsos y costos fijos conservan su calendario |
| Costo obligatorio | El dictamen compara alternativas factibles y el costo de diferir aunque ninguna alcance una recuperación simple |
| Conciliación | El cálculo independiente reproduce caja neta, déficit máximo y recuperación para la misma serie mensual. Con tasa cero, VAN y caja neta coinciden |
| Auditoría directa del Excel | Alterar una salida en una copia calculada identifica la celda discrepante. La plantilla aún vacía informa qué falta para auditar |
| Calidad del dictamen | Cada recomendación identifica la decisión, el criterio que la sostiene, una condición que la cambiaría y un responsable de verificarla |

Ejecutar `python3 -B evals/verificar.py` desde la raíz para comprobar la plantilla en blanco, la integridad del CSV y las propiedades aritméticas de los saldos, la recuperación y el descuento a tasa cero. Estas comprobaciones utilizan únicamente la biblioteca estándar.
