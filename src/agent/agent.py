import re
import time
from typing import List, Dict, Any, Optional
from src.core.llm_provider import LLMProvider
from src.telemetry.logger import logger
from src.tools import execute_tool

class ReActAgent:
    """
    ReAct-style Agent following the Thought → Action → Observation loop.
    Supports: search_arxiv, get_paper_abstract, alpha_formatter,
              performance_monitor (BONUS), guardrail_validator.
    """

    def __init__(self, llm: LLMProvider, tools: List[Dict[str, Any]], max_steps: int = 10):
        self.llm = llm
        self.tools = tools
        self.max_steps = max_steps
        self.history = []

    # ------------------------------------------------------------------
    # System Prompt
    # ------------------------------------------------------------------

    def get_system_prompt(self) -> str:
        tool_descriptions = "\n".join(
            [f"  - {t['name']}: {t['description']}" for t in self.tools]
        )
        return f"""You are an expert quantitative finance research assistant.
You follow the ReAct reasoning framework strictly.

Available tools:
{tool_descriptions}

Output format for EVERY step (never skip Thought):
Thought: <your reasoning about what to do next>
Action: <tool_name>(param_name="value")
Observation: <system will fill this in>

CRITICAL — always use the exact parameter names shown in each tool description:
- search_arxiv(query="your keywords")
- get_paper_abstract(paper_id="2401.12345")
- alpha_formatter(text="full paper text here")

Repeat Thought/Action/Observation until you have all information needed.
When finished, write:
Final Answer: <your complete response>

Operational rules:
1. Always start with search_arxiv to find relevant papers.
2. Call get_paper_abstract for EACH paper found to obtain its abstract.
3. Call alpha_formatter with the raw abstract to produce structured JSON.
   If alpha_formatter returns a validation error, fix the input and retry.
4. Call guardrail_validator on the final JSON before writing Final Answer.
5. Never fabricate paper IDs or abstracts — only use data from Observations.
"""

    # ------------------------------------------------------------------
    # Main ReAct Loop
    # ------------------------------------------------------------------

    def run(self, user_input: str) -> str:
        logger.log_event("AGENT_START", {"input": user_input, "model": self.llm.model_name})

        scratchpad = user_input
        steps = 0

        while steps < self.max_steps:
            step_start = time.time()

            result = self.llm.generate(scratchpad, system_prompt=self.get_system_prompt())
            response_text = result["content"]
            step_latency_ms = int((time.time() - step_start) * 1000)

            logger.log_event("AGENT_STEP", {
                "step": steps + 1,
                "latency_ms": step_latency_ms,
                "tokens": result.get("usage", {}),
                "preview": response_text[:300],
            })

            self._call_performance_monitor(
                step=steps + 1,
                latency_ms=step_latency_ms,
                usage=result.get("usage", {}),
            )

            # ── Final Answer ──────────────────────────────────────────
            if "Final Answer:" in response_text:
                final = response_text.split("Final Answer:", 1)[-1].strip()
                logger.log_event("AGENT_END", {"steps": steps + 1, "status": "success"})
                return final

            # ── Parse & Execute Action ────────────────────────────────
            action_match = re.search(
                r"Action:\s*(\w+)\(([^)]*)\)", response_text, re.DOTALL
            )
            if action_match:
                tool_name = action_match.group(1).strip()
                args_str = action_match.group(2).strip()
                observation = self._execute_tool(tool_name, args_str)

                logger.log_event("TOOL_CALL", {
                    "tool": tool_name,
                    "args": args_str,
                    "observation": str(observation)[:400],
                })

                scratchpad += f"\n{response_text}\nObservation: {observation}"
            else:
                # No action found — append response and continue
                scratchpad += f"\n{response_text}"

            steps += 1
            
        logger.log_event("AGENT_END", {"steps": steps})
        return "Not implemented. Fill in the TODOs!"

    def _execute_tool(self, tool_name: str, args: str) -> str:
        """
        Helper method to execute tools by name.
        """
        for tool in self.tools:
            if tool['name'] == tool_name:
                # TODO: Implement dynamic function calling or simple if/else
                return f"Result of {tool_name}"
        return f"Tool {tool_name} not found."
