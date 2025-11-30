#!/usr/bin/env python3
"""Convert OpenAPI from YAML to JSON and CBOR formats"""

import yaml
import json
import cbor2
import os

def main():
    # Lexo YAML
    with open('openapi.yaml', 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    # Shkruaj JSON
    with open('openapi.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    json_size = os.path.getsize('openapi.json')
    print(f'✓ openapi.json - {json_size:,} bytes')
    
    # Shkruaj CBOR
    with open('openapi.cbor', 'wb') as f:
        cbor2.dump(data, f)
    
    cbor_size = os.path.getsize('openapi.cbor')
    print(f'✓ openapi.cbor - {cbor_size:,} bytes')
    
    # Statistika
    yaml_size = os.path.getsize('openapi.yaml')
    print(f'\n📊 Madhësia e skedarëve:')
    print(f'  YAML:  {yaml_size:,} bytes')
    print(f'  JSON:  {json_size:,} bytes')
    print(f'  CBOR:  {cbor_size:,} bytes (binar, {round(cbor_size/json_size*100)}% të JSON)')
    print(f'\n✓ Të tre formatet janë gati!')

if __name__ == '__main__':
    main()
