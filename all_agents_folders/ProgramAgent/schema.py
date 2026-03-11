from pydantic import BaseModel
from core.enums import ComplexityLevel

class ProgramAgentSchema(BaseModel):
    program_name: str
    description: str
    complexity_level: ComplexityLevel
    learning_outcomes: str
    objectives: str
    prerequisites: str
    introductory_video: str|None
    image: str|None
