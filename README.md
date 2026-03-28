# Digivatie Digital Twin Platform

## Overzicht

Dit platform simuleert, analyseert en optimaliseert workflows met:

- Digital Twin (SimPy)
- Reinforcement Learning (PPO)
- Process Mining (event log analyse)
- Excel parameterisatie
- BPMN-ready structuur

---

## Functionaliteiten

### 1. Workflow input

Je kunt workflows laden via:

- Demo workflow
- Excel parameterbestand
- Event log (process mining)

---

### 2. Excel workflow parameters

Download een template en vul:

| Task | Duration | Waiting | Cost | Resources |
|------|---------|--------|------|----------|

Upload daarna opnieuw.

---

### 3. Event log analyse (Process Mining)

Upload een Excel met:

| CaseID | Activity | Timestamp |

Voorbeeld:

| CaseID | Activity | Timestamp |
|--------|---------|----------|
| 1 | Sorteren | 2024-01-01 08:00 |
| 1 | Wassen | 2024-01-01 09:00 |
| 1 | Ophangen | 2024-01-01 10:00 |

Het systeem berekent automatisch:

- Wachttijden
- Processtructuur (impliciet)
- Input voor simulatie

---

### 4. Simulatie

Gebaseerd op:

- Task durations
- Resources
- Wachttijden

Output:

- Doorlooptijd
- Wachttijd
- Bottlenecks

---

### 5. RL Optimalisatie

Doelstelling:

Minimize:

- Doorlooptijd
- Wachttijd
- Kosten

Acties:

- Verkort taakduur
- Voeg resources toe

---

## Installatie

```bash
pip install -r requirements.txt
streamlit run app.py