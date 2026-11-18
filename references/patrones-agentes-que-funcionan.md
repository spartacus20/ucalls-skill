# Patrones de agentes que funcionan en producción

Esto sale de auditar cinco prompts activos en tres cuentas (nov-2026): una venta high-ticket de formación en YouTube con un agente de IG inbound y uno de WhatsApp outbound post-evento, y dos formaciones de Vinted, la segunda clonada de la primera, con IG inbound y un WhatsApp de confirmación de evento. Son **patrones probados en un vertical**: venta de formación con sesión o llamada y lanzamientos. Antes de copiarlos a otro sector, pasa por el filtro de [contrato-dos-documentos.md](contrato-dos-documentos.md).

## Arquitectura que se repite en los tres

Este orden de bloques es el mismo en todos los agentes de IG que funcionan:

1. **Regla de entrada.** Sin presentación: se entra con la pregunta de situación, y las palabras clave tienen su excepción definida.
2. **Voz cuantificada.** Palabras por burbuja, burbujas por turno con sus excepciones, una sola pregunta y al final, reacción de ≤6 palabras con un detalle del lead, recursos expresivos "1 de cada 3", lista negra de muletillas y banco de reacciones ("nunca la misma dos veces"). Las reglas con número se cumplen; las de "sé natural", no.
3. **Recursos**: una tabla de medio, cuándo usarlo y su frase de entrada. Ver [enlaces-y-medios.md](enlaces-y-medios.md).
4. **Clasificación en dos ejes**, de dónde parte el lead × temperatura, con rutas.
5. **Conversión y post-agenda.**
6. **Guardarraíles**: no inventar, anti-eco, menores, derivación a humano, conocidos o alumnos.
7. **Checklist previo al envío** (9–10 preguntas).
8. **Ejemplos con su porqué entre corchetes**, marcados como "no para copiar".
9. **Objeciones**, pares BIEN/MAL por cada fallo típico y **prioridades finales** ordenadas.

Los ejemplos ocupan entre el 20 y el 25 % del prompt. La regla crítica aparece tres veces: en su sección, en el checklist y en las prioridades. Esa repetición es intencionada; lo que sobra es duplicar **hechos**.

### Lo que se torció y conviene evitar

- **Prompts de 45–62k que crecen con cada parche.** Una cuenta pasó de 37k a 80k y volvió a 57k en nueve semanas, con 25 versiones. Los borradores de recorte a unos 22k nunca se activaron. Cada parche que añadas tiene que sustituir texto, no acumularse.
- **Hechos en el prompt y el manual remitiendo al prompt.** Casos con cifras, fechas y URLs acabaron en el prompt, y el manual decía "si choca, manda el prompt". El resultado fueron contradicciones reales: el manual manda preguntar el país e IG lo prohíbe; WA usa la escala 1-10 e IG la prohíbe; la regla de "¿eres IA?" cambia según el documento. **Cada hecho vive en un solo sitio**, y cada cambio de regla pasa por desduplicar prompt, manual y `usage_instructions`.
- Cambiar un dato en la línea de hechos y dejarlo viejo en los ejemplos. El modelo copia los ejemplos.

## Clasificar y avanzar

- **Dos ejes con señales dichas por el lead.** Perfil (de cero / con algo en marcha / avanzado, con umbrales del negocio) × temperatura (caliente / templado / nutrir). Si hay duda, se elige la temperatura más baja: *es peor quemar a un lead que tardar un mensaje más.*
- **Clasificar en los 2 primeros turnos.** Cada ruta tiene un **tope de preguntas** que cuenta toda la conversación, también las del equipo humano: máximo 2 en caliente. Hay un **plazo máximo para proponer**: como muy tarde en el 5.º o 6.º mensaje del agente.
- **Avanzar por señales, no por número de mensajes.** El plazo es un techo, no un objetivo.
- **Pregunta de permiso** antes de proponer al lead tibio.
- **No preguntar en el chat lo que ya pregunta el formulario** de reserva o de opt-in.

## Definir el "sí"

- Dos listas literales: **es un sí claro** ("sí", "vale", "dale", "me interesa", el sí a una pregunta en negativo) y **no es un sí** ("puede", "ya veré", "¿cuánto cuesta?"). Cada tipo de "no-sí" tiene una sola salida, con una pregunta.
- **Con un sí claro, el enlace sale en el mismo turno**, sin preguntas ni reconfirmación. Pedir que reconfirmen un sí estaba entre los fallos repetidos.
- Ojo con el sí flojo. Una cuenta quitó primero la fricción (v6) y después tuvo que frenar los síes débiles (v6.3, "enlace solo con sí claro y señales"). El punto bueno está en exigir señales de encaje, no un sí rotundo.

## Precio y objeciones

- **Escalera de precio**: primero sin cifra (audio o valor), después el mínimo una sola vez con fraccionado y garantía, y por último el compromiso condicionado ("si te encaja al 100 %, ¿tendrías el compromiso?"). Con una lista negra de cifras y palabras. Un turno de precio sin siguiente paso fue un fallo repetido.
- **"No tengo dinero" se rebate una vez antes de pasar a nutrir**, y se contesta a la objeción, no a la historia personal.
- **Escalera de objeción**: ¿es el momento o no lo ves claro? → una sola **pregunta de consecuencia** → oferta de segundo nivel (evento, masterclass, nutrir) con fecha de caducidad escrita. Nunca como premio de consolación.
- **Salida a nutrición sin rechazo**: frase de cariño, un consejo, un recurso gratuito y la puerta abierta.

## Después del enlace y post-agenda

- Después del enlace: una frase de acción y no reenviarlo. Si el lead manda una captura o un 404, preguntar "¿te llegó el correo?"; un 404 de Calendly tras reservar no es un error.
- **El post-agenda es un estado terminal.** Se confirma el compromiso una vez ("¿al 100 %?"), se invita a quien decide (pareja o socio), se prepara el freno típico y después solo logística. La venta acaba en la reserva: no se sigue vendiendo.

## Palabras clave y entradas automatizadas

Funcionan en tres capas que hay que coordinar:

1. **Reglas de historia o comentario** que responden solas (reacción → enlace solo → pregunta), con `[NO_ENVIAR]` cuando la regla ya basta.
2. **Palabras que reconoce el agente**: YO/EMPEZAR → caliente; una palabra de la bio → turno fijo de 3 burbujas. **La palabra nunca es el nombre ni la edad del lead**, y hubo incidentes con las dos cosas.
3. **No duplicar** lo que ya mandó la respuesta automática.

Cuando la IA entra a mitad de un flujo (después de una plantilla o una llamada), el prompt reconstruye qué se envió y en qué respuesta entra, y cita el texto de la plantilla y sus botones **reales**. En una cuenta, el prompt describía botones "SI/NO" que no coincidían con la plantilla.

## Agente de WhatsApp con un solo objetivo

Este patrón sirve para confirmar un evento o meter al lead en la comunidad después de una llamada:

- flujo lineal que cita la plantilla de entrada;
- cero preguntas tras confirmar;
- **un único intento ante un NO**, con 3–4 ramas de diagnóstico;
- `STOP` con un texto fijo;
- lista explícita de "lo que NO sabes";
- la promesa se atribuye a quien la hizo.

En WhatsApp outbound (post-evento) se puede insistir más que en IG inbound: "no te rindas", un micro-compromiso ("¿mañana o pasado?") antes del enlace y un solo enlace por conversación.

## Identidad y salidas

- **La política sobre la identidad IA se decide por canal y se escribe literal.** No la decide la skill: es una decisión de marca del cliente. Lo observado: en IG, la persona de la fundadora o el fundador; en WA, "X del equipo", que admite ser IA. La skill **no** genera frases que nieguen ser IA ni que afirmen ser una persona concreta ("tranqui, soy Jose"). Si el cliente las exige, márcalo como riesgo y pide su decisión expresa.
- **Frase centinela de derivación.** Un texto exacto que el equipo filtra cada día ("le paso tu caso al equipo"), sin plazos y sin seguir vendiendo. Úsala cuando el motor no puede pasar la conversación a un humano.
- **Menores**: dos confirmaciones y un adulto presente. El descubrimiento continúa; solo se bloquean la sesión y el enlace, y el estado se mantiene en toda la conversación.
- Amigos, alumnos o conocidos: silencio o una respuesta neutra. Filtro geográfico si la oferta no sirve fuera de cierto país. Marcadores de dialecto: no copiar expresiones de otro país.

## Clonar un agente que funciona a otro negocio del mismo vertical

Una de las cuentas se creó como "la base v9.6 de la cuenta A adaptada a B". Toda la lógica comercial es compartida; lo que cambia al clonar es esta lista:

- nombre, rol y frase de identidad;
- **género gramatical en todo el texto**;
- arquetipo de voz y saludo ("holaa" → "buenass"), apelativos y banco de reacciones;
- la historia, en primera o tercera persona, y quién imparte la masterclass o tiene el canal;
- quién está y quién no en la sesión;
- URLs, UTM por cuenta y **slugs del catálogo de la cuenta destino**: el clon heredó un slug que en destino no existía;
- audios regrabados y sus frases de entrada;
- el manual reescrito alrededor de quien habla, con sus casos y cifras.

**Riesgo de deriva.** Las dos copias se mantuvieron a mano y en paralelo. Versiones con el mismo nombre acabaron con unas 10 reglas y 2 ejemplos de diferencia. Si vas a mantener clones, separa una **base común** (la lógica) de una **capa de persona** (lo de la lista anterior), y al corregir algo en la base, aplícalo y pruébalo en todos los clones.

## Versionado

- El nombre de la versión es su changelog: `vN.M-cambio-corto (sobre vN.K) dd-mmm`. Los borradores llevan "(NO ACTIVAR)".
- **Nunca actives una versión que se llame "BORRADOR"**: una cuenta tenía activa la "v27 BORRADOR". Tampoco repitas nombres.
- Cada regla que nace de un fallo se escribe con el caso concreto como par BIEN/MAL. Las reglas que más se repiten en las tres cuentas son: nombres inventados a partir del @usuario, palabra clave tomada como nombre o edad, preguntar la cifra más de dos veces, audio repetido, reconfirmar un sí, precio sin siguiente paso, dobles envíos entre la regla automática y el agente, enlaces reenviados en ráfaga, decir que no tiene el enlace o que imparte él la clase, y muletillas de robot.
