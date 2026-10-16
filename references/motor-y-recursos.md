# Motor, recursos y versiones

## Comprobar el entorno aplicable

El ZIP original documentaba un motor que añadía al prompt información del negocio, catálogos de enlaces/medios, memoria, reglas de agenda, contexto y un contrato de salida. También describía saneado de estilo y un recorte del negocio a 20.000 caracteres. Es evidencia de ese diseño, no prueba de cómo funciona cada despliegue actual.

Cuando la tarea incluye configurar o depurar ejecución, contrasta con herramientas disponibles, configuración visible, código autorizado o pruebas del agente. Si solo se redactan documentos, conserva la incertidumbre en las notas de configuración sin bloquear todo el trabajo. No pidas credenciales innecesarias.

Comprueba únicamente lo relevante:

- Canal y versión elegida para la prueba: borrador o publicada.
- Cómo recibe el motor el prompt y el manual; límite visible frente a límite inyectado.
- Recursos: catálogo, medios, acción disponible o configuración externa que indique el usuario.
- Agenda: enlace externo frente a herramientas reales de disponibilidad y reserva.
- Reglas que alteran mensajes: minúsculas, emojis, puntuación y separación en burbujas.
- Memoria/historial disponibles y seguimientos configurados.

No publiques un cambio solo porque guardarlo cree una nueva versión. La simulación de una versión vieja no valida el borrador nuevo.

Con el MCP de uCalls, varias de estas comprobaciones se hacen leyendo la plataforma: versión activa por canal, versiones en borrador, manual en uso y `aiCharLimit` (caracteres del manual que lee la IA; el resto se corta). El procedimiento de subida, prueba y publicación está en [mcp-ucalls.md](mcp-ucalls.md).

## Enlaces y medios

En instalaciones que admiten `{{link:slug}}` y `{{media:slug}}`, conserva o crea referencias operativas con el slug real. La resolución es responsabilidad del motor; no instruyas al modelo a sustituir un marcador con una URL que no puede ver. Prueba que el mensaje visible contiene el recurso y no el código sin resolver.

Sin ese mecanismo, usa el recurso o acción que exista en el entorno. No impongas esos marcadores en n8n u otro motor. No uses variables de nombre como `{{nombre}}` sin soporte comprobado.

El catálogo debe describir cuándo usar un recurso y su contenido real. Sus instrucciones deben respetar el mismo permiso del prompt y el manual: «cuando lo acepte o solicite», no «cuando parezca interesado».

Si el usuario dice que los enlaces están configurados en otra parte, no vuelvas a exigir la URL para redactar. Registra la dependencia y continúa. Para una prueba real de envío sí hay que poder resolverla; si no, limita la prueba a oferta/aceptación y registra la entrega como no probada.

Falta de recurso: no inventar URL, anunciar envío ni repetir la propuesta. La rama puede quedar pendiente. No afirmar que se avisó al equipo si no se ejecutó esa acción.

## Agenda y acciones

| Capacidad verificada | Instrucción aplicable |
|---|---|
| Enlace externo | Enviar tras solicitud/aceptación; la reserva necesita confirmación real |
| Agenda nativa | Recoger solo los campos requeridos, consultar disponibilidad real y reservar la opción elegida |
| Webhook personalizado | Usar nombre y campos exactos verificados; confirmar por su resultado |
| Sin transferencia humana | Respetar la política de atención manual sin simular una transferencia |
| Capacidad desconocida | No nombrar una herramienta inventada; señalar la dependencia |

Aceptar una llamada no permite elegir por el cliente una hora que no ha aceptado. Pedir cita no elimina los datos obligatorios del sistema de reservas. Una consulta de disponibilidad no demuestra una reserva.

No sobrescribas el formato de salida fijado por el motor. El prompt define la conducta; el motor puede definir JSON, silencio y burbujas. La frase «mensajes breves» no exige una cuota de mensajes. No conviertas una regla histórica del motor en una prohibición universal de URLs, mayúsculas o emojis.

## Límites y manual maestro

Conserva una versión completa del manual. Si se confirma truncamiento o recuperación por fragmentos, prepara una edición de despliegue o una distribución compatible, manteniendo las puertas y bloques necesarios accesibles. No cortar al carácter N y llamar equivalente al resultado.

En uCalls, `aiCharLimit` de `get_api_business_info` es un límite comprobado: úsalo como `business_runtime_max` en el contrato. Mide longitud con la unidad del entorno: puntos de código Unicode o unidades UTF-16 —habituales en contadores JavaScript—. Un emoji puede contar distinto. Si el usuario fija un máximo, valida el archivo final tras todos los cambios.

Un límite de contexto no se arregla únicamente moviendo una regla al principio si las respuestas posteriores quedan inaccesibles. Verifica oferta, permisos, envío, objeciones y confirmación con el contenido que realmente llega al motor. Si no se puede verificar, dilo en las notas de prueba.

## Modificaciones en un proyecto existente

Lee el contenido vigente antes de escribir. Compara con la copia local y preserva cambios manuales de hechos o respuestas que no estén en la corrección pedida. Guarda una copia de trabajo cuando sea útil para revertir.

Antes de atribuir un fallo al modelo, revisa versión probada, manual inyectado, catálogo, criterio de agenda, memoria y saneado. Puede haber una regla correcta en el documento que el modelo nunca recibió.

Guarda y prueba el borrador dentro del alcance autorizado (en uCalls: `..._versions_draft` y `post_api_prompt_editor_test_chat`). Activar, publicar, cambiar integraciones o enviar mensajes reales requiere que esas acciones estén autorizadas; la skill no amplía la petición.
