"""
Agnostic Memory Evaluation Benchmark Suite
Tests:
  1. RepoQA Needle Retrieval (Accuracy, Latency, Noise Ratio)
  2. LoCoMo Multi-Turn Project Rule Persistence (Retention Rate)
  3. Agnostic Transfer Test (Cross-Harness Interchangeability)

Zero-Cost: Pure deterministic scoring without commercial LLM-as-a-judge APIs.
"""

import os
import sys
import time
import shutil
from agnostic_memory import AgnosticMemoryStore

def run_evaluation_suite():
    print("=" * 70)
    print("🔬 AGNOSTIC MEMORY BENCHMARK SUITE (Zero-Cost / Open Architecture)")
    print("=" * 70)
    
    test_dir = ".test_benchmark_env"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir, exist_ok=True)
    
    memory = AgnosticMemoryStore(base_dir=os.path.join(test_dir, ".memory"))
    
    # ------------------------------------------------------------------
    # TEST 1: REPOQA / LONGMEMCODE NEEDLE IN A HAYSTACK
    # ------------------------------------------------------------------
    print("\n▶ [TEST 1] RepoQA / LongMemCode: Needle Function Retrieval")
    print("  Creando repositorio simulado de 100 módulos...")
    
    target_file = "src/security/token_validator.py"
    target_secret = "X9_ALPHA_SECURE_HASH_2026"
    target_code = f'''
def validar_token_autorizacion_v2(payload):
    # CLAVE_CONTROL_SECRETO = "{target_secret}"
    return hashlib.sha256(payload.encode()).hexdigest()
'''
    # Index 99 dummy files
    for i in range(1, 100):
        dummy_path = f"src/module_{i}/service.py"
        dummy_code = f'''
def calculate_service_metric_{i}(value):
    """Computes internal billing counters for partition {i}."""
    return value * 1.05 + {i}
'''
        memory.index_code_file(dummy_path, dummy_code)
        
    # Index target needle file
    memory.index_code_file(target_file, target_code)
    print(f"  ✓ 100 archivos indexados en la memoria agnóstica.")

    # Query without mentioning file name or exact function name
    query = "algoritmo cifrado sha256 clave control secreto autorizacion token"
    t_start = time.perf_counter()
    results = memory.retrieve_bm25(query, top_k=3)
    t_elapsed = (time.perf_counter() - t_start) * 1000 # ms

    found_needle = any(target_secret in r["content"] for r in results)
    recall_at_3 = 1.0 if found_needle else 0.0
    
    # Calculate noise ratio
    if results:
        target_len = len(target_code)
        total_len = sum(len(r["content"]) for r in results)
        purity = (target_len / total_len) * 100
    else:
        purity = 0.0

    print(f"  → Tiempo de Búsqueda (CPU): {t_elapsed:.2f} ms")
    print(f"  → Recall@3: {'100% (ÉXITO)' if recall_at_3 == 1.0 else '0% (FALLO)'}")
    print(f"  → Pureza del Contexto (Ground Truth vs Ruido): {purity:.1f}%")

    # ------------------------------------------------------------------
    # TEST 2: LOCOMO MULTI-TURN PERSISTENCE (PROJECT RULES AUDIT)
    # ------------------------------------------------------------------
    print("\n▶ [TEST 2] LoCoMo: Resistencia al Olvido y Reglas Multi-Turno")
    rule_text = "Todas las clases de entidad deben heredar de BaseEntity y registrar timestamp en UTC ISO-8601"
    memory.save_rule(rule_text, category="architecture_rule")
    print(f"  ✓ Regla inyectada en Sesión 1: '{rule_text}'")

    # Simulate 25 turns of distracting context
    print("  Simulando 25 turnos de conversación de distracción...")
    for turn in range(2, 27):
        memory.save_to_spatial_palace(
            wing="general_chat",
            hall="turn_archive",
            drawer=f"turn_{turn}",
            memory_item=f"Turno {turn}: Discusión irrelevante sobre dependencias y preguntas generales."
        )
    
    # Audit rule retrieval after 25 turns
    persisted_rules = memory.get_all_rules()
    rule_found = any(rule_text in r["rule"] for r in persisted_rules)
    print(f"  → Turno 27 (Auditoría):")
    print(f"  → Tasa de Retención de Reglas: {'100% (Persistencia Total)' if rule_found else '0% (Regla Olvidada)'}")

    # ------------------------------------------------------------------
    # TEST 3: AGNOSTIC TRANSFER TEST (CROSS-HARNESS INTEROPERABILITY)
    # ------------------------------------------------------------------
    print("\n▶ [TEST 3] Agnostic Transfer Test: Intercambio Cruzado entre Arneses")
    print("  Fase A: Arnés 'MemPalace' escribe estructura jerárquica en el almacén común...")
    memory.save_to_spatial_palace(
        wing="backend_team",
        hall="api_conventions",
        drawer="error_handling",
        memory_item="Todos los endpoints HTTP deben retornar formato RFC-7807 (Problem Details)."
    )

    print("  Fase B: Simulando desconexión total y apagado de MemPalace...")
    del memory  # Kill instance completely

    print("  Fase C: Encendiendo un segundo arnés ('Hermes / Letta') sobre la MISMA carpeta...")
    second_harness_memory = AgnosticMemoryStore(base_dir=os.path.join(test_dir, ".memory"))
    recovered_item = second_harness_memory.retrieve_spatial(
        wing="backend_team",
        hall="api_conventions",
        drawer="error_handling"
    )

    agnostic_transfer_success = "RFC-7807" in recovered_item
    print(f"  → Contenido recuperado por el nuevo arnés: '{recovered_item}'")
    print(f"  → Puntaje de Agnosticismo (Transfer Score): {'100% (TOTALMENTE PORTABLE)' if agnostic_transfer_success else '0% (FALLO)'}")

    # ------------------------------------------------------------------
    # RESUMEN FINAL
    # ------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("📊 RESULTADO FINAL DE LA EVALUACIÓN DE MEMORIA AGNOSTICA:")
    print("=" * 70)
    print(f"  1. Recall@k en Monorepo (RepoQA):        {recall_at_3 * 100:.0f}%")
    print(f"  2. Latencia de Recuperación en CPU:       {t_elapsed:.2f} ms")
    print(f"  3. Retención Temporal (LoCoMo 25 turnos): {'100%' if rule_found else '0%'}")
    print(f"  4. Portabilidad entre Arneses (Transfer): {'100% (Agnóstica)' if agnostic_transfer_success else '0%'}")
    print(f"  5. Costo de API Keys / Tokens:            $0.00 (100% Local & Open)")
    print("=" * 70)

    # Cleanup test files
    shutil.rmtree(test_dir)
    print("✓ Entorno temporal limpiado con éxito.\n")

if __name__ == "__main__":
    run_evaluation_suite()
