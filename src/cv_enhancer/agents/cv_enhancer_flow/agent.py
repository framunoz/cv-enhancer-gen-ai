from google.adk.agents import SequentialAgent

from .sub_agents import (
    enhanced_cv_assembly_agent,
    experience_enhancement_orchestrator_agent,
    experience_query_builder_agent,
    experience_retriever_agent,
    job_offer_analyzer_agent,
)

root_agent = SequentialAgent(
    name="CvEnhancerFlowAgent",
    description="A flow that enhances a CV based on a job offer.",
    sub_agents=[
        job_offer_analyzer_agent,
        experience_query_builder_agent,
        experience_retriever_agent,
        experience_enhancement_orchestrator_agent,
        enhanced_cv_assembly_agent,
    ],
)
