---
layout: default
title: "Relative Time"
version: 1.0
---

# <a href="#rel-time-introduction" id="rel-time-introduction" class="headerlink"></a> Relative Time Introduction

Some APIs need to provide the ability to query data by using a relative datetime range. Some use cases are when returning analytics or report data. 

# <a href="#rel-time-conformance" id="rel-time-conformance" class="headerlink"></a> Conformance

The key words may, must, must not, recommended, should, and should not are to be interpreted as described in [[RFC2119](http://tools.ietf.org/html/rfc2119)].

# <a href="#rel-time-conventions" id="rel-time-conventions" class="headerlink"></a> Conventions

## <a href="#rel-time-conventions-uri" id="rel-time-conventions-uri" class="headerlink"></a> URI

Anywhere a **URI** is specified, it **MUST** follow the rules defined in the [Hyperion]({{site.url}}/versions/{{site.latest_version}}) specification.

## <a href="#rel-time-conventions-query-params" id="rel-time-conventions-query-params" class="headerlink"></a> Query Params

APIs **MAY** have the following query string parameters:

* `start` accepts a string value with the start date as datetime format.

* `end` accepts a string value with the end date as datetime format.

If _no_ query parameters are specified, the API **MUST** return a response with a default value for both fields.

## <a href="#rel-time-reflected-date" id="rel-time-reflected-date" class="headerlink"></a> Reflected date

To ensure that the client's request was properly executed, APIs **MUST** return the `start` and `end` datetimes as reflected values in the response body.

APIs **MUST** return the datetime value following [ISO 8601](https://www.w3.org/TR/NOTE-datetime) standard as defined in the [Hyperion]({{site.url}}/versions/{{site.latest_version}}) specification.

> Note: The actual properties to store those values can be API specific.

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

# <a href="#rel-time-datetime" id="rel-time-datetime" class="headerlink"></a> Datetime Format

Accepted values for `start` and `end` query string parameters **MUST** use the `now` keyword with optional modifiers.

The following modifiers and time ranges **MAY** be used in conjunction with the `now` keyword following the format `now[+|-][time_integer][yMwdms]`. 

* `+` add time range to `now` datetime keyword.

* `-` subtract time range from `now` datetime keyword.

* `[time_integer]` time integer value.

* `[y]`ears time range to add to `now` datetime keyword.

* `[M]`onths time range to add to `now` datetime keyword.

* `[w]`eeks time range to add to `now` datetime keyword.

* `[d]`ays time range to add to `now` datetime keyword.

* `[m]`inutes time range to add to `now` datetime keyword.

* `[s]`econds time range to add to `now` datetime keyword.

Example of _time ranges_.

| Requested         | Current Date      | Result          |  
| ----------------- | ----------------- | --------------- |
| now+1d            | 2018-06-18        | 2018-06-19      |
| now-1M            | 2018-06-18        | 2018-05-18      |
| now+1w            | 2018-06-18        | 2018-06-25      |


## <a href="#rel-time-datetime-example" id="rel-time-datetime-example" class="headerlink"></a> Example Usage

Get time series data using default values specified by API (1 week for this example)

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

Get time series data starting one month ago

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

Get time series data starting one week and ending one day before

`https://api.vdms.io/analytics/v1/time-series?start=now-1w&end=now-1d`

```json
{
    "@id": "/analytics/v1/time-series",
    "@type": "TimeSeries",
    "start": "2018-06-11T21:43:25Z",
    "end": "2018-06-17T21:43:25Z",
    ...
}
```