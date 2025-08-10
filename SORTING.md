# Timeline Sorting Logic

This document describes the custom multi-level sorting algorithm used to present a chronological, ordered list of a user's memories on a timeline.

## The Sorting Problem for Intervals and Points

Standard sorting algorithms are not designed to handle a mixed collection of points and intervals without an explicit comparison key. Simply sorting by a single date field results in a loss of precision and an inaccurate representation of the data. A more sophisticated sorting logic is required to ensure a stable, predictable, and user-friendly timeline.

## Proposed Sorting Strategy: The Multi-Level Comparison Function

The sorting logic is a custom comparison function that operates on the `sort_start_date` and `sort_end_date` fields from the canonical data model. The use of a stable sorting algorithm (e.g., Timsort, Merge Sort) is recommended to ensure that items with identical keys are not arbitrarily reordered.

The sorting strategy is as follows:

1.  **Primary Key:** The list is first sorted in **ascending order** based on the `sort_start_date`. This is the most intuitive approach for arranging events chronologically.

2.  **Secondary Key (Tie-breaker 1):** For events with an identical `sort_start_date`, the system sorts by `sort_end_date` in **ascending order**. This ensures that shorter intervals appear before longer ones that begin on the same day. For example, a memory from "1990" (`1990-01-01`/`1990-12-31`) will be placed before a memory from the "1990s" (`1990-01-01`/`1999-12-31`).

3.  **Tertiary Key (Tie-breaker 2):** If both `sort_start_date` and `sort_end_date` are identical, a final tie-breaker is applied. The system can sort by `confidence_score` in **descending order**, placing more certain events before uncertain ones. Alternatively, a stable sort algorithm can simply preserve the original input order.

## Sorting Examples

This table formalizes the multi-level comparison logic:

| Data Type                  | Comparison Rule                           | Example                                                                                                                |
| -------------------------- | ----------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Absolute Date              | Primary Key: `sort_start_date`.           | `1990-01-01` comes before `1990-02-01`.                                                                                  |
| Fuzzy Date (same start)    | Secondary Key: `sort_end_date`.           | `1990` (`1990-01-01`/`1990-12-31`) comes before `199X` (`1990-01-01`/`1999-12-31`).                                     |
| Overlapping Intervals      | Primary Key: `sort_start_date`.           | `[1990-01-01/1991-01-01]` comes before `[1990-06-01/1991-06-01]`.                                                         |
| Identical Start/End Dates  | Tertiary Key: `confidence_score` or Stable Sort. | A photo from `1990` (confidence 1.0) appears before a photo from `1990?` (confidence 0.8), or maintains its original order. |
