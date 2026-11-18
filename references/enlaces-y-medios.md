# Enlaces y medios en uCalls

Esto sale de auditar tres cuentas en producción (nov-2026): un lanzamiento de YouTube con agentes de IG y WhatsApp, y dos formaciones de Vinted, la segunda clonada de la primera. Léelo siempre que el agente mande enlaces, audios, vídeos o imágenes.

## Cómo los trata el motor (comprobado en el código)

- `{{link:slug}}` se sustituye por la URL del catálogo (`agent_links`). Si el enlace tiene `shorten`, la URL se acorta y se registran los clicks por conversación. Con `auto_tracking` o `tracking_params` se añaden UTM.
- `{{media:slug}}` saca el recurso del texto y lo envía como adjunto aparte (`agent_media`: audio, nota de voz, vídeo, imagen o documento).
- Los slugs tienen que cumplir `^[a-z0-9_-]{1,48}$`. **Si un slug no existe o está inactivo, el marcador se borra sin avisar.** El lead recibe "te paso el enlace" y ningún enlace. Una cuenta llevaba desde la v2 usando `{{link:agenda-admision}}` cuando el slug real era `calendly_agenda`. Seguía funcionando a veces solo porque el modelo copiaba la URL que veía en el catálogo.
- **El modelo no ve en el historial los adjuntos que envió.** Ve su propio texto, pero no el audio. Sin una huella escrita, repite audios.
- El motor puede reescribir el estilo después del modelo (minúsculas, puntos, `¿` de apertura, burbujas). En una cuenta corrigió miles de turnos. Si una regla de estilo "no se cumple", mira antes el saneado que el prompt.

## Reglas para construir

1. **Todo recurso va por el catálogo y nunca como URL literal en el prompt ni en el manual.** En las tres cuentas había entre 6 y 13 URLs escritas a mano (testimonios, YouTube, la web, la masterclass, el grupo de WhatsApp). Problemas: no se miden, no caducan y, cuando un dato cambia, se quedan viejas en los ejemplos. Una de las cuentas siguió mandando el enlace antiguo de la comunidad porque solo se actualizó la línea de hechos y el modelo copió el ejemplo.
2. **Comprueba cada slug contra el catálogo real** (`scripts/auditar_recursos.py`) antes de subir un borrador. Si el slug no existe, la rama queda bloqueada, no "probablemente funciona".
3. **Enlace de conversión medible.** El enlace de agenda o de compra lleva `shorten` y `auto_tracking`, o una UTM fija que lea la herramienta de destino (Calendly → Airtable). En una de las cuentas, la IA mandó la agenda en unas 185 conversaciones y solo constaba 1 click, porque nada estaba acortado. Sin medir, el cuello entre el enlace y la reserva es invisible.
4. **Limita cada recurso a sus agentes** (`agent_ids`). Con `agent_ids` vacío, el recurso está disponible para todos. En una cuenta, el agente de confirmación de WhatsApp "veía" los audios de la fundadora y el agente de IG veía el enlace de la comunidad de WhatsApp.
5. **Los recursos con fecha caducan.** El enlace de un directo y la masterclass del día X se desactivan después del evento, y el prompt lleva la fecha escrita ("hasta el 23-nov; después, ruta sin evento"). Una cuenta tenía activo el enlace de un directo ya pasado.
6. **Una sola fuente por texto.** El texto de respaldo de un audio está en el prompt o en su `usage_instructions`, nunca en los dos. En dos cuentas, la frase del prompt y la de `usage_instructions` no coincidían o incluso se contradecían.
7. Nada de marcadores pendientes en producción. Reglas automáticas activas con `[⚠️ FALTA ENLACE]` o `[PENDIENTE: …]` se envían tal cual al lead.

## Patrón "frase de entrada" para audios y vídeos

Es el mejor patrón de las tres cuentas. Úsalo con cualquier medio que no deba repetirse.

- Cada medio va detrás de una **frase de entrada literal y fija** ("te dejo un audio que te lo explico mejor").
- Esa frase queda en el historial y hace de memoria: *si la frase ya está en tus mensajes, ese audio ya se envió; usa el texto de respaldo.*
- Un medio se envía una sola vez por conversación, nunca en el primer mensaje, y el turno no termina en el audio: después va una pregunta o el siguiente paso.
- Si el lead dice que no puede escuchar audios, no se mandan más y se usa el respaldo.
- La frase de entrada tiene que ser idéntica en el prompt y en `usage_instructions`.

Uso observado: los audios de **precio** y de **qué hacemos/formulario** son los que se usan (entre 13 y 33 envíos por cuenta). Los de miedo, "ya lo intenté" o pareja quedaron casi sin uso (0–7). Si un audio no tiene disparador claro en el recorrido, sobra.

## Plantilla de `usage_instructions`

`usage_instructions` dice **cuándo** se usa el recurso. No repite el recorrido comercial.

```text
Cuándo: [disparador observable, p. ej. "el lead pregunta el precio por primera vez"].
Requisito previo: [aceptación o estado, p. ej. "ya dijo sí a la sesión"; el mismo criterio que el prompt].
Antes: escribe exactamente «[frase de entrada]».
Solo la primera vez. Si esa frase ya está en tus mensajes, no lo envíes: usa «[respaldo en texto]».
Nunca: [exclusión, p. ej. "en el primer mensaje" / "si el lead es menor" / "como premio de consolación"].
Caduca: [fecha o evento], si aplica.
```

Alinea el requisito previo con la versión vigente del prompt. En una cuenta, la `usage_instruction` de la agenda seguía exigiendo "dijo que sí a invertir", cuando la v6.3 había quitado esa condición. El modelo recibía dos permisos distintos.

## Recursos que ya mandó la automatización

Cuando la conversación viene de una regla de historia o comentario, o de un workflow que ya mandó el regalo o el enlace:

- El prompt describe qué se envió y en qué respuesta entra la IA.
- La IA no reenvía el recurso, no confirma la palabra clave y no pone el recurso como condición para responder preguntas.
- Si el lead dice que no le llegó, la IA lo manda una sola vez por el catálogo.

Plantilla de regla de historia o comentario: `PALABRA / PROMESA / RECURSO (link|adjunto|ninguno) / ÁNGULO`, con "no sabes quién es" y una pregunta final, o bien `[NO_ENVIAR]` si la regla ya responde por sí misma.

## Auditoría rápida de una cuenta existente

El MCP de uCalls no expone el catálogo de enlaces y medios. Pide al usuario una exportación (slug, nombre, destino o tipo, `usage_instructions`, activo, `agent_ids`, `shorten`/`auto_tracking`) o que lo copie del panel. Si no la hay, revisa al menos los slugs que usa el prompt y márcalos como «sin contrastar con el catálogo».

1. Slugs del prompt y del manual contra el catálogo activo, incluidos los slugs que no existen.
2. URLs literales en prompt, manual y ejemplos.
3. Recursos activos con `agent_ids` vacío o asignados al agente equivocado.
4. Recursos con fecha ya pasada.
5. Enlace de conversión sin `shorten`, `auto_tracking` ni UTM.
6. Frase de entrada distinta entre el prompt y `usage_instructions`.
7. Marcadores `PENDIENTE` o `FALTA` en reglas o manuales activos.

`scripts/auditar_recursos.py` cubre los puntos 1, 2, 3, 5 y 7. Los puntos 4 y 6 hay que revisarlos leyendo.
