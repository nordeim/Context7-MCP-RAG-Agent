## Core JSON Data Structure in n8n

### Standard Data Format
n8n uses a standardized JSON structure for data passing between nodes:

```json
[
  {
    "json": {
      "key1": "value1",
      "key2": "value2"
    },
    "binary": {
      "file-key": {
        "data": "base64-encoded-data",
        "mimeType": "image/png",
        "fileExtension": "png",
        "fileName": "example.png"
      }
    }
  }
]
```

### Configuration Files
n8n configuration files use JSON format:

```json
{
  "executions": {
    "saveDataOnSuccess": "none"
  },
  "generic": {
    "timezone": "Europe/Berlin"
  },
  "nodes": {
    "exclude": ["n8n-nodes-base.executeCommand", "n8n-nodes-base.writeBinaryFile"]
  }
}
```

## JSON in HTTP Request Node

### Valid JSON Format
When using expressions in HTTP Request nodes, wrap JSON in double curly brackets:

```json
{{
    {
    "myjson": {
        "name1": "value1",
        "name2": "value2",
        "array1": ["value1", "value2"]
    }
    }
}}
```

### Custom Authentication JSON
Various authentication formats:

```json
// Headers
{
  "headers": {
    "X-AUTH-USERNAME": "username",
    "X-AUTH-PASSWORD": "password"
  }
}

// Body
{
  "body": {
    "user": "username",
    "pass": "password"
  }
}

// Query string
{
  "qs": {
    "appid": "123456",
    "apikey": "my-api-key"
  }
}
```

## Workflow JSON Structure

### Complete Workflow Definition
```json
{
  "name": "Workflow Name",
  "nodes": [
    {
      "parameters": {},
      "id": "uuid",
      "name": "Node Name",
      "type": "n8n-nodes-base.nodeType",
      "typeVersion": 1,
      "position": [480, 520]
    }
  ],
  "connections": {},
  "active": false,
  "settings": {},
  "tags": []
}
```

### Webhook Data Format
```json
[
  {
    "headers": {
      "host": "n8n.instance.address"
    },
    "params": {},
    "query": {},
    "body": {
      "name": "Jim",
      "age": 30,
      "city": "New York"
    }
  }
]
```

## Data Transformation Examples

### JSON Output Mode
Transforming data with expressions:

```json
{
  "newKey": "new value",
  "array": [{{ $json.id }}, "{{ $json.name }}"],
  "object": {
    "innerKey1": "new value",
    "innerKey2": "{{ $json.id }}",
    "innerKey3": "{{ $json.name }}"
  }
}
```

### JMESPath Queries
Using JMESPath for JSON querying:

```javascript
// Extract first names
{{$jmespath($json.body.people, "[*].first")}}
// Returns: ["James", "Jacob", "Jayden"]

// Multiselect
{{$jmespath($json.body.people, "[].")}}
// Returns: [["James","Green"],["Jacob","Jones"],["Jayden","Smith"]]
```

## Form Configuration JSON

### Form Field Definitions
```json
[
  {
    "fieldLabel": "Email",
    "fieldType": "email",
    "placeholder": "me@mail.com"
  },
  {
    "fieldLabel": "Dropdown Options",
    "fieldType": "dropdown",
    "fieldOptions": {
      "values": [
        {"option": "option 1"},
        {"option": "option 2"}
      ]
    }
  },
  {
    "fieldLabel": "File",
    "fieldType": "file",
    "multipleFiles": true,
    "acceptFileTypes": ".jpg, .png"
  }
]
```

## Common JSON Formats

### Code Node Output
```javascript
return [
  {
    json: {
      key: "value"
    }
  }
];
```

### Discord Embed JSON
```json
{
  "author": "My Name",
  "url": "https://discord.js.org",
  "fields": [
    {
      "name": "Regular field title",
      "value": "Some value here"
    }
  ],
  "footer": {
    "text": "Some footer text here",
    "icon_url": "https://i.imgur.com/AfFp7pu.png"
  }
}
```

### API Response Formats
```json
// Deletion confirmation
{
  "deleted": true
}

// Workflow activation
{
  "active": true,
  "settings": {},
  "staticData": null,
  "tags": []
}
```

These JSON formats cover the main use cases in n8n, from basic data structures to complex workflow configurations and API interactions.
