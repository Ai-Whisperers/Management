# 📂 Gestión de Proyectos

> Cómo manejar y trackear proyectos en Ai-Whisperers

---

## 🎯 Principios de Gestión

1. **Un responsable por proyecto** — Siempre hay alguien "dueño"
2. **Estado visible** — Todos saben cómo va cada proyecto
3. **Actualización regular** — Después de cada meeting
4. **Documentación** — Todo en Drive y GitHub

---

## 📊 Estados de Proyecto

| Estado | Símbolo | Significado |
|--------|---------|-------------|
| Activo | 🟢 | En desarrollo activo |
| En pausa | 🟡 | Temporalmente detenido |
| Bloqueado | 🔴 | Necesita algo para continuar |
| Completado | ✅ | Terminado |
| Archivado | 📦 | Ya no se trabaja |

---

## 📁 Proyectos Actuales

### Repositorios Activos (GitHub)

| Proyecto | Descripción | Responsable | Estado |
|----------|-------------|-------------|--------|
| **Vete** | Plataforma veterinaria multi-tenant | Iván | 🟢 |
| **work-coordination** | Coordinación de AI agents | Iván | 🟢 |
| **Courses-Content** | Contenido de cursos | Kyrian | 🟢 |
| **Taller_Ocampos** | Sistema taller mecánico | — | 🟡 |
| **ultrametric-antigen-AI** | Bioinformática VAE | — | 🟢 |
| **LangAi** | Toolkit de lenguaje AI | — | 🟡 |
| **transcriptions** | Herramienta de transcripción | — | 🟢 |

### Proyectos de Servicio

| Proyecto | Cliente | Responsable | Estado |
|----------|---------|-------------|--------|
| FPUNA Summer Course | FPUNA | Kyrian | ✅ |
| (Próximos cursos) | — | — | — |

---

## 📋 Plantilla de Proyecto

```
┌─────────────────────────────────────────────────────────┐
│  PROYECTO: _____________________________________        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Fecha inicio:  ___/___/2026                            │
│  Responsable:   _____________________                   │
│  Estado:        🟢 🟡 🔴 ✅ 📦                           │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  DESCRIPCIÓN:                                           │
│  ________________________________________________       │
│  ________________________________________________       │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  OBJETIVO:                                              │
│  ________________________________________________       │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  EQUIPO:                                                │
│  - Responsable: _____________________                   │
│  - Soporte:     _____________________                   │
│  - Soporte:     _____________________                   │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  RECURSOS:                                              │
│  - Repo: github.com/Ai-Whisperers/___________           │
│  - Drive: ______________________________________        │
│  - Otros: ______________________________________        │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  MILESTONES:                                            │
│  □ _____________________________ Fecha: ___/___         │
│  □ _____________________________ Fecha: ___/___         │
│  □ _____________________________ Fecha: ___/___         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 📈 Seguimiento de Avance

### Actualización Semanal

Cada proyecto activo debe tener actualización en el Weekly Meeting:

```
┌─────────────────────────────────────────────────────────┐
│  ACTUALIZACIÓN - Proyecto: ____________                 │
│  Semana del: ___/___/2026                               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ¿QUÉ SE HIZO?                                          │
│  ________________________________________________       │
│  ________________________________________________       │
│                                                         │
│  ¿QUÉ FALTA?                                            │
│  ________________________________________________       │
│                                                         │
│  ¿HAY BLOQUEADORES?                                     │
│  □ No  □ Sí: ____________________________________       │
│                                                         │
│  PRÓXIMOS PASOS:                                        │
│  □ ________________________________________________     │
│  □ ________________________________________________     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🔄 Ciclo de Vida de Proyecto

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│  IDEA   │ ──▶ │ ACTIVO  │ ──▶ │COMPLETADO──▶ │ARCHIVADO│
└─────────┘     └─────────┘     └─────────┘     └─────────┘
                     │
                     ▼
                ┌─────────┐
                │ PAUSADO │
                └─────────┘
```

### Transiciones

| De | A | Requiere |
|----|---|----------|
| Idea → Activo | Reunión de kickoff, responsable asignado |
| Activo → Pausado | Decisión documentada, razón clara |
| Pausado → Activo | Reunión, recursos disponibles |
| Activo → Completado | Criterios de éxito cumplidos |
| Completado → Archivado | Retrospectiva realizada |

---

## 📊 Dashboard de Proyectos

### Vista Rápida (para cuaderno)

```
┌─────────────────────────────────────────────────────────┐
│  DASHBOARD - Actualizado: ___/___/2026                  │
├──────────────────┬────────┬───────────┬─────────────────┤
│  Proyecto        │ Estado │ Resp.     │ Próximo paso    │
├──────────────────┼────────┼───────────┼─────────────────┤
│  _______________ │ 🟢🟡🔴 │ _________ │ _______________ │
│  _______________ │ 🟢🟡🔴 │ _________ │ _______________ │
│  _______________ │ 🟢🟡🔴 │ _________ │ _______________ │
│  _______________ │ 🟢🟡🔴 │ _________ │ _______________ │
│  _______________ │ 🟢🟡🔴 │ _________ │ _______________ │
│  _______________ │ 🟢🟡🔴 │ _________ │ _______________ │
└──────────────────┴────────┴───────────┴─────────────────┘
```

---

## 🛠️ Herramientas de Seguimiento

### GitHub
- Ver commits recientes: `git log --oneline --since="1 week ago"`
- Ver contribuidores: `git shortlog -sn`

### Local (Kyrian)
- Repos clonados en: `C:\Users\kyrian\Documents\Projects\`
- Para actualizar: `git pull` en cada repo

### Drive
- Documentos de proyecto en carpetas específicas
- Transcripciones de reuniones

---

## ⚠️ Reglas de Proyectos

1. **Sin responsable = no existe** — Todo proyecto tiene dueño
2. **Sin actualización = problema** — Si no hay update en 2 semanas, revisar
3. **Cambio de estado = documentar** — Siempre anotar por qué
4. **Bloqueo = escalar** — Si algo bloquea, traer a reunión inmediatamente

---

*Documento creado: Febrero 9, 2026*

