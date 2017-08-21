---
version: 1.0-draft
---

# <a href="#introduction" id="introduction" class="headerlink"></a> Introduction

Hyperion is a subset of [JSON-LD](https://json-ld.org/spec/latest/json-ld) and [Hydra](http://www.hydra-cg.com/spec/latest/core) data specifications with some sane defaults. It is pure JSON and meant to provide an easy, low-friction path towards a semantic and hypermedia driven API. The goal is for APIs to use Hyperion as a way to incrementally become JSON-LD complaint. Future versions of this specification will start adding more and more JSON-LD syntax and components.

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
* **MAY** contain all query string parameters and fragments used to retrieve that node or resource.
* **SHOULD** be relative path as it's sometimes difficult for servers to construct an absolute path reliably.
* **SHOULD** use `-` or hyphen as delimiter for words within the path.
* **SHOULD** use `camelCase` for query string parameters.

## <a href="#conventions-casing" id="conventions-casing" class="headerlink"></a> Term and Property Casing

Some specifications _leak_ naming conventions from their backend technologies. To keep JSON language agnostic and easier to consume, we will adhere to JSON naming conventions. 

* **MUST** use `PascalCase` to represent a type.
* **MUST** use `camelCase` to represent a term or property.
* **MUST NOT** use `@` keyword for custom properties as it is reserved.

# <a href="#keywords" id="keywords" class="headerlink"></a> Keywords

Hyperion specifies a couple keywords as part of the core specification:

* `@id`: Used to uniquely identify things that are being described in the document with a [URI](#conventions-uri).
* `@type`: Used to set the data type of a node or typed value.


> Note: To avoid compatibility issues, terms starting with an `@` character are to be avoided as they might be used as keyword in future versions of JSON-LD. Terms starting with an `@` character that are not JSON-LD keywords are treated as any other term, i.e., they are ignored.


# <a href="#document" id="document" class="headerlink"></a> Document Structure

Hyperion is a subset of JSON-LD and Hydra and layers in a few, yet important components. The components are meant to keep your existing JSON documents close to its original design without making drastic changes. For newer JSON documents it provides a lightweight set of terms to allow for easier consumption by clients.

## <a href="#document" id="document" class="headerlink"></a> Document

All requests sent by the client and responses sent by the server **MUST** be a valid JSON document. 

```json
{
    ...
}
```

All JSON properties and terms **MUST** follow [naming conventions](#conventions-casing).

```json
{
    "givenName": "Hubert",
    "familyName": "Farnsworth"
}
```

The _top most_ JSON object **MUST** be a [node object](#document-components-node-object) and **MUST** contain an `@id` term. 

```json
{
    "@id": "/people/1",
    ...
}
```

An example of a node with query string parameters:

```json
{
    "@id": "/people?page=1",
    ...
}
```

The top most JSON object **MUST** be a [node object](#document-components-node-object) and **MUST** contain a `@type` term. 

```json
{
    "@id": "/person/1",
    "@type": "Person",
    "givenName": "Hubert",
    "familyName": "Farnsworth"
}
```
  
## <a href="#document-components" id="document-components" class="headerlink"></a> Document components

### <a href="#document-components-node-object" id="document-components-node-object" class="headerlink"></a> Node Object

A node object represents a JSON object. A node object **MAY** contain the `@id` term unless it is the top most object in which case it **MUST** be included.

The `@id` term represents a unique node identifier and **MUST** be a valid [URI](#conventions-uri).

A node object **MUST** contain the `@type` keyword. 

The value for `@type` term **MAY** be one of the following:

* A string value representing the type in `PascalCase`.
* A valid [URI](#conventions-uri).

An example of `@type` with a URI:

```json
{
    "@id": "/person/1",
    "@type": "http://schema.org/Person",
    "givenName": "Hubert",
    "familyName": "Farnsworth"
}
```

A node object **MAY** contain nested node objects. 

```json
{
    "@id": "/person/1",
    "@type": "Person",
    "givenName": "Hubert",
    "familyName": "Farnsworth",
    "address" : {
        "@id": "/person/1/address",
        "@type": "Address",
        "street": "West 57th Street"
    }
}
```

### <a href="#document-components-collection-object" id="document-components-collection-object" class="headerlink"></a> Collection Object

A `Collection` is a type of node object used to represent a resource returning many of the same kind of _thing_. It **MUST** be the top most JSON object and **MUST NOT** be nested.

A `Collection` **MUST** have the following:

* `@id`: Represents a valid [URI](#conventions-uri). If returning a subset of a collection with a [PartialCollectionView](#document-components-partial-collection-object), then the URI must be the request path excluding all fragments and query string parameters.
* `@type`: Represents a valid [type](document-components-node-object) as string OR [URI](#conventions-uri).
* `items`: Represents an array of [node objects](#document-components-node-object) with the same type. These node objects **SHOULD** have an `@id`.

A `Collection` **MAY** have the following:
* `totalItems`: Represents the total number of _things_ as integer.
* `view`: Represents a node type of [PartialCollectionView](#document-components-partial-collection-object) for paginated collections.

```json
{
    "@id": "/person",
    "@type": "Collection",
    "totalItems": 2,
    "items": [
        {
            "@id": "/person/1",
            "@type": "Person",
            "givenName": "Hubert",
            "familyName": "Farnsworth"
        },
        {
            "@id": "/person/2",
            "@type": "Person",
            "givenName": "Philip",
            "familyName": "Fry"
        }
    ]
}
```


### <a href="#document-components-partial-collection-object" id="document-components-partial-collection-object" class="headerlink"></a> Partial Collection View Object

Since collections can become large, Web APIs often chose to split a collection into multiple pages. A node type of `PartialCollectionView` describes a specific view on the collection which represents only a subset of the collection's items. 

A `PartialCollectionView` **MUST** have the following:

* `@id`: Represents a valid [URI](#conventions-uri).
* `@type`: Represents a valid [type](document-components-node-object) as string OR [URI](#conventions-uri).

A `PartialCollectionView` **MAY** have the following:

* `first`: Represents a valid [URI](#conventions-uri).
* `next`: Represents a valid [URI](#conventions-uri).
* `previous`: Represents a valid [URI](#conventions-uri).
* `last`: Represents a valid [URI](#conventions-uri).

```json
{
    "@id": "/person",
    "@type": "Collection",
    "totalItems": "20",
    "items": [
        {
            "@id": "/person/1",
            "@type": "Person",
            "givenName": "Hubert",
            "familyName": "Farnsworth"
        },
        {
            "@id": "/person/2",
            "@type": "Person",
            "givenName": "Philip",
            "familyName": "Fry"
        },
        ...
    ],
    "view": {
        "@id": "/person?page=1&pageSize=4",
        "@type": "PartialCollectionView",
        "first": "/person?page=1&pageSize=4",
        "next": "/person?page=2&pageSize=4",
        "last": "/person?page=5&pageSize=4"
    }
}
```

### <a href="#document-components-error-code-object" id="document-components-error-code-object" class="headerlink"></a> Error Code Object

Processing errors can be handled by returning a node type of `ErrorCode` to consumers. In addition, an appropriate HTTP status code, as well as a human readable `code` must be returned.

An `ErrorCode` **MUST** have the following:

* `@type`: Represents a valid [type](document-components-node-object) as string OR [URI](#conventions-uri).
* `code`: A human readable error code as string.
* `title`: The main error heading as string.

An `ErrorCode` **MAY** have the following:

* `description`: Detail description about the error as string.
* `statusCode`: Represents the HTTP status code associated with response as integer.
* `details`: Array of [ErrorCodeDetail](#document-components-error-code-detail-object) objects.

```json
{
    "@type": "ErrorCode",
    "code": "invalid_request",
    "statusCode": 400,
    "title": "One or more properties were empty",
    "description": "One or more required fields were empty or missing from the request.",
    "details": [
        {
            "@type": "ErrorCodeDetail",
            "source": "/givenName",
            "description": "Must not be empty"
        },
        {
            "@type": "ErrorCodeDetail",
            "source": "/familyName",
            "description": "Must not be empty"
        }
    ]
}
```

### <a href="#document-components-error-code-detail-object" id="document-components-error-code-detail-object" class="headerlink"></a> Error Code Detail Object

Some errors require more information about what failed and sometimes where the error occurred. API authors can then provide a node type of `ErrorCodeDetail` object to help pin-point errors. 

An `ErrorCode` **MUST** have the following:

* `@type`: Represents a valid [type](document-components-node-object) as string OR [URI](#conventions-uri).
* `description`: Detail description about the error as string.

An `ErrorCode` **MAY** have the following:
* `source`: Represents a JSON Pointer [RFC6901](https://tools.ietf.org/html/rfc6901) as string.