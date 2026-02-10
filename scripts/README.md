# Proposal Generator

Script para generar propuestas y cotizaciones profesionales para Ai-Whisperers.

## Uso

```bash
# Generar propuesta y cotización
python scripts/generate-proposal.py --client "Nombre Cliente" --service chatbot

# Especificar precio personalizado
python scripts/generate-proposal.py --client "Empresa SA" --service automation --price 2000

# Con información de contacto
python scripts/generate-proposal.py --client "Empresa SA" --service consulting \
  --contact "Juan Perez" --email "juan@empresa.com" --phone "+595 981 123456"

# Solo generar cotización
python scripts/generate-proposal.py --client "Empresa SA" --service custom --type quote

# Ver paquetes disponibles
python scripts/generate-proposal.py --client test --service chatbot --list-services
```

## Paquetes de Servicios

| Código | Nombre | Precio Base | Duración |
|--------|--------|-------------|----------|
| chatbot | AI Chatbot Starter | $800 | 7 días |
| automation | Automatización de Procesos | $1,500 | 18 días |
| consulting | Consultoría AI Personalizada | $1,200 | 10 días |
| course | Capacitación AI para Equipos | $2,500 | 6 días |
| custom | Solución AI Personalizada | $3,000 | 33 días |

## Opciones

```
--client, -c       Nombre del cliente (requerido)
--service, -s      Tipo de servicio (requerido)
--price, -p        Precio personalizado (opcional)
--contact          Nombre del contacto (opcional)
--email            Email del contacto (opcional)
--phone            Teléfono del contacto (opcional)
--scope            Descripción personalizada (opcional)
--output-dir, -o   Directorio de salida (default: ./generated)
--type             Tipo: proposal, quote, both (default: both)
--list-services    Listar paquetes disponibles
```

## Archivos Generados

El script genera archivos en el directorio `generated/`:

- `PROPUESTA-{Cliente}-{fecha}.md`
- `COTIZACION-{Cliente}-{fecha}.md`

## Ejemplos

### Chatbot para clínica veterinaria
```bash
python scripts/generate-proposal.py \
  --client "Clinica Veterinaria San Jose" \
  --service chatbot \
  --contact "Dr. Martinez" \
  --email "dr.martinez@clinica.com"
```

### Automatización con precio personalizado
```bash
python scripts/generate-proposal.py \
  --client "Empresa de Contabilidad" \
  --service automation \
  --price 1800 \
  --contact "Lic. Gomez"
```

## Personalización

Los templates se encuentran en `templates/`:
- `propuesta.md` - Template de propuesta
- `cotizacion.md` - Template de cotización

Las variables disponibles son:
- `{{client_name}}` - Nombre del cliente
- `{{date}}` - Fecha actual
- `{{valid_until}}` - Fecha de validez
- `{{service_name}}` - Nombre del servicio
- `{{service_description}}` - Descripción del servicio
- `{{price_gs}}` - Precio en Guaraníes
- `{{contact_info}}` - Información de contacto

## Notas

- Las cotizaciones son válidas por 15 días
- Las propuestas son válidas por 30 días
- El tipo de cambio usado: 1 USD = 7,500 Gs
- Por defecto: 50% anticipo, 50% al finalizar
