---
layout: default
title: "Version - 1.0"
version: 1.0
---

# <a href="#introduction" id="introduction" class="headerlink"></a> Introduction

Hyperion is a lightweight specification for RESTful JSON APIs.  It endeavors to provide guidance and convention for the variety of decisions API-writers need to make during their development.  Hyperion also takes some inspiration from [JSON-LD](https://json-ld.org/spec/latest/json-ld) as a nod to [hypermedia](https://en.wikipedia.org/wiki/HATEOAS), but with emphasis on low-overhead to make it easier for API-writers to adopt.

# <a href="#conformance" id="conformance" class="headerlink"></a> Conformance

The keywords may, must, must not, recommended, should, and should not are to be interpreted as described in [[RFC2119](http://tools.ietf.org/html/rfc2119)].

# <a href="#conventions" id="conventions" class="headerlink"></a> Conventions

## <a href="#conventions-content-negotiation" id="conventions-content-negotiation" class="headerlink"></a> Content Negotiation

Clients **MUST** send all JSON data in request documents with the header
`Content-Type: application/json`.

Servers **MUST** send all JSON data in response documents with the header
`Content-Type: application/json`.

## <a href="#conventions-uri" id="conventions-uri" class="headerlink"></a> URI

Anywhere a **URI** is specified, it must adhere to the following rules:

* **MUST** be a valid URI that is active and responds to requests.
* **MAY** contain all query string parameters used to retrieve that resource.
* **MUST** be relative path as it's sometimes difficult for servers to construct an absolute path reliably.
* **MUST** use `-` or hyphen as delimiter for words within the path.
* **MUST** use `snake_case` for query string parameters.
* **SHOULD** use lowercase characters for words within the path basename (up to the last occurrence of '/').  This is to account for various-case `id`s, such as those found in URL shorteners. E.g. `https://goo.gl/VwUrzz`

### <a href="#conventions-sub-service" id="urls" class="headerlink"></a> Sub-service Path

APIs **MUST** provide a sub-service path in the URI as a way to create a namespace for your endpoints.

A `sub-service` URI path **MUST** have the following:

* First path after the host following [URI](#conventions-uri) conventions. `https://api.company.com/`**`sub-service`**`/`
* Provide support for [versioning](#conventions-versioning). `https://api.company.com/`**`sub-service`**`/v`**`Major[.Minor]`**`/`

These two rules promote clear differentiation of sub-services and versions, allowing independent development.

### <a href="#conventions-http-status-codes" id="conventions-http-status-codes" class="headerlink"></a> HTTP Status Codes

APIs **MUST** respond to requests with an Http Status Code that is found in the following list:

status code | description | [error code](#document-components-error-codes) | notes
--- | --- | --- | ---
200 | OK | | The request has successfully completed processing
201 | Created | | Resource has been created and processed successfully
202 | Accepted | | The request has been accepted for processing, but the processing has not been completed.
204 | No content | | (for deletions only) The deletion process has completed
400 | Bad Request | invalid_input | The request has one or more errors and cannot be processed
401 | Unauthorized | unauthorized | The request did not include a required authentication component
403 | Forbidden | forbidden | The request has failed authorization checks
404 | Not found | not_found | Resource not found
405 | Method not allowed | method_not_allowed | The http method was not valid at the specified URI
409 | Conflict | invalid_operation | The request could not be completed due to a conflict with the current state of the target resource
413 | Payload Too Large | payload_too_large | Request payload is too large and the server will not process it
429 | Too many Requests | rate_limit_reached | Too many requests have been received in a given amount of time
500 | Internal server error | internal_error | The server cannot process the request for an unknown reason
502 | Bad gateway | bad_gateway | The gateway server or proxy received an invalid response from upstream server while fulfilling a request
503 | Service Unavailable | service_unavailable | The server is currently unable to handle requests temporarily due to maintenance or resource exhaustion from high load
504 | Gateway timeout | gateway_timeout | The gateway server or proxy failed to receive a response from upstream server while fulfilling a request


### <a href="#conventions-versioning" id="urls" class="headerlink"></a> Versioning 

APIs **MUST** provide versioning in the URI path, following the sub-service path.

**MUST** increase either `Major` or `Minor` in the version path whenever a breaking change is introduced. `/vMajor[.Minor]`
    
* **SHOULD NOT** increase version if adding new endpoints or fields.

* **SHOULD** increase version if changing behavior for an existing API endpoint:

    * Such as modifying the HTTP status code
    * Changing data format
    * Changing the resource, ie. removing or renaming fields
    * Anything that would violate the [Principal of Least Astonishment](https://en.wikipedia.org/wiki/Principle_of_least_astonishment)


`https://api.company.com/sub-service/v1`

`https://api.company.com/sub-service/v1.1`

## <a href="#conventions-casing" id="conventions-casing" class="headerlink"></a> Naming Conventions

* **MUST** use `PascalCase` and be singular to represent a `@type`.
* **MUST** use `snake_case` to represent a property.
* **MUST NOT** use `@` keyword for custom properties as it is reserved.


## <a href="#date" id="date" class="headerlink"></a> Date Handling

All dates **MUST** be represented as string values following the [ISO 8601](https://www.w3.org/TR/NOTE-datetime) standard.

All dates **MUST** follow [ISO 8601](https://www.w3.org/TR/NOTE-datetime) standard of `YYYY-MM-DD`.

An example of _date_ only value.

```json
{
    "@id": "/users/1",
    "@type": "User",
    "given_name": "Hubert",
    "family_name": "Farnsworth",
    "date_of_birth": "1975-11-30"
}
```

All datetime **MUST** be `UTC` following the [ISO 8601](https://www.w3.org/TR/NOTE-datetime) standard of `YYYY-MM-DDThh:mm:ss.sZ`.

> Note: The `Z` designator at the end is what expresses a datetime as UTC. It will be treated as local datetime without it.

An example of UTC _datetime_ value.

```json
{
    "@id": "/users/1",
    "@type": "User",
    "given_name": "Hubert",
    "family_name": "Farnsworth",
    "date_of_birth": "1975-11-30",
    "created_at": "2017-11-30T21:43:25Z"
}
```

## <a href="#time-series" id="time-series" class="headerlink"></a> Time Series

APIs that need to implement time series functionality **MUST** refer to specifications defined in the [time series]({{site.url}}/versions/{{site.latest_version}}/time-series) section.

An example of _time series_ using relative time.

`https://api.vdms.io/analytics/v1/time-series?start=now-1M&end=now`

```json
{
    "@id": "/analytics/v1/time-series?start=now-1M&end=now",
    "@type": "TimeSeries",
    "start": "2018-05-18T21:43:25Z",
    "end": "2018-06-18T21:43:25Z",
    ...
}
```


# <a href="#keywords" id="keywords" class="headerlink"></a> Keywords

Hyperion specifies a few keywords as part of the core specification:

* `@id`: Used to specify the [URI](#conventions-uri) for the resource. Can be used by clients to navigate back to that specific resource. This **SHOULD NOT** be confused as the identifier for the instance of that resource.

    Example of the difference between `@id` and a similar property like `id`:

```json
{
    "@id": "/connect/userinfo/1",
    "@type": "UserInfo",
    "id": 1,
    "given_name": "Hubert",
    "family_name": "Farnsworth"
}
```

* `@type`: Used to set the type of the [node](#document-components-node). This **MUST** be a string value following the [naming conventions](#conventions-casing).
* `@links`: Used to represent a collection of [link value](#document-components-link-value) related to the resource.


> Note: To avoid compatibility issues, properties starting with an `@` character are restricted as they might be used as keywords in future versions of JSON-LD. Properties starting with an `@` character that are not JSON-LD keywords are treated as any other property, i.e., they are ignored. Keywords are case-sensitive.
>
> Restricted keywords are: `@context`, `@id`, `@value`, `@language`, `@type`, `@container`, `@list`, `@set`, `@reverse`, `@index`, `@base`, `@vocab`, `@graph`, `@nest`, `@prefix`, `@version`, `@links`


# <a href="#document" id="document" class="headerlink"></a> Document Structure

All requests sent by the client and responses sent by the server **MUST** be a valid JSON document.

```json
{
    ...
}
```

All JSON properties **MUST** follow [naming conventions](#conventions-casing).

```json
{
    "given_name": "Hubert",
    "family_name": "Farnsworth"
}
```

The _top most_ JSON object **MUST** be a [node](#document-components-node) and **MUST** contain an `@id` property unless _creating_ a new resource.

```json
{
    "@id": "/users/1",
    ...
}
```

An example of a node with query string parameters:

```json
{
    "@id": "/users?page=1",
    ...
}
```

The top most JSON object **MUST** be a [node](#document-components-node) and **MUST** contain a `@type` property.

```json
{
    "@id": "/users/1",
    "@type": "User",
    "given_name": "Hubert",
    "family_name": "Farnsworth"
}
```


## <a href="#document-components-node" id="document-components-node" class="headerlink"></a> Node

A `Node` represents a JSON object. A `Node` **MUST** contain the `@id` property if it is the top most object. It **SHOULD NOT** be in the JSON object when _creating_ a resource.

The `@id` property represents a valid [URI](#conventions-uri) and follows conventions described in the [keywords section](#keywords).

A `Node` **MUST** contain the `@type` keyword.

The value for `@type` property **MUST** be a string value representing the type following [naming conventions](#conventions-casing).

An example of `@type`:

```json
{
    "@id": "/users/1",
    "@type": "User",
    ...
}
```

A node **MAY** contain nested nodes.

```json
{
    "@id": "/users/1",
    "@type": "User",
    "given_name": "Hubert",
    "family_name": "Farnsworth",
    "address" : {
        "@id": "/users/1/address",
        "@type": "Address",
        "street": "West 57th Street"
    }
}
```

A node **MAY** contain [links](#document-components-link-collection) with the keyword of `@links`.

```json
{
    "@id": "/users/1",
    "@type": "User",
    "@links" : {
        "users": {
            "href": "/users"
        }
    },
    "given_name": "Hubert",
    "family_name": "Farnsworth"
}
```

### <a href="#document-components-link" id="document-components-link" class="headerlink"></a> Link

A `Link` is an object used to represent a collection of [link value](#document-components-link-value) related to the resource.

A `Link` **MUST** have the following:

* Nested within a [node](#document-components-node) with a keyword of `@links`.

* Must contain [link value](#document-components-link-value).

### <a href="#document-components-link-value" id="document-components-link-value" class="headerlink"></a> Link Value

A `LinkValue` is an object containing a valid URI.

A `LinkValue` **MUST** have the property `href` which represents a valid [URI](#conventions-uri).

A `LinkValue` **MAY** have the following:

* `base_path` which represents a path that can be prepended to the `href` value. The value is defined by `scheme`, `host` and optionally a `path`. It **MUST NOT** end with a slash.

* `description` which will provide additional information for each link.


```json
{
    "@id": "/users/1",
    "@type": "User",
    "@links" : {
        "users": {
            "href": "/users",
            "description": "Gets a collection of users"
        },
        "permissions": {
            "href": "/users/1/permissions",
            "description": "Gets a collection of user permissions",
            "base_path": "https://api.xyz.com/security"
        }
    },
    "given_name": "Hubert",
    "family_name": "Farnsworth"
}
```

## <a href="#document-components-collection" id="document-components-collection" class="headerlink"></a> Collection

A `Collection` is a type of [node](#document-components-node) used to represent a resource returning many of the same kind of _thing_ in a generic way. It **MUST** be the top most JSON object and **MUST NOT** be nested.

A `Collection` **MUST** have the following:

* `@id`: Represents a valid [URI](#conventions-uri).
* `@type`: Have a value of `Collection`.
* `items`: Represents an array of _things_.
    * Can be a [node](#document-components-node) with the same type. These nodes **MUST** have an `@id`.
    * Can be any arbitrary _thing_.

A `Collection` **MAY** paginate resources, i.e. return a subset of the full collection. 

A request for a subset of a paginated `Collection` **MUST** use the following query string parameters:

* `page`: The desired subset of the `Collection`
* `page_size`: The number of resources in each paginated `Collection`

A request for a paginated `Collection` without the above query string parameters should result in a default of `page=1` and a `page_size` that is sane for your application.

A paginated `Collection` **MUST** have the following:

* `total_items`: Represents the total number of _things_ as integer.

A paginated `Collection` **MAY** have the following:

* `@links`: Represents a [link](#document-components-link-collection) with the following keywords specific to pagination:
    * `first`: Represents a [link value](#document-components-link-value) navigating to the first page in the collection.
    * `next`: Represents a [link value](#document-components-link-value) navigating to the next page in the collection. **MUST NOT** be displayed if on the last page.
    * `previous`: Represents a [link value](#document-components-link-value) navigating to the previous page in the collection. **MUST NOT** be displayed if on the first page.
    * `last`: Represents a [link value](#document-components-link-value) navigating to the last page in the collection.

```json
{
    "@id": "/users?page=2&page_size=4",
    "@type": "Collection",
    "@links": {
        "first": {
            "href": "/users?page=1&page_size=4"
        },
        "next": {
            "href": "/users?page=3&page_size=4"
        },
        "previous": {
            "href": "/users?page=1&page_size=4"
        },
        "last": {
            "href": "/users?page=5&page_size=4"
        }
    },
    "items": [
        {
            "@id": "/users/1",
            "@type": "User",
            "given_name": "Hubert",
            "family_name": "Farnsworth"
        },
        {
            "@id": "/users/2",
            "@type": "User",
            "given_name": "Philip",
            "family_name": "Fry"
        },
        ...
    ],
    "total_items": 20
}
```

## <a href="#document-entry-point" id="document-entry-point" class="headerlink"></a> Entry Point

An `EntryPoint` is a type of [node](#document-components-node) used to represent a resource that clients can use to get more information about an API and provide [links](#document-components-link-collection) to traverse.

It **MUST** be the top most JSON object and **MUST NOT** be nested.

An `EntryPoint` **MUST** have the following:

* `@id`: Represents a valid [URI](#conventions-uri).
* `@type`: Have a value of `EntryPoint`.
* `@links`: Represents a [link](#document-components-link-collection) with navigational _links_ to other APIs and additional resources.

A `EntryPoint` **SHOULD** have the following in the `@links` object:

* `documentation`: Represents a [link value](#document-components-link-value) navigating to the documentation page.
* `support`: Represents a [link value](#document-components-link-value) navigating to the support page.

An `EntryPoint` **SHOULD** have the following:

* `name`: Represents the name of the API as string.
* `version`: Represents the current version of the API following [versioning](#conventions-versioning) conventions as string.

A `EntryPoint` **MAY** have the following:

* `description`: Represents a description of the API as string.


```json
{
  "@type": "EntryPoint",
  "@id": "/foo/v1",
  "@links": {
    "users": {
      "href": "/foo/v1/users",
      "description": "This is the users endpoint"
    },
    "customers": {
      "href": "/foo/v1/customers",
      "description": "This is the customer endpoint"
    },
    "documentation":{
        "href": "/",
        "base_path": "https://developer.foo.io"
    } ,
    "support": {
        "href": "/support",
        "base_path": "https://developer.foo.io"
    }
  },
  "name": "Foo v1 API",
  "description": "Description about Foo API",
  "version": "v1"
}
```


## <a href="#document-components-error" id="document-components-error" class="headerlink"></a> Error

Processing errors can be handled by returning a [node](#document-components-node) of `Error` to consumers. In addition, an appropriate HTTP status code, a human readable [error code](#document-components-error-codes) must be returned.

An `Error` **MUST** have the following:

* `@type`: Have a value of `Error`.
* `code`: A human readable [error code](#document-components-error-codes) as string following `snake_case`.
* `title`: The main error heading as string.

An `Error` **MAY** have the following:

* `description`: Detail description about the error as string.
* `status_code`: Represents the HTTP status code associated with response as integer.
* `details`: Array of [error detail](#document-components-error-detail).


## <a href="#document-components-error-detail" id="document-components-error-detail" class="headerlink"></a> Error Detail

Some errors require more information about what failed and sometimes where the error occurred. API authors can then provide a [node](#document-components-node) of `ErrorDetail` to help pin-point specific errors.

An `ErrorDetail` **MUST** have the following:

* `@type`: Have a value of `ErrorDetail`.
* `description`: Detail description about the error as string.

An `ErrorDetail` **MAY** have the following:
* `@links`: Represents a [link](#document-components-link-collection) with navigational _links_ to other APIs and additional resources.
* `source`: Represents a JSON Pointer [[RFC6901](https://tools.ietf.org/html/rfc6901)] as string.


```json
{
    "@type": "Error",
    "code": "invalid_request",
    "status_code": 400,
    "title": "One or more properties were empty or invalid",
    "description": "One or more required fields were empty or not meeting validation requirements.",
    "details": [
        {
            "@type": "ErrorDetail",
            "source": "/first_name",
            "description": "Must not be empty and a minimum of 4 characters"
        },
        {
            "@type": "ErrorDetail",
            "@links": {
                "account": {
                    "href": "/v1/account",
                    "base_path": "https://api.xyz.co",
                    "description": "This is the account endpoint"
                }
            },
            "source": "/account_id",
            "description": "Must not be empty"
        }
    ]
}
```

## <a href="#document-components-error-codes" id="document-components-error-codes" class="headerlink"></a> Error Codes

code | description
--- | ---
unauthorized | User or client is not authorized (invalid access token)
forbidden | User or client does not have the correct oauth2 scopes
not_found | Resource does not exist or client does not have permission to that resource
invalid_operation | Request sent has a conflict with the current state of a resource
invalid_input | User or client sent a request that the server could not understand due to invalid syntax or did not meet validation requirements
internal_error | Internal server error occurred
rate_limit_reached | Too many requests have been received in a given amount of time
payload_too_large | Payload too large
method_not_allowed | Method not allowed
internal_error | The server cannot process the request 
bad_gateway | The gateway server or proxy received an invalid response from upstream server while fulfilling a request
service_unavailable | The server is currently unable to handle requests temporarily due to maintenance or resource exhaustion from high load
gateway_timeout | The gateway server or proxy failed to receive a response from upstream server while fulfilling a request
