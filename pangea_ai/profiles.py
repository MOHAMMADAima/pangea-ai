RESEARCHERS = {
    "aima": {
        "name": "Dr. Aima Mohammad",
        "slack_user_id": "U0BGNGGF2S2",
        "slack_names": ["aima.mohammad", "aima", "mohammad aima", "aima mohammad", "dr. aima mohammad", "dr aima mohammad"],
        "level": "junior",
        "years_experience": 3,
        "location": "Lisbon, Portugal 🇵🇹",
        "ecosystem": "Instituto de Higiene e Medicina Tropical — Global Health Research",
        "subjects": ["vaccine equity", "global health", "research collaboration networks", "epidemiology"],
        "methods": ["network analysis", "field research", "data visualization", "systematic reviews"],
        "data_access": ["WHO global immunization datasets", "IHMT Portugal research network data"],
        "recent_work": [
            "Mapping research collaboration gaps in low-income countries: a network analysis (2025)",
            "Geographic disparities in vaccine clinical trial representation: 10-year review (2026)"
        ]
    },
    "amadou": {
        "name": "Prof. Amadou Diallo",
        "slack_user_id": "U0BGU2GS9M1",
        "slack_names": ["amadou.diallo", "amadou diallo", "amadou",  "prof. amadou diallo", "prof amadou diallo"],

        "level": "senior",
        "years_experience": 15,
        "location": "Bamako, Mali 🇲🇱",
        "ecosystem": "West Africa computational epidemiology hub",
        "subjects": ["chikungunya", "viral modeling", "epidemic spread", "arbovirus"],
        "methods": ["predictive modeling", "computational simulation", "advanced statistics"],
        "data_access": ["West Africa spread models", "historical chikungunya datasets Mali"],
        "recent_work": [
            "Spatiotemporal modeling of chikungunya spread across West Africa (2024)",
            "Machine learning approaches to arboviral outbreak prediction in Sahel regions (2025)"
        ]
    },
    "lea": {
        "name": "Dr. Léa Fontaine",
        "slack_user_id": "U0BGXEB4A3W",
        "slack_names": ["lea.fontaine", "lea fontaine", "lea", "léa", "dr. lea fontaine", "dr lea fontaine"],
        "level": "senior",
        "years_experience": 12,
        "location": "Paris, France 🇫🇷",
        "ecosystem": "Vaccinology laboratory — Institut Pasteur",
        "subjects": ["Lassa fever", "hemorrhagic fevers", "arenavirus", "vaccines"],
        "methods": ["vaccine engineering", "MOPEVAC platform", "viral vectors", "immunogenicity profiling"],
        "data_access": ["MOPEVAC platform", "phase 2 clinical trial data"],
        "recent_work": [
            "MOPEVAC platform efficacy against Lassa arenavirus variants (2025)",
            "Cross-reactive immune responses in hemorrhagic fever vaccine candidates (2026)"
        ]
    },
    "priya": {
        "name": "Prof. Priya Sharma",
        "slack_user_id": "U0BGX13P5FX",
        "slack_names": ["priya.sharma", "priya sharma", "priya", "prof. priya sharma", "prof priya sharma" ],
        "level": "junior",
        "years_experience": 4,
        "location": "Mumbai, India 🇮🇳",
        "ecosystem": "South Asia infectious disease field network — ICMR",
        "subjects": ["tuberculosis", "drug-resistant TB", "seroprevalence", "vaccine equity"],
        "methods": ["field epidemiology", "drug susceptibility testing", "contact tracing"],
        "data_access": ["Mumbai TB registry 2020-2026", "ICMR field samples India"],
        "recent_work": [
            "Drug-resistant TB transmission clusters in dense urban Mumbai (2025)",
            "Vaccine equity gaps in South Asian high-burden infectious disease settings (2026)"
        ]
    },
    "kenji": {
        "name": "Dr. Kenji Tanaka",
        "slack_user_id": "U0BH41NSZ0C",
        "slack_names": ["kenji.tanaka", "kenji tanaka", "kenji", "dr. kenji tanaka", "dr kenji tanaka"],
        "level": "senior",
        "years_experience": 13,
        "location": "Tokyo, Japan 🇯🇵",
        "ecosystem": "Asia-Pacific biosafety and virology research center — University of Tokyo",
        "subjects": ["influenza", "zoonotic viruses", "biosafety", "pandemic preparedness"],
        "methods": ["BSL-3 virology", "genomic sequencing", "pandemic modeling"],
        "data_access": ["Asia-Pacific influenza surveillance network", "Japan NIID genomic database"],
        "recent_work": [
            "Novel zoonotic influenza strains detected in Southeast Asian wildlife reservoirs (2025)",
            "Asia-Pacific pandemic preparedness gaps: a genomic surveillance analysis (2026)"
        ]
    },
}

# Build reverse lookup: slack display name -> researcher key
SLACK_NAME_TO_RESEARCHER = {}
for key, profile in RESEARCHERS.items():
    for slack_name in profile.get("slack_names", []):
        SLACK_NAME_TO_RESEARCHER[slack_name.lower()] = key