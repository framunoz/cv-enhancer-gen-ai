# cv-enhancer-gen-ai

```mermaid
flowchart TD
    Start@{ shape: circle }

    Start --> user_input@{ shape: doc, label: "User Input:\n- CV - Job Offer" }
    user_input -- cv | job_offer --> OrchestratorAgent@{ shape: rect }
    OrchestratorAgent e1@-- cv --> CVLoaderAgent@{ shape: rect }
    e1@{ animation: fast }
    OrchestratorAgent e2@-- job_offer --> JobOfferSummarizerAgent
    e2@{ animation: fast }

    CVLoaderAgent --> JsonCV[(Json Resume CV)]
    JsonCV --> Tools@{ shape: das, label: "Tools:\n- Tool 1..." }
    Tools --> InitialWriterAgent
    Tools --> RefinementAgent

    job_offer --> CriticAgent
    JobOfferSummarizerAgent@{ shape: rect }
    JobOfferSummarizerAgent -- summarized_job_offer --> InitialWriterAgent@{ shape: rect }
    InitialWriterAgent -- draft_cv --> CriticAgent
    subgraph Loop refinement
        CriticAgent@{ shape: rect }
        CriticAgent -- cv_feedback, draft_cv --> RefinementAgent@{ shape: rect }
        RefinementAgent -- draft_cv --> CriticAgent
        exit_loop@{ shape: das, label: "exit_loop tool" } --> RefinementAgent
        RefinementAgent ~~~ exit_loop
    end
    
    RefinementAgent -- draft_cv --> enhanced_cv@{ shape: doc }
    enhanced_cv --> Stop@{ shape: dbl-circ }
```

# TODO

- [ ] Implement the agents
- [ ] Add a tool to get job descriptions from job offers
