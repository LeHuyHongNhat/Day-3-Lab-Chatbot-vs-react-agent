import json
import os
from collections import defaultdict
from datetime import datetime


def load_metric_events(log_path: str):
    events = []
    if not os.path.exists(log_path):
        return events

    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError:
                continue

            if payload.get("event") == "LLM_METRIC":
                events.append(payload.get("data", {}))

    return events


def summarize(events):
    if not events:
        return {
            "requests": 0,
            "avg_latency_ms": 0,
            "max_latency_ms": 0,
            "total_tokens": 0,
            "total_cost_estimate": 0.0,
            "providers": {},
        }

    total_latency = sum(int(e.get("latency_ms", 0)) for e in events)
    max_latency = max(int(e.get("latency_ms", 0)) for e in events)
    total_tokens = sum(int(e.get("total_tokens", 0)) for e in events)
    total_cost = sum(float(e.get("cost_estimate", 0.0)) for e in events)

    providers = defaultdict(lambda: {
        "requests": 0,
        "avg_latency_ms": 0,
        "max_latency_ms": 0,
        "total_tokens": 0,
    })

    for e in events:
        p = e.get("provider", "unknown")
        providers[p]["requests"] += 1
        providers[p]["total_tokens"] += int(e.get("total_tokens", 0))
        providers[p]["max_latency_ms"] = max(providers[p]["max_latency_ms"], int(e.get("latency_ms", 0)))

    for p in providers:
        p_events = [int(e.get("latency_ms", 0)) for e in events if e.get("provider", "unknown") == p]
        providers[p]["avg_latency_ms"] = int(sum(p_events) / len(p_events)) if p_events else 0

    return {
        "requests": len(events),
        "avg_latency_ms": int(total_latency / len(events)),
        "max_latency_ms": max_latency,
        "total_tokens": total_tokens,
        "total_cost_estimate": round(total_cost, 6),
        "providers": dict(providers),
    }


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    default_log = os.path.join("logs", f"{today}.log")
    log_path = os.getenv("LAB_LOG_PATH", default_log)

    events = load_metric_events(log_path)
    report = summarize(events)

    print("=" * 60)
    print("Telemetry Summary")
    print("=" * 60)
    print(f"Log file       : {log_path}")
    if not os.path.exists(log_path):
        print("Status         : Log file not found yet. Run chatbot/agent first to generate logs.")
        return
    print(f"Requests       : {report['requests']}")
    print(f"Avg latency    : {report['avg_latency_ms']} ms")
    print(f"Max latency    : {report['max_latency_ms']} ms")
    print(f"Total tokens   : {report['total_tokens']}")
    print(f"Total cost est.: ${report['total_cost_estimate']}")

    print("\nBy provider")
    for provider, data in report["providers"].items():
        print(
            f"- {provider}: requests={data['requests']}, "
            f"avg_latency_ms={data['avg_latency_ms']}, "
            f"max_latency_ms={data['max_latency_ms']}, "
            f"total_tokens={data['total_tokens']}"
        )


if __name__ == "__main__":
    main()
