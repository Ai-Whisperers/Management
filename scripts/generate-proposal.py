#!/usr/bin/env python3
"""
Proposal Generator for Ai-Whisperers

Generates professional proposals and quotes from templates.

Usage:
    python generate-proposal.py --client "Acme Corp" --service "chatbot" --price 1500
    python generate-proposal.py --client "Acme Corp" --service "automation" --price 2500 --output-dir ./proposals
"""

import argparse
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Service package definitions
SERVICE_PACKAGES = {
    "chatbot": {
        "name": "AI Chatbot Starter",
        "description": "Chatbot inteligente para atención al cliente con integración WhatsApp y sitio web",
        "deliverables": [
            "Chatbot configurado con respuestas automáticas",
            "Integración con WhatsApp Business",
            "Panel de administración web",
            "Reportes de conversaciones",
            "1 mes de soporte incluido"
        ],
        "timeline": [
            ("Configuración inicial", 2),
            ("Entrenamiento del chatbot", 3),
            ("Integración y pruebas", 2),
            ("Entrega y capacitación", 1)
        ],
        "default_price": 800,
        "duration_days": 7
    },
    "automation": {
        "name": "Automatización de Procesos",
        "description": "Automatización de flujos de trabajo y procesos repetitivos con inteligencia artificial",
        "deliverables": [
            "Análisis de procesos actuales",
            "Diseño de flujos automatizados",
            "Implementación de automatizaciones",
            "Integración con sistemas existentes",
            "Capacitación del equipo",
            "2 meses de soporte incluido"
        ],
        "timeline": [
            ("Análisis y diagnóstico", 3),
            ("Diseño de solución", 3),
            ("Desarrollo e implementación", 7),
            ("Pruebas y ajustes", 3),
            ("Capacitación y entrega", 2)
        ],
        "default_price": 1500,
        "duration_days": 18
    },
    "consulting": {
        "name": "Consultoría AI Personalizada",
        "description": "Asesoría estratégica para integración de inteligencia artificial en tu negocio",
        "deliverables": [
            "Evaluación de oportunidades AI",
            "Roadmap de implementación",
            "Recomendaciones de herramientas",
            "Plan de capacitación",
            "Sesiones de seguimiento (4h)"
        ],
        "timeline": [
            ("Evaluación inicial", 2),
            ("Análisis de procesos", 3),
            ("Elaboración de propuesta", 3),
            ("Presentación y seguimiento", 2)
        ],
        "default_price": 1200,
        "duration_days": 10
    },
    "course": {
        "name": "Capacitación AI para Equipos",
        "description": "Curso práctico de inteligencia artificial para equipos de trabajo",
        "deliverables": [
            "Material didáctico personalizado",
            "Sesiones prácticas (8 horas)",
            "Ejercicios hands-on",
            "Certificado de participación",
            "Recursos post-curso"
        ],
        "timeline": [
            ("Preparación de material", 3),
            ("Sesión 1: Fundamentos (4h)", 1),
            ("Sesión 2: Práctica avanzada (4h)", 1),
            ("Evaluación y certificación", 1)
        ],
        "default_price": 2500,
        "duration_days": 6
    },
    "custom": {
        "name": "Solución AI Personalizada",
        "description": "Desarrollo de solución a medida según requerimientos específicos",
        "deliverables": [
            "Análisis detallado de requerimientos",
            "Diseño técnico de la solución",
            "Desarrollo e implementación",
            "Pruebas y QA",
            "Documentación completa",
            "Capacitación",
            "3 meses de soporte"
        ],
        "timeline": [
            ("Análisis y planificación", 5),
            ("Diseño técnico", 5),
            ("Desarrollo", 15),
            ("Pruebas", 5),
            ("Despliegue y entrega", 3)
        ],
        "default_price": 3000,
        "duration_days": 33
    }
}


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate professional proposals and quotes for Ai-Whisperers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --client "Acme Corp" --service chatbot --price 1000
  %(prog)s --client "Empresa SA" --service automation --contact "Juan Perez" --email "juan@empresa.com"
  %(prog)s --list-services
        """
    )
    
    parser.add_argument(
        "--client", "-c",
        required=True,
        help="Client/company name"
    )
    parser.add_argument(
        "--service", "-s",
        required=True,
        choices=list(SERVICE_PACKAGES.keys()) + ["custom"],
        help="Service package type"
    )
    parser.add_argument(
        "--price", "-p",
        type=float,
        help="Custom price (overrides default)"
    )
    parser.add_argument(
        "--contact",
        help="Contact person name"
    )
    parser.add_argument(
        "--email",
        help="Contact email"
    )
    parser.add_argument(
        "--phone",
        help="Contact phone"
    )
    parser.add_argument(
        "--scope",
        help="Custom scope description (overrides default)"
    )
    parser.add_argument(
        "--output-dir", "-o",
        default="./generated",
        help="Output directory for generated files (default: ./generated)"
    )
    parser.add_argument(
        "--list-services",
        action="store_true",
        help="List available service packages"
    )
    parser.add_argument(
        "--type",
        choices=["proposal", "quote", "both"],
        default="both",
        help="Type of document to generate (default: both)"
    )
    
    return parser.parse_args()


def list_services():
    """Display available service packages."""
    print("\n📦 Available Service Packages:\n")
    print(f"{'Code':<12} {'Name':<30} {'Default Price':<15}")
    print("-" * 57)
    for code, package in SERVICE_PACKAGES.items():
        print(f"{code:<12} {package['name']:<30} ${package['default_price']:<14,.0f}")
    print()


def format_price_gs(price):
    """Format price in Guaranies (assuming 1 USD = 7,500 Gs)."""
    gs_price = price * 7500
    return f"Gs. {gs_price:,.0f}"


def format_price_usd(price):
    """Format price in USD."""
    return f"${price:,.2f}"


def get_template_path(template_name):
    """Get the path to a template file."""
    # Check in current directory first, then in parent directories
    possible_paths = [
        Path(f"./templates/{template_name}.md"),
        Path(f"../templates/{template_name}.md"),
        Path(f"../../templates/{template_name}.md"),
        Path(__file__).parent.parent / "templates" / f"{template_name}.md",
    ]
    
    for path in possible_paths:
        if path.exists():
            return path
    
    return None


def load_template(template_name):
    """Load a template file."""
    template_path = get_template_path(template_name)
    
    if template_path:
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    # Return embedded templates if file not found
    if template_name == "propuesta":
        return get_embedded_proposal_template()
    elif template_name == "cotizacion":
        return get_embedded_quote_template()
    
    raise FileNotFoundError(f"Template '{template_name}' not found")


def get_embedded_proposal_template():
    """Return embedded proposal template."""
    return """# 📋 Propuesta Comercial

---

**Para:** {{client_name}}  
**De:** Ai-Whisperers  
**Fecha:** {{date}}  
**Válida hasta:** {{valid_until}}

---

## 🎯 Resumen Ejecutivo

{{service_description}}

Esta propuesta presenta una solución diseñada específicamente para las necesidades de {{client_name}}, 
con el objetivo de {{service_goal}} mediante el uso de tecnologías de inteligencia artificial.

---

## 🏢 Sobre Ai-Whisperers

Somos una empresa especializada en:
- AI-powered tools para automatización de negocios
- Capacitaciones en inteligencia artificial
- Desarrollo de soluciones personalizadas

**Ubicación:** Paraguay, LATAM  
**Website:** ai-whisperers.github.io  
**GitHub:** github.com/Ai-Whisperers

---

## 📋 Propuesta de Trabajo

### Alcance

{{scope_description}}

### Entregables

{{deliverables_table}}

### Qué NO incluye

- Mantenimiento después del período de soporte inicial
- Desarrollo de funcionalidades fuera del alcance acordado
- Capacitación adicional sin previa coordinación
- Infraestructura de terceros (servidores, licencias)

---

## 📅 Cronograma

{{timeline_table}}

---

## 💰 Inversión

| Concepto | Precio |
|----------|--------|
| {{service_name}} | {{price_gs}} |
| **TOTAL** | **{{price_gs}}** |

### Forma de Pago
- [x] 50% anticipo (${{deposit_usd}}), 50% al finalizar
- [ ] 100% anticipado
- [ ] Otro: _______

---

## ✅ Próximos Pasos

1. Confirmar interés en la propuesta
2. Agendar reunión para resolver dudas
3. Firmar contrato
4. Pago de anticipo (${{deposit_usd}})
5. Inicio del proyecto

---

## 📞 Contacto

**Kyrian Weiss**  
Co-fundador, Ai-Whisperers  
{{contact_info}}

---

*Esta propuesta es válida por 30 días a partir de la fecha de emisión.*
"""


def get_embedded_quote_template():
    """Return embedded quote template."""
    return """# 💰 Cotización

---

**Nº Cotización:** {{quote_number}}  
**Fecha:** {{date}}  
**Válida hasta:** {{valid_until}}

---

## 📋 Datos del Cliente

| Campo | Valor |
|-------|-------|
| Nombre/Empresa | {{client_name}} |
| Contacto | {{contact_name}} |
| Email | {{contact_email}} |
| Teléfono | {{contact_phone}} |

---

## 🎯 Servicio Solicitado

**Tipo:**
- [x] {{service_name}}

**Descripción:**
{{service_description}}

---

## 📊 Detalle de la Cotización

{{quote_details_table}}

---

## 💵 Resumen

| Concepto | Monto |
|----------|-------|
| Subtotal | {{price_gs}} |
| IVA (10%) | {{tax_gs}} |
| **TOTAL** | **{{total_gs}}** |

---

## 📅 Condiciones

**Forma de pago:**
- [x] 50% anticipo, 50% al finalizar
- [ ] 100% anticipado
- [ ] Otro: _________________

**Tiempo de entrega:** {{duration_days}} días hábiles

**Incluye:**
{{includes_list}}

**No incluye:**
- Mantenimiento post-entrega (excepto período de soporte)
- Infraestructura de terceros
- Capacitación adicional

---

## ✅ Para Aceptar

Para proceder con esta cotización:

1. Confirmar por escrito (email/WhatsApp)
2. Firmar contrato
3. Realizar pago de anticipo

---

## 📞 Contacto

**Ai-Whisperers**  
Kyrian Weiss - Co-fundador  
{{contact_info}}

---

*Esta cotización es válida por 15 días a partir de la fecha de emisión.*
"""


def generate_deliverables_table(deliverables):
    """Generate markdown table for deliverables."""
    table = "| # | Entregable | Descripción |\n"
    table += "|---|------------|-------------|\n"
    for i, item in enumerate(deliverables, 1):
        table += f"| {i} | {item} | Entregable completo |\n"
    return table


def generate_timeline_table(timeline):
    """Generate markdown table for timeline."""
    table = "| Fase | Descripción | Duración |\n"
    table += "|------|-------------|----------|\n"
    total_days = 0
    for phase, days in timeline:
        table += f"| - | {phase} | {days} días |\n"
        total_days += days
    table += f"| **Total** | | **{total_days} días** |\n"
    return table


def generate_quote_details_table(price, service_name):
    """Generate markdown table for quote details."""
    table = "| # | Concepto | Cantidad | Precio Unit. | Subtotal |\n"
    table += "|---|----------|----------|--------------|----------|\n"
    table += f"| 1 | {service_name} | 1 | {format_price_gs(price)} | {format_price_gs(price)} |\n"
    return table


def generate_includes_list(deliverables):
    """Generate markdown list of includes."""
    return "\n".join([f"- {item}" for item in deliverables[:3]])


def generate_proposal(args, package, output_dir):
    """Generate proposal document."""
    template = load_template("propuesta")
    
    today = datetime.now()
    valid_until = today + timedelta(days=30)
    
    price = args.price if args.price else package["default_price"]
    deposit = price * 0.5
    
    contact_info = []
    if args.email:
        contact_info.append(f"Email: {args.email}")
    if args.phone:
        contact_info.append(f"Teléfono: {args.phone}")
    contact_str = "  \n".join(contact_info) if contact_info else "Email: [tu-email]"
    
    replacements = {
        "{{client_name}}": args.client,
        "{{date}}": today.strftime("%d/%m/%Y"),
        "{{valid_until}}": valid_until.strftime("%d/%m/%Y"),
        "{{service_description}}": args.scope if args.scope else package["description"],
        "{{service_goal}}": "mejorar la eficiencia operativa",
        "{{scope_description}}": args.scope if args.scope else package["description"],
        "{{deliverables_table}}": generate_deliverables_table(package["deliverables"]),
        "{{timeline_table}}": generate_timeline_table(package["timeline"]),
        "{{service_name}}": package["name"],
        "{{price_gs}}": format_price_gs(price),
        "{{deposit_usd}}": format_price_usd(deposit),
        "{{contact_info}}": contact_str
    }
    
    proposal = template
    for key, value in replacements.items():
        proposal = proposal.replace(key, value)
    
    # Generate filename
    safe_client = re.sub(r'[^\w\s-]', '', args.client).strip().replace(' ', '_')
    filename = f"PROPUESTA-{safe_client}-{today.strftime('%Y%m%d')}.md"
    filepath = output_dir / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(proposal)
    
    return filepath


def generate_quote(args, package, output_dir):
    """Generate quote document."""
    template = load_template("cotizacion")
    
    today = datetime.now()
    valid_until = today + timedelta(days=15)
    
    price = args.price if args.price else package["default_price"]
    tax = price * 0.10
    total = price + tax
    
    contact_info = []
    if args.email:
        contact_info.append(f"Email: {args.email}")
    if args.phone:
        contact_info.append(f"Teléfono: {args.phone}")
    contact_str = "  \n".join(contact_info) if contact_info else "Email: [tu-email]"
    
    quote_number = f"AIWHISP-2026-{today.strftime('%m%d')}-{abs(hash(args.client)) % 1000:03d}"
    
    replacements = {
        "{{quote_number}}": quote_number,
        "{{date}}": today.strftime("%d/%m/%Y"),
        "{{valid_until}}": valid_until.strftime("%d/%m/%Y"),
        "{{client_name}}": args.client,
        "{{contact_name}}": args.contact if args.contact else "—",
        "{{contact_email}}": args.email if args.email else "—",
        "{{contact_phone}}": args.phone if args.phone else "—",
        "{{service_name}}": package["name"],
        "{{service_description}}": args.scope if args.scope else package["description"],
        "{{quote_details_table}}": generate_quote_details_table(price, package["name"]),
        "{{price_gs}}": format_price_gs(price),
        "{{tax_gs}}": format_price_gs(tax),
        "{{total_gs}}": format_price_gs(total),
        "{{duration_days}}": str(package["duration_days"]),
        "{{includes_list}}": generate_includes_list(package["deliverables"]),
        "{{contact_info}}": contact_str
    }
    
    quote = template
    for key, value in replacements.items():
        quote = quote.replace(key, value)
    
    # Generate filename
    safe_client = re.sub(r'[^\w\s-]', '', args.client).strip().replace(' ', '_')
    filename = f"COTIZACION-{safe_client}-{today.strftime('%Y%m%d')}.md"
    filepath = output_dir / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(quote)
    
    return filepath


def main():
    """Main function."""
    args = parse_arguments()
    
    if args.list_services:
        list_services()
        return 0
    
    # Get service package
    if args.service not in SERVICE_PACKAGES:
        print(f"Error: Unknown service '{args.service}'")
        print("Run with --list-services to see available options")
        return 1
    
    package = SERVICE_PACKAGES[args.service]
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    generated_files = []
    
    # Generate documents
    if args.type in ["proposal", "both"]:
        proposal_path = generate_proposal(args, package, output_dir)
        generated_files.append(proposal_path)
        print(f"[OK] Proposal generated: {proposal_path}")
    
    if args.type in ["quote", "both"]:
        quote_path = generate_quote(args, package, output_dir)
        generated_files.append(quote_path)
        print(f"[OK] Quote generated: {quote_path}")
    
    print(f"\nAll files saved to: {output_dir.absolute()}")
    
    # Print summary
    price = args.price if args.price else package["default_price"]
    print(f"\nSummary:")
    print(f"   Client: {args.client}")
    print(f"   Service: {package['name']}")
    print(f"   Price: {format_price_gs(price)} (${price:,.2f})")
    print(f"   Duration: {package['duration_days']} days")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
