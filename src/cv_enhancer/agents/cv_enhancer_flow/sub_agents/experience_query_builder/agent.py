from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.genai import types

from ...tools.rag import GeminiEmbeddingFunction

PROMPT = f"""
You are a Query Builder Agent. Your task is to construct a search query
that will help retrieve relevant experiences from a resume database based
on the provided job requirements and technology stack.

Job offer summary:
{{summarized_job_offer}}

Please ensure that the query is tailored to the specific technologies
and skills mentioned in the job description. Additionally, consider the
candidate's experience level and relevant certifications.

The output should be a concise search query string that effectively captures
the key requirements and technologies needed for the job.

Consider the following when building the query:
- The database is a vector database containing experiences from resumes,
    including work experience, volunteer work, certifications, projects,
    skills, and interests.
- The documents were stored using the mode `RETRIEVAL_DOCUMENT` of the
    model `{GeminiEmbeddingFunction.EMBEDDING_MODEL}`.
- The query will be of type `RETRIEVAL_QUERY` and should be compatible
    with the same model.
- It is not necessary to include the year of experience or seniority level
    in the query.
- Return ONLY the search query string as the output, without any additional
    commentary or formatting.
"""

retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    initial_delay=1,
    max_delay=60,  # Maximum delay between retries
    exp_base=3,  # Delay multiplier
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)

experience_query_builder_model = Gemini(
    model="gemini-2.5-flash-lite-preview-09-2025",
    retry_options=retry_config,
)

experience_query_builder_agent = Agent(
    name="ExperienceQueryBuilderAgent",
    model=experience_query_builder_model,
    description="""An agent that builds search queries to retrieve relevant experiences
    from a resume database based on job requirements and technology stack.""",
    instruction=PROMPT,
    output_key="search_query",
)
