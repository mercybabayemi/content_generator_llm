sequenceDiagram
    participant CALLER as AboutCourseAgent
    participant CDA as CourseDetailAgent Svc
    participant PR as prompts.py
    participant LLM as LLM Client
    participant API as LLM API

    Note over CALLER,API: CourseDetailAgent — Method Flows

    alt LLM-powered methods
    CALLER->>CDA: create_description(title, complexity)
    CDA->>PR: description_prompt(title, complexity)
    PR-->>CDA: system, user
    CDA->>LLM: call_llm(system, user)
    activate LLM
    LLM->>API: POST /completions
    API-->>LLM: JSON
    deactivate LLM
    LLM-->>CDA: {description: str}
    CDA-->>CALLER: description: str

    CALLER->>CDA: create_prerequisites(title, complexity)
    CDA->>PR: prerequisites_prompt(title, complexity)
    PR-->>CDA: system, user
    CDA->>LLM: call_llm(system, user)
    activate LLM
    LLM->>API: POST /completions
    API-->>LLM: JSON
    deactivate LLM
    LLM-->>CDA: {prerequisites: str}
    CDA-->>CALLER: prerequisites: str
    end

    alt Simple setter methods — no LLM
    CALLER->>CDA: add_image(image_url: str)
    CDA->>CDA: set self.course_image = image_url
    CDA-->>CALLER: Image URL stored

    CALLER->>CDA: add_introductory_video(video_url: str)
    CDA->>CDA: set self.introductory_video = video_url
    CDA-->>CALLER: Video URL stored
    end

    alt Getter methods
    CALLER->>CDA: get_difficulty_level()
    CDA-->>CALLER: ComplexityLevel enum value

    CALLER->>CDA: get_skill_tag()
    CDA-->>CALLER: List[SkillTag]

    CALLER->>CDA: get_price()
    CDA-->>CALLER: price: str
    end
