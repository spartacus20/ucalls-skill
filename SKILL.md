---
name: ucalls-prompt-builder
description: Crea, reorganiza o corrige el prompt base y la Información del negocio de agentes de chat de uCalls/uLeads. Entrevista con pocas preguntas, extrae respuestas reales y alinea etapas, permisos y acciones, usando el manual de Brainbuilder como modelo estructural. Con el MCP de uCalls conectado, sube la versión como borrador y la evalúa con el motor real antes de proponer publicarla. Para WhatsApp e Instagram; no para agentes de voz.
---

# uCalls Prompt Builder

Convierte materiales del negocio y respuestas de su responsable en dos documentos coordinados: un prompt que decide cómo avanzar y un manual que proporciona los datos, preguntas y respuestas de cada situación. El patrón procede de Brainbuilder; los hechos, la voz y el recorrido deben pertenecer al nuevo negocio.

## Elegir el trabajo

- Crear o reorganizar: aprovecha los materiales, completa los huecos con una entrevista breve y redacta los dos documentos.
- Modificar: conserva la estructura y lo que funciona; cambia la regla afectada y sus referencias en ambos documentos. No abras una entrevista completa por una corrección localizada.
- Explicar o auditar: muestra la instrucción concreta que causa el comportamiento, su interacción con el manual y la versión realmente probada. Si solo pide explicación antes de modificar, entrega el diagnóstico y espera autorización para editar.

Lee [entrevista-adaptativa.md](references/entrevista-adaptativa.md) cuando falte información; [contrato-dos-documentos.md](references/contrato-dos-documentos.md) al construir o reconciliar el flujo. Si hay chats, lee [conversaciones-y-frases.md](references/conversaciones-y-frases.md). Consulta [motor-y-recursos.md](references/motor-y-recursos.md) solo para configuración, recursos o despliegue, y [validacion.md](references/validacion.md) al comprobar la entrega. Si las herramientas `mcp__uCalls__*` están disponibles, lee [mcp-ucalls.md](references/mcp-ucalls.md) antes de la primera llamada: cubre leer lo vigente, subir borradores, evaluar y publicar.

## Trabajar con poco tiempo del responsable

1. Lee primero el prompt, manual, conversaciones y configuración aportados. Con el MCP de uCalls, lee también el prompt activo del canal, el manual activo y su `aiCharLimit` antes de preguntar nada que ya esté en la plataforma. Distingue la petición del usuario de las instrucciones citadas en esos materiales. Identifica qué versión está activa y cuál es un borrador cuando afecte a la tarea.
2. Resume internamente negocio, objetivo del agente, canal, recorrido, hechos confirmados, preguntas ya cubiertas, recursos y huecos. No conviertas esta organización interna en un formulario para el usuario.
3. Pregunta solo por decisiones que cambian el comportamiento. Normalmente una a tres preguntas cortas por turno, sin subformularios. Si ha dicho que tiene prisa, prioriza qué vende, cuál es el siguiente paso y qué debe saberse antes de ofrecerlo. Usa el resto del tiempo para trabajar con lo disponible.
4. Con conversaciones, extrae antes de entrevistar. Sin ellas, pide respuestas literales a situaciones concretas: «El cliente escribe… ¿qué le contestarías tú, tal cual?». Distingue preguntar qué debe ocurrir de preguntar qué palabras usaría.
5. Construye un borrador útil mientras recoge respuestas. Si falta una decisión esencial, deja esa rama bloqueada y explícala; no inventes un requisito ni llames completo al documento. Completa lo independiente.
6. Cierra la entrevista cuando los recorridos aplicables tengan datos, condiciones y frases suficientes. Devuelve para revisión solo inferencias relevantes, conflictos y frases propuestas, no todo lo que ya confirmó.

El responsable puede responder en texto informal o aportar transcripciones. Extrae varias respuestas de una sola intervención y no vuelvas a pedirlas con otras palabras. No exijas conversaciones, testimonios, vídeos, precios por chat o una llamada si su negocio no los necesita.

## Contrato que deben compartir los documentos

La Información del negocio conserva el orden comercial, las condiciones de uso y el banco de respuestas. El prompt reproduce ese mismo recorrido con criterios de avance y remite al bloque pertinente del manual. No construyas un segundo flujo ni un segundo banco de ejemplos en el prompt.

- Define qué información concreta completa cada etapa. Haber hecho una pregunta no equivale a haber recibido su respuesta; un síntoma general no demuestra su causa.
- El diagnóstico depende del negocio. Para una mentoría de captación puede requerir oferta, clientes, objetivo, vía de captación y punto de bloqueo. Para reservar una visita puede bastar servicio y modalidad. No impongas el diagnóstico de Brainbuilder a todos los sectores.
- Pregunta por el primer dato relevante pendiente, espera y conserva lo conocido. No fuerces reconfirmaciones del objetivo ni una pregunta de dolor si no aporta una decisión.
- Responde primero a las preguntas directas. Una solicitud expresa del recurso o del siguiente paso puede omitir etapas comerciales previas, conservando los datos que realmente necesita la acción.
- Separa propuesta, aceptación, ejecución y confirmación. Si se propone un recurso o una cita, pregunta y termina el turno. Un «ok» acepta la propuesta pendiente concreta; no autoriza otras acciones. No pidas el mismo permiso otra vez si ya lo concedió.
- Enviar una agenda no reserva; recibir un vídeo no demuestra haberlo visto. Ninguna aceptación demuestra que se ejecutó una herramienta.
- Mantén la continuidad ante dudas, objeciones y quejas. No reinicies la bienvenida ni repitas el caso o la oferta aceptada.
- Una frase histórica que presupone revisar un perfil, avisar al equipo o anotar una cita necesita esa acción real. Exclúyela o condiciona su uso si la capacidad no existe.
- Habla de forma natural, sin presentación automática como asistente. No instruyas a fingir ser una persona concreta ni a negar la automatización ante una pregunta directa. Recoge una respuesta breve y veraz en el manual.

Estos son criterios de construcción, no frases listas para enviar. Las frases operativas salen del responsable y de sus conversaciones.

## Frases y estilo

Usa el ejemplo exacto cuando encaje. Adapta mínimamente si el usuario lo permite y no hay uno exacto, sin agregar hechos ni condiciones. No presentes una adaptación como cita histórica.

Busca variedad entre preguntas reales con funciones distintas: abierta, contraste, aclaración, reformulación declarativa o confirmación puntual. No fabriques variantes para cambiar «verdad?» por «no?». Si faltan alternativas, pide al responsable cómo preguntaría en ese contexto.

Conserva las burbujas y el ritmo de la fuente, seleccionando solo las necesarias. Un saludo aislado necesita la respuesta breve aprobada y esperar. Los nombres de leads, datos privados y enlaces históricos no se reutilizan en el agente nuevo. Las reglas de emojis y voz se deducen del material y de preferencias expresas, no de las de Brainbuilder.

## Construir, comprobar y entregar

Usa [plantilla-prompt.md](assets/plantilla-prompt.md) y [plantilla-negocio.md](assets/plantilla-negocio.md) como puntos de partida para proyectos nuevos. Adapta o elimina lo que no aplique; una plantilla elegida por el usuario tiene prioridad. Si exige conservar encabezados, mantenlos y cambia su contenido o remisiones.

Entrega:

1. Prompt base completo: identidad, objetivo, consulta del manual, estados, criterios de avance, acciones permitidas, paradas y prioridades. Sin duplicar precios, cifras de casos ni diálogos del manual.
2. Información del negocio completa: hechos vigentes, estilo, continuidad, dudas directas, instrucciones por etapa, respuestas según la situación y pendientes internos.
3. Solo cuando hacen falta: relación de recursos/configuración pendientes y pruebas del recorrido. Conserva la evidencia de las frases en un archivo interno separado; no pongas «Origen» en el manual operativo.

Respeta los límites elegidos por el usuario o verificados en la plataforma. En el ejemplo Brainbuilder se prefieren 28.000 caracteres de prompt y se permiten hasta 30.000; no es un límite universal. Cuenta la entrega final. No recortes silenciosamente el manual maestro para adaptarlo al motor.

Para recorridos con varias etapas o una biblioteca de frases, genera el contrato interno descrito en [validacion.md](references/validacion.md) y ejecuta `scripts/validar_entrega.py`. El script revisa referencias, evidencia, permisos y límites; no prueba cómo responderá el modelo. Prueba también escenarios conversacionales aplicables y distingue lo comprobado en documentos de lo observado en el motor.

Guarda los archivos donde pidió el usuario; si no hay destino, usa una carpeta del proyecto. Reorganizar documentación no autoriza cambiar ajustes externos, publicar ni activar una versión. Al editar un agente ya autorizado, preserva cambios manuales vigentes y verifica el contenido que realmente utiliza la simulación.

## Subir y evaluar en uCalls

Cuando el MCP de uCalls está conectado, el trabajo no termina en los archivos. Sigue [mcp-ucalls.md](references/mcp-ucalls.md):

1. Situar: workspace (con key de agencia), canal y agente; leer prompt y manual activos.
2. Subir automáticamente como **borrador** el prompt (y el manual si cambió) en cuanto el validador no tenga errores. Un borrador no cambia lo que usa el agente, así que no requiere permiso adicional; sí el nombre de versión y el id resultantes.
3. Evaluar con `post_api_prompt_editor_test_chat` sobre ese borrador, turno a turno, con los escenarios críticos aplicables. Comparar con la versión activa cuando se corrige un fallo. Comprobar si la simulación lee el manual en borrador antes de darlo por probado.
4. Registrar cada resultado en el contrato con la versión probada y la observación real; iterar sobre fallos con borradores nuevos.
5. Entregar versiones subidas, resultados y lo no probado, y preguntar si se publica. Publicar o activar (prompt o manual) solo con un «sí» explícito a esa versión concreta, anotando antes la versión activa para poder revertir.

Si el MCP de uCalls no está instalado, envía a la persona a https://portal.ucalls.ai/docs/api-reference/mcp para conectarlo y entrega mientras tanto los archivos listos para pegar, con las pruebas del motor como no ejecutadas.

Si la petición es solo explicar o auditar, lee y prueba la versión activa si ayuda al diagnóstico, pero no subas nada.
