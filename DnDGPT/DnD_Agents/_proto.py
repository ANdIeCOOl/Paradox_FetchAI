from uagents import Model, Protocol, Context
"""AGENT ADDRESSES"""
SCENARIO_ADDRESS = "agent1q03cseuyk38flt9gmzydteahvf8c5afl4s8rxsse8p9k9lh335evcs6pm3z"
FACT_GIVER_ADDRESS = ""
GUIDE_ADDRESS = ""


class Scenes(Model):
    scene: str  # Receives information from the fact giver/guide

class Facts(Model):
    fact: str  # Receives information from the fact giver/guide
 
class Narrations(Model):
    narration: str  #This is the Narration Facts. send to describer Scenario,

class Errors(Model):
    error: str  #This is the Errors that occur, helps in interpretability

PROTOCOL_NAME="narrator"
PROTOCOL_VERSION="6.9"

narrator_protocol = Protocol(name=PROTOCOL_NAME, version=PROTOCOL_VERSION) #for talking use message, for LLM stuff use on_query

@narrator_protocol.on_message(model=Facts, replies=Narrations)
async def narrate_facts(ctx: Context, sender: str, msg: Facts):
    """
    Narrate the facts 
    """
    try:

        narration = "This is a narration of the facts" #send facts to LLM and get a narration
        
        #store narration in ctx or database, see which works easier for context

        await ctx.send(SCENARIO_ADDRESS, Narrations(narration=narration)) #here send to describer scenario not back to sender

    except Exception as e:
        await ctx.send(sender, Errors(error=(f"I am unable to narrate the facts at this time due to"
                                            "{e}. Please try again later.")))
    
from uagents import Model, Protocol, Context
"""AGENT ADDRESSES"""

NARRATOR_ADDRESS = "agent1qv0gczjk9nnvj57rvtfgmp3j6e9x29k0kx8rjnq6nhu65p9cpqvlc3x2pj5"
FACT_GIVER_ADDRESS = ""
GUIDE_ADDRESS = ""
MASTER_ADDRESS = ""


"""
Scenario Protocols for DnDGPT
"""

PROTOCOL_VERSION="6.9"

scenario_protocol = Protocol(name=PROTOCOL_NAME, version=PROTOCOL_VERSION) #for talking use message, for LLM stuff use on_query

@scenario_protocol.on_message(model=Narrations, replies=Scenes)
async def narrate_facts(ctx: Context, sender: str, msg: Narrations):
    """
    Describe the Narration 
    """
    try:
         #send facts to LLM and get a descriptive narration
        scene = "This is a scene of the narration"
        
        #store scenario in ctx or database, see which works easier for context

        ctx.logger.info(f"Sending Descriptive Scene to Master")
        await ctx.send(MASTER_ADDRESS, Scenes(scene=scene)) #here send to describer scenario not back to sender

    except Exception as e:
        await ctx.send(sender, Errors(error=(f"I am unable to narrate the facts at this time due to"
                                            "{e}. Please try again later.")))
    







