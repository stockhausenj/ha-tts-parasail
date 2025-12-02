"""Test Parasail TTS integration with mocked API responses."""
import base64
import io
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


class MockResponse:
    """Mock aiohttp response for testing."""

    def __init__(self, status, sse_events):
        """Initialize mock response."""
        self.status = status
        self._sse_events = sse_events
        self._index = 0

    async def __aenter__(self):
        """Enter context manager."""
        return self

    async def __aexit__(self, *args):
        """Exit context manager."""
        pass

    async def text(self):
        """Return error text."""
        return "Error response"

    @property
    def content(self):
        """Return content iterator."""
        return self

    def __aiter__(self):
        """Return async iterator."""
        return self

    async def __anext__(self):
        """Return next line."""
        if self._index >= len(self._sse_events):
            raise StopAsyncIteration
        line = self._sse_events[self._index]
        self._index += 1
        return line.encode('utf-8')


def create_sse_audio_response():
    """Create a mock SSE response with audio data."""
    # Create a small WAV header
    wav_header = b'RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00'

    # Split into chunks and base64 encode
    chunk1 = base64.b64encode(wav_header[:8]).decode('utf-8')
    chunk2 = base64.b64encode(wav_header[8:]).decode('utf-8')

    sse_events = [
        'data: {"type":"start","priority":"normal"}',
        '',
        f'data: {{"type":"audio","chunk":1,"audio_content":"{chunk1}"}}',
        '',
        f'data: {{"type":"audio","chunk":2,"audio_content":"{chunk2}"}}',
        '',
    ]

    return MockResponse(200, sse_events)


def create_sse_error_response():
    """Create a mock SSE response with error."""
    sse_events = [
        'data: {"type":"error","message":"Invalid API key"}',
        '',
    ]

    return MockResponse(200, sse_events)


@pytest.mark.asyncio
async def test_tts_entity_async_get_tts_audio():
    """Test TTS entity audio generation."""
    # Import here to avoid issues if Home Assistant isn't installed
    import sys
    from pathlib import Path

    # Add custom_components to path
    repo_path = Path(__file__).parent.parent
    sys.path.insert(0, str(repo_path))

    try:
        from custom_components.parasail_tts.tts import ParasailTTSEntity
        from custom_components.parasail_tts.const import CONF_API_KEY, CONF_VOICE
    except ImportError as e:
        pytest.skip(f"Could not import integration: {e}")

    # Create mock config entry
    config_entry = MagicMock()
    config_entry.data = {
        CONF_API_KEY: "test_api_key",
        CONF_VOICE: "oai_nova",
    }
    config_entry.options = {}
    config_entry.entry_id = "test_entry"

    # Create TTS entity
    entity = ParasailTTSEntity(config_entry)
    entity.hass = MagicMock()

    # Mock the session
    mock_session = MagicMock()
    mock_response = create_sse_audio_response()
    mock_session.post.return_value = mock_response

    with patch('custom_components.parasail_tts.tts.async_get_clientsession', return_value=mock_session):
        result = await entity.async_get_tts_audio("Test message", "en", None)

    # Verify result
    assert result is not None
    assert isinstance(result, tuple)
    assert len(result) == 2

    audio_format, audio_data = result
    assert audio_format in ["wav", "mp3"]
    assert isinstance(audio_data, bytes)
    assert len(audio_data) > 0

    # Verify it's a WAV file
    assert audio_data[:4] == b'RIFF'

    print(f"✓ TTS entity test passed: {audio_format} format, {len(audio_data)} bytes")


@pytest.mark.asyncio
async def test_config_flow_validation():
    """Test config flow validation."""
    import sys
    from pathlib import Path

    # Add custom_components to path
    repo_path = Path(__file__).parent.parent
    sys.path.insert(0, str(repo_path))

    try:
        from custom_components.parasail_tts.config_flow import validate_input
        from custom_components.parasail_tts.const import CONF_API_KEY, CONF_VOICE
    except ImportError as e:
        pytest.skip(f"Could not import integration: {e}")

    # Create mock hass
    hass = MagicMock()

    # Mock the session
    mock_session = MagicMock()
    mock_response = create_sse_audio_response()
    mock_session.post.return_value = mock_response

    data = {
        CONF_API_KEY: "test_api_key",
        CONF_VOICE: "oai_nova",
    }

    with patch('custom_components.parasail_tts.config_flow.async_get_clientsession', return_value=mock_session):
        result = await validate_input(hass, data)

    # Verify result
    assert result is not None
    assert "title" in result
    assert "oai_nova" in result["title"]

    print(f"✓ Config flow validation test passed: {result['title']}")


@pytest.mark.asyncio
async def test_config_flow_error_handling():
    """Test config flow handles API errors."""
    import sys
    from pathlib import Path

    # Add custom_components to path
    repo_path = Path(__file__).parent.parent
    sys.path.insert(0, str(repo_path))

    try:
        from custom_components.parasail_tts.config_flow import validate_input, InvalidAuth
        from custom_components.parasail_tts.const import CONF_API_KEY, CONF_VOICE
    except ImportError as e:
        pytest.skip(f"Could not import integration: {e}")

    # Create mock hass
    hass = MagicMock()

    # Mock the session with error response
    mock_session = MagicMock()
    mock_response = create_sse_error_response()
    mock_session.post.return_value = mock_response

    data = {
        CONF_API_KEY: "invalid_key",
        CONF_VOICE: "oai_nova",
    }

    with patch('custom_components.parasail_tts.config_flow.async_get_clientsession', return_value=mock_session):
        with pytest.raises(InvalidAuth):
            await validate_input(hass, data)

    print("✓ Config flow error handling test passed")


if __name__ == "__main__":
    # Run tests directly
    import asyncio

    print("Running integration tests...\n")

    async def run_tests():
        """Run all tests."""
        try:
            await test_tts_entity_async_get_tts_audio()
            print()
            await test_config_flow_validation()
            print()
            await test_config_flow_error_handling()
            print("\n✅ All integration tests passed!")
        except Exception as e:
            print(f"\n❌ Test failed: {e}")
            import traceback
            traceback.print_exc()

    asyncio.run(run_tests())
