sequenceDiagram
    participant U as User
    participant EP as Endpoint
    participant SVC as ProgramAgent Service
    participant PR as prompts.py
    participant LLM as LLM Client
    participant API as Ollama Local Server (localhost:11434)

    Note over U,API: Program Creation Flow

    U->>EP: POST /program/create
    Note right of U: {instruction, complexity_level}
    EP->>SVC: create_program(instruction, complexity)

    SVC->>PR: build_description_prompt(instruction, complexity)
    PR-->>SVC: system_prompt, user_prompt
    SVC->>LLM: call_llm(system, user)
    activate LLM
    LLM->>API: POST /chat/completions
    API-->>LLM: raw JSON response
    deactivate LLM
    LLM-->>SVC: {description: str}

    SVC->>PR: build_objectives_prompt(instruction, complexity)
    PR-->>SVC: system_prompt, user_prompt
    SVC->>LLM: call_llm(system, user)
    activate LLM
    LLM->>API: POST /chat/completions
    API-->>LLM: raw JSON response
    deactivate LLM
    LLM-->>SVC: {objectives: str}

    SVC->>PR: build_prerequisites_prompt(instruction, complexity)
    PR-->>SVC: system_prompt, user_prompt
    SVC->>LLM: call_llm(system, user)
    activate LLM
    LLM->>API: POST /chat/completions
    API-->>LLM: raw JSON response
    deactivate LLM
    LLM-->>SVC: {prerequisites: str}

    SVC->>PR: build_learning_outcomes_prompt(instruction, complexity)
    PR-->>SVC: system_prompt, user_prompt
    SVC->>LLM: call_llm(system, user)
    activate LLM
    LLM->>API: POST /chat/completions
    API-->>LLM: raw JSON response
    deactivate LLM
    LLM-->>SVC: {learning_outcomes: str}

    SVC->>SVC: assemble ProgramAgentSchema
    SVC-->>EP: ProgramAgentSchema
    EP-->>U: 200 OK — program JSON

    Note over U,API: Optional — add media after creation
    U->>EP: POST /program/{id}/image
    EP->>SVC: add_image(image_url)
    SVC-->>EP: updated program
    EP-->>U: 200 OK




    
