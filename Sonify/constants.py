NOTES = [
    ['C'], ['C#', 'Db'], ['D'], ['D#', 'Eb'], ['E'], ['F'], ['F#', 'Gb'],
    ['G'], ['G#', 'Ab'], ['A'], ['A#', 'Bb'], ['B']
]

def get_keys():
    base_keys = {
        'c_major': ['C', 'D', 'E', 'F', 'G', 'A', 'B'],
        'd_major': ['D', 'E', 'F#', 'G', 'A', 'B', 'C#'],
        'e_major': ['E', 'F#', 'G#', 'A', 'B', 'C#', 'D#'],
        'f_major': ['F', 'G', 'A', 'Bb', 'C', 'D', 'E', 'F'],
        'g_major': ['G', 'A', 'B', 'C', 'D', 'E', 'F#'],
        'a_major': ['A', 'B', 'C#', 'D', 'E', 'F#', 'G#', 'A'],
        'b_major': ['B', 'C#', 'D#', 'E', 'F#', 'G#', 'A#', 'B'],
        'c_sharp_major': ['Db', 'Eb', 'F', 'Gb', 'Ab', 'Bb', 'C', 'Db'],
        'd_sharp_major': ['Eb', 'F', 'G', 'Ab', 'Bb', 'C', 'D'],
        'f_sharp_major': ['F#', 'G#', 'A#', 'B', 'C#', 'D#', 'F', 'F#'],
        'g_sharp_major': ['Ab', 'Bb', 'C', 'Db', 'Eb', 'F', 'G', 'Ab'],
        'a_sharp_major': ['Bb', 'C', 'D', 'Eb', 'F', 'G', 'A', 'Bb']
    }

    base_keys['d_flat_major'] = base_keys['c_sharp_major']
    base_keys['e_flat_major'] = base_keys['d_sharp_major']
    base_keys['g_flat_major'] = base_keys['f_sharp_major']
    base_keys['a_flat_major'] = base_keys['g_sharp_major']
    base_keys['b_flat_major'] = base_keys['a_sharp_major']

    return base_keys


KEYS = get_keys()

# Instrument and Percussion map from
# https://www.midi.org/specifications/item/gm-level-1-sound-set

INSTRUMENTS = {
    'accordion': 22,
    'acoustic bass': 33,
    'acoustic grand piano': 1,
    'acoustic guitar (nylon)': 25,
    'acoustic guitar (steel)': 26,
    'agogo': 114,
    'alto sax': 66,
    'applause': 127,
    'bagpipe': 110,
    'banjo': 106,
    'baritone sax': 68,
    'bassoon': 71,
    'bird tweet': 124,
    'blown bottle': 77,
    'brass section': 62,
    'breath noise': 122,
    'bright acoustic piano': 2,
    'celesta': 9,
    'cello': 43,
    'choir aahs': 53,
    'church organ': 20,
    'clarinet': 72,
    'clavi': 8,
    'contrabass': 44,
    'distortion guitar': 31,
    'drawbar organ': 17,
    'dulcimer': 16,
    'electric bass (finger)': 34,
    'electric bass (pick)': 35,
    'electric grand piano': 3,
    'electric guitar (clean)': 28,
    'electric guitar (jazz)': 27,
    'electric guitar (muted)': 29,
    'electric piano 1': 5,
    'electric piano 2': 6,
    'english horn': 70,
    'fiddle': 111,
    'flute': 74,
    'french horn': 61,
    'fretless bass': 36,
    'fx 1 (rain)': 97,
    'fx 2 (soundtrack)': 98,
    'fx 3 (crystal)': 99,
    'fx 4 (atmosphere)': 100,
    'fx 5 (brightness)': 101,
    'fx 6 (goblins)': 102,
    'fx 7 (echoes)': 103,
    'fx 8 (sci-fi)': 104,
    'glockenspiel': 10,
    'guitar fret noise': 121,
    'guitar harmonics': 32,
    'gunshot': 128,
    'harmonica': 23,
    'harpsichord': 7,
    'helicopter': 126,
    'honky-tonk piano': 4,
    'kalimba': 109,
    'koto': 108,
    'lead 1 (square)': 81,
    'lead 2 (sawtooth)': 82,
    'lead 3 (calliope)': 83,
    'lead 4 (chiff)': 84,
    'lead 5 (charang)': 85,
    'lead 6 (voice)': 86,
    'lead 7 (fifths)': 87,
    'lead 8 (bass + lead)': 88,
    'marimba': 13,
    'melodic tom': 118,
    'music box': 11,
    'muted trumpet': 60,
    'oboe': 69,
    'ocarina': 80,
    'orchestra hit': 56,
    'orchestral harp': 47,
    'overdriven guitar': 30,
    'pad 1 (new age)': 89,
    'pad 2 (warm)': 90,
    'pad 3 (polysynth)': 91,
    'pad 4 (choir)': 92,
    'pad 5 (bowed)': 93,
    'pad 6 (metallic)': 94,
    'pad 7 (halo)': 95,
    'pad 8 (sweep)': 96,
    'pan flute': 76,
    'percussive organ': 18,
    'piccolo': 73,
    'pizzicato strings': 46,
    'recorder': 75,
    'reed organ': 21,
    'reverse cymbal': 120,
    'rock organ': 19,
    'seashore': 123,
    'shakuhachi': 78,
    'shamisen': 107,
    'shanai': 112,
    'sitar': 105,
    'slap bass 1': 37,
    'slap bass 2': 38,
    'soprano sax': 65,
    'steel drums': 115,
    'string ensemble 1': 49,
    'string ensemble 2': 50,
    'synth bass 1': 39,
    'synth bass 2': 40,
    'synth drum': 119,
    'synth voice': 55,
    'synthbrass 1': 63,
    'synthbrass 2': 64,
    'synthstrings 1': 51,
    'synthstrings 2': 52,
    'taiko drum': 117,
    'tango accordion': 24,
    'telephone ring': 125,
    'tenor sax': 67,
    'timpani': 48,
    'tinkle bell': 113,
    'tremolo strings': 45,
    'trombone': 58,
    'trumpet': 57,
    'tuba': 59,
    'tubular bells': 15,
    'vibraphone': 12,
    'viola': 42,
    'violin': 41,
    'voice oohs': 54,
    'whistle': 79,
    'woodblock': 116,
    'xylophone': 14
}

PERCUSSION = {
    'acoustic bass drum': 35,
    'acoustic snare': 38,
    'bass drum 1': 36,
    'cabasa': 69,
    'chinese cymbal': 52,
    'claves': 75,
    'closed hi hat': 42,
    'cowbell': 56,
    'crash cymbal 1': 49,
    'crash cymbal 2': 57,
    'electric snare': 40,
    'hand clap': 39,
    'hi bongo': 60,
    'hi wood block': 76,
    'hi-mid tom': 48,
    'high agogo': 67,
    'high floor tom': 43,
    'high timbale': 65,
    'high tom': 50,
    'long guiro': 74,
    'long whistle': 72,
    'low agogo': 68,
    'low bongo': 61,
    'low conga': 64,
    'low floor tom': 41,
    'low timbale': 66,
    'low tom': 45,
    'low wood block': 77,
    'low-mid tom': 47,
    'maracas': 70,
    'mute cuica': 78,
    'mute hi conga': 62,
    'mute triangle': 80,
    'open cuica': 79,
    'open hi conga': 63,
    'open hi-hat': 46,
    'open triangle': 81,
    'pedal hi-hat': 44,
    'ride bell': 53,
    'ride cymbal 1': 51,
    'ride cymbal 2': 59,
    'short guiro': 73,
    'short whistle': 71,
    'side stick': 37,
    'splash cymbal': 55,
    'tambourine': 54,
    'vibraslap': 58
}