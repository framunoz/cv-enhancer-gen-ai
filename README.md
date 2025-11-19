# cv-enhancer-gen-ai

```mermaid
flowchart TD
    A[User Uploads CV] --> JsonCV[(Json Resume CV)]
    JsonCV --> Tools@{ shape: das, label: "Tools:\n- Tool 1\n- Tool 2" }
    Tools --> InitialWriterAgent
    Tools --> RefinementAgent

    Input@{ shape: sl-rect, label: "Input CV Formats" }
    Input --> CriticAgent
    Input --> JobOfferSummAgent@{ shape: rect, label: "Job Offer Summarizer Agent" }
    JobOfferSummAgent -- summarized_job_offer --> InitialWriterAgent@{ shape: rect, label: "Initial Writer Agent" }
    InitialWriterAgent -- draft_cv --> CriticAgent
    subgraph Loop refinement
        CriticAgent@{ shape: rect, label: "Critic Agent" }
        CriticAgent -- cv_feedback, draft_cv --> RefinementAgent@{ shape: rect, label: "Refinement Agent" }
        RefinementAgent -- draft_cv --> CriticAgent
        Exit@{ shape: das, label: "exit_loop tool" } --> RefinementAgent
    end
    
    RefinementAgent -- draft_cv --> FinalCV@{ shape: doc, label: "Final Enhanced CV" }
```

# TODO

- [ ] Implement the agents
- [ ] Add a tool to get job descriptions from job offers

    JobOfferSummAgent -- summarized_job_offer --> WriterAgents@{ shape: processes, label: "Writer Agents" }
