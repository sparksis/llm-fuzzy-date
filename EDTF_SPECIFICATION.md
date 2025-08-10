# Extended Date/Time Format (EDTF) Specification

**February 4, 2019**

## Introduction

The Extended Date/Time Format (EDTF) was created by the Library of Congress with the participation and support of the bibliographic community as well as communities with related interests. It defines features to be supported in a date/time string, features considered useful for a wide variety of applications.

See Background. Note, in particular, a draft specification was issued in 2012. The full functionality of the draft specification is retained in this specification, however several syntactic changes were necessary, to satisfy international requirements.

## Differences

This specification differs from the earlier draft as follows:
* the unspecified date character (formerly lower case ‘u’) is superseded by the character (upper case) 'X';
* Masked precision is eliminated;
* the uncertain and approximate qualifiers, '?' and '~',  when applied together, are combined into a single qualifier character '%';
* “qualification from the left” is introduced and replaces the grouping mechanism using parentheses;
* the extended interval syntax  keywords 'unknown' and 'open' have been replaced with null and the double-dot notation ['..'] respectively;
* the year prefix 'y' and the exponential indicator 'e', both previously lowercase, are now 'Y' and 'E' (uppercase); and
* the significant digit indicator 'p' is now 'S' (uppercase).

## Compliance

Three conformance levels are defined: level 0, level 1, and level 2. Level 0 specifies features of ISO 8601-1; Levels 1 and 2 specify features described ISO 8601-2. An implementation must support all of the features listed for Level 0. The vendor must state one of the following levels of support:
* Level 0 is supported.
* Level 0 is supported, and in addition the following features of levels 1 and 2 are supported (list features).
* Level 1 is supported.
* Level 1 is supported, and in addition the following features of level 2 are supported (list features).
* Level 2 is supported.

Two communication parties that agree to operate according to this specification must suppress, during their communication, any features of ISO 8601-1 that are not included in level 0.

## Extended format

EDTF requires “extended format” as defined in 8601: hyphen between calendar components and colon between clock components (e.g. 2005-09-24T10:00:00). “Basic format" as defined in ISO 8601, which omits separators (e.g. 20050924T100000), is not permitted.

## Level 0

Level 0 requires support for the following features.

### Date

* complete representation: [year][“-”][month][“-”][day]
  Example 1 ‘1985-04-12’ refers to the calendar date 1985 April 12th with day precision.
* reduced precision for year and month: [year][“-”][month]
  Example 2 ‘1985-04’ refers to the calendar month 1985 April with month precision.
* reduced precision for year: [year]
  Example 3 ‘1985’ refers to the calendar year 1985 with year precision.

### Date and Time

* [date][“T”][time]
  Complete representations for calendar date and (local) time of day
  Example 1 ‘1985-04-12T23:20:30’ refers to the date 1985 April 12th at 23:20:30 local time.
* [dateI][“T”][time][“Z”]
  Complete representations for calendar date and UTC time of day
  Example 2 ‘1985-04-12T23:20:30Z’ refers to the date 1985 April 12th at 23:20:30 UTC time.
* [dateI][“T”][time][shiftHour]
  Date and time with timeshift in hours (only)
  Example 3 ‘1985-04-12T23:20:30-04’ refers to the date 1985 April 12th time of day 23:20:30 with time shift of 4 hours behind UTC.
* [dateI][“T”][time][shiftHourMinute]
  Date and time with timeshift in hours and minutes
  Example 4 ‘1985-04-12T23:20:30+04:30’ refers to the date 1985 April 12th, time of day 23:20:30 with time shift of 4 hours and 30 minutes ahead of UTC.

### Time Interval

EDTF Level 0 adopts representations of a time interval where both the start and end are dates: start and end date only; that is, both start and duration, and duration and end, are excluded. Time of day is excluded.
* Example 1 ‘1964/2008’ is a time interval with calendar year precision, beginning sometime in 1964 and ending sometime in 2008.
* Example 2 ‘2004-06/2006-08’ is a time interval with calendar month precision, beginning sometime in June 2004 and ending sometime in August of 2006.
* Example 3 ‘2004-02-01/2005-02-08’ is a time interval with calendar day precision, beginning sometime on February 1, 2004 and ending sometime on February 8, 2005.
* Example 4 ‘2004-02-01/2005-02’ is a time interval beginning sometime on February 1, 2004 and ending sometime in February 2005. Since the start endpoint precision (day) is different than that of the end endpoint (month) the precision of the time interval at large is undefined.
* Example 5 ‘2004-02-01/2005’ is a time interval beginning sometime on February 1, 2004 and ending sometime in 2005. The start endpoint has calendar day precision and the end endpoint has calendar year precision. Similar to the previous example, the precision of the time interval at large is undefined.
* Example 6 ‘2005/2006-02’ is a time interval beginning sometime in 2005 and ending sometime in February 2006.

## Level 1

Level 1 of this specification requires support for Level 0 as well as the following features:

### Letter-prefixed calendar year

'Y' may be used at the beginning of the date string to signify that the date is a year, when (and only when) the year exceeds four digits, i.e. for years later than 9999 or earlier than -9999.
* Example 1 ‘Y170000002’ is the year 170000002
* Example 2 ‘Y-170000002’ is the year -170000002

### Seasons

The values 21, 22, 23, 24 may be used used to signify ' Spring', 'Summer', 'Autumn', 'Winter', respectively, in place of a month value (01 through 12) for a year-and-month format string.
* Example ‘2001-21’ Spring, 2001

### Qualification of a date (complete)

The characters '?', '~' and '%' are used to mean "uncertain", "approximate", and "uncertain" as well as "approximate", respectively. These characters may occur only at the end of the date string and apply to the entire date.
* Example 1 ‘1984?’ year uncertain (possibly the year 1984, but not definitely)
* Example 2 ‘2004-06~’' year-month approximate
* Example 3 ‘2004-06-11%’ entire date (year-month-day) uncertain and approximate

### Unspecified digit(s) from the right

The character 'X' may be used in place of one or more rightmost digits to indicate that the value of that digit is unspecified, for the following cases:
1. A year with one or two (rightmost) unspecified digits in a year-only expression (year precision)
   Example 1 ‘201X’
   Example 2 ‘20XX’
2. Year specified, month unspecified in a year-month expression (month precision)
   Example 3 ‘2004-XX’
3. Year and month specified, day unspecified in a year-month-day expression (day precision)
   Example 4 ‘1985-04-XX’
4. Year specified, day and month unspecified in a year-month-day expression (day precision)
   Example 5 ‘1985-XX-XX’

### Extended Interval (L1)
1. A null string may be used for the start or end date when it is unknown.
2. Double-dot (“..”) may be used when either the start or end date is not specified, either because there is none or for any other reason.
3. A modifier may appear at the end of the date to indicate "uncertain" and/or "approximate"

### Open end time interval
* Example 1 ‘1985-04-12/..’ interval starting at 1985 April 12th with day precision; end open
* Example 2 ‘1985-04/..’ interval starting at 1985 April with month precision; end open
* Example 3 ‘1985/..’ interval starting at year 1985 with year precision; end open

### Open start time interval
* Example 4 ‘../1985-04-12’ interval with open start; ending 1985 April 12th with day precision
* Example 5 ‘../1985-04’ interval with open start; ending 1985 April with month precision
* Example 6 ‘../1985’ interval with open start; ending at year 1985 with year precision

### Time interval with unknown end
* Example 7 ‘1985-04-12/’ interval starting 1985 April 12th with day precision; end unknown
* Example 8 ‘1985-04/’ interval starting 1985 April with month precision; end unknown
* Example 9 ‘1985/’ interval starting year 1985 with year precision; end unknown

### Time interval with unknown start
* Example 10 ‘/1985-04-12’ interval with unknown start; ending 1985 April 12th with day precision
* Example 11 ‘/1985-04’ interval with unknown start; ending 1985 April with month precision
* Example 12 ‘/1985’ interval with unknown start; ending year 1985 with year precision

### Negative calendar year

* Example 1 ‘-1985’

## Level 2

Level 2 requires support for Level 1 as well as the following features:

### Exponential year

'Y' at the beginning of the string (which indicates "year", as in level 1) may be followed by an integer, followed by 'E' followed by a positive integer. This signifies "times 10 to the power of". Thus 17E8 means "17 times 10 to the eighth power".
* Example ‘Y-17E7’ the calendar year -17*10 to the seventh power= -170000000

### Significant digits

A year (expressed in any of the three allowable forms: four-digit, 'Y' prefix, or exponential) may be followed by 'S', followed by a positive integer indicating the number of significant digits.
* Example 1 ‘1950S2’ some year between 1900 and 1999, estimated to be 1950
* Example 2 ‘Y171010000S3’ some year between 171000000 and 171999999 estimated to be 171010000
* Example 3 ‘Y3388E2S3’ some year between 338000 and 338999, estimated to be 338800.

### Sub-year groupings

Level 2 extends the season feature of Level 1 to include the following sub-year groupings.

21 Spring (independent of location)
22 Summer (independent of location)
23 Autumn (independent of location)
24 Winter (independent of location)
25 Spring - Northern Hemisphere
26 Summer - Northern Hemisphere
27 Autumn - Northern Hemisphere
28 Winter - Northern Hemisphere
29 Spring - Southern Hemisphere
30 Summer - Southern Hemisphere
31 Autumn - Southern Hemisphere
32 Winter - Southern Hemisphere
33 Quarter 1 (3 months in duration)
34 Quarter 2 (3 months in duration)
35 Quarter 3 (3 months in duration)
36 Quarter 4 (3 months in duration)
37 Quadrimester 1 (4 months in duration)
38 Quadrimester 2 (4 months in duration)
39 Quadrimester 3 (4 months in duration)
40 Semestral 1 (6 months in duration)
41 Semestral 2 (6 months in duration)
* Example ‘2001-34’ second quarter of 2001

### Set representation

1. Square brackets wrap a single-choice list (select one member).
2. Curly brackets wrap an inclusive list (all members included).
3. Members of the set are separated by commas.
4. No spaces are allowed, anywhere within the expression.
5. Double-dots indicates all the values between the two values it separates, inclusive.
6. Double-dot at the beginning or end of the list means "on or before" or "on or after" respectively.
7. Elements immediately preceeding and/or following as well as the elements represented by a double-dot, all have the same precision. Otherwise, different elements may have different precisions

### One of a set
* Example 1 ‘[1667,1668,1670..1672]’ One of the years 1667, 1668, 1670, 1671, 1672
* Example 2 ‘[..1760-12-03]’ December 3, 1760; or some earlier date
* Example 3 ‘[1760-12..]’ December 1760, or some later month
* Example 4 ‘[1760-01,1760-02,1760-12..]’ January or February of 1760 or December 1760 or some later month
* Example 5 ‘[1667,1760-12]’ Either the year 1667 or the month December of 1760.
* Example 6 ‘[..1984]’ The year 1984 or an earlier year

### All Members
* Example 7 ‘{1667,1668,1670..1672}’ All of the years 1667, 1668, 1670, 1671, 1672
* Example 8 ‘{1960,1961-12}’ The year 1960 and the month December of 1961.
* Example 9 ‘{..1984}’ The year 1984 and all earlier years

### Qualification

#### Group Qualification

A qualification character to the immediate right of a component applies to that component as well as to all components to the left.
* Example 1 ‘2004-06-11%’ year, month, and day uncertain and approximate
* Example 2 ‘2004-06~-11’ year and month approximate
* Example 3 ‘2004?-06-11’ year uncertain

#### Qualification of Individual Component

A qualification character to the immediate left of a component applies to that component only.
* Example 4 ‘?2004-06-~11’ year uncertain; month known; day approximate
* Example 5 ‘2004-%06-11’ month uncertain and approximate; year and day known

### Unspecified Digit

For level 2 the unspecified digit, 'X', may occur anywhere within a component.
* Example 1 ‘156X-12-25’ December 25 sometime during the 1560s
* Example 2 ‘15XX-12-25’ December 25 sometime during the 1500s
* Example 3 ‘XXXX-12-XX’ Some day in December in some year
* Example 4 '1XXX-XX’ Some month during the 1000s
* Example 5 ‘1XXX-12’ Some December during the 1000s
* Example 6 ‘1984-1X’ October, November, or December 1984

### Interval

For Level 2 portions of a date within an interval may be designated as approximate, uncertain, or unspecified.
* Example 1 ‘2004-06-~01/2004-06-~20’ An interval in June 2004 beginning approximately the first and ending approximately the 20th
* Example 2 ‘2004-06-XX/2004-07-03’ An interval beginning on an unspecified day in June 2004 and ending July 3.
