import logging
from langchain_core.messages import HumanMessage
from app.utils.logger import dump_agent_history
from app.utils.helper import extract_text

logger = logging.getLogger(__name__)

async def process_message_background(
    agent, whatsapp_client, contact_number, content, processing_ids,
    contact_id, business_number, phone_id, message_id  
):
    try:
        logger.info(f"📥 Incoming message from {contact_number}: {content}")

        state = {
            "messages": [HumanMessage(content=content)],
            "phone_id": phone_id,
            "contact_id": contact_id,
            "business_number": business_number,
            "contact_number": contact_number,
            "thread_id": f"{business_number}::{contact_number}"
        }

        result = await agent.ainvoke(   
            state,
            config={"configurable": {"thread_id": state["thread_id"]}}
        )

        if "messages" in result and result["messages"]:
            last_msg = result["messages"][-1]
            response = extract_text(last_msg.content)
        else:
            response = str(result)

        logger.info(f"📤 Sending reply to {contact_number}: {response}")

        state["last_bot_message"] = response


        await whatsapp_client.send_message(
            contact_number, response, contact_id, business_number
        )

        dump_agent_history(agent, state["thread_id"])

    except Exception as e:
        logger.exception(f"❌ Error while processing message: {e}")
    finally:
        processing_ids.discard(message_id)