"""Constants for the Parasail TTS integration."""

DOMAIN = "parasail_tts"

CONF_API_KEY = "api_key"
CONF_MODEL = "model"
CONF_VOICE = "voice"

DEFAULT_MODEL = "parasail-resemble-tts-en"
DEFAULT_VOICE = "fb2d2858"  # Lucy
DEFAULT_TEMPERATURE = 0.1

PARASAIL_API_BASE = "https://api.parasail.io/v1"

# Available TTS models on Parasail
PARASAIL_TTS_MODELS = [
    "parasail-resemble-tts-en",
]

# Available Resemble AI voices for TTS
# Format: "voice_id" for internal use
# Rapid Voices - English (US)
PARASAIL_TTS_VOICES = [
    "fb2d2858",  # Lucy
    "2429ddfa",  # Claire
    "08975946",  # Meera
    "cfb9967c",  # Fiona
    "7c4296be",  # Grant
    "91b49260",  # Abigail
    "c1faa6af",  # Chloe
    "7213a9ea",  # Grace
    "55f5b8dc",  # Linda
    "38a0b764",  # Aaron
    "96d225a3",  # Jessica
    "c99f388c",  # Anaya
    "68e421ed",  # Mark
    "4e972f71",  # Lauren
    "61fcb769",  # Evelyn
    "bee581c1",  # Ethan
    "637c2521",  # Elaine
    "8d516bf5",  # Lisa
    "1cf47426",  # Marisol
    "12066e89",  # Gavin
    "c49e1b04",  # Laura
    "0b15fe25",  # Christina
    "0942a9fe",  # Eric
    "6a3e095e",  # Jason
    "018dc07a",  # Dylan
    "bec88a80",  # Brian
    "9595cc9e",  # Erica
    "082cb68f",  # Dorothy
    "a3b3f1df",  # Emmanuel
    "8d93c97d",  # Deborah
    "d1959511",  # Archer
    "e8d6d3c8",  # Darlene
    "175ac7a6",  # Gordon
    "ba707fb5",  # Gianluca
    "9ed9d19b",  # Rajesh
    "ac7df359",  # Walter
    "e8883d33",  # Andy
    "4ed28aa9",  # Minho
    "28f1626c",  # Rupert
    "d2f26a3e",  # Andrew
    # Rapid Voices - Other Languages
    "3143af68",  # Anita (German)
    "1d28deab",  # Isabel (Spanish)
    "af3b3fad",  # Fatima (Hindi)
    "02136f6a",  # Sofia (Portuguese)
    "daa6b448",  # Dipankar (Hindi)
    "01aa67f7",  # Diego (Portuguese)
    "a253156d",  # Jota (Spanish)
    "e7e459d6",  # Ulrich (German)
    "6e922b40",  # Nasser (Arabic)
    "b7088a9c",  # Sana (Arabic)
    # Professional Voices
    "3f5fb9f1",  # Professor Shaposhnikov
    "7d94218f",  # Maureen
    "482babfc",  # Maureen (Angry)
    "b15e550f",  # Maureen (Caring)
    "91947e5c",  # Maureen (Happy)
    "e984fb89",  # Maureen (Announcer)
    "bca7481c",  # Maureen (Sad)
    "251c9439",  # Maureen (Scared)
    "7f40ff35",  # Carl Bishop (Conversational)
    "99751e42",  # Carl Bishop (Happy)
    "eacbc44f",  # Carl Bishop (Scared)
    "f2906c4a",  # Willow (Whispering)
    "c815cd7a",  # Willow II (Whispering)
    "e2180df0",  # William (Whispering)
    "aaa56e79",  # Steve (Scared)
    "adb84c77",  # Tanja
    "4f5a470b",  # Tanja (Telephonic)
    "abbbc383",  # Tanja (Warm Word Weaver)
    "33eecc17",  # Primrose
    "0097f246",  # Primrose (Winded)
    "1ff0045f",  # Vivian
    "f453b918",  # Vicky
    "ff225977",  # Tyler
    "779842bf",  # Tarkos
    "af72c1ac",  # Siobhan
    "d3e61caf",  # Seth
    "e28236ee",  # Samantha
    "0f2f9a7e",  # Sam
    "3e907bcc",  # Robert
    "14ca34b3",  # Rico
    "85ba84f2",  # Richard Garifo
    "19eae884",  # Radio Nikole
    "1864fd63",  # Pete
    "33e64cd2",  # Paula J
    "aa8053cc",  # Orion
    "ef49f972",  # Olivia
    "07c1d6b5",  # Olga
    "db37643c",  # Niki
    "3a02dc40",  # Mike
    "1c49e774",  # Melody
    "f4da4639",  # Matt Weller
    "ae8223ca",  # Luna
    "78671217",  # Lothar
    "4884d94a",  # Liz
    "8a73f115",  # Little Brittle
    "805adead",  # Little Ari
    "2211cb8c",  # Kessi
    "3dbfbf3d",  # Ken
    "c9ee13b4",  # Katya
    "28b4cc5a",  # Kate
]

# Voice name mapping for display purposes
VOICE_NAMES = {
    # Rapid Voices - English (US)
    "fb2d2858": "Lucy",
    "2429ddfa": "Claire",
    "08975946": "Meera",
    "cfb9967c": "Fiona",
    "7c4296be": "Grant",
    "91b49260": "Abigail",
    "c1faa6af": "Chloe",
    "7213a9ea": "Grace",
    "55f5b8dc": "Linda",
    "38a0b764": "Aaron",
    "96d225a3": "Jessica",
    "c99f388c": "Anaya",
    "68e421ed": "Mark",
    "4e972f71": "Lauren",
    "61fcb769": "Evelyn",
    "bee581c1": "Ethan",
    "637c2521": "Elaine",
    "8d516bf5": "Lisa",
    "1cf47426": "Marisol",
    "12066e89": "Gavin",
    "c49e1b04": "Laura",
    "0b15fe25": "Christina",
    "0942a9fe": "Eric",
    "6a3e095e": "Jason",
    "018dc07a": "Dylan",
    "bec88a80": "Brian",
    "9595cc9e": "Erica",
    "082cb68f": "Dorothy",
    "a3b3f1df": "Emmanuel",
    "8d93c97d": "Deborah",
    "d1959511": "Archer",
    "e8d6d3c8": "Darlene",
    "175ac7a6": "Gordon",
    "ba707fb5": "Gianluca",
    "9ed9d19b": "Rajesh",
    "ac7df359": "Walter",
    "e8883d33": "Andy",
    "4ed28aa9": "Minho",
    "28f1626c": "Rupert",
    "d2f26a3e": "Andrew",
    # Rapid Voices - Other Languages
    "3143af68": "Anita (German)",
    "1d28deab": "Isabel (Spanish)",
    "af3b3fad": "Fatima (Hindi)",
    "02136f6a": "Sofia (Portuguese)",
    "daa6b448": "Dipankar (Hindi)",
    "01aa67f7": "Diego (Portuguese)",
    "a253156d": "Jota (Spanish)",
    "e7e459d6": "Ulrich (German)",
    "6e922b40": "Nasser (Arabic)",
    "b7088a9c": "Sana (Arabic)",
    # Professional Voices
    "3f5fb9f1": "Professor Shaposhnikov",
    "7d94218f": "Maureen",
    "482babfc": "Maureen (Angry)",
    "b15e550f": "Maureen (Caring)",
    "91947e5c": "Maureen (Happy)",
    "e984fb89": "Maureen (Announcer)",
    "bca7481c": "Maureen (Sad)",
    "251c9439": "Maureen (Scared)",
    "7f40ff35": "Carl Bishop (Conversational)",
    "99751e42": "Carl Bishop (Happy)",
    "eacbc44f": "Carl Bishop (Scared)",
    "f2906c4a": "Willow (Whispering)",
    "c815cd7a": "Willow II (Whispering)",
    "e2180df0": "William (Whispering)",
    "aaa56e79": "Steve (Scared)",
    "adb84c77": "Tanja",
    "4f5a470b": "Tanja (Telephonic)",
    "abbbc383": "Tanja (Warm Word Weaver)",
    "33eecc17": "Primrose",
    "0097f246": "Primrose (Winded)",
    "1ff0045f": "Vivian",
    "f453b918": "Vicky",
    "ff225977": "Tyler",
    "779842bf": "Tarkos",
    "af72c1ac": "Siobhan",
    "d3e61caf": "Seth",
    "e28236ee": "Samantha",
    "0f2f9a7e": "Sam",
    "3e907bcc": "Robert",
    "14ca34b3": "Rico",
    "85ba84f2": "Richard Garifo",
    "19eae884": "Radio Nikole",
    "1864fd63": "Pete",
    "33e64cd2": "Paula J",
    "aa8053cc": "Orion",
    "ef49f972": "Olivia",
    "07c1d6b5": "Olga",
    "db37643c": "Niki",
    "3a02dc40": "Mike",
    "1c49e774": "Melody",
    "f4da4639": "Matt Weller",
    "ae8223ca": "Luna",
    "78671217": "Lothar",
    "4884d94a": "Liz",
    "8a73f115": "Little Brittle",
    "805adead": "Little Ari",
    "2211cb8c": "Kessi",
    "3dbfbf3d": "Ken",
    "c9ee13b4": "Katya",
    "28b4cc5a": "Kate",
}
