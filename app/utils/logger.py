import logging

logger = logging.getLogger(__name__)


def dump_agent_history(agent, thread_id: str):
    """Log the agent's conversation history for debugging purposes."""
    try:
        snapshot = agent.get_state({"configurable": {"thread_id": thread_id}})
        messages = snapshot.values.get("messages", [])

        if not messages:
            logger.debug("[HISTORY] No messages found for thread %s", thread_id)
            return

        for i, msg in enumerate(messages):
            msg_type = type(msg).__name__
            content = str(getattr(msg, "content", ""))[:200]
            logger.debug(
                "[HISTORY] thread=%s | [%d] %s: %s",
                thread_id,
                i,
                msg_type,
                content,
            )

    except Exception as e:
        logger.warning(
            "[HISTORY] Failed to dump history for %s: %s",
            thread_id,
            e,
        )
