from uagents import Model #keep these as verbs like doing stuff
from uagents import Protocol, Context, Bureau
import asyncio
from .models import Narrations, Facts, Scenes, Sounds, Errors

"""AGENT ADDRESSES"""
SCENARIO_ADDRESS = "agent1q03cseuyk38flt9gmzydteahvf8c5afl4s8rxsse8p9k9lh335evcs6pm3z"
FACT_GIVER_ADDRESS = ""
GUIDE_ADDRESS = ""
MASTER_ADDRESS = ""
NARRATOR_ADDRESS = ""

"""all uagent models have a string parameter
    but will check speed with querying the database or sendding whole thing 
"""
class Response(Model):
    response: str

class Describing_Narration(Model):
    id: int  
    # scene: str  # converts the narration to a scene for better visualization

class Determning_Facts(Model):
    id: int  
    # fact: str  # Receives information from the fact giver/guide
class Narrating_Facts(Model):
    id: int  
    # narration: str  #This is the Narration Facts. send to describer Scenario,

class Error_Messages(Model):
    id: int  
    # error: str  #This is the Errors that occur, helps in interpretability

class Scenes_to_Sound(Model):
    id: int  
    # sound: str  #This give SFX to the scene for better immersion develop if time permits

    

PROTOCOL_VERSION="6.9"

"""
Fact checker Protocols for DnDGPT
"""
factGiver_protocol = Protocol(name="factGiver_proto", version=PROTOCOL_VERSION) #for talking use message, for LLM stuff use on_query

@factGiver_protocol.on_message(model=Response, replies=Determning_Facts)
async def describe_narration(ctx: Context, sender: str, msg: Describing_Narration):
    """
    Describe the Narration 
    """
    try:
        #send response to LLM and get facts from guide
        fact = "This is a fact from the Dungeon Master"
        
        #store fact in ctx or database, see which works easier for context

        await ctx.send(NARRATOR_ADDRESS, Determning_Facts(fact=fact)) #here send to describer scenario not back to sender

    except Exception as e:
        await ctx.send(sender, Error_Messages(error=(f"I am unable to describe the narration at this time due to"
                                            "{e}. Please try again later.")))

"""
Narrator Protocols for DnDGPT
"""
narrator_protocol = Protocol(name="narrator_proto", version=PROTOCOL_VERSION) #for talking use message, for LLM stuff use on_query

@narrator_protocol.on_message(model=Determning_Facts, replies=Narrating_Facts)
async def narrate_facts(ctx: Context, sender: str, msg: Determning_Facts):
    """
    Narrate the facts 
    """
    try:

        narration = "This is a narration of the facts" #send facts to LLM and get a narration
        
        #store narration in ctx or database, see which works easier for context

        await ctx.send(SCENARIO_ADDRESS, Narrating_Facts(narration=narration)) #here send to describer scenario not back to sender

    except Exception as e:
        await ctx.send(sender, Error_Messages(error=(f"I am unable to narrate the facts at this time due to"
                                            "{e}. Please try again later.")))
    



"""
Scenario Protocols for DnDGPT
"""


scenario_protocol = Protocol(name="scenario_proto", version=PROTOCOL_VERSION) #for talking use message for interation, for LLM stuff use on_query

@scenario_protocol.on_message(model=Narrating_Facts, replies=Describing_Narration)
async def narrate_facts(ctx: Context, sender: str, msg: Narrating_Facts):
    """
    Describe the Narration 
    """
    try:
         #send facts to LLM and get a descriptive narration
        scene = "This is a scene of the narration"
        
        #store scenario in ctx or database, see which works easier for context

        ctx.logger.info(f"Sending Descriptive Scene to Master")
        await ctx.send(MASTER_ADDRESS, Describing_Narration(scene=scene)) #here send to describer scenario not back to sender

    except Exception as e:
        await ctx.send(sender, Error_Messages(error=(f"I am unable to narrate the facts at this time due to"
                                            "{e}. Please try again later.")))



"""The DnD Dungeon has multiple worker"""
# Narrator = Agent(name='Narrator', seed="Narrator")
# ActionAgent = Agent(name='ActionAgent', seed="ActionAgent")
# CharacterAgent = Agent(name='CharacterAgent', seed="CharacterAgent")
# RulesAgent = Agent(name='RulesAgent', seed="RulesAgent")
# VFXAgent = Agent(name='VFXAgent', seed="VFXAgent")
# SceneryAgent =  Agent(name='SceneryAgent', seed="SceneryAgent")

"""Take input from user first to create a scene"""


DungeonMaster = Bureau() # DM Bureau communicates with characters Bureau
# DungeonMaster.add_agents(Narrator)
# DungeonMaster.add_agents(ActionAgent)
# DungeonMaster.add_agents(CharacterAgent)
# DungeonMaster.add_agents(RulesAgent)
# DungeonMaster.add_agents(VFXAgent)

