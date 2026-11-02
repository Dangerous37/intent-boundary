import re


def tokens(text):
    return frozenset(re.findall(r"\w+", text.casefold()))


def evaluate(data):
    seen, splits = set(), {}
    for split in ("train", "calibration", "test"):
        rows = []
        for row in data[split]:
            words, label = tokens(row["text"]), row["intent"]
            if not words or words in seen:
                raise ValueError("empty or overlapping normalized sample")
            if label is not None and (not isinstance(label, str) or not label):
                raise ValueError("invalid label")
            if split == "train" and label is None:
                raise ValueError("training examples need an intent")
            seen.add(words)
            rows.append((words, label))
        if not rows:
            raise ValueError("empty split")
        splits[split] = rows
    labels = {label for _,label in splits["train"]}
    def score(words):
        options = [(len(words & sample)/len(words | sample), label) for sample,label in splits["train"]]
        return min(options, key=lambda item: (-item[0], item[1]))
    def scored(split):
        result = []
        for words, label in splits[split]:
            if label is not None and label not in labels:
                raise ValueError("unsupported evaluation label")
            value, prediction = score(words)
            result.append((value, prediction, label))
        return result
    calibration = scored("calibration")
    candidates = {value for value,_,_ in calibration} | {1.0}
    def accuracy(cutoff):
        return sum((p if v > 0 and v >= cutoff else None) == a for v,p,a in calibration)
    threshold = max(candidates, key=lambda cutoff: (accuracy(cutoff), cutoff))
    rows = [{"actual": a, "score": v, "prediction": p if v > 0 and v >= threshold else None}
            for v,p,a in scored("test")]
    return {"threshold": threshold, "cases": rows,
            "false_accepts": sum(r["actual"] is None and r["prediction"] is not None for r in rows),
            "correct": sum(r["actual"] == r["prediction"] for r in rows)}
