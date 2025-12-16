import yaml,sys
p='docker-compose.producer-manager.yml'
try:
    with open(p,'r',encoding='utf-8') as f:
        y=yaml.safe_load(f)
    print('YAML OK')
except Exception as e:
    print('YAML ERR',e)
    sys.exit(1)

