# Pangea AI — Slack Agent for Good

> *"Science knows no country, because knowledge belongs to humanity, and is the torch which illuminates the world."*
> — Louis Pasteur, 1876

---

## The problem

During COVID-19, a virologist in Tokyo had the genomic data. A field epidemiologist in Senegal had the population access. A vaccinologist in Paris had the platform.

**They never connected.**

The cost of that silence: 7 million lives.

This wasn't a failure of science. It was a failure of infrastructure.

Today, 76% of vaccine clinical trial participants are White — while the communities bearing the highest disease burden in West Africa, South Asia, and Southeast Asia remain absent from the research designed to protect them. A vaccine tested on part of humanity protects part of humanity.

The data that would make vaccines truly universal exists. It lives in the field — in Amazonian ecosystems, in Sahelian surveillance networks, in South Asian cohort registries. It just never reaches the lab.

Pangea AI was built to change that — inside Slack, where scientific collaboration already happens.

---

## What Pangea AI does

Pangea AI is a Slack agent that connects vaccine researchers with complementary expertise and unique geographic field access — automatically, where they already work.

### `/pangea [topic]` — find your ideal collaborator
Type a research topic. Pangea AI detects your identity from your Slack profile, finds the researcher whose expertise complements yours, and explains precisely:
- **What YOU bring to THEM** — your methods, data access, geographic terrain
- **What THEY bring to YOU** — capabilities you cannot replicate from your location

Not a similarity score. A scientific justification. Bidirectional.

### Collaboration network graph
Pangea AI visualizes the existing network of past collaborations in real time — who has worked with whom, on what topic, and when. If you share a mutual colleague with your suggested match, Pangea AI tells you immediately and quantifies the network distance.

### AI-drafted introduction message
One click generates a personalized, scientifically grounded outreach message — culturally adapted to the recipient's academic context, referencing their recent work, with shared scientific keywords. Delivered directly to their Slack DM.

### App Home dashboard
Your global research network at a glance: 5 researchers across 5 continents, their expertise, collaboration history, and live impact metrics — matches made, countries connected, disciplines bridged.

### Proactive matching
Pangea AI detects research topics in channel conversations and surfaces collaboration opportunities automatically — without any command needed.

---

## Why inside Slack

Not another platform to log into. Not another directory to browse. An agent that works where scientists already are — that sees who needs whom, and makes the connection happen before the next outbreak begins.

Because the next pandemic is already forming somewhere. And the researcher who can stop it may already know someone who knows someone who has exactly what they need. They just don't know it yet.

---

## Research network (demo)

5 fictional but scientifically accurate researcher profiles anchored on the Institut Pasteur international network:

| Researcher | Location | Expertise | Unique access |
|---|---|---|---|
| Dr. Aima Mohammad | Lisbon, Portugal 🇵🇹 | Vaccine equity, global health | WHO immunization datasets |
| Dr. Léa Fontaine | Paris, France 🇫🇷 | Lassa fever, vaccinology | MOPEVAC platform |
| Prof. Amadou Diallo | Bamako, Mali 🇲🇱 | Chikungunya, viral modeling | West Africa spread models |
| Prof. Priya Sharma | Mumbai, India 🇮🇳 | Tuberculosis, seroprevalence | ICMR field samples |
| Dr. Kenji Tanaka | Tokyo, Japan 🇯🇵 | Influenza, pandemic preparedness | Asia-Pacific genomic surveillance |

---

## Tech stack

| Technology | Role |
|---|---|
| **Slack Bolt for Python** | Agent framework, Socket Mode |
| **Slack Block Kit** | Rich interactive UI cards |
| **Slack users.info API** | Researcher identity detection from Slack profiles |
| **Anthropic Claude Haiku** | AI-generated scientific collaboration proposals |
| **NetworkX + Matplotlib** | Real-time collaboration network graph generation |
| **Python** | Bidirectional complementarity matching engine |

**Roadmap:** MCP server integration (ORCID, Semantic Scholar) · Real-Time Search API for proactive weekly suggestions · Slack Marketplace submission

---

## Getting started

### Prerequisites
- Python 3.12+
- Slack workspace with admin access
- Anthropic API key

### Installation

```bash
git clone https://github.com/MOHAMMADAima/pangea-ai.git
cd pangea-ai
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

### Configuration

Create a `.env` file:
```
SLACK_BOT_TOKEN=xoxb-your-token
SLACK_APP_TOKEN=xapp-your-token
ANTHROPIC_API_KEY=sk-ant-your-key
```

### Slack app setup

Required bot scopes: `chat:write` · `channels:history` · `im:history` · `im:write` · `app_mentions:read` · `users:read` · `files:write`

Enable: Socket Mode · Event Subscriptions (`message.channels` · `message.im` · `app_home_opened`) · Slash Commands (`/pangea`) · Interactivity · App Home tab

### Run

```bash
python app.py
```

### Usage

```
/pangea Lassa fever
/pangea chikungunya modeling
/pangea tuberculosis drug resistant
/pangea influenza pandemic preparedness
```

---

## Impact

Every match made. Every country connected. Every discipline bridged. Pangea AI tracks the science getting closer to saving lives.

> *"I am utterly convinced that Science and Peace will triumph over Ignorance and War, that nations will eventually unite not to destroy but to edify."*
> — Louis Pasteur

---

## Built for

**Slack Agent Builder Challenge 2026** · Track: Slack Agent for Good

*Built solo in 48 hours.*

---

*Pangea AI — from discovery to connection in one click.*
