import talon

if hasattr(talon, "test_mode"):
    # Only include this when we're running tests

    import json
    import sys

    import pytest

    from apps.windows_hinting import windows_hinting_pipe as pipe

    class FakeTransport:
        """Replays a canned response and records what was written."""

        def __init__(self, response: bytes = b"", error: Exception = None):
            self.response = response
            self.error = error
            self.written = b""
            self.closed = False

        def write(self, data: bytes) -> None:
            self.written += data

        def read_line(self, deadline: float, max_bytes: int) -> bytes:
            if self.error:
                raise self.error
            request_id = json.loads(self.written)["id"]
            return self.response.replace(b"$ID", request_id.encode())

        def close(self) -> None:
            self.closed = True

    def call_with(transport, command="ping", args=None):
        return pipe.call(command, args, transport_factory=lambda timeout: transport)

    def test_request_framing():
        line = pipe.encode_request("select", ["AB", "right"], "x-1")
        assert line.endswith(b"\n") and line.count(b"\n") == 1
        assert json.loads(line) == {
            "protocol": 1,
            "command": "select",
            "args": ["AB", "right"],
            "id": "x-1",
        }

    def test_call_returns_response_and_closes():
        transport = FakeTransport(
            b'{"protocol":1,"id":"$ID","ok":true,"code":"OK","message":"",'
            b'"data":{"active":true,"hintCount":3}}'
        )
        response = call_with(transport, "status")
        assert response["data"] == {"active": True, "hintCount": 3}
        assert json.loads(transport.written)["command"] == "status"
        assert transport.closed

    def test_server_error_maps_to_code():
        transport = FakeTransport(
            b'{"protocol":1,"id":"$ID","ok":false,"code":"ERR_LABEL_NOT_FOUND","message":"nope"}'
        )
        with pytest.raises(pipe.WindowsHintingError) as e:
            call_with(transport, "select", ["ZZ"])
        assert e.value.code == "ERR_LABEL_NOT_FOUND"
        assert e.value.message == "nope"
        assert transport.closed

    def test_mismatched_id_rejected():
        transport = FakeTransport(b'{"protocol":1,"id":"other","ok":true,"code":"OK"}')
        with pytest.raises(pipe.WindowsHintingError) as e:
            call_with(transport)
        assert e.value.code == "CLIENT_BAD_RESPONSE"

    def test_garbage_response_rejected():
        with pytest.raises(pipe.WindowsHintingError) as e:
            call_with(FakeTransport(b"not json"))
        assert e.value.code == "CLIENT_BAD_RESPONSE"

    def test_transport_error_still_closes():
        transport = FakeTransport(error=pipe.WindowsHintingError("CLIENT_TIMEOUT"))
        with pytest.raises(pipe.WindowsHintingError):
            call_with(transport)
        assert transport.closed

    def test_normalize_label():
        assert pipe.normalize_label("a b") == "AB"
        assert pipe.normalize_label(" c ") == "C"

    def test_fallback_keys_cover_actions():
        assert set(pipe.FALLBACK_ACTION_KEYS) == set(pipe.SELECT_ACTIONS) - {""}

    @pytest.mark.skipif(sys.platform != "win32", reason="Windows only")
    def test_current_user_sid_format():
        sid = pipe.current_user_sid()
        assert sid.startswith("S-1-5-")
        assert pipe.pipe_name() == r"\\.\pipe\WindowsHinting-" + sid
