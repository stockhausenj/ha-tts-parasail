"""Standalone test for Parasail TTS integration."""
import asyncio
import base64
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch


# Add custom_components to path
repo_path = Path(__file__).parent.parent
sys.path.insert(0, str(repo_path))


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


async def test_tts_entity():
    """Test TTS entity audio generation."""
    print("Test 1: TTS Entity Audio Generation")
    print("-" * 50)

    try:
        from custom_components.parasail_tts.tts import ParasailTTSEntity
        from custom_components.parasail_tts.const import CONF_API_KEY, CONF_VOICE, CONF_MODEL, DEFAULT_MODEL
    except ImportError as e:
        print(f"❌ Failed to import integration: {e}")
        return False

    # Create mock config entry
    config_entry = MagicMock()
    config_entry.data = {
        CONF_API_KEY: "test_api_key",
        CONF_VOICE: "oai_nova",
        CONF_MODEL: DEFAULT_MODEL,
    }
    config_entry.options = {}
    config_entry.entry_id = "test_entry"

    # Create TTS entity
    entity = ParasailTTSEntity(config_entry)
    entity.hass = MagicMock()

    print(f"  Entity name: {entity._attr_name}")
    print(f"  Supported languages: {entity.supported_languages}")
    print(f"  Default language: {entity.default_language}")

    # Mock the session
    mock_session = MagicMock()
    mock_response = create_sse_audio_response()
    mock_session.post.return_value = mock_response

    with patch('custom_components.parasail_tts.tts.async_get_clientsession', return_value=mock_session):
        result = await entity.async_get_tts_audio("Test message", "en", None)

    # Verify result
    if result is None:
        print("❌ Result is None")
        return False

    if not isinstance(result, tuple) or len(result) != 2:
        print(f"❌ Result format incorrect: {result}")
        return False

    audio_format, audio_data = result

    if audio_format not in ["wav", "mp3"]:
        print(f"❌ Invalid audio format: {audio_format}")
        return False

    if not isinstance(audio_data, bytes) or len(audio_data) == 0:
        print(f"❌ Invalid audio data: {type(audio_data)}, {len(audio_data)} bytes")
        return False

    # Verify it's a WAV file
    if audio_data[:4] != b'RIFF':
        print(f"❌ Audio doesn't start with RIFF header: {audio_data[:4]}")
        return False

    print(f"  ✓ Generated audio: {audio_format} format")
    print(f"  ✓ Audio size: {len(audio_data)} bytes")
    print(f"  ✓ Audio header: {audio_data[:4]}")
    print("  ✅ TTS entity test PASSED\n")
    return True


async def test_config_flow_validation():
    """Test config flow validation."""
    print("Test 2: Config Flow Validation")
    print("-" * 50)

    try:
        from custom_components.parasail_tts.config_flow import validate_input
        from custom_components.parasail_tts.const import CONF_API_KEY, CONF_VOICE
    except ImportError as e:
        print(f"❌ Failed to import config flow: {e}")
        return False

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
    if result is None:
        print("❌ Validation result is None")
        return False

    if "title" not in result:
        print(f"❌ Validation result missing 'title': {result}")
        return False

    if "oai_nova" not in result["title"]:
        print(f"❌ Title doesn't contain voice name: {result['title']}")
        return False

    print(f"  ✓ Validation successful")
    print(f"  ✓ Title: {result['title']}")
    print("  ✅ Config flow validation PASSED\n")
    return True


async def test_config_flow_error_handling():
    """Test config flow handles API errors."""
    print("Test 3: Config Flow Error Handling")
    print("-" * 50)

    try:
        from custom_components.parasail_tts.config_flow import validate_input, InvalidAuth
        from custom_components.parasail_tts.const import CONF_API_KEY, CONF_VOICE
    except ImportError as e:
        print(f"❌ Failed to import config flow: {e}")
        return False

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

    try:
        with patch('custom_components.parasail_tts.config_flow.async_get_clientsession', return_value=mock_session):
            await validate_input(hass, data)
        print("❌ Should have raised InvalidAuth exception")
        return False
    except InvalidAuth:
        print("  ✓ Correctly raised InvalidAuth for error response")
        print("  ✅ Config flow error handling PASSED\n")
        return True


async def test_http_error_handling():
    """Test handling of HTTP errors."""
    print("Test 4: HTTP Error Response Handling")
    print("-" * 50)

    try:
        from custom_components.parasail_tts.tts import ParasailTTSEntity
        from custom_components.parasail_tts.const import CONF_API_KEY, CONF_VOICE, CONF_MODEL, DEFAULT_MODEL
    except ImportError as e:
        print(f"❌ Failed to import integration: {e}")
        return False

    # Create mock config entry
    config_entry = MagicMock()
    config_entry.data = {
        CONF_API_KEY: "test_api_key",
        CONF_VOICE: "oai_nova",
        CONF_MODEL: DEFAULT_MODEL,
    }
    config_entry.options = {}
    config_entry.entry_id = "test_entry"

    # Create TTS entity
    entity = ParasailTTSEntity(config_entry)
    entity.hass = MagicMock()

    # Mock the session with 401 error
    mock_session = MagicMock()
    mock_response = MagicMock()
    mock_response.status = 401
    mock_response.text = asyncio.coroutine(lambda: "Unauthorized")()

    async def mock_post(*args, **kwargs):
        return mock_response

    mock_response.__aenter__ = asyncio.coroutine(lambda self: self)
    mock_response.__aexit__ = asyncio.coroutine(lambda self, *args: None)

    mock_session.post.side_effect = mock_post

    with patch('custom_components.parasail_tts.tts.async_get_clientsession', return_value=mock_session):
        result = await entity.async_get_tts_audio("Test message", "en", None)

    # Should return None on error
    if result is not None:
        print(f"❌ Should return None on HTTP error, got: {result}")
        return False

    print("  ✓ Correctly returned None for 401 error")
    print("  ✅ HTTP error handling PASSED\n")
    return True


async def main():
    """Run all tests."""
    print("=" * 50)
    print("Parasail TTS Integration Tests")
    print("=" * 50)
    print()

    results = []

    try:
        results.append(await test_tts_entity())
        results.append(await test_config_flow_validation())
        results.append(await test_config_flow_error_handling())
        results.append(await test_http_error_handling())

        print("=" * 50)
        print("Test Summary")
        print("=" * 50)
        passed = sum(results)
        total = len(results)
        print(f"Passed: {passed}/{total}")

        if passed == total:
            print("\n✅ ALL TESTS PASSED!")
            return 0
        else:
            print(f"\n❌ {total - passed} TEST(S) FAILED")
            return 1

    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
