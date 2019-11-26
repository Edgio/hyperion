---
layout: default
title: "Time Series"
version: 1.0
---

# <a href="#time-series-introduction" id="time-series-introduction" class="headerlink"></a> Time Series Introduction

Some APIs need the ability to be able to return data based on a time range. For example, handling reporting or scheduling data.

# <a href="#time-series-conformance" id="time-series-conformance" class="headerlink"></a> Conformance

The keywords may, must, must not, recommended, should, and should not are to be interpreted as described in [[RFC2119](http://tools.ietf.org/html/rfc2119)].

# <a href="#time-series-conventions" id="time-series-conventions" class="headerlink"></a> Conventions

## <a href="#time-series-conventions-uri" id="time-series-conventions-uri" class="headerlink"></a> URI

Anywhere a **URI** is specified, it **MUST** follow the rules defined in the [Hyperion]({{site.url}}/versions/{{site.latest_version}}) specification.

## <a href="#time-series-conventions-query-params" id="time-series-conventions-query-params" class="headerlink"></a> Querystring Parameters

APIs **MAY** have the following querystring parameters:

* `start` accepts a string value with the start date as [absolute](#time-series-absolute-datetime) or [relative](#time-series-datetime) datetime format.

* `end` accepts a string value with the end date as [absolute](#time-series-absolute-datetime) or [relative](#time-series-datetime) datetime format.

If _no_ query parameters are specified, the API **MUST** return a response with a default value for both fields. 

## <a href="#time-series-reflected-date" id="time-series-reflected-date" class="headerlink"></a> Reflected date

To ensure that the client's request was properly executed, APIs **MUST** return the `start` and `end` datetimes as reflected values in the response body.

APIs **MUST** return the datetime value following [ISO 8601](https://www.w3.org/TR/NOTE-datetime) standard as defined in the [Hyperion]({{site.url}}/versions/{{site.latest_version}}) specification.

Example of the `start` and `end` time range _reflected_ in the response body.

`https://api.vdms.io/analytics/v1/time-series?start=now-1M`

```json
{
    "@id": "/analytics/v1/time-series",
    "@type": "TimeSeries",
    "start": "2018-05-18T21:43:25Z",
    "end": "2018-06-18T21:43:25Z",
    ...
}
```

# <a href="#time-series-datetime" id="time-series-datetime" class="headerlink"></a> Relative Datetime Format

APIs **MUST** accept a datetime keyword with optional modifiers when handling relative datetime.

The following modifiers and time ranges **MAY** be used in conjunction with a datetime keyword following the format `(now|start_day|start_week|start_month|start_year)[+|-][time_integer][yMwdms]`. 

* `now` uses the current datetime.

* `start_day` uses the midnight of today.

* `start_week` uses the midnight of Monday of the current week.

* `start_month` uses the midnight of the fist day of the current month.

* `start_year` uses the midnight of the first day of the current year.

* `+` add time range to a datetime keyword.

* `-` subtract time range from a datetime keyword.

* `[time_integer]` time integer value.

* `[y]`ears time range to add/subtract to a datetime keyword.

* `[M]`onths time range to add/subtract to a datetime keyword. 

* `[w]`eeks time range to add/subtract to a datetime keyword.

* `[d]`ays time range to add/subtract to a datetime keyword.

* `[m]`inutes time range to add/subtract to a datetime keyword.

* `[s]`econds time range to add/subtract to a datetime keyword.

> Note: If a requested datetime falls on an invalid date when using month time range `[M]`, APIs must add/subtract days until a valid datetime is found.

Example of _datetime ranges_.

| Requested         | Current Date      | Result          | Notes 
| ----------------- | ----------------- | --------------- | --------------- 
| now+1d            | 2018-06-18        | 2018-06-19      | 
| now+1w            | 2018-06-18        | 2018-06-25      | 
| now-1M            | 2018-05-31        | 2018-04-30      | Since April does not have 31 days, we subtract a day until we reached a valid date
| now-1M            | 2018-06-18        | 2018-05-18      |

# <a href="#time-series-absolute-datetime" id="time-series-absolute-datetime" class="headerlink"></a> Absolute Datetime Format

APIs **MUST** accept absolute datetime following [ISO 8601](https://www.w3.org/TR/NOTE-datetime) standard as defined in the [Hyperion]({{site.url}}/versions/{{site.latest_version}}) specification.

# <a href="#time-series-datetime-example" id="time-series-datetime-example" class="headerlink"></a> Example Usage

> Note: In the following examples, `now` represents `2018-06-18T00:00:00Z`

This example gets time series data using API default values. Notice how the `start` and `end` querystring parameters were not supplied.

`https://api.vdms.io/analytics/v1/time-series`

```json
{
    "@id": "/analytics/v1/time-series",
    "@type": "TimeSeries",
    "start": "2018-06-11T21:43:25Z",
    "end": "2018-06-18T21:43:25Z",
    ...
}
```

This example gets time series data using a [relative datetime](#time-series-datetime) of _one month ago_ for the `start` querystring parameter.

`https://api.vdms.io/analytics/v1/time-series?start=now-1M`

```json
{
    "@id": "analytics/v1/time-series?start=now-1M",
    "@type": "TimeSeries",
    "start": "2018-05-18T21:43:25Z",
    "end": "2018-06-18T21:43:25Z",
    ...
}
```

This example gets time series data using a [relative datetime](#time-series-datetime) of _one week ago_ for `start` and one day ago for `end` querystring parameters.

`https://api.vdms.io/analytics/v1/time-series?start=now-1w&end=now-1d`

```json
{
    "@id": "analytics/v1/time-series?start=now-1w&end=now-1d",
    "@type": "TimeSeries",
    "start": "2018-06-11T21:43:25Z",
    "end": "2018-06-17T21:43:25Z",
    ...
}
```

This example gets time series data using an [absolute datetime](#time-series-absolute-datetime) for `start` and [relative datetime](#time-series-datetime) of _one day ago_ for `end` querystring parameters.

`https://api.vdms.io/analytics/v1/time-series?start=2018-05-18T21:43:25Z&end=now-1d`

```json
{
    "@id": "analytics/v1/time-series?start=2018-05-18T21:43:25Z&end=now-1d",
    "@type": "TimeSeries",
    "start": "2018-05-18T21:43:25Z",
    "end": "2018-06-17T21:43:25Z",
    ...
}
```
