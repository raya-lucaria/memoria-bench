"""
Agnostic Memory Core Engine (Standard Library Python 3)
Zero External Dependencies - 100% Offline & Free

Architecture:
  - Universal Memory Store: JSONL records + File hierarchy
  - Hybrid Retrieval: BM25/Lexical TF-IDF + Loci Spatial Hierarchy + AST Code Symbol Index
  - Agnostic Interfaces: Can be read & written by Hermes, MemPalace, Letta, Mem0, and PrimeAgent
"""

import os
import json
import re
import math
import time
from typing import List, Dict, Any, Optional

class AgnosticMemoryStore:
    def __init__(self, base_dir: str = ".agnostic_memory"):
        self.base_dir = base_dir
        self.rules_file = os.path.join(base_dir, "rules.jsonl")
        self.code_index_file = os.path.join(base_dir, "code_index.json")
        self.palace_dir = os.path.join(base_dir, "palace")
        os.makedirs(self.base_dir, exist_ok=True)
        os.makedirs(self.palace_dir, exist_ok=True)
        
        # In-memory indices for evaluation
        self.documents = []  # List of {"id": str, "path": str, "content": str, "tokens": List[str]}
        self.rules = []      # List of {"id": str, "rule": str, "category": str, "timestamp": float}
        self.symbols = {}    # symbol_name -> {"path": str, "line": int, "signature": str}

    # -------------------------------------------------------------
    # Write / Ingest APIs (Harness-Agnostic)
    # -------------------------------------------------------------
    def save_rule(self, rule_text: str, category: str = "coding_standard") -> Dict[str, Any]:
        """Saves a project rule/convention permanently."""
        record = {
            "id": f"rule_{len(self.rules) + 1}",
            "rule": rule_text,
            "category": category,
            "timestamp": time.time()
        }
        self.rules.append(record)
        with open(self.rules_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
        return record

    def index_code_file(self, file_path: str, content: str):
        """Indexes a source file for lexical and symbol retrieval."""
        tokens = self._tokenize(content)
        doc = {
            "id": file_path,
            "path": file_path,
            "content": content,
            "tokens": tokens
        }
        self.documents.append(doc)
        
        # Extract AST/Regex Symbols (Classes & Functions)
        for line_no, line in enumerate(content.splitlines(), start=1):
            func_match = re.match(r'^\s*def\s+([a-zA-Z0-9_]+)\s*\((.*?)\):', line)
            if func_match:
                name, args = func_match.groups()
                self.symbols[name] = {"path": file_path, "line": line_no, "type": "function", "args": args}
            
            class_match = re.match(r'^\s*class\s+([a-zA-Z0-9_]+)(?:\((.*?)\))?:', line)
            if class_match:
                name, bases = class_match.groups()
                self.symbols[name] = {"path": file_path, "line": line_no, "type": "class", "bases": bases or ""}

    def save_to_spatial_palace(self, wing: str, hall: str, drawer: str, memory_item: str):
        """Method of Loci (MemPalace style) hierarchical memory write."""
        target_dir = os.path.join(self.palace_dir, wing, hall)
        os.makedirs(target_dir, exist_ok=True)
        file_path = os.path.join(target_dir, f"{drawer}.txt")
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(memory_item + "\n")

    # -------------------------------------------------------------
    # Read / Retrieval APIs (Evaluated by Benchmarks)
    # -------------------------------------------------------------
    def retrieve_bm25(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Lexical BM25 retrieval across indexed files."""
        if not self.documents:
            return []
        
        query_tokens = self._tokenize(query)
        N = len(self.documents)
        avgdl = sum(len(d["tokens"]) for d in self.documents) / max(N, 1)
        k1 = 1.5
        b = 0.75

        # Document frequencies
        df = {}
        for q in query_tokens:
            df[q] = sum(1 for d in self.documents if q in d["tokens"])

        scored = []
        for d in self.documents:
            score = 0.0
            doc_len = len(d["tokens"])
            token_counts = {}
            for t in d["tokens"]:
                token_counts[t] = token_counts.get(t, 0) + 1

            for q in query_tokens:
                if q in token_counts:
                    f = token_counts[q]
                    idf = math.log((N - df[q] + 0.5) / (df[q] + 0.5) + 1.0)
                    tf = (f * (k1 + 1)) / (f + k1 * (1 - b + b * (doc_len / avgdl)))
                    score += idf * tf
            
            if score > 0:
                scored.append({"path": d["path"], "score": score, "content": d["content"]})

        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]

    def retrieve_symbol(self, symbol_name: str) -> Optional[Dict[str, Any]]:
        """Deterministic AST/Symbol retrieval (PrimeAgent style)."""
        return self.symbols.get(symbol_name)

    def retrieve_spatial(self, wing: str, hall: str, drawer: str) -> str:
        """Retrieves targeted memory drawer from MemPalace spatial hierarchy."""
        file_path = os.path.join(self.palace_dir, wing, hall, f"{drawer}.txt")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        return ""

    def get_all_rules(self) -> List[Dict[str, Any]]:
        """Returns all persisted rules."""
        if not self.rules and os.path.exists(self.rules_file):
            with open(self.rules_file, "r", encoding="utf-8") as f:
                self.rules = [json.loads(line) for line in f if line.strip()]
        return self.rules

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r'[a-zA-Z0-9_]+', text.lower())
