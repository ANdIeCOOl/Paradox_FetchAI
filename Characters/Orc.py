from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low #remote communication not bureau but just in case

class Message1(Model):
    pass
class Message2(Model):
    pass
class Message3(Model):
    pass
class Message4(Model):
    pass
name,seed = 'Orc', 1 # read this from a file or get input from chat

orc = Agent(name=name, seed=seed)
fund_agent_if_low(orc)

