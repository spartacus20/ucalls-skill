# Un recorrido, dos documentos

## Reparto de responsabilidades

| Prompt base | Información del negocio |
|---|---|
| Identidad operativa y objetivo del agente | Negocio, oferta, audiencia y datos prácticos vigentes |
| Cómo reconstruir estado y consultar el manual | Voz, ritmo, emojis y uso de las frases |
| Resumen del mismo orden de etapas | Instrucciones y condiciones detalladas de cada etapa |
| Criterios explícitos para avanzar o esperar | Preguntas y respuestas literales por situación |
| Permisos, excepciones y acciones disponibles | Testimonios, precios y explicaciones aprobadas |
| Límites, paradas y prioridades | Dudas directas, objeciones, incidencias y pendientes |

La duplicación imprescindible es el criterio de avance, con el mismo significado. No mantengas versiones comerciales paralelas. Una frase de envío dentro del manual no autoriza enviar si falta la aceptación exigida por la etapa.

No uses «si hay conflicto siempre manda el prompt» para conservar dos instrucciones incompatibles. Reconcílialas antes de entregar. El orden comercial sale del manual acordado; el prompt lo ejecuta. Los hechos y frases vigentes salen del manual; las capacidades deben coincidir con el entorno real. Una petición explícita del usuario manda sobre la plantilla de esta skill.

## Estructura de referencia y adaptación

Brainbuilder combina datos del negocio, estilo, continuidad, dudas directas, etapas, respuestas condicionales y pendientes. Su recorrido completo incluye bienvenida, objetivo, diagnóstico, caso, oferta de vídeo, envío, propuesta de llamada, atajo por interés avanzado, agenda, confirmación, incidencias y seguimientos.

Traslada la lógica, no sus supuestos:

| Situación del nuevo proyecto | Adaptación |
|---|---|
| Venta consultiva con recurso previo | Mantener diagnóstico pertinente, recurso opcional y propuesta del siguiente paso |
| Cliente solicita cita o compra directamente | Atajo a los datos necesarios y ejecución; no imponer dolor, caso o vídeo |
| Atención informativa sin venta | Resolver dudas, aclarar lo necesario y cerrar; eliminar cualificación comercial |
| Sin casos aprobados | Omitir prueba social; no bloquear el recorrido solo por eso |
| Sin recurso previo | Omitir oferta/envío de recurso; conservar aceptación del siguiente paso si lo propone el agente |
| Varias ofertas | Rama por necesidad y oferta; no juntar condiciones o testimonios distintos |
| Agenda nativa | Separar consulta real de disponibilidad, elección del cliente y reserva confirmada |
| Agenda externa | Enviar tras solicitud/aceptación; esperar evidencia de reserva |

La categoría de género de los casos, los formadores, la financiación, los emojis, los nombres de leads y las exclusiones de historias no se convierten en políticas universales. Conserva esas decisiones únicamente donde el usuario las haya pedido o el negocio las justifique.

## Escribir una etapa utilizable

Cada etapa activa necesita:

1. Qué la activa y para qué sirve.
2. Qué hechos ya deberían conocerse, cuáles faltan y qué respuesta completa el paso.
3. Situaciones concretas con una variante pertinente, no una lista de preguntas que se envía junta.
4. Cuándo preguntar, responder, ejecutar o guardar silencio.
5. Dónde continuar tras aceptar, dudar, rechazar o aplazar.

Formato de bloque del manual:

```markdown
### ETAPA 2 · CONTEXTO Y OBJETIVO

Cuándo: falta un dato que cambia el encaje o la recomendación.
Para completar: los campos definidos para este negocio constan en el historial.
No repetir: datos respondidos; no hacer otra confirmación de un objetivo explícito.

#### Situación: [dato concreto pendiente, con contexto suficiente]

Usar si: [condición verificable].
Respuesta: [insertar aquí solo las burbujas reales o autorizadas].
Después: esperar respuesta; actualizar lo conocido; avanzar solo si se completa el criterio.
No usar si: [otra intención o dato ya resuelto].
```

El ejemplo es una plantilla de autoría. Sus campos nunca se entregan al lead. En el resultado final, los huecos se llevan al apartado interno de pendientes y las ramas incompletas se bloquean.

No repitas «Origen: conversación X» en el manual operativo. La trazabilidad vive en la evidencia interna. Tampoco mezcles frases excluidas con respuestas activas bajo títulos atractivos: conserva las exclusiones en evidencia, y en el manual solo su política cuando haga falta.

## Criterio de diagnóstico

Define los campos observables que permiten recomendar un paso. La frase «estudia el caso y profundiza» no basta para dirigir el agente.

En Brainbuilder, el ajuste reciente exige antes de una oferta proactiva conocer oferta o negocio que quiere construir, situación de clientes, objetivo, vía de captación y punto concreto de bloqueo. «Me cuesta vender» no determina si faltan consultas, si son poco adecuadas o si no se cierran. Tener virales no demuestra disponer de clientes.

En otro negocio el criterio puede ser diferente. Para visitas inmobiliarias: inmueble de interés, intención y datos imprescindibles de visita; no asumir ingresos o financiación. Para atención de pedidos: identificación necesaria del pedido y consulta concreta; no investigar dolor comercial. Para atención clínica administrativa: servicio solicitado y modalidad; no convertir la conversación en un diagnóstico médico.

Una respuesta válida puede ser «aún no tengo clientes» o «todavía no tengo oferta». No fuerces cifras ni rechaces desconocidos sin una política confirmada. No pidas toda la lista en un turno. Responde primero a una duda, luego aclara el primer campo pertinente que falte.

Incluye el mismo criterio en la etapa del manual y el resumen del prompt. En las prioridades finales, recuerda la puerta crítica de forma breve y coherente, sin crear una excepción nueva.

## Propuesta, permiso y ejecución

Para cada recurso o acción identifica un alcance concreto: catálogo, vídeo de X, llamada, visita, compra o reserva. Registra internamente qué se ofreció y su respuesta.

| Última situación | Qué permite una respuesta breve |
|---|---|
| Oferta de un vídeo pendiente | «ok» permite enviar ese vídeo |
| Vídeo ya enviado | «ok» confirma recepción; no prueba que lo vio ni acepta una llamada |
| Propuesta de visita pendiente | «sí» acepta la visita; completar solo datos necesarios para reservar |
| Enlace de agenda enviado | «gracias» no demuestra reserva |
| Pregunta sobre su objetivo | «sí» confirma ese objetivo; no acepta un recurso |
| Rechazó una propuesta | Un asentimiento posterior a otro tema no revive el permiso |

Cuando el agente ofrece el paso, el turno termina después de pedir permiso. Cuando el usuario lo solicita expresamente, no hace falta volver a ofrecerlo. Con varias ofertas o un antecedente ambiguo, aclara cuál acepta; no interpretes «ok» como permiso global.

Si falta el recurso, conserva la aceptación como entrega pendiente. No repitas la oferta ni anuncies un envío imposible. Solicitar un recurso no prueba que exista; el recurso puede estar en un catálogo, medio, herramienta o configuración externa válida.

La prueba social es opcional y debe relacionarse con la dificultad, no solo con el perfil superficial. No garantiza replicar resultados. El permiso posterior se pide para el recurso real: solo atribúyele explicar un caso si contiene ese caso. No uses «si pudiéramos llevarte al mismo resultado» como una promesa individual.

## Consultar frases sin sonar a interrogatorio

Antes de cada turno, el agente debe identificar intención, etapa, hechos conocidos, duda o propuesta pendiente y acciones ejecutadas. A continuación selecciona un bloque del manual y solo sus burbujas necesarias.

Para reformular, busca una razón: resolver ambigüedad, relacionar contexto o contrastar un objetivo. Si está claro, avanzar puede ser la mejor variación. No concatenes validación, paráfrasis y otra pregunta que vuelve a confirmar lo mismo. No añadas «verdad?» o «no?» a una cita que no los llevaba.

Las dudas directas pueden interrumpir cualquier etapa. Se atienden con el bloque pertinente y luego se retoma lo pendiente sin perder una aceptación ya concedida. Las quejas y las preguntas de identidad no son saludos.

## Modificar y reconciliar

Para cambios pequeños, localiza todas las apariciones relevantes de la regla: continuidad, etapa, objeción, checklist, prioridades, instrucciones de enlaces y criterio de agenda. Cambia solo las contradicciones afectadas. No basta con añadir una prohibición al final si otro bloque aún invita a saltar el permiso.

Para una reorganización amplia, deriva el prompt del manual acordado. Comprueba remisiones antiguas como «los casos están en el prompt» cuando ya se movieron al negocio, diferencias de duración o precio y atajos que confunden interés general con aceptación.

Si debe conservarse una estructura antigua, un apartado llamado «EJEMPLOS» puede remitir a bloques del manual; no es necesario rellenarlo con un segundo diálogo. Si no hay esa restricción, elimina apartados redundantes.
