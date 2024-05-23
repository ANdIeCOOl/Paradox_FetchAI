from uagents import Agent, Context, Protocol, Model
from uagents.setup import fund_agent_if_low 

scenario = Agent(name='scenario', seed="Scenario", port=8001, endpoint="http://127.0.0.1:8001/submit")
#print(f"Scenario address: {Scenario.address}")
# agent1q03cseuyk38flt9gmzydteahvf8c5afl4s8rxsse8p9k9lh335evcs6pm3z
fund_agent_if_low(scenario.wallet.address())

from proto import scenario_protocol
scenario.include(scenario_protocol)

print(scenario.address)

if __name__ == "__main__":
    scenario.run()