# Domain Registry Service

## Usage
Responses from this service will have the following form:

```json
{
    "data": "Object of varying type containing the content of the response",
    "message": "A description of the event that occurred."
}
```

From here on, we'll just describe that will appear in the `data` field.

## Domain Management

### List all domains

**Definition**

`GET /domains`

**Sample Request**

```python
import requests
def get_domains():
    return requests.get(
        "https://api.gyozamail.dev/domains",
        auth=("api", "YOUR_API_KEY"))
```

**Response**

- `200 - OK` upon successful retrieval of all domains

```json
{
  "items": [
    {
      "name": "gyozamail.dev",
      "added-date": "Sun, 30 Aug 2020 18:22:33 GMT",
      "events": [
        "accepted",
        "rejected",
        "opened"
      ]
    },
    {
      "name": "realgengarhours.com",
      "added-date": "Sun, 30 Aug 2020 18:23:08 GMT",
      "events": [
        "rejected",
        "failed",
        "stored"
      ]
    },
    {
      "name": "ellio.tech",
      "added-date": "Sun, 30 Aug 2020 18:24:00 GMT",
      "events": [
        "delivered",
        "rejected",
        "failed"
      ]
    }
  ]
}
```

### Adding a new domain

**Definition**

`POST /domains`

**Arguments**

- `"name": string` a globally unique FQDN (Fully Qualified Domain Name)
- `"events": list of strings` selected events that you would like to generate unique URLs for

**Sample Request**

```python
import requests
def add_domain():
    return requests.post(
        "https://api.gyozamail.dev/domains",
        auth=("api", "YOUR_API_KEY"),
        params=({
            "name": "gyozamail.dev",
            "events": ["accepted", "rejected", "opened"]
        }))
```

**Response**

- `201 - Created` on successful addition of domain

```json
{
      "name": "gyozamail.dev",
      "added-date": "Sun, 30 Aug 2020 18:22:33 GMT",
      "events": [
        "accepted",
        "rejected",
        "opened"
      ]
}
```

### Retrieving domains

**Definition**

`GET /domains/<domain_name>`

**Sample Request**

```python
import requests
def get_domain():
    return requests.get(
        "https://api.gyozamail.dev/domains/gyozamail.dev",
        auth=("api", "YOUR_API_KEY"))
```

**Response**

- `404 - Not Found` if the domain does not exist
- `200 - OK` on successful retrieval of a domain

```json
{
      "name": "gyozamail.dev",
      "added-date": "Sun, 30 Aug 2020 18:22:33 GMT",
      "events": [
        "accepted",
        "rejected",
        "opened"
      ]
}
```

### Deleting domains

**Definition**

`DELETE /domains/<domain_name>`

**Sample Request**

```python
import requests
def delete_domain():
    return requests.delete(
        "https://api.gyozamail.dev/domains/gyozamail.dev",
        auth=("api", "YOUR_API_KEY"))
```

**Response**

- `404 - Not Found` if the domain does not exist
- `204 - No Content` on successful deletion of a domain

```json
{
  "deleted_items": {
    "name": "deletethis.dev"
  },
  "message": "Domain deleted successfully."
}
```

## Event Management

### Retrieving event URLs for domains

**Definition**

`GET /<domain_name>/events`

**Sample Request**

```python
import requests
def get_domain_events():
    return requests.get(
        "https://api.gyozamail.dev/gyozamail.dev/events",
        auth=("api", "YOUR_API_KEY"))
```

**Response**

- `404 - Not Found` if the domain does not exist
- `200 - OK` on successful retrieval of a domain

```json
{
    "name": "gyozamail.dev",
    "events": {
      "accepted": [
          "http://gyozamail.dev/hooks/accepted/"
       ], 
      "rejected": [
          "http://gyozamail.dev/hooks/rejected/"
       ],  
      "opened": [
          "http://gyozamail.dev/hooks/opened/"
       ]
}}
```

### Updating event URLs for domains
**Definition**

`PUT /<domain_name>/events`

**Arguments**

- `"events": list of strings` event types that you would like to add to the domain

**Sample Request**

```python
import requests
def update_domain_events():
    return requests.put(
        "https://api.gyozamail.dev/YOUR_DOMAIN_NAME/events",
        auth=("api", "YOUR_API_KEY"),
        params={"events": ["clicked", "complained"]})
```

**Response**

- `404 - Not Found` if the domain does not exist
- `200 - OK` on successful retrieval of a domain

**Sample Response**

```json
{
    "name": "gyozamail.dev",
    "events": {
      "accepted": [
          "http://gyozamail.dev/hooks/accepted/"
       ], 
      "rejected": [
          "http://gyozamail.dev/hooks/rejected/"
       ],  
      "opened": [
          "http://gyozamail.dev/hooks/opened/"
       ],
      "clicked": [
          "http://gyozamail.dev/hooks/clicked/"
       ],
      "complained": [
          "http://gyozamail.dev/hooks/complained/"
       ]
}}
```
