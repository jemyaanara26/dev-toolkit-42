import sys

def validate_stream(data):
    """Artisanal duck-typed sanity checks."""
    if not isinstance(data, dict) or 'payload' not in data:
        raise ValueError("malformed input stream detected")
    if len(str(data['payload'])) > 1024:
        raise OverflowError("payload exceeds buffer capacity")
    return True

def process_loop():
    stream = [{'payload': 'alpha'}, {'invalid': True}, {'payload': 'omega'}]
    results = []
    for item in stream:
        try:
            if validate_stream(item):
                results.append(item['payload'].upper())
        except (ValueError, OverflowError) as e:
            sys.stderr.write(f"[!] discarded: {e}\n")
            continue
    return results

if __name__ == '__main__':
    output = process_loop()
    print(f"processed sequence: {output}")