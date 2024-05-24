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
OUPUT_ADDRESS = ""

"""all uagent models have a string parameter
    but will check speed with querying the database or sendding whole thing 
"""
class GuidedResponses(Model):
    guided_response: str

class GuidedResponses_Final(Model):
    final_guided_response: str

class FactCheckedResponses(Model):
    fact_resp: str

class Described_Narrations(Model): #this is the scene
    id: int  
    scene: str  # converts the guided response to a scene for better to interactive scene

class FactCheckedScenes(Model):
    fact_scene: str


class Described_Narrations_Final(Model): #this is the scene
    id: int  
    final_scene: str  #

class Narrated_Scenes(Model):
    id: int  
    narration: str  # this is the narration of the scene created by the scenario builder with a narrative perspective


class Error_Messages(Model):
    id: int  
    error: str  #This is the Errors that occur, helps in interpretability

class Scenes_to_Sound(Model):
    id: int  
    sound: str  #This give SFX to the scene for better immersion develop if time permits

class Input_Action(Model):
    id: int  
    action: str  #This is the Actions that occur in the scene comes as input

class Output_Action(Model):
    id: int  
    action: str  #This is the Actions that occur in the environment goes as output
    
PROTOCOL_VERSION="6.9"







"""-----------------------------------------------------------------------------------------------------------------------
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


"""
FactChecked Guided Action --> Guide
Sends the Guided Actions to the Guide, with relevant suggestions to imporve the actions
"""
@guide_protocol.on_message(model=FactCheckedResponses, replies=GuidedResponses_Final) 
async def Final_Guided_Action(ctx:Context, sender: str, msg: FactCheckedResponses):
    """
    Give guidance to Scenario Builder
    """
    try:
        
        #Create a final guide to create the Scenario
        
        final_guided_response = "final response of guide"

        
        #store action in ctx or database, see which works easier for context

        await ctx.send(SCENARIO_ADDRESS, GuidedResponses_Final(final_guided_response=final_guided_response)) #here send to describer scenario not back to sender

    except Exception as e:
        await ctx.send(sender, Error_Messages(error=(f"I am unable to guide the actions at this time due to"
                                            "{e}. Please try again later.")))



"""
FactChecked Guided Actions ----> Scenario Builder
Sends the Guided Actions to the Scenario Builder, with relevant suggestions
"""
@guide_protocol.on_message(model=FactCheckedResponses, replies=GuidedResponses) #here is where dialouges is useful, how to implement 
async def guide_scene(ctx: Context, sender: str, msg: FactCheckedResponses):
    """
    Give guidance to Scenario Builder
    """
    try:
        #create a DM quest guide and the check actions the guide and also update quest guide if necessary
        final_guided_response = "final response of guide"

        
        #store action in ctx or database, see which works easier for context

        await ctx.send(SCENARIO_ADDRESS, GuidedResponses(guided_response=final_guided_response)) #here send to describer scenario not back to sender

    except Exception as e:
        await ctx.send(sender, Error_Messages(error=(f"I am unable to guide the actions at this time due to"
                                            "{e}. Please try again later.")))




"""----------------------------------------------------------------------------------------------------------
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
async def factCheck_guide(ctx: Context, sender: str, msg: Described_Narrations):
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
Described_Narrations ----> FactChecked Scenes
FactChecker --> Scenario Builder
Takes in the Described Narration and then Fact Checks the Scene and sends the Scene to the Scenario Builder 
"""

@factGiver_protocol.on_message(model=Described_Narrations, replies=FactCheckedScenes)
async def FactCheckScene(ctx: Context, sender: str, msg: Described_Narrations):
    """
    Fact Check the Scene 
    """
    try:

        #query database for the scene and check the facts, try to keep querying back to get context of previous narrations
        #send the parsed scene to the LLM and get a fact checked scene

        #fact_scene is obtained by sending the scene to the LLM and getting a fact checked scene using RAG
        fact_scene = "This is a fact checked scene" #fact_checked scene contains suggestions for the Sceanrio Builder



        await ctx.send(SCENARIO_ADDRESS, FactCheckedScenes(fact_scene=fact_scene)) #here send to describer scenario not back to sender

    except Exception as e:
        await ctx.send(sender, Error_Messages(error=(f"I am unable to fact check the scene at this time due to"
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
@scenario_protocol.on_message(model=GuidedResponses, replies=Described_Narrations)
async def CreateScene(ctx: Context, sender: str, msg: GuidedResponses):
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
        await ctx.send(FACT_GIVER_ADDRESS, Described_Narrations(scene=scene)) #here send to describer differetn elements in the scene
            # that may be interactive. Create a description for them using guide and fact checker

    except Exception as e:
        await ctx.send(sender, Error_Messages(error=(f"I am unable to narrate the facts at this time due to"
                                            "{e}. Please try again later.")))




"""
Scenario Builder --> Fact Checker
This Protocol receives The final Guided Story with relevant facts and infomation,
This received input should be transformed into a Scene for better immersion and interaction
"""
@scenario_protocol.on_message(model=FactCheckedScenes, replies=Described_Narrations)
async def ReCreateScene(ctx: Context, sender: str, msg: FactCheckedScenes):
    """
    Create an interactive scenes with guidance from the guide 
    """
    try:
         #send guide info and receive interactive scene updated with fact checked scene
        scene = "This is a interative sence"
        #maybe also get update on characters and items in the scene that were updated by the fact checker
        

        """#send scene to interactive parser, that parsers interactive elements amd returns a list of interactive items
        #interactive_elements = interactive_parser(scene) #this is a function that returns a list of interactive elements
    
        #some element1 comtains name, category, description, all valid from DnD guide charateristics
    
        
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
            
            Updating the interactive elements needs some brain compute, come back to this later
            """ 
        


        ctx.logger.info(f"Sending Descriptive Scene to For Fact Check")
        await ctx.send(FACT_GIVER_ADDRESS, Described_Narrations(scene=scene)) #here send to describer differetn elements in the scene
            # that may be interactive. Create a description for them using guide and fact checker

    except Exception as e:
        await ctx.send(sender, Error_Messages(error=(f"I am unable to create a scene at this time due to"
                                            "{e}. Please try again later.")))



"""
Scenario --> Narrator
"""
@scenario_protocol.on_message(model=FactCheckedScenes, replies=Described_Narrations_Final) #another model to send to 
async def CreateFinalScene(ctx: Context, sender: str, msg: FactCheckedScenes):
    """
    Create an interactive This is Final Scene node before sending to Narrator
    """
    try:
         #send guide info and receive interactive scene updated with fact checked scene
        scene = "This is a interative sence"
        #maybe also get update on characters and items in the scene that were updated by the fact checker
        

        """#send scene to interactive parser, that parsers interactive elements amd returns a list of interactive items
        #interactive_elements = interactive_parser(scene) #this is a function that returns a list of interactive elements
    
        #some element1 comtains name, category, description, all valid from DnD guide charateristics
    
        
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
            
            Updating the interactive elements needs some brain compute, come back to this later
            """ 
        


        ctx.logger.info(f"Sending Descriptive Scene to For Fact Check")
        await ctx.send(NARRATOR_ADDRESS, Described_Narrations_Final(final_scene=scene)) #here send to describer differetn elements in the scene
            # that may be interactive. Create a description for them using guide and fact checker

    except Exception as e:
        await ctx.send(sender, Error_Messages(error=(f"I am unable to create a scene at this time due to"
                                            "{e}. Please try again later.")))



"""-----------------------------------------------------------------------------------------------------------------------
Narrator Protocols for DnDGPT
"""
narrator_protocol = Protocol(name="narrator_proto", version=PROTOCOL_VERSION) #for talking use message, for LLM stuff use on_query

@narrator_protocol.on_message(model=Described_Narrations_Final, replies=(Narrated_Scenes, Scenes_to_Sound) )
async def narrate_scene(ctx: Context, sender: str, msg: Described_Narrations_Final):
    """
    Narrate the facts 
    """
    try:

        narration = "This is a narration of the scene" #send scene to LLM and get a narration with sound effects in print etc

        spoken_narration = None #this is spoken audio genreated from text to speech model if time permits
        
        #store narration in ctx or database, see which works easier for context

        await ctx.send(OUPUT_ADDRESS, (Narrated_Scenes(narration=narration), Scenes_to_Sound(sound=spoken_narration)))
         #Sends this back to DM

    except Exception as e:
        await ctx.send(sender, Error_Messages(error=(f"I am unable to narrate the facts at this time due to"
                                            "{e}. Please try again later.")))
    




interactive_element = Protocol(name="interactive_proto", version=PROTOCOL_VERSION) #custom interactive elements for the scene




















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