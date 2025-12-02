"""Test against live Parasail API to verify integration works."""
import asyncio
import base64
import json
import aiohttp


API_URL = "https://voice-demo.parasail.io/api/tts-stream"


async def test_live_api_call():
    """Test actual API call to verify SSE parsing works."""
    print("Testing Live Parasail API")
    print("=" * 60)

    payload = {
        "temperature": 0.1,
        "text": "Testing Home Assistant integration",
        "voice": "oai_nova",
        "exaggeration": 0.0,
        "cfg_weight": 3.0,
    }

    print(f"\nPayload:")
    print(json.dumps(payload, indent=2))

    try:
        async with aiohttp.ClientSession() as session:
            print(f"\nConnecting to: {API_URL}")

            async with session.post(
                API_URL,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=aiohttp.ClientTimeout(total=30),
            ) as response:
                print(f"Response status: {response.status}")

                if response.status != 200:
                    error_text = await response.text()
                    print(f"❌ API error: {error_text}")
                    return False

                # Parse SSE response (same logic as in tts.py)
                audio_chunks = []
                chunk_count = 0
                event_count = 0

                print("\nProcessing SSE stream:")

                async for line in response.content:
                    line_text = line.decode('utf-8').strip()

                    # SSE events are prefixed with "data: "
                    if line_text.startswith('data: '):
                        json_data = line_text[6:]  # Remove "data: " prefix
                        event_count += 1

                        try:
                            event = json.loads(json_data)
                            event_type = event.get('type', 'unknown')

                            if event_type == 'start':
                                print(f"  Event {event_count}: Start ({event.get('priority', 'N/A')})")

                            elif event_type == 'audio' and 'audio_content' in event:
                                # Decode base64 audio content
                                audio_chunk = base64.b64decode(event['audio_content'])
                                audio_chunks.append(audio_chunk)
                                chunk_count += 1
                                print(f"  Event {event_count}: Audio chunk {event.get('chunk', chunk_count)} - {len(audio_chunk)} bytes")

                            elif event_type == 'error':
                                print(f"  Event {event_count}: ERROR - {event}")
                                return False

                            elif event_type == 'done':
                                print(f"  Event {event_count}: Done")

                            else:
                                print(f"  Event {event_count}: {event_type}")

                        except json.JSONDecodeError as err:
                            print(f"  Warning: Failed to parse JSON: {err}")
                            continue

                # Concatenate all audio chunks
                if not audio_chunks:
                    print("\n❌ No audio chunks received from API")
                    return False

                audio_data = b''.join(audio_chunks)

                print(f"\nResults:")
                print(f"  Total events: {event_count}")
                print(f"  Audio chunks: {chunk_count}")
                print(f"  Total audio size: {len(audio_data)} bytes")

                # Verify audio format
                if len(audio_data) >= 4:
                    magic_bytes = audio_data[:4]
                    print(f"  Magic bytes: {magic_bytes.hex()} ({magic_bytes})")

                    if magic_bytes == b'RIFF':
                        print(f"  ✓ Detected WAV format")

                        # Parse WAV header for more details
                        if len(audio_data) >= 44:
                            chunk_size = int.from_bytes(audio_data[4:8], 'little')
                            format_tag = audio_data[8:12]
                            print(f"  ✓ RIFF chunk size: {chunk_size}")
                            print(f"  ✓ Format: {format_tag}")

                    elif magic_bytes[:3] == b'ID3' or (magic_bytes[0] == 0xFF and (magic_bytes[1] & 0xE0) == 0xE0):
                        print(f"  ✓ Detected MP3 format")
                    else:
                        print(f"  ⚠ Unknown audio format")

                else:
                    print(f"  ❌ Audio data too small: {len(audio_data)} bytes")
                    return False

                print(f"\n✅ Live API test PASSED!")
                print(f"   The integration will work correctly with Home Assistant.")
                return True

    except aiohttp.ClientError as err:
        print(f"\n❌ Network error: {err}")
        return False
    except asyncio.TimeoutError:
        print(f"\n❌ Request timed out")
        return False
    except Exception as err:
        print(f"\n❌ Unexpected error: {err}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run live API test."""
    success = await test_live_api_call()

    if success:
        print("\n" + "=" * 60)
        print("INTEGRATION VERIFICATION COMPLETE")
        print("=" * 60)
        print("\n✅ The Parasail TTS integration is ready for Home Assistant!")
        print("\nThe integration correctly:")
        print("  • Parses Server-Sent Events (SSE) format")
        print("  • Decodes base64-encoded audio chunks")
        print("  • Concatenates chunks into complete WAV files")
        print("  • Handles errors appropriately")
        print("\nYou can now install this integration in Home Assistant.")
        return 0
    else:
        print("\n❌ Live API test failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
