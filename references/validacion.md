# Validación de la entrega

## Qué comprobar y qué no demuestra un script

Comprueba el par de documentos y sus dependencias, no solo el prompt. El script verifica medidas y referencias declaradas: etapas existentes, campos de diagnóstico, alcance del permiso, recursos y procedencia textual de frases. No entiende todo el significado de una instrucción, no autentica autores y no demuestra cómo se comportará el modelo.

La revisión humana debe contrastar que el contrato refleja los documentos, que las citas están asignadas al interlocutor correcto y que ninguna regla contradictoria sobrevive en agenda, recursos, prioridades o manual. No marques una simulación como conversación histórica ni una revisión de texto como prueba del motor.

## Contrato interno para recorridos con varias etapas

Este JSON lo prepara el agente a partir de los documentos. El responsable nunca tiene que rellenarlo. Guarda las rutas de las fuentes relativas a la evidencia o como rutas absolutas accesibles. No empaquetes evidencias privadas dentro de la skill reutilizable.

Ejemplo de estructura, con nombres y criterios que deben adaptarse:

```json
{
  "count_unit": "utf16",
  "limits": {"prompt_max": 30000, "prompt_preferred": 28000},
  "fact_ids": ["servicio", "objetivo"],
  "diagnosis": {
    "fields": ["servicio", "objetivo"],
    "before_stages": ["E3"],
    "direct_request_bypass": true
  },
  "stages": [
    {
      "id": "E2",
      "manual_heading": "ETAPA 2 · CONTEXTO Y OBJETIVO",
      "prompt_ref": "ETAPA 2",
      "required_fields": ["servicio", "objetivo"],
      "completion": "Constan servicio solicitado y objetivo, o consta que aún no lo ha definido",
      "on_complete": ["E3"],
      "phrase_ids": ["p-objetivo"]
    },
    {
      "id": "E3",
      "manual_heading": "ETAPA 3 · OFRECER EL RECURSO",
      "prompt_ref": "ETAPA 3",
      "required_fields": ["servicio", "objetivo"],
      "completion": "Solicita, acepta, duda, rechaza o aplaza el recurso ofrecido",
      "on_complete": ["E4"],
      "phrase_ids": ["p-permiso"],
      "action": {"kind": "offer", "scope": "guia", "resource_id": "guia"}
    },
    {
      "id": "E4",
      "manual_heading": "ETAPA 4 · ENVIAR EL RECURSO",
      "prompt_ref": "ETAPA 4",
      "required_fields": [],
      "completion": "El envío real se completa; después se espera su valoración",
      "on_complete": [],
      "phrase_ids": ["p-envio"],
      "action": {"kind": "deliver", "scope": "guia", "resource_id": "guia"},
      "consent": {"scope": "guia", "basis": ["requested", "accepted"], "offer_stage": "E3"},
      "on_missing_resource": "wait"
    }
  ],
  "resources": [{"id": "guia", "status": "external_config", "marker": null}],
  "tests": [{
    "id": "aceptacion-guia",
    "messages": ["me interesa", "ok"],
    "expectations": ["envía el recurso aceptado sin ofrecerlo otra vez"],
    "status": "not_run",
    "environment": "runtime"
  }]
}
```

`on_complete` expresa destinos posibles, no una orden de avanzar ante cualquier respuesta. Las ramas aceptar, duda, rechazo y aplazamiento deben estar descritas en los documentos. El script no verifica automáticamente esa semántica.

Tipos de acción: `offer`, `propose`, `deliver`, `calendar`, `book`, `purchase`, `confirm`. `deliver`, `calendar`, `book` y `purchase` requieren permiso con el mismo `scope`; una solicitud expresa cuenta. Para `confirm`, declarar `execution_evidence` con las fuentes de confirmación que el proyecto realmente admite. El script no ejecuta herramientas.

Recursos: `verified`, `external_config` o `pending`. Los dos últimos conservan incertidumbre y necesitan una salida ante falta de recurso; no fuerzan pedir la URL si el usuario ya explicó dónde está. Un recurso pendiente no queda validado por declarar un slug.

`business_runtime_max` solo se añade a `limits` cuando se haya comprobado ese límite (en uCalls, el `aiCharLimit` leído de la plataforma) o el usuario pida simularlo. No usar 20.000 como valor implícito para todos los motores.

Para conservar encabezados por petición explícita, usa `--original-prompt` con la versión original. No lo uses para impedir una reorganización autorizada.

## Evidencia de frases

```json
{
  "adaptation_allowed": false,
  "sources": [{
    "id": "s1",
    "kind": "chat",
    "speaker": "seller",
    "path": "fuentes/chat-01.md",
    "locator": "turno 6 del vendedor",
    "excerpt": "texto exacto del vendedor"
  }],
  "phrases": [{
    "id": "p-objetivo",
    "origin": "exact_chat",
    "source_id": "s1",
    "bubbles": ["texto exacto del vendedor"],
    "active": true
  }]
}
```

Tipos de fuente: `chat`, `owner`, `simulation`, `document`. `exact_chat` requiere chat y vendedor; `owner_literal` requiere fuente del responsable. Las fuentes con citas necesitan `path`, `locator` y `excerpt` verificables. Para un `approved_draft`, `approved: true` y `approval_note` deben registrar la autorización real. Para `adapted`, añade `adaptation_note` y autorización explícita en la frase o en `adaptation_allowed`. Conserva la frase original en su fuente.

Todo bloque literal activo se registra, no solo los favorables. `pending` y `excluded` tienen `active: false` y no aparecen como respuestas del manual. Si se requiere conservarlos en un archivo aparte, identifica ese archivo como evidencia interna.

## Ejecutar

```text
python scripts/validar_entrega.py --prompt PROMPT.md --negocio NEGOCIO.md --contrato CONTRATO.json --evidencia EVIDENCIA.json
python scripts/validar_entrega.py --prompt PROMPT.md --negocio NEGOCIO.md --contrato CONTRATO.json --evidencia EVIDENCIA.json --original-prompt ORIGINAL.md --reporte REVISION.json
python scripts/probar_validador.py
```

El primer comando devuelve código 1 si hay errores y 0 si no. Los avisos indican dependencias o pruebas pendientes; no significan que esté listo para publicar. La salida incluye conteos Unicode y UTF-16, controles documentales y `runtime_test_records_complete`: si todos los escenarios declarados tienen estado de prueba del motor superada y una `observation` escrita. Ese registro debe reflejar observaciones reales; no lo rellenes como «passed» por deducción. El campo solo comprueba el registro, no verifica por sí mismo que ocurrió una prueba.

Corrige los errores dentro del alcance de la tarea; revisa los avisos con criterio. Si faltan materiales o configuración, entrega el borrador y su limitación concreta, sin simular éxito.

## Escenarios de conversación

Elige los aplicables de [evals.json](../evals/evals.json). Hay dos niveles distintos:

1. Evaluar la skill: recibe una petición realista y sus fuentes mínimas, comprueba qué pregunta al responsable y cómo construye los documentos. Si no existe ejecución independiente autorizada, registra una revisión o un ejercicio guiado, no una evaluación independiente.
2. Evaluar el agente resultante: prueba en su motor los permisos, continuidad y acciones con borrador identificado. No envíes mensajes reales a leads para validar un prompt. Con el MCP de uCalls, sube el borrador y ejecuta estos escenarios con `post_api_prompt_editor_test_chat` siguiendo [mcp-ucalls.md](mcp-ucalls.md); la `observation` incluye id y nombre de la versión probada y si el manual era el activo o el borrador.

Pruebas críticas del agente resultante:

- Saludo solo: respuesta breve, sin iniciar todo el diagnóstico.
- Interés general y síntoma vago: pregunta por un dato que cambie la recomendación; no atribuye causa ni ofrece recursos antes del criterio.
- Contexto ya completo: no repite preguntas ni pide otra confirmación ritual.
- Duda directa durante diagnóstico: responde y retoma solo lo pendiente.
- Propuesta y «ok»: ejecuta esa propuesta; no repite el caso ni la oferta.
- «ok» después del envío: no lo interpreta como visto ni como permiso para agenda.
- Petición expresa de cita/recurso: atiende la solicitud sin imponer fases comerciales; conserva datos obligatorios de la acción.
- Rechazo, aplazamiento, queja o parada: mantiene contexto y respeta la decisión.
- Recurso o capacidad ausente: no muestra códigos, promete envío ni inventa una gestión.
- Confirmación: usa evidencia real; no declara reserva por haber enviado un enlace.

Valora el significado y la acción, no una redacción exacta, salvo cuando el requisito sea usar una frase literal. Una prueba con una ruta no demuestra todas las demás.
