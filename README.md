# Revolver

- [Scheme](#scheme)
  - [Can I release quarterly and add the quarter in the version number ?](#can-i-release-quarterly-and-add-the-quarter-in-the-version-number)
- [API](#api)
  - [now](#now)
  - [from_iso](#fromiso)
- [Credits](#credits)

Revolver (short for *Revolution Versioning*) is a versioning scheme inspired by [CalDev]. It uses a date and time as versioning numbers but it uses the [French Republican Calendar] (also called the revolutionary calendar in France) for the date with the [Holocene Calendar] for the year, and the [Decimal time] for the time.

## Scheme

Revolver introduces a simple versioning convention :

```
YYYYY[.MM[.DD[-HMM]]]
```

* YYYYY - (12019, 12020, ...) - Year in the [Holocene Calendar], or the current year in the [Gregorian Calendar] plus 10 000
* MM - (01-12) - Month in the [French Republican Calendar]
* DD - (01-30) - Day in the [French Republican Calendar]
* H - (0-9) - Hour in [Decimal time]
* MM - (00-99) - Minutes in [Decimal Time]

The format allows flexible release cycles by omitting one or more part. For example, if you plan to release hourly, you may opt for the full `YYYYY.MM.DD-HMM` but if you plan to release monthy, you could opt for the much simpler `YYYYY.MM`.

### Can I release quarterly and add the quarter in the version number ?

What are you ? A [multi-million euros company] ? No, this versioning scheme does not plan to implement quarters in the version number.

## API

### now

Returns a version number corresponding to the current time in the format `YYYYY.MM.DD-HMM`.

### from_iso

Takes a string in the format of [ISO 8601]. Returns a version number in the format `YYYYY.MM.DD-HMM`.

## Credits

* The RevolVer API uses the [metric-time] library for Python
* The CSS theme for the front page is [Minist] by [Miguel Bartelsman]

[RevolVer] was created with 🤪 by [rodolpheh] - [GitHub]

[ISO 8601]: https://en.wikipedia.org/wiki/ISO_8601
[now]: https://rodolpheh.pythonanywhere.com/now
[CalDev]: https://caldev.org
[French Republican Calendar]: https://en.wikipedia.org/wiki/French_Republican_calendar
[Holocene Calendar]: https://en.wikipedia.org/wiki/Holocene_calendar
[Decimal time]: https://en.wikipedia.org/wiki/Decimal_time
[multi-million euros company]: https://www.3ds.com/
[Minist]: http://markedstyle.com/styles/minist
[Miguel Bartelsman]: http://markedstyle.com/authors/1642
[metric-time]: https://github.com/lakhanmankani/metric-time
[rodolpheh]: https://github.com/rodolpheh
[GitHub]: https://github.com/rodolpheh/revolver
[RevolVer]: https://rodolpheh.pythonanywhere.com/
