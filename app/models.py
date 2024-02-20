temperature_schema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "unitCode": { "type": "string" },
    "value": { "type": "number" },
    "qualityControl": { "type": "string" }
  },
  "required": ["unitCode", "value", "qualityControl"]
}

single_observation_schema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["properties"],
  "properties": {
    "properties": {
      "type": "object",
      "required": ["station", "temperature", "timestamp"],
      "properties": {
        "station": {
          "type": "string"
        },
        "temperature": {
          "type": "object"
        },
        "timestamp": {
          "type": "string",
          "format": "date-time"
        }
      }
    }
  }
}

many_observations_schema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "@context": { "type": "array" },
    "type": { "type": "string" },
    "features": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string" },
          "type": { "type": "string" },
          "geometry": { "type": "object" },
          "properties": { "type": "object" }
        },
        "required": ["id", "type", "geometry", "properties"]
      }
    }
  },
  "required": ["@context", "type", "features"]
}
