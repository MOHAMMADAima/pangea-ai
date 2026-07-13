import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import io
from .profiles import RESEARCHERS

# Past collaborations database
PAST_COLLABORATIONS = [
    {
        "researcher_a": "lea",
        "researcher_b": "amadou",
        "date": "March 2024",
        "topic": "Chikungunya vaccine distribution modeling in West Africa",
        "outcome": "Joint paper published in Lancet Infectious Diseases"
    },
    {
        "researcher_a": "priya",
        "researcher_b": "kenji",
        "date": "September 2024",
        "topic": "Cross-regional TB and zoonotic disease surveillance protocols",
        "outcome": "WHO technical report co-authored"
    },
    {
        "researcher_a": "amadou",
        "researcher_b": "kenji",
        "date": "January 2025",
        "topic": "Pandemic spread modeling: comparing Sahel and Asia-Pacific patterns",
        "outcome": "Preprint submitted to bioRxiv"
    },
    {
        "researcher_a": "lea",
        "researcher_b": "priya",
        "date": "June 2025",
        "topic": "MOPEVAC platform validation using South Asian hemorrhagic fever data",
        "outcome": "Phase 2 trial protocol co-designed"
    },
    {
        "researcher_a": "aima",
        "researcher_b": "lea",
        "date": "November 2024",
        "topic": "Geographic disparities in vaccine trial representation across Sub-Saharan Africa",
        "outcome": "Policy brief submitted to WHO Global Health Equity Initiative"
    },
    {
        "researcher_a": "aima",
        "researcher_b": "kenji",
        "date": "February 2025",
        "topic": "Global health collaboration network mapping: Asia-Pacific and Europe",
        "outcome": "Dataset published on Zenodo, 200+ downloads"
    },
    {
        "researcher_a": "amadou",
        "researcher_b": "priya",
        "date": "April 2024",
        "topic": "Computational modeling of TB spread in high-density urban settings",
        "outcome": "Abstract presented at CROI 2024, Boston"
    },
    {
        "researcher_a": "aima",
        "researcher_b": "amadou",
        "date": "July 2024",
        "topic": "Equity mapping of arboviral surveillance networks in West Africa",
        "outcome": "Grant application submitted to Wellcome Trust"
    },
    {
        "researcher_a": "lea",
        "researcher_b": "kenji",
        "date": "October 2024",
        "topic": "Cross-reactive immune responses between arenavirus and influenza vaccine platforms",
        "outcome": "Collaborative patent filed, USPTO 2024"
    },
    {
        "researcher_a": "priya",
        "researcher_b": "amadou",
        "date": "December 2024",
        "topic": "Drug-resistant pathogen modeling across South Asia and West Africa",
        "outcome": "Review paper in Journal of Global Health, under revision"
    },
    {
        "researcher_a": "aima",
        "researcher_b": "priya",
        "date": "March 2025",
        "topic": "Vaccine equity indicators in South Asian high-burden settings",
        "outcome": "Dataset and methodology shared via Open Science Framework"
    },
    {
        "researcher_a": "kenji",
        "researcher_b": "lea",
        "date": "May 2025",
        "topic": "BSL-3 containment protocols for hemorrhagic fever vaccine production in Asia",
        "outcome": "Joint training program launched at University of Tokyo"
    },
]


def get_collaborations_for_researcher(researcher_key: str) -> list:
    """Get all past collaborations involving a researcher."""
    collabs = []
    for collab in PAST_COLLABORATIONS:
        if collab["researcher_a"] == researcher_key or collab["researcher_b"] == researcher_key:
            other_key = collab["researcher_b"] if collab["researcher_a"] == researcher_key else collab["researcher_a"]
            collabs.append({
                "partner": RESEARCHERS[other_key]["name"],
                "partner_key": other_key,
                "date": collab["date"],
                "topic": collab["topic"],
                "outcome": collab["outcome"]
            })
    return collabs


def get_shared_connections(researcher_a_key: str, researcher_b_key: str) -> list:
    """Find researchers that both A and B have collaborated with."""
    a_partners = {c["partner_key"] for c in get_collaborations_for_researcher(researcher_a_key)}
    b_partners = {c["partner_key"] for c in get_collaborations_for_researcher(researcher_b_key)}
    shared = a_partners & b_partners
    return [RESEARCHERS[k]["name"] for k in shared if k != researcher_a_key and k != researcher_b_key]


def generate_network_graph(highlight_a: str = None, highlight_b: str = None) -> bytes:
    """Generate a collaboration network graph as PNG bytes."""
    G = nx.Graph()

    # Add nodes
    for key, researcher in RESEARCHERS.items():
        G.add_node(key, name=researcher["name"].split()[-1], location=researcher["location"])

    # Add edges from past collaborations
    for collab in PAST_COLLABORATIONS:
        G.add_edge(
            collab["researcher_a"],
            collab["researcher_b"],
            date=collab["date"],
            topic=collab["topic"][:40] + "..."
        )

    # Layout
    pos = {
        "aima": (0.2, 0.5),
        "amadou": (0.5, 0.2),
        "lea": (0.5, 0.8),
        "priya": (0.8, 0.3),
        "kenji": (0.8, 0.7),
    }

    fig, ax = plt.subplots(1, 1, figsize=(10, 7))
    fig.patch.set_facecolor('#0F1117')
    ax.set_facecolor('#0F1117')

    # Draw edges
    edge_colors = []
    edge_widths = []
    for edge in G.edges():
        if highlight_a and highlight_b and set(edge) == {highlight_a, highlight_b}:
            edge_colors.append('#00D4AA')
            edge_widths.append(4)
        elif highlight_a and highlight_a in edge:
            edge_colors.append('#4A9EFF')
            edge_widths.append(2.5)
        elif highlight_b and highlight_b in edge:
            edge_colors.append('#FF6B6B')
            edge_widths.append(2.5)
        else:
            edge_colors.append('#444444')
            edge_widths.append(1.5)

    nx.draw_networkx_edges(G, pos, ax=ax,
                          edge_color=edge_colors,
                          width=edge_widths,
                          alpha=0.8)

    # Draw nodes
    node_colors = []
    node_sizes = []
    for node in G.nodes():
        if node == highlight_a:
            node_colors.append('#4A9EFF')
            node_sizes.append(2000)
        elif node == highlight_b:
            node_colors.append('#FF6B6B')
            node_sizes.append(2000)
        else:
            node_colors.append('#666666')
            node_sizes.append(1200)

    nx.draw_networkx_nodes(G, pos, ax=ax,
                          node_color=node_colors,
                          node_size=node_sizes,
                          alpha=0.95)

    # Draw labels
    labels = {key: RESEARCHERS[key]["name"].replace("Dr. ", "").replace("Prof. ", "").split()[-1] + 
              "\n" + RESEARCHERS[key]["location"].split(",")[0]
              for key in G.nodes()}

    nx.draw_networkx_labels(G, pos, labels, ax=ax,
                           font_size=9,
                           font_color='white',
                           font_weight='bold')

    # Edge labels
    edge_labels = {(collab["researcher_a"], collab["researcher_b"]): collab["date"]
                   for collab in PAST_COLLABORATIONS}
    nx.draw_networkx_edge_labels(G, pos, edge_labels, ax=ax,
                                font_size=7,
                                font_color='#AAAAAA',
                                bbox=dict(boxstyle='round,pad=0.2', facecolor='#1A1A2E', alpha=0.7))

    # Title
    ax.set_title("Pangea AI — Global Research Collaboration Network",
                color='white', fontsize=13, fontweight='bold', pad=15)

    # Legend
    if highlight_a and highlight_b:
        legend_elements = [
            mpatches.Patch(color='#4A9EFF', label=f'{RESEARCHERS[highlight_a]["name"].split()[-1]} (you)'),
            mpatches.Patch(color='#FF6B6B', label=f'{RESEARCHERS[highlight_b]["name"].split()[-1]} (suggested match)'),
            mpatches.Patch(color='#00D4AA', label='New connection'),
            mpatches.Patch(color='#666666', label='Network members'),
        ]
        ax.legend(handles=legend_elements, loc='lower left',
                 facecolor='#1A1A2E', labelcolor='white', fontsize=8)

    ax.axis('off')
    plt.tight_layout()

    # Save to bytes
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=120, bbox_inches='tight',
               facecolor='#0F1117')
    plt.close()
    buf.seek(0)
    return buf.getvalue()