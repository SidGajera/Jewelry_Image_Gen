"""Pipeline package for the Lucent Carat Lab catalog generator.

Modules:
  fallback.py  — geometry-immutable composite engine (the default path for
                 preserving source-ring geometry; wraps the locked scripts).
  qc.py        — geometry/provenance verification of a finished image.
  pipeline.py  — orchestration + the default-composite policy per shot type.
"""
