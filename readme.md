# Estrategia de Trading con Python

Esta estrategia de trading está implementada en Python utilizando la biblioteca `backtrader`. La estrategia se basa en el cruce de dos medias móviles simples (SMA) para generar señales de compra y venta en un activo financiero.

## Descripción de la estrategia

La estrategia utiliza dos parámetros configurables:

- `maperiod`: El período de la primera media móvil simple.
- `maperiod2`: El período de la segunda media móvil simple.

La estrategia se define como una clase llamada `TestStrategy` que hereda de `bt.Strategy` de `backtrader`. A continuación se presentan los principales métodos de la estrategia:

- `log(txt, dt=None)`: Una función para imprimir mensajes de registro.
- `notify_order(order)`: El método que se ejecuta cuando se produce un cambio en una orden (ejecución, cancelación, rechazo, etc.).
- `notify_trade(trade)`: El método que se ejecuta cuando se cierra una operación.
- `next()`: El método que se ejecuta en cada nuevo tick de datos y que contiene la lógica principal de la estrategia.

### Visualización de gráficos

La estrategia incluye una funcionalidad para proyectar gráficos que muestran las barras en velas, las medias móviles y los puntos de compra y venta. Puedes utilizar la función `plot()` de `backtrader` para visualizar los datos en un gráfico. Asegúrate de tener instalada una biblioteca gráfica compatible, como `matplotlib`, para poder ver los gráficos.

### Manejo de datos en formato CSV

La estrategia guarda los datos utilizados en la estrategia en un archivo CSV. Esto permite cargar datos históricos y utilizarlos para realizar backtesting o ejecutar la estrategia en tiempo real. Puedes utilizar la biblioteca `pandas` para leer y escribir datos en formato CSV.

## Ejecución de la estrategia
![1](https://github.com/Rsolitario/indicadores_py/assets/6273761/5346763c-0bc9-466a-8401-0a36576befef)
![2](https://github.com/Rsolitario/indicadores_py/assets/6273761/74a87492-52e6-4766-9a45-8d2f1aba14ac)
![3](https://github.com/Rsolitario/indicadores_py/assets/6273761/d94071cd-8424-4465-a4c9-4bbced355864)
![4](https://github.com/Rsolitario/indicadores_py/assets/6273761/dccf4191-fcaf-4883-88cc-04b1ecefb9f0)
