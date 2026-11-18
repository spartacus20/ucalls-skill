"""Audita enlaces y medios de un agente uCalls contra su catálogo, sin llamar al modelo.

Uso:
  python3 auditar_recursos.py --docs prompt.md manual.md --catalog catalogo.json [--agent-id UUID] [--conversion-slug calendly_agenda]

catalogo.json: {"links": [...], "media": [...]} con los campos de agent_links / agent_media
(slug, is_active, agent_ids, usage_instructions; en links también shorten, auto_tracking, tracking_params, target).

Errores (exit 1): marcador con slug inexistente o inactivo (el motor lo borra sin avisar),
marcadores PENDIENTE/FALTA en los documentos.
Avisos: URLs literales, recursos sin agent_ids, recursos asignados a otro agente,
enlace de conversión sin medición, slugs con formato inválido.
"""
import argparse
import json
import re
import sys
from pathlib import Path

PLACEHOLDER = re.compile(r"\{\{\s*(link|media)\s*:\s*([^}\s]+)\s*\}\}")
SLUG_OK = re.compile(r"^[a-z0-9_-]{1,48}$")
URL = re.compile(r"https?://[^\s)\]>\"'*]+", re.I)
PENDING = re.compile(r"\[\s*(?:⚠️\s*)?(?:PENDIENTE|FALTA)[^\]]*\]", re.I)


def load_catalog(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return {kind: {item["slug"]: item for item in data.get(key, []) if item.get("slug")}
            for kind, key in (("link", "links"), ("media", "media"))}


def audit(docs, catalog, agent_id=None, conversion_slugs=()):
    errors, warnings = [], []

    def issue(bucket, code, msg):
        bucket.append({"code": code, "message": msg})

    used = set()
    for name, text in docs.items():
        for kind, slug in PLACEHOLDER.findall(text):
            used.add((kind, slug))
            if not SLUG_OK.match(slug):
                issue(errors, "SLUG_FORMAT", f"{name}: {{{{{kind}:{slug}}}}} no cumple ^[a-z0-9_-]{{1,48}}$; el motor no lo resolverá")
                continue
            item = catalog[kind].get(slug)
            if not item:
                issue(errors, "SLUG_MISSING", f"{name}: {{{{{kind}:{slug}}}}} no existe en el catálogo; el motor borra el marcador sin avisar")
            elif not item.get("is_active", True):
                issue(errors, "SLUG_INACTIVE", f"{name}: {{{{{kind}:{slug}}}}} está inactivo")
            elif agent_id and item.get("agent_ids") and agent_id not in item["agent_ids"]:
                issue(errors, "SLUG_OTHER_AGENT", f"{name}: {{{{{kind}:{slug}}}}} está asignado a otros agentes, no a {agent_id}")
        for url in sorted(set(URL.findall(text))):
            issue(warnings, "LITERAL_URL", f"{name}: URL literal {url.split('?')[0]}; pásala al catálogo como {{{{link:slug}}}}")
        for mark in sorted(set(PENDING.findall(text))):
            issue(errors, "PENDING_MARK", f"{name}: marcador {mark!r}; se enviaría tal cual al lead")

    for kind, items in catalog.items():
        for slug, item in items.items():
            if not item.get("is_active", True):
                continue
            ids = item.get("agent_ids") or []
            if not ids:
                issue(warnings, "UNSCOPED", f"{kind}:{slug} activo para todos los agentes (agent_ids vacío)")
            if PENDING.search(item.get("usage_instructions") or ""):
                issue(errors, "PENDING_MARK", f"{kind}:{slug} tiene un marcador pendiente en usage_instructions")
            if kind == "link" and slug in conversion_slugs:
                measured = item.get("shorten") or item.get("auto_tracking") or item.get("tracking_params") \
                    or "utm_" in (item.get("target") or "")
                if not measured:
                    issue(warnings, "UNMEASURED", f"link:{slug} es de conversión y no tiene shorten, auto_tracking ni UTM")

    for kind, slug in sorted(used):
        if SLUG_OK.match(slug) and slug in catalog[kind] and not (catalog[kind][slug].get("usage_instructions") or "").strip():
            issue(warnings, "NO_USAGE", f"{kind}:{slug} sin usage_instructions; el modelo no sabe cuándo usarlo")

    dedupe = lambda items: [dict(t) for t in dict.fromkeys(tuple(sorted(i.items())) for i in items)]
    errors, warnings = dedupe(errors), dedupe(warnings)
    return {"ok": not errors, "errors": errors, "warnings": warnings,
            "placeholders": sorted(f"{k}:{s}" for k, s in used)}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--docs", nargs="+", required=True, help="prompt, manual u otros textos a revisar")
    ap.add_argument("--catalog", required=True)
    ap.add_argument("--agent-id")
    ap.add_argument("--conversion-slug", action="append", default=[], help="slug del enlace de agenda/compra (repetible)")
    args = ap.parse_args()
    docs = {Path(p).name: Path(p).read_text(encoding="utf-8") for p in args.docs}
    result = audit(docs, load_catalog(args.catalog), args.agent_id, set(args.conversion_slug))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
