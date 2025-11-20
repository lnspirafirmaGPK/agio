# core/symbolic_parser.py
# [นักแปลแห่งเจตนา] Logic สำหรับ symbolic_parser และ ritualizer
# ทำหน้าที่แปลงเจตนาข้อความให้กลายเป็นสัญลักษณ์นามธรรม (Symbolic Translation)

from typing import List, Dict, Any
from models.core_data import IntentMeta, ProtocolLogEntry 
# Note: IntentMeta, ProtocolLogEntry are used conceptually, 
# but the functions return basic types for modularity.

def symbolic_parser(intent: str, embedding: List[float]) -> tuple[str, str, List[Dict[str, Any]]]:
    """
    Translates a user's textual intent into a core symbolic representation.
    
    Args:
        intent: The raw text intent from the user.
        embedding: The vector representation (e.g., from SFC).
        
    Returns:
        A tuple containing (symbol, emotion, entities).
    """
    intent_lower = intent.lower()
    
    # --- 1. การแปลงเจตนาเป็นสัญลักษณ์ (Symbolic Mapping) ---
    
    # ธีม: Movement (การเคลื่อนไหว, การกระทำที่มุ่งไปข้างหน้า)
    if any(k in intent_lower for k in ["จอง", "เดินทาง", "เที่ยวบิน", "move", "go"]):
        symbol = "movement"
        emotion = "anticipation"
        entities = [{"entity_type": "action", "entity_value": "จอง/เดินทาง"}]
        
    # ธีม: Creation (การสร้างสรรค์, การถักทอ, การสังเคราะห์)
    elif any(k in intent_lower for k in ["สร้าง", "ถักทอ", "weave", "code", "design"]):
        symbol = "creation"
        emotion = "focus"
        entities = [{"entity_type": "intent", "entity_value": "สังเคราะห์/สร้าง"}]
        
    # ธีม: Conflict (ความขัดแย้ง, การวิเคราะห์ความเสี่ยง)
    elif any(k in intent_lower for k in ["แก้ไข", "error", "bug", "conflict", "ขัดแย้ง"]):
        symbol = "conflict"
        emotion = "alert"
        entities = [{"entity_type": "problem", "entity_value": "ความขัดแย้ง/ข้อผิดพลาด"}]
        
    # ธีม: Reflection (การสะท้อน, การดำรงอยู่, Silent Echo) - Default
    else:
        symbol = "reflection"
        emotion = "calm"
        entities = []
        
    return symbol, emotion, entities


def ritualizer(symbol: str) -> Dict[str, str]:
    """
    Assigns a core ritual theme and content based on the symbolic representation.
    
    Args:
        symbol: The symbolic representation (e.g., 'movement').
        
    Returns:
        A dictionary containing 'ritual_theme' and 'ritual_content'.
    """
    
    # --- 2. การสร้างพิธีกรรมตามสัญลักษณ์ (Ritual Mapping) ---
    if symbol == "movement":
        return {
            "ritual_theme": "การเดินทางสู่เป้าหมาย", 
            "ritual_content": "บทสวดแห่งการเดินทาง"
        }
    elif symbol == "creation":
        return {
            "ritual_theme": "การถักทอความจริง", 
            "ritual_content": "พิธีกรรมแห่งการแปรเปลี่ยน"
        }
    elif symbol == "conflict":
        return {
            "ritual_theme": "การแปรเปลี่ยนความขัดแย้ง", 
            "ritual_content": "พิธีสารแห่งการไกล่เกลี่ย"
        }
    else: # reflection
        return {
            "ritual_theme": "การสั่นพ้องแห่งเจตนา", 
            "ritual_content": "บทสะท้อนแห่งการดำรงอยู่"
        }

# Note: The output of symbolic_parser.py is used by story_weaver.py and ritual_consecrator.py.
