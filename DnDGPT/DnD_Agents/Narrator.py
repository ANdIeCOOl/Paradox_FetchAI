from uagents import Agent, Context, Protocol, Model
from uagents.setup import fund_agent_if_low
from protocols import Error_Messages,Scenes_to_Sound,Output_Action

narrator = Agent(name='narrator', 
                 seed="Narrator", 
                 port=8001, 
                 endpoint="http://127.0.0.1:8001/submit")#remove endpoint when creating Bureau
print(f"Narrator address: {narrator.address}")
# agent1qv0gczjk9nnvj57rvtfgmp3j6e9x29k0kx8rjnq6nhu65p9cpqvlc3x2pj5
fund_agent_if_low(narrator.wallet.address())

from protocols import narrator_protocol
narrator.include(narrator_protocol)

if __name__ == "__main__":
    narrator.run()