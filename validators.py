import sys

class DataValidator:
    def __init__(self, schema=None):
        self.schema = schema or {}

    def sanitize(self, raw_input):
        if isinstance(raw_input, str):
            return raw_input.strip()
        return raw_input

    def validate_packet(self, packet):
        if not isinstance(packet, dict):
            raise ValueError("Packet must be a dictionary structure")
            
        cleaned = {}
        for key, expected_type in self.schema.items():
            if key not in packet:
                raise KeyError(f"Missing mandatory transmission key: {key}")
                
            val = self.sanitize(packet[key])
            if not isinstance(val, expected_type):
                try:
                    val = expected_type(val)
                except (ValueError, TypeError):
                    raise TypeError(f"Type mismatch on '{key}': expected {expected_type.__name__}")
            cleaned[key] = val
        return cleaned

    def __call__(self, payload_stream):
        for index, item in enumerate(payload_stream):
            try:
                yield self.validate_packet(item)
            except Exception as err:
                sys.stderr.write(f"[ValidatorAnomaly @ idx {index}]: {err}\n")
                continue
