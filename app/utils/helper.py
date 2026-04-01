import logging, json
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

logger = logging.getLogger(__name__)

def extract_text(content):
    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        texts = []
        for block in content:
            if isinstance(block, dict):
                if block.get("type") == "text":
                    texts.append(block.get("text", ""))
            elif isinstance(block, str):
                texts.append(block)
        return "\n".join(texts).strip()

    return str(content).strip()

def extract_message_content(msg):
    if isinstance(msg, HumanMessage):
        return str(msg.content).strip()

    if isinstance(msg, AIMessage):
        tool_calls = getattr(msg, "additional_kwargs", {}).get("tool_calls")
        if tool_calls:
            return json.dumps(tool_calls, indent=2, ensure_ascii=False)

        content = msg.content
        if isinstance(content, list):
            cleaned = []
            for part in content:
                if isinstance(part, dict):
                    p = part.copy()
                    if "extras" in p:
                        p.pop("extras", None)  
                    cleaned.append(p.get("text", "")) 
                elif isinstance(part, str):
                    cleaned.append(part)
            return "\n".join(cleaned).strip()

        return str(content or "").strip()

    if isinstance(msg, ToolMessage):
        return json.dumps(msg.content, indent=2, ensure_ascii=False)

    if isinstance(msg, dict):
        content = msg.get("content")

        if isinstance(content, list):
            texts = []
            for block in content:
                if isinstance(block, dict):
                    block.pop("extras", None) 
                    texts.append(block.get("text", ""))
                elif isinstance(block, str):
                    texts.append(block)
            return "\n".join(texts).strip()

        if isinstance(content, str):
            return content.strip()

        return ""


    return str(msg)

def detect_message_type(msg):
    if isinstance(msg, HumanMessage):
        return "HumanMessage"

    if isinstance(msg, AIMessage):
        tool_calls = getattr(msg, "additional_kwargs", {}).get("tool_calls")
        return "ToolCall" if tool_calls else "AIMessage"

    if isinstance(msg, ToolMessage):
        return "ToolResult"

    if isinstance(msg, dict):
        msg_type = msg.get("type")
        if msg_type == "human":
            return "HumanMessage"
        if msg_type == "ai":
            return "AIMessage"
        return "ToolResult"

    return "UnknownMessage"
