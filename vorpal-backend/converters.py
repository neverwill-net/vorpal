from app import app
import uuid

@app.url_value_preprocessor
def convert_uuid(endpoint, values):
    if values:
        for key, value in values.items():
            if isinstance(value, str) and len(value) == 36:
                try:
                    uuid.UUID(value)
                except ValueError:
                    continue
                values[key] = value.lower()

