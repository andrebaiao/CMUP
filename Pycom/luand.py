def encodePayload(m_type, day, hour, minute, flag, delay=0):
    assert 0 <= m_type <= 3
    assert 0 <= day <= 6
    assert 0 <= hour <= 24
    assert 0 <= minute <= 60
    assert 0 <= flag <= 1  # type=3 (set/downlink) -> flag=0:add,flag=1:rm; #type=1 (info) -> flag=0:on_time;flag=1:has_delay [check delay]
    assert 0 <= delay <= 120

    payload_meta = 0
    payload_meta |= (m_type << 22)

    payload_meta |= (day << 19)

    payload_meta |= (hour << 14)

    payload_meta |= (minute << 8)

    payload_all = payload_meta

    payload_all |= (flag << 7)

    payload_all |= (delay << 0)

    return payload_all


def decodePayload(payload: bytes):  # Note: assumes 3 bytes
    unbyted = int.from_bytes(payload, "little")

    u_type = ((((2 ** 2) - 1) << 22) & unbyted) >> 22

    u_day = ((((2 ** 3) - 1) << 19) & unbyted) >> 19

    u_hour = ((((2 ** 5) - 1) << 14) & unbyted) >> 14

    u_min = ((((2 ** 6) - 1) << 8) & unbyted) >> 8

    u_flag = ((((2 ** 1) - 1) << 7) & unbyted) >> 7

    u_delay = ((((2 ** 7) - 1) << 0) & unbyted) >> 0

    return u_type, u_day, u_hour, u_min, u_flag, u_delay


if __name__ == "__main__":
    print(encodePayload(3, 6, 24, 60, 1, 120))
    print(decodePayload(encodePayload(3, 6, 24, 60, 1, 120).to_bytes(3, 'little')))
