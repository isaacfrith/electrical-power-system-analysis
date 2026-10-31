You will build a simulated suburban low-voltage feeder in pandapower and find how much rooftop solar it can take before voltages break 253 V, then test how much smart inverter settings raise that limit and who pays for it in curtailed solar.
Research question: How much rooftop solar can a typical suburban feeder host before voltages breach the Australian upper limit of 253 V, and how much do AS/NZS 4777.2 volt-var and volt-watt settings raise that limit, at what cost in curtailed energy?

What you end up with
• A reusable, config-driven Python project that builds a feeder, runs scenarios and saves results.
• A hosting capacity chart: maximum feeder voltage against solar penetration, with a band for random placement, for three inverter modes.
• A curtailment chart: energy lost per house against distance from the transformer.