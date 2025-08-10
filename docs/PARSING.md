# Parsing Architecture

This document explains the multi-layered parsing architecture used to handle the wide spectrum of user-provided temporal expressions.

## The Problem: Ambiguity in Human Temporal Expression

User-provided temporal information is often ambiguous, conversational, or follows local conventions (e.g., `02/03/2025`). A rigid parser would create a frustrating user experience. Our goal is to design a system that can gracefully handle imprecision and interpret the user's intent.

## Multi-Layered Parsing Architecture

The system employs a two-tiered parsing mechanism to handle both structured and conversational inputs.

### Tier 1: Deterministic Rule-Based Parsing

This initial layer handles inputs that conform to standard, unambiguous date formats like ISO 8601. It is designed to be fast and efficient, serving as the primary processing engine for well-formed inputs. This tier includes robust validation to ensure calendrical accuracy (e.g., rejecting `2024-02-30`).

### Tier 2: LLM-Assisted Semantic Parsing for "Grace"

If the rule-based parser fails or encounters an ambiguous format, the input is passed to a Large Language Model (LLM). The LLM acts as a semantic layer, interpreting natural language and returning a structured, canonical output.

This "grace" mechanism presents the LLM's interpretation back to the user for confirmation (e.g., "Did you mean: 1985~?"). This interactive feedback loop is a best practice for handling ambiguous user input.

## LLM Instructions for Temporal Correction

The LLM-assisted parsing component follows a two-step process:

1.  **Transformation to a Structured Format:** The LLM is prompted to translate the user's query into a structured JSON object containing a canonical EDTF string and a confidence score. The prompt uses few-shot examples to guide the LLM towards a deterministic output.

    *   **Example Prompt Injection:**
        ```json
        {
          "query": "I think it was around July 1995",
          "today": "2024-04-15"
        }
        ```
    *   **Expected LLM Output (JSON):**
        ```json
        {
          "canonical_date": "1995-07~?",
          "confidence_score": 0.6
        }
        ```
    *   **Constraint:** The LLM should not compute relative dates itself. It must return a relative formula for the application logic to resolve.

2.  **Validation and Refinement:** The application's business logic processes the structured JSON to resolve any formulas. The final parsed EDTF string is then validated. The confidence score determines whether user confirmation is needed.

For optimal performance, the LLM should be configured with low `temperature` and `top_p` values to encourage deterministic, factual output.

## Normalization Examples

The following table demonstrates the normalization process:

| User Input                         | Rule-Based Output (if applicable) | LLM-Assisted Output (Canonical EDTF) | LLM Confidence |
| ---------------------------------- | --------------------------------- | ------------------------------------ | -------------- |
| "1990"                             | `1990-01-01`                      | `1990`                               | 1.0            |
| "the 1990s"                        | null                              | `199X`                               | 0.9            |
| "early 1990"                       | null                              | `1990-01~`                           | 0.7            |
| "the 80s"                          | null                              | `198X`                               | 0.9            |
| "last month"                       | null                              | ``                                   | 1.0            |
| "I think it was around July 1995"  | null                              | `1995-07~?`                          | 0.6            |
