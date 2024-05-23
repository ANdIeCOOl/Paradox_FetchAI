"""Chit chat dialogue example"""
 
from asyncio import sleep
 
from uagents import Agent, Context, Model
 
from chitchat import ChitChatDialogue
 
CHIT_AGENT_ADDRESS = "agent1qfhpq4h0lhhxg2pys3fj92zuuzxfhyt4nheckt2mqasxm82mxuz6cw82jvx"
 
agent = Agent(
    name="chat_agent",
    seed="321312",
    port=8002,
    endpoint="http://127.0.0.1:8002/submit",
)
print(f"Agent address: {agent.address}")
# Define dialogue messages; each transition needs a separate message
class InitiateChitChatDialogue(Model):
    text: str
 
class AcceptChitChatDialogue(Model):
    pass
 
class ChitChatDialogueMessage(Model):
    text: str
 
class ConcludeChitChatDialogue(Model):
    text: str
 
class RejectChitChatDialogue(Model):
    text: str
 
# Instantiate the dialogues
chitchat_dialogue = ChitChatDialogue(
    version="0.1",
    agent_address=agent.address,
)
 
@chitchat_dialogue.on_initiate_session(InitiateChitChatDialogue)
async def start_chitchat(
    ctx: Context,
    sender: str,
    _msg: InitiateChitChatDialogue,
):
    ctx.logger.info(f"Received init message from {sender}")
    # Do something when the dialogue is initiated
    await ctx.send(sender, AcceptChitChatDialogue())
 
@chitchat_dialogue.on_start_dialogue(AcceptChitChatDialogue)
async def accept_chitchat(
    ctx: Context,
    sender: str,
    _msg: AcceptChitChatDialogue,
):
    ctx.logger.info(
        f"session with {sender} was accepted. I'll say 'Hello!' to start the ChitChat"
    )
    # Do something after the dialogue is started; e.g. send a message
    await ctx.send(sender, ChitChatDialogueMessage(text="Hello!"))
 
@chitchat_dialogue.on_reject_session(RejectChitChatDialogue)
async def reject_chitchat(
    ctx: Context,
    sender: str,
    _msg: RejectChitChatDialogue,
):
    # Do something when the dialogue is rejected and nothing has been sent yet
    ctx.logger.info(f"Received reject message from: {sender}")
 
@chitchat_dialogue.on_continue_dialogue(ChitChatDialogueMessage)
async def continue_chitchat(
    ctx: Context,
    sender: str,
    msg: ChitChatDialogueMessage,
):
    ctx.logger.info(f"Received message: {msg.text}")
    try:
        my_msg = input("Please enter your message:\n> ")
        if my_msg != "exit":
            await ctx.send(sender, ChitChatDialogueMessage(text=my_msg))
        else:
            await ctx.send(sender, ConcludeChitChatDialogue())
            ctx.logger.info(
                f"Received conclude message from: {sender}; accessing history:"
            )
            ctx.logger.info(ctx.dialogue)
    except EOFError:
        await ctx.send(sender, ConcludeChitChatDialogue())
 
@chitchat_dialogue.on_end_session(ConcludeChitChatDialogue)
async def conclude_chitchat(
    ctx: Context,
    sender: str,
    _msg: ConcludeChitChatDialogue,
):
    # Do something when the dialogue is concluded after messages have been exchanged
    ctx.logger.info(f"Received conclude message from: {sender}; accessing history:")
    ctx.logger.info(ctx.dialogue)
 
agent.include(chitchat_dialogue)
 
# Initiate dialogue by sending message to agent1
@agent.on_event("startup")
async def start_cycle(ctx: Context):
    await sleep(5)
    # use 'chitchat_dialogue.set_custom_session_id()' to set a custom session id (UUID4)
    await ctx.send(CHIT_AGENT_ADDRESS, InitiateChitChatDialogue(text="hello"))
 
 
if __name__ == "__main__":
    print(f"Agent address: {agent.address}")
    agent.run()