# Modelo financiero incremental

## Registro de supuestos

| Supuesto | Unidad | Conservador | Base | Favorable | Fuente o método | Fecha | Responsable | Estado |
|---|---|---:|---:|---:|---|---|---|---|

Vincular los meses proyectados al escenario seleccionado. Exponer cualquier estimación que cambie dentro del horizonte, por ejemplo la adopción progresiva o la coexistencia temporal de dos plataformas.

## Cálculos

- **Flujo incremental del periodo** = ahorro efectivo + margen incremental − implementación − costos operativos incrementales. Excluir del costo operativo los costos variables ya descontados al calcular el margen.
- **Caja acumulada** = suma del flujo incremental hasta ese periodo. Si nunca hay déficit, reportar que el payback no aplica. Si hubo déficit y queda sin recuperar, reportar que el payback está fuera del horizonte. Si el saldo vuelve a caer después de recuperarse, indicar el mes de primera recuperación y el déficit posterior.
- **VAN** = suma de los flujos de cada periodo descontados más el flujo inicial en su valor original. Para una tasa anual efectiva y flujos al cierre de cada mes, descontar el flujo del mes m dividiéndolo por (1 + tasa anual)^(m/12). Alinear tasas nominales o reales con los flujos del mismo tipo.
- **Punto de equilibrio** = valor de un supuesto que permite alcanzar la condición acordada, por ejemplo caja acumulada igual a cero al mes 12. Indicar qué otras variables se mantienen fijas.
- Mostrar costo total y valor operativo aunque falten datos para VAN o payback. No inferir que un valor ausente equivale a cero.

## Ejemplo ficticio

Una automatización de solicitudes internas cuesta 3.600.000 unidades monetarias en el mes 0 y 250.000 al mes del mes 1 al 12. Se estima reducir 800.000 al mes en horas extra pagadas desde el mes 3.

| Resultado del escenario base | Valor |
|---|---:|
| Costo total | 6.600.000 |
| Ahorro efectivo en 10 meses | 8.000.000 |
| Caja acumulada al mes 12 | 1.400.000 |
| Payback simple | Mes 10 |
| Ahorro mensual mínimo para recuperar al mes 12 | 660.000 |

Si el ahorro parte en el mes 5 y baja a 600.000 mensuales, la caja al mes 12 es −1.800.000 y no se recupera en el horizonte. El piloto debe medir la precisión de la clasificación y comprobar con Gestión de Personas que el gasto de horas extra efectivamente se pueda reducir. Cualquier capacidad adicional se sigue en horas y queda fuera de esos montos.

## Lecturas

- [FAST Standard](https://fast-standard.org/the-fast-standard/)
- [Financial Modelling Code de ICAEW](https://www.icaew.com/-/media/corporate/files/technical/technology/excel/financial-modelling-code.ashx)
- [The AQuA Book](https://www.gov.uk/guidance/the-aqua-book)
