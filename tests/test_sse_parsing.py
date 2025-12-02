"""Test SSE parsing and base64 decoding."""
import base64
import json


def test_sse_event_parsing():
    """Test parsing of SSE event format."""
    # Simulate an SSE event line
    sse_line = 'data: {"type":"audio","chunk":1,"audio_content":"UklGRg=="}'

    # Parse as our code does
    if sse_line.startswith('data: '):
        json_data = sse_line[6:]  # Remove "data: " prefix
        event = json.loads(json_data)

        assert event['type'] == 'audio'
        assert event['chunk'] == 1
        assert 'audio_content' in event


def test_base64_decoding():
    """Test base64 decoding of audio content."""
    # RIFF header in base64
    riff_base64 = base64.b64encode(b'RIFF').decode('utf-8')

    # Decode as our code does
    decoded = base64.b64decode(riff_base64)

    assert decoded == b'RIFF'


def test_chunk_concatenation():
    """Test concatenating multiple audio chunks."""
    # Simulate multiple chunks
    chunk1 = b'RIFF'
    chunk2 = b'test'
    chunk3 = b'data'

    chunks = [chunk1, chunk2, chunk3]
    result = b''.join(chunks)

    assert result == b'RIFFtestdata'
    assert len(result) == 12
