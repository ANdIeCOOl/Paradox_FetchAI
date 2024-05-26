"""
This a test script that gives input the Dungeon Master input and track response graph
If you have time try runnning time it

1.Also this just a check -----Here
2.Check again with reading and writing to the DataBase ----     Pending
3.Implement LLMs --------------------------------------------   Pending
4.Check again with reading and writing to the DataBase ----     Pending
5.Build Characters and Their Actions/Responses --------------   Pending
"""
from uagents import Agent, Context, Protocol, Model, Bureau
from uagents.setup import fund_agent_if_low
from protocols import guide_protocol, Input_Action, GuidedResponses
import hashlib

# class GuidedResponses(Model):
#     guided_response: str

# class GuidedResponses_Final(Model):
#     final_guided_response: str

# class FactCheckedResponses(Model):
#     fact_resp: str

# class Described_Narrations(Model): #this is the scene
#     id: int  
#     scene: str  # converts the guided response to a scene for better to interactive scene

# class FactCheckedScenes(Model):
#     fact_scene: str


# class Described_Narrations_Final(Model): #this is the scene
#     id: int  
#     final_scene: str  #

# class Narrated_Scenes(Model):
#     id: int  
#     narration: str  # this is the narration of the scene created by the scenario builder with a narrative perspective


# class Error_Messages(Model):
#     id: int  
#     error: str  #This is the Errors that occur, helps in interpretability

# class Scenes_to_Sound(Model):
#     id: int  
#     sound: str  #This give SFX to the scene for better immersion develop if time permits

# class Input_Action(Model):
#     id: int   
#     action: str  #This is the Actions that occur in the scene comes as input

# class Output_Action(Model):
#     id: int  
#     action: str  #This is the Actions that occur in the environment goes as output



__all__ = ['Input_Action', "GuidedResponses"]

character = Agent(name='character',seed="character", 
                  port=8004, 
                  endpoint="http://127.0.0.1:8004/submit")#remove endpoint when creating Bureau


guide= Agent(name="guide", 
             seed="Guide", 
             port=8002, 
             endpoint="http://127.0.0.1:8002/submit")


GUIDE_ADDRESS= "agent1qge4q2a34xceg4pgkrrencsu8s9hwdrlczzuas594llmeuaxak09qsk73mu"

@character.on_interval(period=10.0, messages=Input_Action)
async def testIO(ctx: Context):
    action = "Start of Adventure. Characters assemble and discuss to work togther"
    ctx.logger.info(f"Character sending action Report to Dungeon Master")
    await ctx.send(GUIDE_ADDRESS,  #note if you just 
                   Input_Action(id=int(1),
                        action="Start of Adventure. Characters assemble and discuss to work togther",                                                                         
                    ) )



guide.on_message(model=Input_Action, replies=GuidedResponses)
async def guide_actions(ctx: Context, sender: str, msg: Input_Action):
    """
    Guide the actions 
    """

    try:
        #create a DM quest guide and the check actions the guide and also update quest guide if necessary
        guided_actions = "This is response of environment to inputed actions"

        
        #store action in ctx or database, see which works easier for context

        await ctx.send(sender, GuidedResponses(guided_response=guided_actions)) #here send to describer scenario not back to sender

    except Exception as e:
        await ctx.send(sender, Error_Messages(error=(f"I am unable to guide the actions at this time due to"
                                            "{e}. Please try again later.")))

#guide.include(guide_protocol)
bureau = Bureau()
bureau.add(guide)
bureau.add(character)


if __name__ == "__main__":
    bureau.run() #Runs the bureau with the agents
    #character.run() #Runs the character agent