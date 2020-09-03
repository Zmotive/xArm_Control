from dataclasses import dataclass


@dataclass(frozen=True)
class CmdTuple:
    cmdVal: int
    len: int
    motorId: int = 0
    has_callback: bool = False
