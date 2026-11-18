# Sugerir estrategia: embudo, agentes y workflows

Léelo cuando el usuario pida estrategia ("¿qué montamos para el lanzamiento?", "¿cómo recupero a los que no contestan?", "¿qué flujo pongo después de la llamada?"), o cuando al construir un agente veas que el cuello de botella está fuera del prompt.

Las cifras salen de 10 workflows en producción de tres cuentas (lanzamientos de formación, nov-2026), medidos en la base de datos. Úsalas como **referencia de orden de magnitud**, no como promesa. Al citarlas, di de dónde salen.

## 1. Diagnosticar antes de sugerir

Una sugerencia sin diagnóstico es una opinión. Antes de proponer nada:

1. **Dibuja el embudo real de la cuenta**, de la entrada a la conversión: opt-in o mensaje → contacto (llamada o chat) → respuesta → recurso o enlace → reserva → asistencia → venta.
2. **Pon un número en cada salto, o marca el salto como "no medido".** Con el MCP: `get_api_calls_campaign_stats`, `get_api_agents_performance`, `get_api_workflows_by_id_batches` y `get_api_dashboard_metrics`. Si no hay dato, el primer paso de la estrategia es medir ese salto.
3. **Localiza el cuello**, es decir, el salto con más pérdida o el que no se ve. En las tres cuentas estaba en dos sitios:
   - **Enlace → reserva**: la IA mandó la agenda en unas 185 conversaciones y solo ~21 % dijo después que había reservado. No había clicks medidos.
   - **Llamada no contestada**: el 64–66 % de los opt-ins se quedó sin contactar y no había reintento.
4. Propón **un cambio por cuello**, con su métrica de éxito y la fecha en que se revisa. No reescribas el prompt si el problema es un flujo, y al revés.

Recuerda la regla de dispersión: una prueba nueva lleva su tesis y su criterio de éxito escritos, y es pequeña.

## 2. Recetas que han funcionado

### R1 · Opt-in → llamada inmediata (speed-to-lead)
- **Disparador:** webhook del formulario o CRM con nombre, email, teléfono y etiqueta de origen.
- **Secuencia:** condición por origen → espera de 2–5 min → llamada en franja horaria (09/10–20/21 h, zona del lead) → **reintento a las 3–4 h → otro al día siguiente en la franja contraria → R5**.
- **Observado:** 34–36 % contestadas al primer intento, duración mediana de 75–78 s y entre un 41 y un 54 % de las contestadas con confirmación o éxito. El 18–27 % entra fuera de horario y espera a que abra la franja.
- **Fallos vistos:**
  - El filtro por etiqueta con texto exacto dejó **sin llamar al orgánico** en las dos cuentas (86 y 162 leads), por una errata ("OGÁNICO") y por nombres distintos. Valida el filtro contra el último payload real o usa "contiene".
  - Ninguna de las dos cuentas tenía reintento.

### R2 · Post-llamada → plantilla de WhatsApp con un CTA de un toque (la mejor)
- **Disparador:** webhook post-llamada, **filtrado por la variable que extrae el agente de voz** (p. ej. `pide_enlace=si`) o por campaña.
- **Secuencia:** plantilla con `{{1}}` = nombre y 2 botones (sí / no). El "sí" lo atiende el agente IA con el enlace del catálogo, o una rama `btn:0` que lo manda como mensaje de sesión.
- **Observado:**
  - 81 % de respuesta y 76 % de clic en el sí cuando se filtra por `pide_enlace`.
  - 58 % y 52 % en "día del directo", sin filtrar.
  - 59 % en reactivación.

  Confirmar una intención ya expresada convierte casi el doble que preguntar en frío.
- **Fallos vistos:**
  - `{{1}}` sin fallback (14 fallos): pon uno.
  - 49 contactos recibieron la plantilla dos veces, una tras la llamada de mañana y otra tras la de tarde. Usa una etiqueta "enviado" como filtro.
  - Créditos de plantilla agotados.
- **Implicación para el prompt:** el agente de WhatsApp tiene que conocer el texto y los botones exactos de la plantilla, y responder al texto del botón.

### R3 · Replay o envío masivo con A/B y cadena de sesión
- **Disparador:** etiqueta de segmento lanzada como lote **por goteo**. 50 cada 2 min funcionó sin incidencias.
- **Secuencia:**
  1. Etiqueta "enviado".
  2. Reparto entre 2–4 plantillas con botones "Pásamelo / Ya la vi / No más avisos".
  3. **"Pásamelo"**: espera de ~10–15 s y 3–4 mensajes de sesión cortos con pausas de 5 s: el enlace más **una pregunta de cualificación** que abre la conversación al agente.
  4. **"Ya la vi"**: la misma pregunta de cualificación.
  5. **"No más avisos"**: disculpa y etiqueta de baja, que se excluye de todos los flujos.
- **Observado:** 21–27 % "pásamelo", 29 % de respuesta en 48 h y un 2,6 % de bajas. Las 4 variantes rindieron igual: con unos 370 envíos por variante no se detectan diferencias de 2 pp. Para que un A/B tenga sentido hacen falta diferencias grandes o miles de envíos por variante.
- **Fallos vistos:**
  - **El primer día se perdió el 87 % del envío (1.592 errores 402) por falta de créditos de plantilla.**
  - Una variante se publicó sin la rama de baja.
  - 1.243 inscripciones se quedaron esperando el clic para siempre.
  - El enlace iba pegado como texto, así que no había clicks medibles.

### R4 · Follow-up dentro de 24 h: "¿pudiste agendar?"
- **Disparador:** etiqueta, por lote o automática, para quien recibió el enlace de agenda y no consta que haya reservado.
- **Secuencia:** 2–4 textos de sesión cortos y coloquiales ("buenas, ¿pudiste agendar? así aviso al team"). Después, sigue el agente IA.
- **Observado:** 38 % de respuesta (n = 21). Es barato, porque va en la ventana de 24 h y sin plantilla.
- **Fallos vistos:** no se puede medir si reservaron hasta que no se conecta el webhook de Calendly o GHL.

### R5 · Reenganche fuera de 24 h
- **Disparador:** etiqueta que pone R1 automáticamente tras el último reintento sin respuesta, o un lote de conversaciones caducadas.
- **Secuencia:** 2 plantillas cortas y abiertas ("¿estás por ahí?" / "¿te quedó alguna duda?") → si no responde en 24–48 h, cierre con etiqueta.
- **Observado:** sin evidencia. Solo se alimentó con 4 leads frente a unos 1.500 no contactados. Es la receta más infrautilizada: **conéctala a R1 antes de recomendar nada más.**

### R6 · Citas externas → registro y atribución
- **Disparador:** webhook de Airtable o Calendly al crearse la cita. El filtro `utm_source` (cuenta) + `utm_medium` (p. ej. `ig_ia_interna`) atribuye la cita a la IA.
- **Secuencia:** `book_appointment` con la fecha variable, o un webhook al flujo de la subcuenta.
- **Observado:** 0 de 6 elegibles se procesaron:
  - **Las rutas `{{trigger.body.fields.Fecha de Agenda}}` no admiten espacios** (solo `[a-zA-Z0-9_.]`), así que la fecha y los campos llegaron vacíos.
  - El flujo de destino estaba en borrador.
- La UTM fija en la agenda fue **la única medición real de conversión de la IA** en una de las cuentas. Recomiéndala siempre, pero prueba el flujo con un payload real (`post_api_workflows_by_id_test`).

### R7 · Higiene de pruebas
- Todo flujo de prueba lleva "PRUEBA" en el nombre y una allowlist de teléfonos, y se pausa al terminar.
- El canal del disparador tiene que coincidir con el de la acción. Un flujo de prueba que entraba por IG y mandaba un WhatsApp, y que quedó activo, generó 3.882 inscripciones inútiles.

## 3. Secuencia típica de un lanzamiento

Combinación observada en las cuentas que mejor funcionaron:

```
Anuncio / orgánico → opt-in (formulario o Airtable)
  → R1 llamada en 3 min (+ reintentos) ──no contesta──→ R5
  → la llamada extrae variables (asistencia, interés, pide_enlace)
  → R2 plantilla de confirmación / grupo, solo a quien pidió el enlace
  → recordatorios el día del evento (llamada mañana/tarde + R2)
  → R3 replay a no asistentes 24–48 h después
  → el agente de chat cualifica y manda la agenda → R4 a las 24 h
  → R6 registra y atribuye la cita
```

El agente de chat de IG va en paralelo para el tráfico inbound (palabras clave, historias, bio). Su prompt tiene que saber qué le llega ya desde los flujos.

## 4. Comprobaciones antes de proponer publicar un workflow

1. Cada botón de cada plantilla tiene una salida conectada, o el agente IA está preparado para su texto exacto.
2. Toda variable `{{n}}` tiene fallback.
3. Hay **créditos de plantilla** suficientes para el tamaño del lote, y el lote va por goteo.
4. Los filtros por etiqueta o campo están comprobados contra los valores reales: la lista de etiquetas (`get_api_pipeline_tags`) o el último payload del webhook.
5. Ninguna ruta `{{…}}` tiene espacios.
6. Ninguna espera de clic es indefinida: espera + condición de respuesta + salida.
7. Las llamadas tienen reintento y salida hacia el reenganche.
8. Los enlaces son `agent_links` con seguimiento de clicks, no texto pegado.
9. Hay una etiqueta "enviado" contra duplicados y una de baja excluida en todos los flujos.
10. La simulación (`post_api_workflows_by_id_test`) se ha hecho con un payload real.

Desde el MCP, los flujos quedan en borrador: publicar o activar lo hace una persona en el panel. Entrega la propuesta con los warnings y el resultado de la simulación.

## 5. Cómo entregar una sugerencia de estrategia

Formato corto y accionable:

| Cuello detectado | Dato (o "no medido") | Cambio propuesto | Receta | Métrica de éxito | Revisión |
|---|---|---|---|---|---|

Después, como mucho 3 acciones ordenadas por impacto en caja y facilidad, separando lo que va al **prompt o manual** de lo que va a **workflows**, **catálogo** o **plataforma**. No propongas bajar el objetivo del cliente. Si algo no funciona, propón cambiar el método.
