from pydantic import BaseModel

from fconline_coach_agent import constant, models, utils, verifier
from fconline_coach_agent.prompts import casual, indiv_updater, parser, router, updater


class AgentOutput(BaseModel):
    answer: str
    mode: str


class AudioAgent(models.BaseAgent):
    def __init__(self) -> None:
        super().__init__()

    def run(self, query: str) -> str:
        prompt: str = parser.prompt.format(input=query)
        return self._client.run(question=prompt)[0]


class Router(models.BaseAgent):
    def __init__(self, friendly: bool = False) -> None:
        super().__init__()
        self._friendly = friendly

    def run(self, query: str) -> dict | str:
        prompt: str = router.prompt.format(input=query)
        cnt = 0
        while cnt < self._tol:
            json_data = self._client.run(question=prompt)[0]
            if verifier.router_verifier(json_data, friendly=self._friendly):
                parsed = utils.convert_markdownjson_to_json(json_data)
                if isinstance(parsed, dict):
                    return parsed
            cnt += 1
        raise ValueError(constant.ROUTER_ERR)


class MultiRouter(models.BaseAgent):
    def __init__(self, friendly: bool = False) -> None:
        super().__init__()
        self._friendly = friendly

    def run(self, query: str) -> list[dict] | str:
        prompt: str = router.multi_prompt.format(input=query, max_outputs=2)
        cnt = 0
        while cnt < self._tol:
            json_data = self._client.run(question=prompt)[0]
            if verifier.router_verifier(json_data, multi=True, friendly=self._friendly):
                parsed = utils.convert_markdownjson_to_json(json_data)
                if isinstance(parsed, list) and isinstance(parsed[0], dict):
                    return parsed
            cnt += 1
        raise ValueError(constant.ROUTER_ERR)


class IndivTacticUpdater(models.BaseAgent):
    def __init__(self, mode: str = "json") -> None:
        super().__init__()
        self._mode = mode

    def run(self, query: str, formation: str) -> str:
        if self._mode == "json":
            msg = indiv_updater.get_json_only_prompt(query, formation)
        else:
            msg = indiv_updater.get_full_narrative_prompt(query, formation)
        cnt = 0
        while cnt < self._tol:
            results = models.ModelClient().run(
                question=msg,
                model=constant.LONG_MODEL_NM,
                temperature=constant.TEMPERATURE,
            )[0]
            if verifier.indiv_tactic_output_verifier(results, mode=self._mode):
                return results.replace(constant.SEPERATOR, "")
            cnt += 1
        raise ValueError(constant.INDIV_TACTIC_ERR)


class TeamTacticUpdater(models.BaseAgent):
    def __init__(self, mode: str = "json") -> None:
        super().__init__()
        self._mode = mode

    def run(self, query: str, current_tactic: str) -> str:
        if self._mode == "json":
            msg = updater.get_json_only_prompt(
                query=query, current_tactic=current_tactic
            )
        else:
            msg = updater.get_full_narrative_prompt(
                query=query, current_tactic=current_tactic
            )
        cnt = 0
        while cnt < self._tol:
            results = models.ModelClient().run(
                question=msg,
                model=constant.LONG_MODEL_NM,
                temperature=constant.TEMPERATURE,
            )[0]
            if verifier.team_tactic_output_verifier(results, mode=self._mode):
                return results.replace(constant.SEPERATOR, "")
            cnt += 1
        raise ValueError(constant.TEAM_TACTIC_ERR)


class CasualTalker(models.BaseAgent):
    def __init__(self, tol: int = 5) -> None:
        super().__init__(tol)

    def run(self, query: str) -> str:
        cnt = 0
        while cnt < self._tol:
            try:
                results = models.ModelClient().run(
                    question=casual.prompt.format(question=query),
                    model=constant.MODEL_NM,
                    temperature=constant.TEMPERATURE,
                )[0]
                return results
            except Exception:
                cnt += 1
        raise ValueError(constant.CHATBOT_ERR)


def run_tactic_updater(args) -> AgentOutput:
    query, current_tactic, formation, mode = args
    match mode:
        case "team_tactic":
            result = TeamTacticUpdater("narrative").run(
                query=query, current_tactic=current_tactic
            )
        case "indiv_tactic":
            result = IndivTacticUpdater("narrative").run(
                query=query, formation=formation
            )
        case "default":
            result = CasualTalker().run(query=query)
        case _:
            raise ValueError(
                "mode는 'team_tactic', 'indiv_tactic', 'default' 중 하나여야 합니다."
            )

    return AgentOutput(answer=result, mode=mode)


class MultiAgent:
    def __init__(self, query: str, current_tactic: str, parallel: bool = False) -> None:
        self._is_valid_input = verifier.verify_input(query, current_tactic)
        self._current_tactic = current_tactic
        self._query = query
        self._current_tactic = current_tactic
        self._parallel = parallel

    def update(self) -> list[AgentOutput]:
        if self._is_valid_input is False:
            return [AgentOutput(answer=constant.INVALID_QUERY_ERR, mode="default")]

        routes = MultiRouter().run(self._query)
        if isinstance(routes, str):
            raise ValueError(f"Invalid Router result : {routes}")  # error message

        tasks = [
            (
                resp["next_inputs"],
                self._current_tactic.strip(),
                next(
                    data
                    for data in utils.convert_markdownjson_to_json(self._current_tactic)
                    if "포메이션" in data
                )["포메이션"],
                router.model_mapper[resp["destination"]],
            )
            for resp in routes  # [(query, current_tactic, formation, mode)]
        ]

        return [run_tactic_updater(task) for task in tasks]
