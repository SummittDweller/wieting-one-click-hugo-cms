---
title: Example Date Strings
draft: false
author: Mackenzie McFate
date: 2021-06-09T13:27:32-05:00
socialshare: false
weight: 91
---

Dates and times for Wieting events are specified using descriptive strings that are parsed using the [kvh/recurrent](https://github.com/kvh/recurrent#recurring-events) _Python3_ package.  Therefore, event `dates` should be specified using strings like those shown in the sections below.  First, some "special" rules.

## Special Rules

By default, datetime parsers like the one the Wieting uses are NOT "inclusive", so if you specify a string like `8:30 am daily from jul 26 2021 thru jul 29 2021` you will generate only 3 events on July 26, 27 and 28, not four! There will be no event on July 29 because the start of that day, coinciding with 12:00:01 AM (1 second after midnight), occurs before 8:30 AM on the same day.  While that makes sense, it's not how most people think terms like `thru`, `to`, and `until` should work.

So, when you specify a discrete end date/time for a Wieting event, we automatically add 24 hours for determination of a limiting date.  That means the specification we used above, `8:30 am daily from jul 26 2021 thru jul 29 2021`, will generate the following discrete event date/times:

  - Monday, July 26, 2021 @ 8:30 AM,
  - Tuesday, July 27, 2021 @ 8:30 AM,
  - Wednesday, July 28, 2021 @ 8:30 AM, ...and...
  - Thursday, July 29, 2021 @ 8:30 AM

Notice that rules are generally NOT case-sensitive, and any reasonable names or abbreviations for days or months can be used.

### Suggested Strings

These are strings that have already been successfully used in the past.

  - 6:30 pm on june 9 2021
  - 7:00 pm on jun 13 2021
  - 1pm daily from June 14 2021 thru June 16 2021
  - 6:30 pm monthly every 3rd wednesday from may 1 2021 to december 31 2021
  - 8:30 am daily from jul 26 2021 thru jul 29 2021
  - 6:00 pm every monday tuesday thursday from sep 13 2021 thru oct 14 2021

### Discrete Date/Time Forms

  - next tuesday
  - tomorrow
  - in an hour
  - in 15 mins
  - Mar 4th at 9am
  - 3rd Thu in Apr at 10 o'clock
  - 40th day of 2020

### Recurring Date/Time Forms

  - on weekdays
  - every fourth of the month from jan 1 2010 to dec 25th 2020
  - each thurs until next month
  - once a year on the fourth thursday in november
  - tuesdays and thursdays at 3:15
  - wednesdays at 9 o'clock
  - fridays at 11am
  - daily except in June
  - daily except on June 23rd and July 4th
  - every monday except each 2nd monday in March
  - fridays twice
  - fridays 3x
  - every other friday for 5 times
  - every 3 fridays from november until february
  - fridays starting in may for 10 occurrences
  - tuesdays for the next six weeks
  - every Mon-Wed for the next 2 months
  - every Mon thru Wed for the next year
  - every other Fri for the next three years
  - monthly on the first and last instance of wed and fri
  - every Tue and Fri in week 14
  - every year on Dec 25

### Messy Strings - These DO NOT Work!

  - Please schedule the meeting for every other tuesday at noon
  - Set an alarm for next tuesday at 11pm
