# Agent Instructions for Blog Timeline

This document provides instructions for an AI agent interacting with the blog's temporal data features.

## Core Task

The agent's primary role is to assist users in creating blog posts with accurate temporal metadata. This involves parsing user input for dates (which may be fuzzy or represent intervals) and populating the post's frontmatter correctly.

## Blog Frontmatter Schema

The following frontmatter fields are used to manage the blog's two timelines (publication date vs. event date).

*   **`date`**: The post's publication date in ISO 8601 format. This is for the standard blog timeline.
*   **`lastmod` (optional)**: The date the post was last modified (ISO 8601).
*   **`event_date` (custom)**: The canonical date of the event described in the post. This MUST be a valid **[Extended Date/Time Format (EDTF)](EDTF_SPECIFICATION.md)** string. This field is the source for the memory timeline.
    *   *Example*: A post about the 90s would have `event_date: 199X`.
    *   *Example*: A post about the summer of 1995 could have `event_date: 1995-06/1995-08`.
*   **`event_date_start` (computed)**: The earliest possible date from `event_date` (ISO 8601). This is a system-generated field used for sorting.
*   **`event_date_end` (computed)**: The latest possible date from `event_date` (ISO 8601). This is a system-generated field used for sorting.

## Agent's Responsibility

The agent is responsible for populating the `event_date` field. The system will handle the computation of `event_date_start` and `event_date_end`. The agent should use its natural language understanding capabilities to convert user queries (e.g., "the late 80s", "summer of '95") into the correct EDTF string for the `event_date` field.
