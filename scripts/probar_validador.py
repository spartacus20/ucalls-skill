"""Regression tests for harmful contract/evidence mistakes, using synthetic fixtures."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from validar_entrega import counts, validate


class DeliveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.quote = "Qué te gustaría conseguir?\nQuieres que te comparta la guía?\nAquí tienes la guía"
        (self.root / "source.txt").write_text(self.quote, encoding="utf-8")
        self.prompt = "## IDENTIDAD\nAtiende al negocio. ETAPA 1 pregunta objetivo. ETAPA 2 ofrece; termina el turno. ETAPA 3 envía solo si solicitó o aceptó la guía."
        self.business = "## ETAPA 1 · OBJETIVO\nQué te gustaría conseguir?\n## ETAPA 2 · PROPUESTA\nQuieres que te comparta la guía?\n## ETAPA 3 · ENTREGA\nAquí tienes la guía"
        self.contract = {
            "count_unit": "utf16", "limits": {"prompt_max": 30000},
            "fact_ids": ["objetivo"],
            "diagnosis": {"fields": ["objetivo"], "before_stages": ["E2"]},
            "stages": [
                {"id": "E1", "manual_heading": "ETAPA 1 · OBJETIVO", "prompt_ref": "ETAPA 1", "required_fields": ["objetivo"], "completion": "Conocemos qué busca", "on_complete": ["E2"], "phrase_ids": ["p1"]},
                {"id": "E2", "manual_heading": "ETAPA 2 · PROPUESTA", "prompt_ref": "ETAPA 2", "required_fields": ["objetivo"], "completion": "Responde a la oferta", "on_complete": ["E3"], "phrase_ids": ["p2"], "action": {"kind": "offer", "scope": "guia", "resource_id": "guia"}},
                {"id": "E3", "manual_heading": "ETAPA 3 · ENTREGA", "prompt_ref": "ETAPA 3", "required_fields": [], "completion": "Envío real terminado", "on_complete": [], "phrase_ids": ["p3"], "action": {"kind": "deliver", "scope": "guia", "resource_id": "guia"}, "consent": {"scope": "guia", "basis": ["requested", "accepted"], "offer_stage": "E2"}},
            ],
            "resources": [{"id": "guia", "status": "verified", "marker": None}],
            "tests": [{"id": "ok", "messages": ["ok"], "expectations": ["Entrega la guía aceptada"], "status": "not_run", "environment": "runtime"}],
        }
        self.evidence = {
            "sources": [{"id": "s1", "kind": "chat", "speaker": "seller", "path": "source.txt", "locator": "fixture de prueba; no es un chat de cliente real", "excerpt": self.quote}],
            "phrases": [{"id": f"p{i+1}", "origin": "exact_chat", "source_id": "s1", "bubbles": [q], "active": True} for i, q in enumerate(self.quote.splitlines())],
        }

    def tearDown(self):
        self.temp.cleanup()

    def run_check(self, **changes):
        return validate(changes.get("prompt", self.prompt), changes.get("business", self.business),
                        changes.get("contract", self.contract), changes.get("evidence", self.evidence),
                        self.root, changes.get("original"))

    def assert_code(self, result, code):
        self.assertIn(code, {e["code"] for e in result["errors"]}, result)

    def test_valid_pair_is_not_a_runtime_test(self):
        result = self.run_check()
        self.assertTrue(result["structural_ok"])
        self.assertFalse(result["runtime_test_records_complete"])

    def test_symptom_does_not_replace_diagnostic_fields(self):
        self.contract["fact_ids"].append("situacion_clientes")
        self.contract["diagnosis"]["fields"].append("situacion_clientes")
        self.assert_code(self.run_check(), "INCOMPLETE_DIAGNOSIS")

    def test_unknown_fact_cannot_complete_stage(self):
        self.contract["stages"][0]["required_fields"] = ["facturacion_inventada"]
        self.assert_code(self.run_check(), "UNKNOWN_FACT")

    def test_missing_completion_is_rejected(self):
        self.contract["stages"][0]["completion"] = ""
        self.assert_code(self.run_check(), "STAGE_COMPLETION")

    def test_unknown_route_is_rejected(self):
        self.contract["stages"][0]["on_complete"] = ["E99"]
        self.assert_code(self.run_check(), "UNKNOWN_STAGE")

    def test_video_permission_cannot_authorize_calendar(self):
        self.contract["stages"][2]["action"]["kind"] = "calendar"
        self.contract["stages"][2]["action"]["scope"] = "llamada"
        self.assert_code(self.run_check(), "CONSENT_SCOPE")

    def test_interest_is_not_consent(self):
        self.contract["stages"][2]["consent"]["basis"] = ["interested"]
        self.assert_code(self.run_check(), "CONSENT_BASIS")

    def test_delivery_requires_consent(self):
        del self.contract["stages"][2]["consent"]
        self.assert_code(self.run_check(), "CONSENT_SCOPE")

    def test_direct_request_needs_no_second_offer(self):
        self.contract["stages"][2]["consent"] = {"scope": "guia", "basis": ["requested"]}
        self.assertTrue(self.run_check()["structural_ok"])

    def test_acceptance_uses_same_prior_offer(self):
        self.contract["stages"][1]["action"]["scope"] = "otro-recurso"
        self.assert_code(self.run_check(), "OFFER_SCOPE")

    def test_external_configuration_needs_no_url(self):
        self.contract["resources"][0]["status"] = "external_config"
        self.contract["stages"][2]["on_missing_resource"] = "wait"
        result = self.run_check()
        self.assertTrue(result["structural_ok"])
        self.assertFalse(result["runtime_test_records_complete"])

    def test_missing_resource_has_explicit_fallback(self):
        self.contract["resources"][0]["status"] = "pending"
        self.assert_code(self.run_check(), "MISSING_RESOURCE_PATH")

    def test_unknown_marker_is_rejected(self):
        self.assert_code(self.run_check(prompt=self.prompt + " {{link:inventado}}"), "UNKNOWN_MARKER")

    def test_calendar_link_is_not_booking_evidence(self):
        self.contract["stages"][2]["action"] = {"kind": "confirm", "scope": "reserva"}
        self.assert_code(self.run_check(), "EXECUTION_EVIDENCE")

    def test_customer_text_is_not_seller_text(self):
        self.evidence["sources"][0]["speaker"] = "customer"
        self.assert_code(self.run_check(), "NOT_REAL_SELLER")

    def test_simulation_is_not_historical_chat(self):
        self.evidence["sources"][0]["kind"] = "simulation"
        self.assert_code(self.run_check(), "NOT_REAL_SELLER")

    def test_altered_quote_cannot_claim_literal_origin(self):
        self.evidence["phrases"][0]["bubbles"] = ["Qué te gustaría conseguir, verdad?"]
        self.business += "\nQué te gustaría conseguir, verdad?"
        self.assert_code(self.run_check(), "NOT_LITERAL")

    def test_reordered_bubbles_cannot_claim_literal_origin(self):
        self.evidence["phrases"][0]["bubbles"] = self.quote.splitlines()[::-1]
        self.assert_code(self.run_check(), "NOT_LITERAL")

    def test_quote_must_exist_in_raw_source(self):
        self.evidence["sources"][0]["excerpt"] = "Texto que no aparece en el archivo"
        self.assert_code(self.run_check(), "SOURCE_QUOTE_MISSING")

    def test_json_export_literals_are_decoded(self):
        (self.root / "source.json").write_text(json.dumps({"messages": [{"role": "seller", "text": q} for q in self.quote.splitlines()]}), encoding="utf-8")
        self.evidence["sources"][0]["path"] = "source.json"
        self.assertTrue(self.run_check()["structural_ok"])

    def test_pending_phrase_never_active(self):
        self.evidence["phrases"][0]["origin"] = "pending"
        self.assert_code(self.run_check(), "INACTIVE_PHRASE")

    def test_excluded_phrase_not_in_operative_manual(self):
        self.evidence["phrases"][0].update(origin="excluded", active=False)
        self.assert_code(self.run_check(), "EXCLUDED_IN_MANUAL")

    def test_proposed_phrase_needs_authorization(self):
        self.evidence["phrases"][0]["origin"] = "approved_draft"
        self.assert_code(self.run_check(), "UNAPPROVED_DRAFT")

    def test_minimal_adaptation_is_marked_and_authorized(self):
        self.evidence["phrases"][0].update(origin="adapted", adaptation_note="Retirada de referencia personal", approved=True)
        self.assertTrue(self.run_check()["structural_ok"])

    def test_manual_phrase_must_match_registered_text(self):
        self.assert_code(self.run_check(business=self.business.replace("Qué te gustaría conseguir?", "Qué buscas?")), "PHRASE_MISSING")

    def test_unicode_and_utf16_are_distinct(self):
        self.assertEqual(counts("a🙌"), {"unicode": 2, "utf16": 3})

    def test_limit_counts_actual_final_text(self):
        self.contract["limits"]["prompt_max"] = len(self.prompt)
        self.assert_code(self.run_check(prompt=self.prompt + "🙌"), "PROMPT_LIMIT")

    def test_no_implicit_twenty_thousand_limit(self):
        self.assertTrue(self.run_check(business=self.business + "x" * 21000)["structural_ok"])

    def test_declared_truncation_reports_inaccessible_stage(self):
        self.contract["limits"]["business_runtime_max"] = 60
        self.assert_code(self.run_check(), "STAGE_NOT_VISIBLE")

    def test_explicit_structure_preservation_is_checked(self):
        self.assert_code(self.run_check(original=self.prompt.replace("IDENTIDAD", "OTRA")), "HEADINGS_CHANGED")

    def test_failed_runtime_test_blocks_clean_delivery(self):
        self.contract["tests"][0]["status"] = "failed"
        self.assert_code(self.run_check(), "FAILED_TEST")

    def test_document_walkthrough_never_claims_runtime(self):
        self.contract["tests"][0].update(status="passed", environment="document_walkthrough", observation="Revisión guiada")
        self.assertFalse(self.run_check()["runtime_test_records_complete"])

    def test_passed_label_without_observation_is_insufficient(self):
        self.contract["tests"][0]["status"] = "passed"
        self.assertFalse(self.run_check()["runtime_test_records_complete"])

    def test_complete_runtime_records_do_not_authenticate_execution(self):
        self.contract["tests"][0].update(status="passed", observation="Registro sintético para probar la comprobación documental")
        self.assertTrue(self.run_check()["runtime_test_records_complete"])
        self.assertTrue(self.run_check()["manual_review"])

    def test_cli_writes_report_and_returns_failure_for_invalid_input(self):
        for name, content in {"prompt.md": self.prompt, "business.md": self.business, "contract.json": "[]"}.items():
            (self.root / name).write_text(content, encoding="utf-8")
        result = subprocess.run([sys.executable, "-X", "utf8", str(Path(__file__).with_name("validar_entrega.py")), "--prompt", str(self.root / "prompt.md"), "--negocio", str(self.root / "business.md"), "--contrato", str(self.root / "contract.json"), "--reporte", str(self.root / "report.json")], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 1)
        self.assertFalse(json.loads((self.root / "report.json").read_text(encoding="utf-8"))["structural_ok"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
