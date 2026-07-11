# 🌍 Pangea AI — Slack Agent for Good

> **Bridging global vaccine research by connecting scientists with complementary expertise and unique geographic field access.**

Built for the **[Slack Agent Builder Challenge 2026](https://slackhack.devpost.com/)** · Track: **Slack Agent for Good**

---

## The Problem

A vaccine is only as effective as the populations it was designed for. Yet today, most vaccine research happens in centralized labs — disconnected from the field researchers who have irreplaceable access to local ecosystems, endemic populations, and real-world epidemiological data.

**The result:** vaccines developed without the geographic and biological diversity they need to work globally.

## The Solution

Pangea AI is a Slack agent that detects emerging research topics in scientific community conversations and surfaces high-value researcher connections — explaining precisely what each scientist brings to the other, and drafting the introduction message to make it happen.

---

## ✨ Features

### 🔬 Intelligent Bidirectional Matching
Unlike existing tools that show a similarity score, Pangea AI explains **what A brings to B** and **what B brings to A** — separately. Complementarity, not redundancy.

### 🗺️ Geographic Intelligence
Each researcher profile includes their location, ecosystem access, and local populations — because a researcher based in the Amazonian rainforest has access to data that cannot be replicated in a Paris lab.

### 🎓 Mentorship Detection
When the experience gap between two researchers exceeds 8 years on similar subjects, Pangea AI automatically reframes the match as a mentorship opportunity rather than a peer collaboration.

### ✉️ AI-Drafted Introduction Messages
One click generates a personalized, culturally adapted introduction email — with scientific keywords, a reference to the recipient's work, and a concrete next step.

---

## 🛠️ Tech Stack

| Technology | Role |
|---|---|
| **Slack Agent Builder** | Agent scaffolding and deployment |
| **Slack Bolt for Python** | Event handling and Socket Mode |
| **Block Kit** | Rich interactive UI cards |
| **Anthropic Claude** | Scientific justification generation + email drafting |
| **MCP (roadmap)** | External researcher profile data sources |
| **Real-Time Search (roadmap)** | Live workspace signal detection |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- A Slack workspace with admin access
- Anthropic API key

### Installation

```bash
git clone https://github.com/MOHAMMADAima/pangea-ai.git
cd pangea-ai
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Configuration

Create a `.env` file:
SLACK_BOT_TOKEN=xoxb-your-token
SLACK_APP_TOKEN=xapp-your-token
ANTHROPIC_API_KEY=sk-ant-your-key

### Run

```bash
python app.py
```

### Usage

In any Slack channel where Pangea AI is invited:
/pangea oropouche virus transmission
/pangea Lassa fever hemorrhagic
/pangea chikungunya modeling

---

## 🧬 Researcher Profiles (Demo)

Pangea AI ships with 4 fictional but scientifically accurate researcher profiles anchored on the Institut Pasteur international network:

| Researcher | Location | Expertise | Access |
|---|---|---|---|
| Dr. Camille Verrier | Cayenne, French Guiana 🇬🇫 | Oropouche, Arbovirus | Amazonian Aedes populations |
| Dr. Amadou Diallo | Paris, France 🇫🇷 | Chikungunya, Viral modeling | West Africa spread models |
| Dr. Léa Fontaine | Paris, France 🇫🇷 | Lassa fever, Vaccinology | MOPEVAC platform |
| Karim Belhadj | Dakar, Senegal 🇸🇳 | Hemorrhagic fevers, Seroprevalence | Rural Senegal field data |

---

## 🗺️ Roadmap

- [ ] MCP server integration for live researcher profiles (ORCID, Semantic Scholar)
- [ ] Real-Time Search API for proactive weekly match suggestions
- [ ] Slack Marketplace submission
- [ ] Multi-workspace support for research networks

---

## 🏆 Impact

> *"A vaccine designed without diverse geographic and biological data risks being less effective for the populations who need it most."*

Pangea AI addresses a documented gap: a decade of disparities in vaccine clinical trials, where communities bearing the highest disease burden are consistently underrepresented in research design.

By connecting field researchers with vaccinology labs — inside Slack, where scientific collaboration already happens — Pangea AI helps ensure that the next generation of vaccines is built on data as diverse as the world it aims to protect.

---

## 👩‍💻 Author

Built solo in 48 hours for the Slack Agent Builder Challenge 2026.

---

*🧬 Pangea AI — From discovery to connection in one click.*