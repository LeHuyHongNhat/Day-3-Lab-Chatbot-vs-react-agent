from typing import Dict, Any, List, Optional
from src.telemetry.logger import logger

class PerformanceTracker:
    """
    Tracking industry-standard metrics for LLMs.
    """
    def __init__(self):
        self.session_metrics = []

    def track_request(
        self,
        provider: str,
        model: str,
        usage: Dict[str, int],
        latency_ms: int,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Logs a single request metric to our telemetry.
        """
        metric = {
            "provider": provider,
            "model": model,
            "prompt_tokens": usage.get("prompt_tokens", 0),
            "completion_tokens": usage.get("completion_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0),
            "latency_ms": latency_ms,
            "cost_estimate": self._calculate_cost(model, usage) # Mock cost calculation
        }
        if metadata:
            metric.update(metadata)

        self.session_metrics.append(metric)
        logger.log_event("LLM_METRIC", metric)

    def get_summary(self) -> Dict[str, Any]:
        """
        Returns aggregate metrics from this process session.
        """
        if not self.session_metrics:
            return {
                "requests": 0,
                "avg_latency_ms": 0,
                "max_latency_ms": 0,
                "total_tokens": 0,
                "total_cost_estimate": 0.0,
                "by_provider": {},
            }

        latencies = [m.get("latency_ms", 0) for m in self.session_metrics]
        total_tokens = sum(m.get("total_tokens", 0) for m in self.session_metrics)
        total_cost = sum(m.get("cost_estimate", 0.0) for m in self.session_metrics)

        by_provider: Dict[str, Dict[str, Any]] = {}
        for m in self.session_metrics:
            provider = m.get("provider", "unknown")
            if provider not in by_provider:
                by_provider[provider] = {
                    "requests": 0,
                    "total_tokens": 0,
                    "avg_latency_ms": 0,
                    "max_latency_ms": 0,
                }

            provider_bucket = by_provider[provider]
            provider_bucket["requests"] += 1
            provider_bucket["total_tokens"] += m.get("total_tokens", 0)
            provider_bucket["max_latency_ms"] = max(provider_bucket["max_latency_ms"], m.get("latency_ms", 0))

        for provider, bucket in by_provider.items():
            provider_latencies = [
                m.get("latency_ms", 0) for m in self.session_metrics if m.get("provider", "unknown") == provider
            ]
            if provider_latencies:
                bucket["avg_latency_ms"] = int(sum(provider_latencies) / len(provider_latencies))

        return {
            "requests": len(self.session_metrics),
            "avg_latency_ms": int(sum(latencies) / len(latencies)),
            "max_latency_ms": max(latencies),
            "total_tokens": total_tokens,
            "total_cost_estimate": round(total_cost, 6),
            "by_provider": by_provider,
        }

    def _calculate_cost(self, model: str, usage: Dict[str, int]) -> float:
        """
        TODO: Implement real pricing logic.
        For now, returns a dummy constant.
        """
        return (usage.get("total_tokens", 0) / 1000) * 0.01

# Global tracker instance
tracker = PerformanceTracker()
