import sys
from logging import Formatter, Logger, StreamHandler, getLogger
from typing import Any
import json
import socket
from dataclasses import dataclass, asdict, fields, replace, is_dataclass, field
import select

from models.models import BallData, Shot

@dataclass
class GSProPlayer:
    Handed: str | None = None
    Club: str | None = None
    DistanceToTarget: float | None = None


@dataclass
class GSProMessage:
    Code: int
    Message: str | None = None
    Player: GSProPlayer | None = None
    Xtra: dict = field(default_factory=dict)  # other attributes passed through in extra

    @classmethod
    def create_from_dict(cls, dct: dict[str, Any]) -> "GSProMessage":
        dct = dict(dct)
        kwargs = {}
        for f in fields(cls):
            if f.name in dct:
                kwargs[f.name] = dct.pop(f.name)
        kwargs["Xtra"] = dct
        return cls(**kwargs)


class GSProSession:

    def __init__(self, gspro_host="127.0.0.1", gspro_port=921):
        self.gspro_host = gspro_host
        self.gspro_port = gspro_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.shots_and_responses = []

        self.__logger = Logger(__name__).get_logger()

        self.__logger.info(f"connecting to gspro {self.gspro_host}:{self.gspro_port}")
        self.sock.connect((self.gspro_host, self.gspro_port))
        self.__logger.info(f"{self.sock=}")

    def send_heartbeat(self):
        self.send_shot(Shot.heartbeat())

    def recv_data(self):
        self.__logger.info("receiving response")
        resp_bytes = self.sock.recv(2048)
        self.__logger.info(f"recv msg size: {len(resp_bytes)}")
        msgs = [GSProMessage.create(dct) for dct in parse_gspro_data(resp_bytes)]
        self.shots_and_responses.extend(msgs)
        self.__logger.info(resp_bytes)

    def send_shot(self, golfshot: Shot):
        self.__logger.info(f"sending {golfshot=}")
        shot_data = golfshot.as_msg()
        self.__logger.info(f"---------- {golfshot.ShotNumber} ------------")
        self.__logger.info(shot_data)
        self.__logger.info("----------------------------------------------")
        self.shots_and_responses.append(golfshot)
        nbytes_sent = self.sock.send(shot_data)

        if len(shot_data) != nbytes_sent:
            raise ValueError(f"{len(shot_data)=} {nbytes_sent=}")

    def data_available(self) -> bool:
        self.__logger.info(f"checking data avail")
        r, _, _ = select.select([self.sock], [], [], 0)
        self.__logger.info(f"{r=}")
        self.__logger.info(f"{self.sock in r=}")
        return self.sock in r

    def close(self):
        self.sock.close()

def asdict_ignore_none(obj) -> dict[str, Any]:
    """Like dataclasses.asdict ignoring keys whose value is None

    :param obj: an instance of a Dataclass
    :return: a dict without any None values

    Examples:

        assert (
          asdict_ignore_none(ShotDataOptions())
          == {'ContainsBallData': True, 'ContainsClubData': False}
        )
        assert (
          asdict_ignore_none(ShotDataOptions(IsHeartbeat=False))
          == {'ContainsBallData': True, 'ContainsClubData': False, 'IsHeartbeat': False}
        )

    """

    assert is_dataclass(obj)
    result = dict()
    for f in fields(obj):
        val = getattr(obj, f.name)
        if val is not None:
            if is_dataclass(val):
                result[f.name] = asdict_ignore_none(val)
            else:
                result[f.name] = val
    return result


def parse_gspro_data(data: bytes) -> list[dict[str, Any]]:
    """Parse data from gspro into a list of json decoded objects

    :param resp: chunk of data received from gspro
    :return: list of json decoded objects

    Example:
        data = bytes('{"Code":200,"Message":"Ball Data received","Player":null}{"Code":201,"Message":"GSPro Player Information","Player":{"Handed":"RH","Club":"DR","DistanceToTarget":380.0}}{"Code":202,"Message":"GSPro ready","Player":null}{"Code":203,"Message":"GSPro round ended","Player":null}',
                     encoding="utf8")
        msgs = parse_gspro_data(data)
        print(len(msgs))  # 4
        print(msgs[0])    # {"Code': 200, 'Message': 'Ball Data received', 'Player': None}
        print(msgs[1])    # {'Code': 201, 'Message': 'GSPro Player Information', 'Player': {'Handed': 'RH', 'Club': 'DR', 'DistanceToTarget': 380.0}}
        print(msgs[2])    # {'Code': 202, 'Message': 'GSPro ready', 'Player': None}
        print(msgs[3])    # {'Code': 203, 'Message': 'GSPro round ended', 'Player': None}

    """

    data = data.decode()  # convert to str
    len_processed = 0
    result = []

    while len_processed < len(data):
        assert data[len_processed] == "{", f"{len_processed=} {data[len_processed]=}"
        msg = None
        start = len_processed
        while msg is None:
            idx_of_close_bracket = data.find("}", start)
            substr = data[len_processed: idx_of_close_bracket+1]
            # print(f"trying {start=} {idx_of_close_bracket=} {substr=}")
            try:
                msg = json.loads(substr)
                # print(f"parsed {len(substr)} bytes {substr=}")
            except json.decoder.JSONDecodeError:
                start = start + len(substr)
        result.append(msg)
        len_processed = len_processed + len(substr)
    return result


def test_serialize():
    hb = Shot.heartbeat()
    hb_dct = asdict_ignore_none(hb)

    assert "BallData" not in hb_dct
    assert hb_dct["ShotDataOptions"]["IsHeartbeat"]


def test_resp():
    data = bytes(
        '{"Code":200,"Message":"Ball Data received","Player":null}{"Code":201,"Message":"GSPro Player Information","Player":{"Handed":"RH","Club":"DR","DistanceToTarget":380.0}}{"Code":202,"Message":"GSPro ready","Player":null}{"Code":203,"Message":"GSPro round ended","Player":null}',
        encoding="utf8")
    msgs = parse_gspro_data(data)
    assert len(msgs) == 4

    objs = [GSProMessage.create_from_dict(dct) for dct in msgs]
    assert len(objs) == 4

    for msg, obj in zip(msgs, objs):
        print(msg)
        assert msg["Code"] == obj.Code
        assert msg["Message"] == obj.Message
        if msg["Player"] is None:
            assert obj.Player is None
