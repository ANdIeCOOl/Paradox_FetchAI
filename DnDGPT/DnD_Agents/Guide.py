from uagents import Agent, Context, Protocol, Model
from uagents.setup import fund_agent_if_low
from protocols import Error_Messages,GuidedResponses,FactCheckedResponses,Input_Action

guide= Agent(name="guide", 
             seed="Guide", 
             port=8002, 
             endpoint="http://127.0.0.1:8002/submit") #remove endpoint when creating Bureau

print(f"Guide address: {guide.address}")
fund_agent_if_low(guide.wallet.address())

from protocols import guide_protocol
#guide.include(guide_protocol)
#print(guide_protocol.Input_Action.model_json_schema)

# if __name__ == "__main__":
#     guide.run() #Runs the guide agent

