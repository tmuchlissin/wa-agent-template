import logging
from app.utils.helper import extract_message_content, detect_message_type
logger = logging.getLogger(__name__)


def dump_agent_history(agent, thread_id: str):
    try:
        snapshot = agent.get_state({"configurable": {"thread_id": thread_id}})
        
        # logger.info(f"🔧 Raw state loaded: {snapshot}")
        
        messages = snapshot.values.get("messages", [])

        if not messages:
            logger.debug("[HISTORY] No messages found for thread %s", thread_id)
            return

        for i, msg in enumerate(messages, start=1):
            clean_text = extract_message_content(msg)
            msg_type = detect_message_type(msg)
            logger.info(f"[{i}] {msg_type}: {clean_text}")

        return messages

    except Exception as e:
        logger.warning(
            "[HISTORY] Failed to dump history for %s: %s",
            thread_id,
            e,
        )