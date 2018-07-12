---
layout: default
title: "Datetime Range"
version: 1.0
---

# <a href="#datetime-range-introduction" id="datetime-range-introduction" class="headerlink"></a> Datetime Range Introduction

Some APIs need the ability to be able to return data based on a time range. For example, handling reporting or scheduling data.

# <a href="#datetime-range-conformance" id="datetime-range-conformance" class="headerlink"></a> Conformance

The keywords may, must, must not, recommended, should, and should not are to be interpreted as described in [[RFC2119](http://tools.ietf.org/html/rfc2119)].

# <a href="#datetime-range-conventions" id="datetime-range-conventions" class="headerlink"></a> Conventions

## <a href="#datetime-range-conventions-uri" id="datetime-range-conventions-uri" class="headerlink"></a> URI

Anywhere a **URI** is specified, it **MUST** follow the rules defined in the [Hyperion]({{site.url}}/versions/{{site.latest_version}}) specification.

## <a href="#datetime-range-conventions-query-params" id="datetime-range-conventions-query-params" class="headerlink"></a> Querystring Parameters

APIs **MAY** have the following querystring parameters:

* `start` accepts a string value with the start date as [absolute](#datetime-range-absolute-datetime) or [relative](#datetime-range-datetime) datetime format.

* `end` accepts a string value with the end date as [absolute](#datetime-range-absolute-datetime) or [relative](#datetime-range-datetime) datetime format.

If _no_ query parameters are specified, the API **MUST** return a response with a default value for both fields. 

## <a href="#datetime-range-reflected-date" id="datetime-range-reflected-date" class="headerlink"></a> Reflected date

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

# <a href="#datetime-range-datetime" id="datetime-range-datetime" class="headerlink"></a> Relative Datetime Format

APIs **MUST** accept the `now` keyword with optional modifiers when handling relative datetime.

The following modifiers and time ranges **MAY** be used in conjunction with the `now` keyword following the format `now[+|-][time_integer][yMwdms]`. 

* `+` add time range to `now` datetime keyword.

* `-` subtract time range from `now` datetime keyword.

* `[time_integer]` time integer value.

* `[y]`ears time range to add/subtract to `now` datetime keyword.

* `[M]`onths time range to add/subtract to `now` datetime keyword.

* `[w]`eeks time range to add/subtract to `now` datetime keyword.

* `[d]`ays time range to add/subtract to `now` datetime keyword.

* `[m]`inutes time range to add/subtract to `now` datetime keyword.

* `[s]`econds time range to add/subtract to `now` datetime keyword.


Example of _datetime ranges_.

| Requested         | Current Date      | Result          |  
| ----------------- | ----------------- | --------------- |
| now+1d            | 2018-06-18        | 2018-06-19      |
| now-1M            | 2018-06-18        | 2018-05-18      |
| now+1w            | 2018-06-18        | 2018-06-25      |


# <a href="#datetime-range-absolute-datetime" id="datetime-range-absolute-datetime" class="headerlink"></a> Absolute Datetime Format

APIs **MUST** accept absolute datetime following [ISO 8601](https://www.w3.org/TR/NOTE-datetime) standard as defined in the [Hyperion]({{site.url}}/versions/{{site.latest_version}}) specification.

# <a href="#datetime-range-datetime-example" id="datetime-range-datetime-example" class="headerlink"></a> Example Usage

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

This example gets time series data using a [relative datetime](#datetime-range-datetime) of _one month ago_ for the `start` querystring parameter.

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

This example gets time series data using a [relative datetime](#datetime-range-datetime) of _one week ago_ for `start` and one day ago for `end` querystring parameters.

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

This example gets time series data using an [absolute datetime](#datetime-range-absolute-datetime) for `start` and [relative datetime](#datetime-range-datetime) of _one day ago_ for `end` querystring parameters.

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