"""
This a test script that gives input the Dungeon Master input and track response graph
If you have time try runnning time it

1.Also this just a check -----Here
2.Check again with reading and writing to the DataBase ----     Pending
3.Implement LLMs --------------------------------------------   Pending
4.Check again with reading and writing to the DataBase ----     Pending
5.Build Characters and Their Actions/Responses --------------   Pending
"""

from protocols import Input_Action, Output_Action
from uagents import Agent, Context, Protocol, Model
from uagents.setup import fund_agent_if_low

character = Agent(name='character',seed="character", 
                  port=8004, 
                  endpoint="http://127.0.0.1:8004/submit")#remove endpoint when creating Bureau

input_action = Input_Action(
    id=1,
    action="Start of Adventure. Characters assemble and discuss to work togther"
)

GUIDE_ADDRESS= "agent1qge4q2a34xceg4pgkrrencsu8s9hwdrlczzuas594llmeuaxak09qsk73mu"

character.on_event("startup")
async def testIO(ctx: Context, action: Input_Action):
    ctx.logger.info(f"Character sending action Report to Dungeon Master")
    await ctx.send(GUIDE_ADDRESS, action)

    #Also try to keep a middle-connector type agent that maybe has three subgents to spilt talks concurrently, load balance maybe?
