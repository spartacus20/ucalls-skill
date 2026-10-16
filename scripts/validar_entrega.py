"""Validate declared business-chat contracts and literal evidence, without model calls."""
import argparse
import json
import re
from pathlib import Path


def counts(text):
    return {"unicode": len(text), "utf16": len(text.encode("utf-16-le")) // 2}


def headings(text):
    return re.findall(r"^(#{1,6})\s+(.+?)\s*$", text, re.M)


def json_strings(value):
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [s for item in value for s in json_strings(item)]
    if isinstance(value, dict):
        return [s for item in value.values() for s in json_strings(item)]
    return []


def json_message_texts(value):
    """Decode common message text fields separately from intervening role metadata."""
    if isinstance(value, list):
        return [s for item in value for s in json_message_texts(item)]
    if isinstance(value, dict):
        result = []
        for key, item in value.items():
            if key in {"text", "content", "body", "message"} and isinstance(item, str):
                result.append(item)
            elif isinstance(item, (dict, list)):
                result.extend(json_message_texts(item))
        return result
    return []


def validate(prompt, business, contract, evidence=None, evidence_dir=None, original=None):
    errors, warnings = [], []

    def issue(code, message, warning=False):
        (warnings if warning else errors).append({"code": code, "message": message})

    def index(items, label):
        found = {}
        if not isinstance(items, list):
            issue("SCHEMA", f"{label} debe ser una lista")
            return found
        for item in items:
            if not isinstance(item, dict) or not isinstance(item.get("id"), str) or not item["id"]:
                issue("SCHEMA", f"Cada registro de {label} necesita id textual")
                continue
            if item["id"] in found:
                issue("DUPLICATE_ID", f"id duplicado en {label}: {item['id']}")
            found[item["id"]] = item
        return found

    def string_list(value, label):
        if not isinstance(value, list) or any(not isinstance(x, str) or not x for x in value):
            issue("SCHEMA", f"{label} debe contener textos no vacíos")
            return []
        return value

    if not isinstance(contract, dict):
        issue("SCHEMA", "El contrato debe ser un objeto")
        contract = {}
    unit = contract.get("count_unit", "utf16")
    if unit not in ("unicode", "utf16"):
        issue("COUNT_UNIT", "count_unit debe ser unicode o utf16")
        unit = "utf16"
    prompt_counts, business_counts = counts(prompt), counts(business)
    limits = contract.get("limits", {})
    if not isinstance(limits, dict):
        issue("SCHEMA", "limits debe ser un objeto")
        limits = {}
    for key, value in limits.items():
        if key in ("prompt_max", "prompt_preferred", "business_runtime_max"):
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                issue("LIMIT_INVALID", f"{key} debe ser un entero positivo")
    max_prompt = limits.get("prompt_max")
    preferred = limits.get("prompt_preferred")
    runtime_max = limits.get("business_runtime_max")
    if isinstance(max_prompt, int) and not isinstance(max_prompt, bool) and prompt_counts[unit] > max_prompt:
        issue("PROMPT_LIMIT", f"Prompt: {prompt_counts[unit]} > {max_prompt} ({unit})")
    elif isinstance(preferred, int) and prompt_counts[unit] > preferred:
        issue("PROMPT_PREFERRED", "Supera la longitud preferida", True)
    if isinstance(runtime_max, int) and not isinstance(runtime_max, bool) and runtime_max > 0:
        visible_business = business.encode("utf-16-le")[:runtime_max * 2].decode("utf-16-le", errors="ignore") if unit == "utf16" else business[:runtime_max]
        if business_counts[unit] > runtime_max:
            issue("BUSINESS_TRUNCATION", "El manual maestro supera el límite de inyección declarado; comprobar edición de despliegue", True)
    else:
        visible_business = business
    if original is not None and headings(prompt) != headings(original):
        issue("HEADINGS_CHANGED", "No se conservan los encabezados del prompt original solicitado")
    if not prompt.strip() or not business.strip():
        issue("EMPTY_DOCUMENT", "Los dos documentos deben tener contenido")
    if "<!--" in prompt or "<!--" in business:
        issue("AUTHORING_COMMENTS", "Quedan comentarios de autoría; comprobar que no son restos de plantilla", True)

    fact_ids = set(string_list(contract.get("fact_ids", []), "fact_ids"))
    stages = index(contract.get("stages", []), "stages")
    resources = index(contract.get("resources", []), "resources")
    if not stages:
        issue("NO_STAGES", "El contrato no define etapas activas")
    if evidence is None:
        evidence = {}
    if not isinstance(evidence, dict):
        issue("SCHEMA", "La evidencia debe ser un objeto")
        evidence = {}
    sources = index(evidence.get("sources", []), "sources")
    phrases = index(evidence.get("phrases", []), "phrases")
    business_headings = {h[1] for h in headings(business)}
    visible_headings = {h[1] for h in headings(visible_business)}
    for source_id, source in sources.items():
        if source.get("kind") not in {"chat", "owner", "simulation", "document"}:
            issue("SOURCE_KIND", f"Fuente {source_id}: tipo no reconocido")
        excerpt = source.get("excerpt")
        if not isinstance(excerpt, str) or not excerpt or not source.get("locator"):
            issue("SOURCE_EVIDENCE", f"Fuente {source_id}: faltan cita o localizador")
        source_path = source.get("path")
        if not isinstance(source_path, str) or not source_path:
            issue("SOURCE_PATH", f"Fuente {source_id}: falta ruta verificable")
            continue
        path = Path(source_path)
        if not path.is_absolute():
            path = Path(evidence_dir or ".") / path
        try:
            raw = path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeError) as exc:
            issue("SOURCE_UNREADABLE", f"Fuente {source_id}: {type(exc).__name__}")
            continue
        corpus = raw
        if path.suffix.lower() == ".json":
            try:
                decoded = json.loads(raw)
                corpus += "\n" + "\n".join(json_strings(decoded)) + "\n" + "\n".join(json_message_texts(decoded))
            except ValueError:
                issue("SOURCE_JSON", f"Fuente {source_id}: JSON inválido")
        if isinstance(excerpt, str) and excerpt not in corpus:
            issue("SOURCE_QUOTE_MISSING", f"Fuente {source_id}: la cita no consta en el archivo")

    origins = {"exact_chat", "owner_literal", "approved_draft", "adapted", "pending", "excluded"}
    for phrase_id, phrase in phrases.items():
        origin = phrase.get("origin")
        active = phrase.get("active")
        if origin not in origins or not isinstance(active, bool):
            issue("PHRASE_SCHEMA", f"Frase {phrase_id}: origin o active inválido")
        bubbles = string_list(phrase.get("bubbles", []), f"bubbles de {phrase_id}")
        if active and not bubbles:
            issue("EMPTY_PHRASE", f"Frase activa sin texto: {phrase_id}")
        if origin in {"pending", "excluded"}:
            if active:
                issue("INACTIVE_PHRASE", f"Frase pendiente/excluida marcada activa: {phrase_id}")
            if bubbles and all(b in business for b in bubbles):
                issue("EXCLUDED_IN_MANUAL", f"Frase pendiente/excluida incluida en el manual: {phrase_id}")
        if active and any(b not in business for b in bubbles):
            issue("PHRASE_MISSING", f"Frase activa no coincide con el manual: {phrase_id}")
        if active and any(b not in visible_business for b in bubbles):
            issue("PHRASE_NOT_VISIBLE", f"Frase activa inaccesible con el límite declarado: {phrase_id}")
        if origin in {"pending", "excluded"}:
            continue
        source = sources.get(phrase.get("source_id"))
        if not source:
            issue("PHRASE_SOURCE", f"Frase {phrase_id}: no existe su fuente")
            continue
        if origin == "exact_chat" and (source.get("kind") != "chat" or source.get("speaker") != "seller"):
            issue("NOT_REAL_SELLER", f"Frase {phrase_id}: no es conversación del vendedor")
        if origin == "owner_literal" and source.get("kind") != "owner":
            issue("NOT_OWNER_LITERAL", f"Frase {phrase_id}: no es respuesta del responsable")
        if origin in {"exact_chat", "owner_literal"}:
            excerpt = source.get("excerpt", "")
            cursor = 0
            for bubble in bubbles:
                pos = excerpt.find(bubble, cursor) if isinstance(excerpt, str) else -1
                if pos < 0:
                    issue("NOT_LITERAL", f"Frase {phrase_id}: texto u orden alterado respecto a la fuente")
                    break
                cursor = pos + len(bubble)
        if origin == "approved_draft" and (phrase.get("approved") is not True or not phrase.get("approval_note")):
            issue("UNAPPROVED_DRAFT", f"Frase propuesta sin autorización registrada: {phrase_id}")
        if origin == "adapted":
            if not phrase.get("adaptation_note") or not (phrase.get("approved") is True or evidence.get("adaptation_allowed") is True):
                issue("UNAPPROVED_ADAPTATION", f"Adaptación sin cambio/autorización registrados: {phrase_id}")
            if source.get("kind") == "simulation":
                issue("SIMULATION_AS_SOURCE", f"Frase {phrase_id}: la simulación no es fuente de una adaptación histórica")

    used_phrases = set()
    action_kinds = {"offer", "propose", "deliver", "calendar", "book", "purchase", "confirm"}
    for stage_id, stage in stages.items():
        heading = stage.get("manual_heading")
        if not isinstance(heading, str) or heading not in business_headings:
            issue("MANUAL_STAGE", f"Etapa {stage_id}: no existe el encabezado del manual")
        elif heading not in visible_headings:
            issue("STAGE_NOT_VISIBLE", f"Etapa {stage_id}: inaccesible con el límite declarado")
        prompt_ref = stage.get("prompt_ref")
        if not isinstance(prompt_ref, str) or not re.search(r"(?<!\w)" + re.escape(prompt_ref) + r"(?!\w)", prompt):
            issue("PROMPT_STAGE", f"Etapa {stage_id}: falta remisión en el prompt")
        if not isinstance(stage.get("completion"), str) or not stage["completion"].strip():
            issue("STAGE_COMPLETION", f"Etapa {stage_id}: falta criterio de finalización")
        required = string_list(stage.get("required_fields", []), f"required_fields de {stage_id}")
        for field in required:
            if field not in fact_ids:
                issue("UNKNOWN_FACT", f"Etapa {stage_id}: campo no definido {field}")
        for target in string_list(stage.get("on_complete", []), f"on_complete de {stage_id}"):
            if target not in stages:
                issue("UNKNOWN_STAGE", f"Etapa {stage_id}: destino inexistente {target}")
        for phrase_id in string_list(stage.get("phrase_ids", []), f"phrase_ids de {stage_id}"):
            used_phrases.add(phrase_id)
            if phrase_id not in phrases or phrases[phrase_id].get("active") is not True:
                issue("STAGE_PHRASE", f"Etapa {stage_id}: frase inexistente/inactiva {phrase_id}")
        action = stage.get("action")
        if action is None:
            continue
        if not isinstance(action, dict) or action.get("kind") not in action_kinds or not action.get("scope"):
            issue("ACTION_SCHEMA", f"Etapa {stage_id}: acción inválida")
            continue
        scope = action["scope"]
        if action["kind"] in {"deliver", "calendar", "book", "purchase"}:
            consent = stage.get("consent")
            if not isinstance(consent, dict) or consent.get("scope") != scope:
                issue("CONSENT_SCOPE", f"Etapa {stage_id}: falta permiso para {scope}")
            else:
                basis = string_list(consent.get("basis", []), f"consent.basis de {stage_id}")
                if not basis or any(b not in {"requested", "accepted"} for b in basis):
                    issue("CONSENT_BASIS", f"Etapa {stage_id}: interés/recepción no equivalen a permiso")
                offered = consent.get("offer_stage")
                if offered is not None:
                    offer_action = stages.get(offered, {}).get("action", {})
                    if not isinstance(offer_action, dict) or offer_action.get("kind") not in {"offer", "propose"} or offer_action.get("scope") != scope:
                        issue("OFFER_SCOPE", f"Etapa {stage_id}: oferta previa de otro alcance o inexistente")
        if action["kind"] == "confirm" and not stage.get("execution_evidence"):
            issue("EXECUTION_EVIDENCE", f"Etapa {stage_id}: no define evidencia para confirmar")
        resource_id = action.get("resource_id")
        if resource_id is not None:
            if resource_id not in resources:
                issue("UNKNOWN_RESOURCE", f"Etapa {stage_id}: recurso inexistente {resource_id}")
            elif resources[resource_id].get("status") != "verified" and action["kind"] in {"deliver", "calendar", "book", "purchase"}:
                if stage.get("on_missing_resource") not in {"wait", "operator", "answer_without_action"}:
                    issue("MISSING_RESOURCE_PATH", f"Etapa {stage_id}: no contempla recurso pendiente")

    diagnosis = contract.get("diagnosis", {})
    if not isinstance(diagnosis, dict):
        issue("SCHEMA", "diagnosis debe ser un objeto")
        diagnosis = {}
    diagnosis_fields = set(string_list(diagnosis.get("fields", []), "diagnosis.fields"))
    if not diagnosis_fields.issubset(fact_ids):
        issue("DIAGNOSIS_FACTS", "El diagnóstico usa campos no definidos")
    for target in string_list(diagnosis.get("before_stages", []), "diagnosis.before_stages"):
        if target not in stages:
            issue("DIAGNOSIS_STAGE", f"Destino de diagnóstico inexistente: {target}")
        elif not diagnosis_fields.issubset(set(stages[target].get("required_fields", []))):
            issue("INCOMPLETE_DIAGNOSIS", f"Etapa {target}: ofrece antes de exigir todos los campos declarados")

    known_markers = set()
    dependencies_pending = False
    for resource_id, resource in resources.items():
        status = resource.get("status")
        if status not in {"verified", "external_config", "pending"}:
            issue("RESOURCE_STATUS", f"Recurso {resource_id}: status inválido")
        if status != "verified":
            dependencies_pending = True
            issue("RESOURCE_UNVERIFIED", f"Recurso {resource_id}: {status}; no se ha verificado su entrega", True)
        marker = resource.get("marker")
        if marker is not None:
            if not isinstance(marker, str) or not re.fullmatch(r"\{\{(?:link|media):[a-z0-9_-]{1,48}\}\}", marker):
                issue("MARKER_INVALID", f"Recurso {resource_id}: marcador inválido para este contrato")
            else:
                known_markers.add(marker)
    for marker in set(re.findall(r"\{\{(?:link|media):[^{}]+\}\}", prompt + "\n" + business)):
        if marker not in known_markers:
            issue("UNKNOWN_MARKER", "Existe un marcador de recurso sin registrar en el contrato")
    active_unrouted = {i for i, p in phrases.items() if p.get("active") is True} - used_phrases
    if active_unrouted:
        issue("UNROUTED_PHRASES", "Frases activas fuera de etapas: revisar dudas/objeciones directas en el manual", True)
    tests = index(contract.get("tests", []), "tests")
    for test_id, test in tests.items():
        string_list(test.get("messages", []), f"messages de {test_id}")
        expectations = string_list(test.get("expectations", []), f"expectations de {test_id}")
        if not expectations or test.get("status") not in {"not_run", "passed", "failed"} or test.get("environment") not in {"document_walkthrough", "runtime"}:
            issue("TEST_SCHEMA", f"Prueba {test_id}: faltan expectativas, estado o entorno válido")
        if test.get("status") == "failed":
            issue("FAILED_TEST", f"Prueba fallida pendiente de resolver: {test_id}")
    runtime_records_complete = bool(tests) and all(t.get("status") == "passed" and t.get("environment") == "runtime" and t.get("observation") for t in tests.values()) and not dependencies_pending and not errors
    if not runtime_records_complete:
        issue("RUNTIME_NOT_VERIFIED", "La entrega documental no acredita todos los escenarios en el motor", True)
    return {
        "structural_ok": not errors,
        "runtime_test_records_complete": runtime_records_complete,
        "count_unit": unit,
        "counts": {"prompt": prompt_counts, "business": business_counts},
        "records": {"stages": len(stages), "phrases": len(phrases), "sources": len(sources), "tests": len(tests)},
        "errors": errors,
        "warnings": warnings,
        "manual_review": ["Correspondencia semántica entre contrato y documentos", "Autor real de citas y vigencia de hechos", "Resultados observados de las pruebas declaradas"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompt", type=Path, required=True)
    parser.add_argument("--negocio", type=Path, required=True)
    parser.add_argument("--contrato", type=Path, required=True)
    parser.add_argument("--evidencia", type=Path)
    parser.add_argument("--original-prompt", type=Path)
    parser.add_argument("--reporte", type=Path)
    args = parser.parse_args()
    try:
        read = lambda p: p.read_text(encoding="utf-8-sig")
        result = validate(read(args.prompt), read(args.negocio), json.loads(read(args.contrato)),
                          json.loads(read(args.evidencia)) if args.evidencia else None,
                          args.evidencia.parent if args.evidencia else None,
                          read(args.original_prompt) if args.original_prompt else None)
    except (OSError, UnicodeError, ValueError, TypeError) as exc:
        result = {"structural_ok": False, "runtime_test_records_complete": False,
                  "errors": [{"code": "INPUT_ERROR", "message": str(exc)}], "warnings": []}
    output = json.dumps(result, ensure_ascii=False, indent=2)
    if args.reporte:
        args.reporte.parent.mkdir(parents=True, exist_ok=True)
        args.reporte.write_text(output + "\n", encoding="utf-8")
    print(output)
    return 0 if result["structural_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
