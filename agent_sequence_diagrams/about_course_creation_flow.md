sequenceDiagram
    participant U as User
    participant EP as Endpoint
    participant CA as CourseAgent Svc
    participant ACA as AboutCourseAgent Svc
    participant CDA as CourseDetailAgent Svc
    participant COD as CourseObjectiveDetails Svc
    participant LLM as LLM Client
    participant API as LLM API

    Note over U,API: Course + About Course Creation

    U->>EP: POST /course/create
    Note right of U: {course_title, program_id, complexity}
    EP->>CA: create_course(course_title, program_ref)

    CA->>ACA: create_course_detail(course_title, complexity)

    ACA->>CDA: create_description(course_title, complexity)
    CDA->>LLM: call_llm(description_prompt)
    activate LLM
    LLM->>API: POST /chat/completions
    API-->>LLM: raw JSON
    deactivate LLM
    LLM-->>CDA: {description: str}
    CDA-->>ACA: description set

    ACA->>CDA: create_prerequisites(course_title, complexity)
    CDA->>LLM: call_llm(prerequisites_prompt)
    activate LLM
    LLM->>API: POST /chat/completions
    API-->>LLM: raw JSON
    deactivate LLM
    LLM-->>CDA: {prerequisites: str}
    CDA-->>ACA: prerequisites set

    ACA->>CDA: get_difficulty_level() → ComplexityLevel
    CDA-->>ACA: complexity_level

    Note over ACA,COD: Now build course objectives
    ACA->>ACA: create_objective()
    ACA->>COD: add_objective(objective_text)
    COD->>LLM: call_llm(objectives_prompt)
    activate LLM
    LLM->>API: POST /chat/completions
    API-->>LLM: raw JSON
    deactivate LLM
    LLM-->>COD: {objective: List[str]}
    COD-->>ACA: objectives set

    ACA-->>CA: AboutCourseAgent assembled
    CA->>CA: assemble CourseAgentSchema
    CA-->>EP: CourseAgentSchema
    EP-->>U: 200 OK — course JSON
