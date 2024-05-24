from uagents import Agent, Context, Protocol, Model
from uagents.setup import fund_agent_if_low
from protocols import Response, Describing_Narration, Determning_Facts,Narrating_Facts,Error_Messages,Scenes_to_Sound

narrator = Agent(name='narrator', seed="Narrator", port=8001, endpoint="http://127.0.0.1:8001/submit")
#print(f"Narrator address: {Narrator.address}")
# agent1qv0gczjk9nnvj57rvtfgmp3j6e9x29k0kx8rjnq6nhu65p9cpqvlc3x2pj5
fund_agent_if_low(narrator.wallet.address())

from protocols import narrator_protocol
narrator.include(narrator_protocol)



print(narrator.address)



if __name__ == "__main__":
    narrator.run()