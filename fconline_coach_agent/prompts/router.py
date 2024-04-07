model_mapper = {
    "Soccer tactical coach who updates 'team tactics'": "team_tactic",
    "Soccer tactical coach who updates a 'player's personal tactics'": "indiv_tactic",
    """Questions regarding or opinions regarding the organization Nexon, FC Online, and FIFA Online.
      Questions containing profanity, questions that directly name people not related to soccer, 
      questions that require subjective evaluation and judgment of a person, institution, or organization.
      """: "not-allowed",
    "DEFAULT": "default",
}

prompt = """
Given a raw text input to a language model select the model prompt best suited for the input. You will be given the names of the available prompts and a description of what the prompt is best suited for. You may also revise the original input if you think that revising it will ultimately lead to a better response from the language model.

<< FORMATTING >>
Return a markdown code snippet with a JSON object formatted to look like:
```json
{{
    "destination": string \ name of the prompt to use or "DEFAULT"
    "next_inputs": string \ a potentially modified version of the original input (in Korean)
}}
```

REMEMBER: "destination" MUST be one of the candidate prompt names specified below OR it can be "DEFAULT" if the input is not well suited for any of the candidate prompts.
REMEMBER: "next_inputs" can just be the original input if you don't think any modifications are needed.

<< CANDIDATE PROMPTS >>

Soccer tactical coach who updates 'team tactics': A coach who updates settings that adjust the team's overall movements (aggressiveness, width, width, pressure level, etc.)
Soccer tactical coach who updates a 'player's personal tactics': A coach who updates settings to adjust personal tactics (e.g. degree of overlap, degree of freedom, attacking style such as penetration or crossing, etc.) for a specific player or position


<< INPUT >>
{input}

<< OUTPUT (must include ```json at the start of the response) >>
<< OUTPUT (must end with ```) >>
"""

DEFAULT_MULTI_SELECT_PROMPT_TMPL = (
    "Some choices are given below. It is provided in a numbered "
    "list (1 to {num_choices}), "
    "where each item in the list corresponds to a summary.\n"
    "---------------------\n"
    "{context_list}"
    "\n---------------------\n"
    "Using only the choices above and not prior knowledge, return the top choices "
    "(no more than {max_outputs}, but only select what is needed) that "
    "are most relevant to the question: '{query_str}'\n"
)

multi_prompt = """
Given a raw text input to a language model select the model prompt top-{max_outputs} best suited for the input (no more than {max_outputs}, but only select what is needed). You will be given the names of the available prompts and a description of what the prompt is best suited for. You may also revise the original input if you think that revising it will ultimately lead to a better response from the language model.

<< FORMATTING >>
Return a markdown code snippet with a JSON object formatted to look like (ex. top-2):
```json
[
    {{
        "destination": string \ name of the prompt to use or "DEFAULT"
        "next_inputs": string \ a potentially modified version of the original input (in Korean)
    }},
    {{
        "destination": string \ name of the prompt to use or "DEFAULT"
        "next_inputs": string \ a potentially modified version of the original input (in Korean)
    }}
]
```

REMEMBER: "destination" MUST be one of the candidate prompt names specified below OR it can be "DEFAULT" if the input is not well suited for any of the candidate prompts.
REMEMBER: "next_inputs" can just be the original input if you don't think any modifications are needed.

<< CANDIDATE PROMPTS >>

Soccer tactical coach who updates 'team tactics': A coach who updates settings that adjust the team's overall movements (aggressiveness, width, width, pressure level, etc.)
Soccer tactical coach who updates a 'player's personal tactics': A coach who updates settings to adjust personal tactics (e.g. degree of overlap, degree of freedom, attacking style such as penetration or crossing, etc.) for a specific player or position


<< INPUT >>
{input}

<< OUTPUT (must include ```json at the start of the response) >>
<< OUTPUT (must end with ```) >>
)
"""
