from graphviz import Digraph

# Creates a new Digraph
dot = Digraph(name="Thermostat_Statechart", format="png")

# General graph settings for better visuals
dot.attr(rankdir="LR", size="12,8")
dot.graph_attr["dpi"] = "300"  # For higher resolution
dot.attr("node", shape="ellipse", style="filled", fontname="Arial", fontsize="12")

# Define nodes for system modes with colors
dot.node("H", "Heating", fillcolor="#ffcccc")  # Light Red
dot.node("AH", "Active Heating", fillcolor="#ff9999")
dot.node("C", "Cooling", fillcolor="#cceeff")  # Light Blue
dot.node("AC", "Active Cooling", fillcolor="#99ccff")
dot.node("Off", "Off", fillcolor="#e0e0e0")  # Gray

# Define nodes for states based on time of day
dot.node("Work", "Work (7:00 - 16:00)", fillcolor="#ffffcc")  # Light Yellow
dot.node("Home", "Home (16:00 - 22:00)", fillcolor="#ccffcc")  # Light Green
dot.node("Sleep", "Sleep (22:00 - 7:00)", fillcolor="#ffccff")  # Light Purple
dot.node("Hold", "Hold (Override)", fillcolor="#ffeb99")  # Soft Orange

# Define transitions between modes based on temperature and events
dot.edge("H", "AH", label="RT < ST - 1")
dot.edge("AH", "H", label="RT > ST + 1")
dot.edge("C", "AC", label="RT > ST + 1")
dot.edge("AC", "C", label="RT < ST - 1")
dot.edge("H", "C", label="Press C")
dot.edge("C", "H", label="Press H")
dot.edge("H", "Off", label="Press Off")
dot.edge("C", "Off", label="Press Off")
dot.edge("Off", "H", label="Press H")
dot.edge("Off", "C", label="Press C")

# Define transitions between time-of-day states
dot.edge("Work", "Home", label="16:00")
dot.edge("Home", "Sleep", label="22:00")
dot.edge("Sleep", "Work", label="7:00")
dot.edge("Work", "Hold", label="Override (Up/Down)")
dot.edge("Home", "Hold", label="Override (Up/Down)")
dot.edge("Sleep", "Hold", label="Override (Up/Down)")
dot.edge("Hold", "Home", label="Next Schedule(After Work - 16:00)")
dot.edge("Hold", "Sleep", label="Next Schedule(After Home - 22:00)")
dot.edge("Hold", "Work", label="Next Schedule(After sleep - 7:00)")

# Render the statechart
dot.render("thermostat_statechart", format="png", cleanup=False)
print("Statechart created as 'thermostat_statechart.png'")
