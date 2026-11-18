# Prompts de referencia (producción, nov-2026)

Prompts activos de tres cuentas, volcados el 18-nov-2026, con su Información del negocio y su catálogo de enlaces y medios. Las URLs aparecen como `[URL:dominio]`. Los patrones que contienen están destilados en [../patrones-agentes-que-funcionan.md](../patrones-agentes-que-funcionan.md); lee primero ese archivo y abre estos solo para ver **cómo se redactó** algo concreto.

## Cómo usarlos

- **Sirven para estructura, criterio y técnica**: orden de bloques, cómo se cuantifica la voz, rutas perfil × temperatura, listas de "sí", checklist, pares BIEN/MAL, plantilla de `usage_instructions` y agente de un solo objetivo.
- **No sirven como fuente de hechos ni de frases** para otro negocio. Persona, historia, precios, casos, palabras clave, fechas y dialecto son de cada cliente. Las frases del nuevo agente salen de su responsable ([conversaciones-y-frases.md](../conversaciones-y-frases.md)).
- **No los tomes como modelo de longitud.** Tienen entre 45 y 62k caracteres por acumulación de parches, y sus recortes nunca se activaron. Apunta a menos y no dupliques hechos.
- No copies sus defectos (lista de abajo). Cuando uses uno como base, pasa `scripts/auditar_recursos.py` contra el catálogo de la cuenta **destino**.

## Archivos

| Caso | Archivos | Qué mirar |
|---|---|---|
| **lanzamiento-youtube**: formación high-ticket; IG inbound + WA outbound post-evento | `lanzamiento-youtube-prompt-ig.md` (45k), `-prompt-wa.md` (32k), `-negocio.md`, `-catalogo.md` | Clasificación en dos ejes con desempate conservador; listas literales de "sí claro / no es un sí"; escalera de precio; "no tengo dinero" se rebate una vez; post-enlace y post-agenda; WA con micro-compromiso e insistencia; nombres de versión como changelog |
| **vinted-a**: formación Vinted; IG inbound por palabras clave + WA de confirmación de comunidad | `vinted-a-prompt-ig.md` (58k), `-prompt-wa.md` (16k), `-negocio.md`, `-catalogo.md` | Regla de entrada; voz cuantificada; tabla de audios con frase de entrada; palabra de la bio → turno fijo; escalera de objeción → masterclass con caducidad; **agente WA de un solo objetivo** (un intento ante un NO, STOP, "lo que NO sabes") |
| **vinted-b-clon**: el mismo vertical, clonado de vinted-a v9.6 | `vinted-b-clon-prompt-ig.md` (62k), `-negocio.md`, `-catalogo.md` | Compáralo con vinted-a para ver **qué cambia al clonar** (persona, género, saludo, apelativos, historia, quién da la clase, UTM y slugs) y cómo derivan dos copias mantenidas a mano |

## Defectos conocidos (no replicar)

**lanzamiento-youtube**
- URLs literales en el prompt: Calendly en WA; recurso de regalo, grupo y canal en IG. Además, `[ENLACE OFICIAL DE AGENDA]` en lugar de un marcador.
- La `usage_instruction` del Calendly de IG pide "sí a invertir", condición que la v6.3 quitó.
- El enlace del directo del 10-nov sigue activo después del evento.
- Contradicciones con el manual: preguntar el país, la escala 1-10, la lista de palabras clave.
- La versión activa de WA se llama "BORRADOR".
- La frase de negar ser IA en IG es decisión de marca del cliente. No la generes por defecto.

**vinted-a**
- 13 URLs literales: masterclass, vídeos de testimonios, YouTube, web.
- Los ejemplos de WA llevaban el enlace antiguo de la comunidad y llegó a enviarse.
- Los botones descritos en WA ("SI/NO") no son los de la plantilla real.
- Audios y enlace de la comunidad con `agent_ids` vacío: cada agente ve los recursos del otro.
- Regla "¿eres IA?" contradictoria entre el prompt y el manual.
- El manual activo tiene un `[PENDIENTE: …]`, y hay una regla de comentario activa con `[⚠️ FALTA ENLACE]`.

**vinted-b-clon**
- **`{{link:agenda-admision}}` no existe en su catálogo; el slug real es `calendly_agenda`.** El motor borra el marcador. Es el error típico al clonar.
- La masterclass está en el catálogo, pero el prompt la escribe en crudo 6 veces.
- Los audios se nombran de forma descriptiva y no casan con los slugs del catálogo.
- Las frases de entrada de dos audios no coinciden con su `usage_instructions`.
- "tranqui soy Jose" afirma ser una persona: es un riesgo y no va en ninguna plantilla.
- El manual tiene un `[PENDIENTE: …]`.

Estos defectos eran ciertos el 18-nov-2026. Si vas a trabajar sobre una de estas cuentas, lee lo vigente en la plataforma antes de dar uno por abierto o por corregido.
