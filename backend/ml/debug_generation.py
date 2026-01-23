from ml.dataset_enrichment import DatasetEnricher
import os
import json

enricher = DatasetEnricher()
# Essayer de générer juste 3 paires pour tester
test_lang = "bété"
print(f"DEBUG: Testing generation for {test_lang}...")
new_pairs = enricher.generate_translations(test_lang, count=3)
print(f"DEBUG: New pairs received: {len(new_pairs)}")
print(f"DEBUG: Data: {json.dumps(new_pairs, indent=2, ensure_ascii=False)}")
