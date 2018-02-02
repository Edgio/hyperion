---
version: 1.0
---

# <a href="#introduction" id="introduction" class="headerlink"></a> Introduction

Hyperion is a lightweight data specification that is a subset of [JSON-LD](https://json-ld.org/spec/latest/json-ld) with some sane defaults. It is pure JSON and meant to provide an easy, low-friction path towards a semantic and [hypermedia](https://en.wikipedia.org/wiki/HATEOAS) driven API. The goal is for APIs to use Hyperion as a way to incrementally become JSON-LD complaint. Future versions of this specification may start adding more and more JSON-LD syntax and components.

# <a href="#conformance" id="conformance" class="headerlink"></a> Conformance

The key words may, must, must not, recommended, should, and should not are to be interpreted as described in [[RFC2119](http://tools.ietf.org/html/rfc2119)].

# <a href="#conventions" id="conventions" class="headerlink"></a> Conventions

## <a href="#conventions-content-negotiation" id="conventions-content-negotiation" class="headerlink"></a> Content Negotiation

Clients **MUST** send all JSON data in request documents with the header
`Content-Type: application/json`.

Servers **MUST** send all JSON data in response documents with the header
`Content-Type: application/json`.

## <a href="#conventions-uri" id="conventions-uri" class="headerlink"></a> URI

Anywhere a **URI** is specified, it must adhere to the following rules:

* **MUST** be a valid URI.
* **MAY** contain all query string parameters used to retrieve that resource.
* **MUST** be relative path as it's sometimes difficult for servers to construct an absolute path reliably.
* **MUST** use `-` or hyphen as delimiter for words within the path.
* **MUST** use `snake_case` for query string parameters.
* **SHOULD** use lowercase characters for words within the path basename (up to the last occurence of '/').  This is to account for various-case `id`s, such as those found in URL shorteners. E.g. `https://goo.gl/VwUrzz`

### <a href="#urls" id="urls" class="headerlink"></a> URI Path Design

This section describes the structure of the URI path, which must adhere to the following rules:

* **MUST** at the top level include support for sub-service name spacing: `https://api.company.com/`**`sub-service`**`/`
* **MUST** at the second level, provide support for versioning: `https://api.company.com/`**`sub-service`**`/v`**`x[.y]`**`/`

* **MUST** increase either `x` or `y` in the version path whenever a breaking change is introduced.  Additions to existing API calls **do not** require version changes.

These two rules promote clear differentiation of sub-services and versions, allowing independent development.

## <a href="#conventions-casing" id="conventions-casing" class="headerlink"></a> Naming Conventions

* **MUST** use `PascalCase` and be singular to represent a `@type`.
* **MUST** use `snake_case` to represent a property.
* **MUST NOT** use `@` keyword for custom properties as it is reserved.

# <a href="#keywords" id="keywords" class="headerlink"></a> Keywords

Hyperion specifies a few keywords as part of the core specification:

* `@id`: Used to specify the [URI](#conventions-uri) for the resource. Can be used by clients to navigate back to that specific resource. This **SHOULD NOT** be confused as the idenitifier for the instance of that resource.

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

* `@type`: Used to set the type of the [node object](#document-components-node-object). This **MUST** be a string value following the [naming conventions](#conventions-casing).
* `@links`: Used to represent a collection of [link value objects](#document-components-link-value-object) related to the resource.


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

The _top most_ JSON object **MUST** be a [node object](#document-components-node-object) and **MUST** contain an `@id` property unless _creating_ a new resource.

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

The top most JSON object **MUST** be a [node object](#document-components-node-object) and **MUST** contain a `@type` property.

```json
{
    "@id": "/users/1",
    "@type": "User",
    "given_name": "Hubert",
    "family_name": "Farnsworth"
}
```


## <a href="#document-components-node-object" id="document-components-node-object" class="headerlink"></a> Node Object

A `Node` object represents a JSON object. A `Node` object **MUST** contain the `@id` property if it is the top most object. It **SHOULD NOT** be in the JSON object when _creating_ a resource.

The `@id` property represents a valid [URI](#conventions-uri) and follows conventions described in the [keywords section](#keywords).

A `Node` object **MUST** contain the `@type` keyword.

The value for `@type` property **MUST** be a string value representing the type following [naming conventions](#conventions-casing).

An example of `@type`:

```json
{
    "@id": "/users/1",
    "@type": "User",
    ...
}
```

A node object **MAY** contain nested node objects.

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

A node object **MAY** contain a [link object](#document-components-link-collection-object) with the keyword of `@links`.

```json
{
    "@id": "/users/1",
    "@type": "User",
    "@links" : {
        "person": {
            "href": "/users"
        }
    },
    "given_name": "Hubert",
    "family_name": "Farnsworth"
}
```

## <a href="#document-components-link-object" id="document-components-link-object" class="headerlink"></a> Link Object

A `Link` is an object used to represent a collection of [link value objects](#document-components-link-value-object) related to the resource.

A `Link` **MUST** have the following:

* Nested within a [node object](#document-components-node-object) with a keyword of `@links`.

* Must contain [link value objects](#document-components-link-value-object).

### <a href="#document-components-link-value-object" id="document-components-link-value-object" class="headerlink"></a> Link Value Object

A `LinkValue` is an object containing a valid URI and basePath.

A `LinkValue` **MUST** have the property `href` which represents a valid [URI](#conventions-uri).

A `LinkValue` **MAY** have the property `base_path` which represents a path that can be prepended to the `href` value. The value is defined by `scheme`, `host` and optionally a `path`. It **MUST NOT** end with a slash.

```json
{
    "@id": "/users/1",
    "@type": "User",
    "@links" : {
        "person": {
            "href": "/users"
        },
        "permissions": {
            "href": "/users/1/permissions",
            "base_path": "https://api.xyz.com/security"
        }
    },
    "given_name": "Hubert",
    "family_name": "Farnsworth"
}
```

## <a href="#document-components-collection-object" id="document-components-collection-object" class="headerlink"></a> Collection Object

A `Collection` is a type of [node object](#document-components-node-object) used to represent a resource returning many of the same kind of _thing_ in a generic way. It **MUST** be the top most JSON object and **MUST NOT** be nested.

A `Collection` **MUST** have the following:

* `@id`: Represents a valid [URI](#conventions-uri).
* `@type`: Have a value of `Collection`.
* `items`: Represents an array of _things_.
    * Can be a [node objects](#document-components-node-object) with the same type. These node objects **MUST** have an `@id`.
    * Can be any arbritary _thing_.

A `Collection` **MAY** have the following:

* `total_items`: Represents the total number of _things_ as integer.
* `@links`: Repesents a [link object](#document-components-link-collection-object) with the following keywords specific to pagination:
    * `first`: Represents a [link value object](#document-components-link-value-object) navigating to the first page in the collection.
    * `next`: Represents a [link value object](#document-components-link-value-object) navigating to the next page in the collection. **MUST NOT** be displayed if on the last page.
    * `previous`: Represents a [link value object](#document-components-link-value-object) navigating to the previous page in the collection. **MUST NOT** be displayed if on the first page.
    * `last`: Represents a [link value object](#document-components-link-value-object) navigating to the last page in the collection.

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


## <a href="#document-components-error-object" id="document-components-error-object" class="headerlink"></a> Error Object

Processing errors can be handled by returning a [node object](#document-components-node-object) of `Error` to consumers. In addition, an appropriate HTTP status code, a human readable `code` must be returned.

An `Error` **MUST** have the following:

* `@type`: Have a value of `Error`.
* `code`: A human readable error code as string following `snake_case`.
* `title`: The main error heading as string.

An `Error` **MAY** have the following:

* `description`: Detail description about the error as string.
* `status_code`: Represents the HTTP status code associated with response as integer.
* `details`: Array of [error detail objects](#document-components-error-detail-object).

```json
{
    "@type": "Error",
    "code": "invalid_request",
    "status_code": 400,
    "title": "One or more properties were empty",
    "description": "One or more required fields were empty or missing from the request.",
    "details": [
        {
            "@type": "ErrorDetail",
            "source": "/given_name",
            "description": "Must not be empty"
        },
        {
            "@type": "ErrorDetail",
            "source": "/family_name",
            "description": "Must not be empty"
        }
    ]
}
```

## <a href="#document-components-error-detail-object" id="document-components-error-detail-object" class="headerlink"></a> Error Detail Object

Some errors require more information about what failed and sometimes where the error occurred. API authors can then provide a [node object](#document-components-node-object) of `ErrorDetail` to help pin-point specific errors.

An `ErrorDetail` **MUST** have the following:

* `@type`: Have a value of `ErrorDetail`.
* `description`: Detail description about the error as string.

An `ErrorDetail` **MAY** have the following:
* `source`: Represents a JSON Pointer [[RFC6901](https://tools.ietf.org/html/rfc6901)] as string.


# <a href="#date" id="date" class="headerlink"></a> Date Handling

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
