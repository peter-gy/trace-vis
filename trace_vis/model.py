import dataclasses
import datetime


@dataclasses.dataclass(frozen=True, kw_only=True)
class TraceHop:
    hop: int
    domain: str
    ip: str
    time_ms: float

    def as_dict(self) -> dict:
        return dict(hop=self.hop,
                    domain=self.domain,
                    ip=self.ip,
                    time_ms=self.time_ms)


@dataclasses.dataclass(frozen=True, kw_only=True)
class TraceRun:
    target: str
    date: datetime.datetime
    hops: list[TraceHop]

    def as_dict(self) -> dict:
        return dict(target=self.target,
                    date=self.date.isoformat(),
                    hops=[hop.as_dict() for hop in self.hops])
