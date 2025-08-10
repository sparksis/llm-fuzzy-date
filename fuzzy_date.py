import edtf
import datetime
from functools import total_ordering
from edtf.parser.edtf_exceptions import EDTFParseException

def _struct_time_to_date(st):
    """Converts a time.struct_time to a datetime.date."""
    if st:
        return datetime.date(st.tm_year, st.tm_mon, st.tm_mday)
    return None

@total_ordering
class FuzzyDate:
    def __init__(self, user_input, confidence=1.0):
        self.original_input = user_input
        self.confidence_score = confidence

        try:
            self.edtf_obj = edtf.parser.parse_edtf(user_input)
            self.canonical_date = str(self.edtf_obj)
        except EDTFParseException as e:
            # For now, we'll re-raise the exception.
            # In the future, this is where the LLM parser would be called.
            raise ValueError(f"Could not parse '{user_input}' as an EDTF date.") from e

        self.sort_start_date = _struct_time_to_date(self.edtf_obj.lower_strict())
        self.sort_end_date = _struct_time_to_date(self.edtf_obj.upper_strict())

        # The edtf library doesn't seem to have a direct granularity attribute.
        # We can try to infer it, but for now, we'll leave it as None.
        self.granularity = None

    def __repr__(self):
        return f"FuzzyDate(original_input='{self.original_input}', canonical_date='{self.canonical_date}')"

    def __lt__(self, other):
        if not isinstance(other, FuzzyDate):
            return NotImplemented

        # Primary key: sort_start_date (ascending)
        if self.sort_start_date != other.sort_start_date:
            return self.sort_start_date < other.sort_start_date

        # Secondary key: sort_end_date (ascending)
        if self.sort_end_date != other.sort_end_date:
            return self.sort_end_date < other.sort_end_date

        # Tertiary key: confidence_score (descending)
        # We compare self > other to get descending order.
        return self.confidence_score > other.confidence_score

    def __eq__(self, other):
        if not isinstance(other, FuzzyDate):
            return NotImplemented
        return (self.sort_start_date == other.sort_start_date and
                self.sort_end_date == other.sort_end_date and
                self.confidence_score == other.confidence_score)

def parse_user_input(user_query):
    """
    Parses a user's temporal query into a FuzzyDate object.

    In the future, this function will incorporate the LLM-based parsing
    for ambiguous queries.
    """
    # For now, we assume a confidence of 1.0 for any parsable date.
    # The LLM would provide a different confidence score.
    return FuzzyDate(user_query)

def get_timeline(fuzzy_dates):
    """
    Sorts a list of FuzzyDate objects according to the specification.
    """
    return sorted(fuzzy_dates)
