import json
from dataclasses import dataclass
from typing import TypedDict, List, Dict, Any

# --- INPUT TYPES (For Type-Safe Reading) ---

class ActionSchema(TypedDict):
    text: str
    action: Dict[str, Any]
    function: str

class RawCardSchema(TypedDict):
    id: str
    title: str
    seed: int
    execute: ActionSchema
    write: ActionSchema

class ColorGroupSchema(TypedDict):
    color: str
    hexCode: str
    delete: ActionSchema
    cards: List[RawCardSchema]

# --- OUTPUT TYPE (The Fully Formed Object) ---

@dataclass
class HydratedCard:
    id: str
    title: str
    seed: int
    color: str
    hex_code: str
    execute: ActionSchema
    write: ActionSchema
    delete: ActionSchema  # Now bundled per card

# --- TRANSFORMATION LOGIC ---

def hydrate_deck(raw_data: List[ColorGroupSchema]) -> List[HydratedCard]:
    """
    Flattens the nested color groups into a single list of 
    fully populated card objects.
    """
    deck = []
    
    for group in raw_data:
        color_name = group['color']
        hex_val = group['hexCode']
        shared_delete = group['delete']
        
        for card in group['cards']:
            # Create a fully-formed object
            hydrated = HydratedCard(
                id=card['id'],
                title=card['title'],
                seed=card['seed'],
                color=color_name,
                hex_code=hex_val,
                execute=card['execute'],
                write=card['write'],
                delete=shared_delete
            )
            deck.append(hydrated)
            
    return deck

# --- USAGE EXAMPLE ---

def run_hydration(json_file_path: str):
    with open(json_file_path, 'r') as f:
        raw_json = json.load(f)
        
    # Transform
    full_deck = hydrate_deck(raw_json)
    
    print(f"Successfully hydrated {len(full_deck)} cards.")
    
    # Accessing data safely
    sample_card = full_deck[0]
    print(f"Sample Card: {sample_card.title} ({sample_card.color})")
    print(f"Execute Logic: {sample_card.execute['function']}")
    
    return full_deck
