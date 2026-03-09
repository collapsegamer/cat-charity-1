from typing import Any, Iterable, List


def invest(
        target: Any,
        sources: Iterable[Any]
) -> List[Any]:
    modified = [target]
    for source in sources:
        invested_amount = min(
            target.full_amount - target.invested_amount,
            source.full_amount - source.invested_amount
        )
        for obj in (target, source):
            obj.invested_amount += invested_amount
            obj.recalculate_state()
        modified.append(source)
        if target.fully_invested:
            break
    return modified
