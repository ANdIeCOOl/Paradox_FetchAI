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
class GuidedResponses(Model):
    guided_response: str

class FactCheckedResponses(Model):
    fact_resp: str

class FactCheckedScenes(Model):
    fact_scene: str

class Described_Narrations(Model):
    id: int  
    # scene: str  # converts the guided response to a scene for better to interactive scene

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

class Input_Action(Model):
    id: int  
    # action: str  #This is the Actions that occur in the scene
    
PROTOCOL_VERSION="6.9"







"""
GUIDER Protocols for DnDGPT
Information:
It Sends the Reponses to the Fact Checker to double Check the Facts. 
Guider is based on RAG, checking the documents stored interally and also facts from the Fact Checker.
Also has database Access for consistency. see how ctx works also
"""

guide_protocol = Protocol(name="guide_proto", version=PROTOCOL_VERSION) # 

"""
Guide --> Fact Checker
This Protocol Receieves Input Action From Characters and Guides the Actions as The Environment
Sends the Guided Actions using Map(prebuilt/if time permits adjust) to Fact Checker to Double Check the Facts and get relevabt suggestions
"""

guide_protocol.on_message(model=Input_Action, replies=GuidedResponses)
async def guide_actions(ctx: Context, sender: str, msg: Input_Action):
    """
    Guide the actions 
    """
    try:
        #create a DM quest guide and the check actions the guide and also update quest guide if necessary
        guided_actions = "This is response of environment to inputed actions"

        
        #store action in ctx or database, see which works easier for context

        await ctx.send(FACT_GIVER_ADDRESS, GuidedResponses(guided_response=guided_actions)) #here send to describer scenario not back to sender

    except Exception as e:
        await ctx.send(sender, Error_Messages(error=(f"I am unable to guide the actions at this time due to"
                                            "{e}. Please try again later.")))



""""
FactChecked Guided Actions ----> Scenario Builder
Sends the Guided Actions to the Scenario Builder, with relevant suggestions
"""
@guide_protocol.on_message(model=GuidedResponses, replies=Described_Narrations) #here is where dialouges is useful, how to implement 
async def guide_actions(ctx: Context, sender: str, msg: GuidedResponses):
    """
    Guide the actions 
    """
    try:
        #create a DM quest guide and the check actions the guide and also update quest guide if necessary
        scene = "This is response of guide to inputed actions"

        
        #store action in ctx or database, see which works easier for context

        await ctx.send(SCENARIO_ADDRESS, Described_Narrations(scene=scene)) #here send to describer scenario not back to sender

    except Exception as e:
        await ctx.send(sender, Error_Messages(error=(f"I am unable to guide the actions at this time due to"
                                            "{e}. Please try again later.")))








"""
Fact checker Protocols for DnDGPT
Fact cheker uses  retrieved and cached corpus, predetermined bu Rules to check facts using RAG
Fact Checker is implemented to check the guides facts accoring to the Rule Book.
Fact Checker checks the facts of Scenario generaeted by Scenrio Creater and facts checks that also.

"""
factGiver_protocol = Protocol(name="factGiver_proto", version=PROTOCOL_VERSION) #for talking use message, for LLM stuff use on_query


""" 
FactChecker --> Guide
Gets the Guided Story from Guided, 
Fact Checks it on QuestGuide and send releveant suggestions to the Guide using RAG
"""
@factGiver_protocol.on_message(model=GuidedResponses, replies=FactCheckedResponses)
async def describe_narration(ctx: Context, sender: str, msg: Described_Narrations):
    """
    Describe the Narration 
    """
    try:
      
        fact_resp=""
        await ctx.send(GUIDE_ADDRESS, FactCheckedResponses(fact_resp=fact_resp)) #here send to describer scenario not back to sender

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
The Scenario Builder uses the Guided Story Elements to create an interactive Scene, filled with characters, items, and interactive world elements
Scenario Builder is implemented to create a scene from the guided actions and facts checked by the Fact Checker 
Then the Scenario Bulder sends the Scene to the Narrator to describe the Scene decriptively.

"""

scenario_protocol = Protocol(name="scenario_proto", version=PROTOCOL_VERSION) #for talking use message for interation, for LLM stuff use on_query

"""
Scenario Builder --> Fact Checker
This Protocol receives The final Guided Story with relevant facts and infomation,
This received input should be transformed into a Scene for better immersion and interaction
"""
@scenario_protocol.on_message(model=Described_Narrations, replies=FactCheckedScenes)
async def CreateScene(ctx: Context, sender: str, msg: Described_Narrations):
    """
    Create an interactive scenes with guidance from the guide 
    """
    try:
         #send guide info and receive interactive scene
        scene = "This is a interative sence"
        

        #send scene to interactive parser, that parsers interactive elements amd returns a list of interactive items
        #interactive_elements = interactive_parser(scene) #this is a function that returns a list of interactive elements
        """
        some element1 comtains name, category, description, all valid from DnD guide charateristics
        """
        
        interactive_elements = ["some element1", "some element2", "some element3"]

        #store scenario in ctx or database, see which works easier for context

        #create agent for each character and append to list of NPC 
        #NPC=[] #make is a class instance so for each instace one set of NPC
        #ctx.storage.get("NPC")
        #for element in interactive_elements:
            #NPC.append(Agent(name=element.name, seed=element.name)) #Why wont this work? 
        #ctx.storage.set("NPC",NPC) #store the NPC in the context
            #Build backstrory(NPC[-1]) #fuction returns self
            #USe API SCRIPT TO GENERATE CHARACTERS
        




        ctx.logger.info(f"Sending Descriptive Scene to For Fact Check")
        await ctx.send(GUIDE_ADDRESS, Described_Narrations(scene=scene)) #here send to describer differetn elements in the scene
            # that may be interactive. Create a description for them using guide and fact checker

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

