from uagents import Agent, Context, Protocol, Model
from uagents.setup import fund_agent_if_low
from protocols import (Error_Messages, GuidedResponses, FactCheckedResponses, 
                       Described_Narrations, FactCheckedScenes)

fact_checker = Agent(name="fact_checker", 
                     seed="FactChecker", 
                     port=8003, 
                     endpoint="http://127.0.0.1:8003/submit") #remove endpoint when creating Bureau

print(f"FactChecker address: {fact_checker.address}")
fund_agent_if_low(fact_checker.wallet.address())

from protocols import fact_checker_protocol
fact_checker.include(fact_checker_protocol)

if __name__ == "__main__":
    fact_checker.run()

