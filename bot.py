# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount
import asyncio
import time
import threading


class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    async def on_message_activity(self, turn_context: TurnContext):
        # await turn_context.send_activity(f"You said '{ turn_context.activity.text }'")
        print(turn_context.activity)

        conversation_reference = TurnContext.get_conversation_reference(turn_context.activity)

        
        await turn_context.send_activity(f"Processing ......")
        asyncio.create_task(self.send_proactive_message(turn_context, conversation_reference))

     

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")


    async def send_proactive_message(self, turn_context: TurnContext, conversation_reference):
        # Wait for 30 seconds asynchronously
        await asyncio.sleep(30)

        # Use `continue_conversation` to send a proactive message using the stored conversation reference
        await turn_context.adapter.continue_conversation(
            conversation_reference,
            lambda ctx: ctx.send_activity("This is a proactive message in the same conversation."),
            turn_context.activity.channel_id
        )