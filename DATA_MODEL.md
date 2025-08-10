# Data Model

This document details the canonical data schema for representing temporal data in the system. The core of the specification is the adoption of the Extended Date/Time Format (EDTF) to handle the nuances of uncertain and approximate temporal expressions.

## The Inadequacy of Standard Data Types

Standard date and time objects are insufficient for handling temporal uncertainty. A fuzzy date like "the 1990s" represents an interval, not a single point. Storing this as a simple date, such as `1990-01-01`, fundamentally corrupts the data by losing the user's original intent and forcing an arbitrary precision.

## Adopting the Extended Date/Time Format (EDTF)

To address these limitations, we adopt the Extended Date/Time Format (EDTF), an international standard (ISO 8601-2), as our canonical model.

Key features of EDTF leveraged in this system include:

*   **Uncertainty and Approximation:** `?` and `~` can be appended to a date string (e.g., `1984?`, `2004-06~`).
*   **Ranges:** A forward slash `/` denotes a time interval (e.g., `1990/1999` for "the 1990s"). Open-ended ranges are also supported (e.g., `[..1984]`).
*   **Unspecified Digits:** `X` can represent an unknown digit (e.g., `156X` for the 1560s).
*   **Collections:** A set of discrete, possible dates can be represented using square brackets (e.g., `[1667,1668,1670..1672]`).

## Canonical Representation of Date Types

All temporal data is stored internally in a canonical format:

*   **Absolute Dates:** Standard ISO 8601 date string (e.g., `2024-01-15`).
*   **Fuzzy Dates:** An EDTF string (e.g., `199X` or `1990-01-01/1999-12-31` for "1990s").
*   **Date Ranges:** ISO 8601-2 interval format (e.g., `2024-01-01/2024-03-31`).
*   **Relative Dates:** Converted into an EDTF range against a `NOW` timestamp during parsing. The original input is preserved.

## Core Data Structure

The core data structure is defined as follows:

| Field Name         | Data Type           | Description                                                                    | Example                                                               |
| ------------------ | ------------------- | ------------------------------------------------------------------------------ | --------------------------------------------------------------------- |
| `primary_id`       | `UUID`              | Unique identifier for the memory/event.                                        | `81d4512b-b892-4f38-9e66-7b561c28f32c`                                |
| `canonical_date`   | `EDTF String`       | The core date representation of the event.                                     | `1995-07-21?` (Uncertain), `199X` (Decade), `2004/2006` (Range)        |
| `sort_start_date`  | `ISO 8601 Date`     | The earliest possible date in the `canonical_date` range. Used for sorting.    | `1995-07-21` for `1995-07-21?`; `1990-01-01` for `199X`                |
| `sort_end_date`    | `ISO 8601 Date`     | The latest possible date in the `canonical_date` range. Used for sorting.      | `1995-07-21` for `1995-07-21?`; `1999-12-31` for `199X`                |
| `granularity`      | `Enum`              | The precision of the original user input.                                      | `YYYY`, `YYYY-MM`, `YYYY-MM-DD`                                         |
| `confidence_score` | `Float (0-1)`       | A numerical representation of the system's certainty.                          | `0.9` (High confidence), `0.6` (Low confidence)                       |
| `original_input`   | `Text`              | The raw user-provided string for future re-evaluation.                         | `"I think it was around July 1995"`                                   |

## Blog-Specific Frontmatter for Temporal Context

The specification is designed for a blog where a post's publication date and the date of a specific memory or event can be different. To accommodate this, the system will use a standardized frontmatter schema. This schema ensures a clear separation between a blog post's metadata and the temporal data of the event it describes, which is crucial for building a canonical timeline.

Blog platforms like Jekyll and Hugo use frontmatter to store metadata such as date and title. The proposed schema extends this with a custom field to store the canonical EDTF date.

The proposed frontmatter properties are:

- **`date`**: This standard property represents the blog post's publication date. It's a precise ISO 8601 string and should be used by the blog engine for its own purposes.
- **`lastmod` (optional)**: This field can be used to track the date a post was last modified.
- **`event_date` (custom)**: This is the core property for the memory-based timeline. This custom variable will store the canonical EDTF string that represents the event being described in the post.
- **`event_date_start` (computed)**: A hidden or system-generated field that stores the earliest possible date from `event_date` as a standard ISO 8601 date. This field is used as a primary key for sorting the canonical timeline.
- **`event_date_end` (computed)**: A hidden or system-generated field that stores the latest possible date from `event_date` as a standard ISO 8601 date. This field is used as a secondary key for sorting.

Here is an example of a blog post's frontmatter using the YAML format:

```yaml
---
title: "The Summer I Worked at the Video Store"
date: 2024-04-15T10:30:00-07:00
lastmod: 2024-04-15T10:30:00-07:00
event_date: 1995-06-XX/1995-08-XX
---
```