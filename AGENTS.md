# Temporal Data Management Specification

**Core Capability**: Processes, normalizes, and sorts heterogeneous temporal data (points, ranges, fuzzy dates) for timeline visualization.

**Canonical Format**: All temporal data is represented as an Extended Date/Time Format (EDTF) string, an ISO 8601-2 compliant format.

### Core Data Fields
- **canonical_date**: The EDTF string representation of the event.
- **sort_start_date**: The earliest possible date of the event (ISO 8601).
- **sort_end_date**: The latest possible date of the event (ISO 8601).
- **granularity**: The precision of the original input (e.g., `YYYY`, `YYYY-MM-DD`).
- **confidence_score**: The system's confidence in the parsed date (0-1).
- **original_input**: The raw user-provided string.

### Frontmatter Properties for Blog Posts
- **date**: Post publication date (ISO 8601).
- **lastmod**: Post last modified date (ISO 8601).
- **event_date**: Canonical date of the event described in the post (EDTF).

### Format Examples
- **Year**: `YYYY` (e.g., `1995`)
- **Month**: `YYYY-MM` (e.g., `1995-07`)
- **Date**: `YYYY-MM-DD` (e.g., `1995-07-21`)
- **Fuzzy/Approximate**: `YYYY~`, `YYYY?` (e.g., `1995~`, `1995-07?`)
- **Decade**: `199X` (e.g., `199X`)
- **Range**: `YYYY/YYYY` (e.g., `1990/1999`)
- **Open-ended range**: `[..YYYY]` or `[YYYY..]` (e.g., `[..1995]`, `[1995..]`)

### LLM Interaction Protocol
- **Purpose**: Disambiguate and normalize ambiguous natural language date inputs.
- **Method**: For inputs not parsed deterministically, a few-shot prompt is used to instruct the LLM to return a canonical EDTF string and a confidence score.
- **Example Prompt Injection**:
  ```json
  {
    "query": "I think it was around July 1995",
    "today": "2024-04-15"
  }
  ```
- **Expected LLM Output (JSON)**:
  ```json
  {
    "canonical_date": "1995-07~?",
    "confidence_score": 0.6
  }
  ```
- **Constraint**: LLM should not compute relative dates. It must return a relative formula for the application logic to resolve.

### Key Functions
- `parse_user_input(string user_query)`: Returns a canonical EDTF string and confidence score.
- `get_timeline(sort_direction)`: Returns a sorted list of events based on the defined multi-level sort logic.
