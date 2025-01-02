import mido
import time
import fluidsynth


fs = fluidsynth.Synth(gain=1.0)
fs.start(driver="alsa")

sfid=fs.sfload("/usr/share/sounds/sf2/General_MIDI_64_1.6.sf2")

#Set  instrument
fs.program_select(0, sfid, 0, 22)

# Antal steg i sequencern (16 sextondelar)
steps = 16

# MIDI-port
#output_port_name = 'Your MIDI Output Device'
#output_port = mido.open_output(output_port_name)

# Tempo i BPM
bpm = 120
step_duration = 60 / bpm / 4  # Längd för en sextondel

# Struktur för att spara noter
# Varje steg innehåller en lista med noter
sequencer = [
    {'notes': [{'note': 60, 'velocity': 100, 'length': 4}, {'note': 64, 'velocity': 100, 'length': 2}]},  # C4 och E4
    {'notes': []},  # Inga noter
    {'notes': [{'note': 67, 'velocity': 100, 'length': 2}]},  # G4
    {'notes': []},  # Inga noter
    {'notes': [{'note': 62, 'velocity': 100, 'length': 4}]},  # D4
    {'notes': []},  # Inga noter
    {'notes': [{'note': 65, 'velocity': 100, 'length': 4}]},  # F4
    {'notes': []},  # Inga noter
    {'notes': [{'note': 69, 'velocity': 100, 'length': 4}]},  # A4
    {'notes': []},  # Inga noter
    {'notes': [{'note': 72, 'velocity': 100, 'length': 4}]},  # C5
    {'notes': []},  # Inga noter
    {'notes': []},  # Inga noter
    {'notes': []},  # Inga noter
    {'notes': []},  # Inga noter
    {'notes': []}   # Inga noter
]

# Funktion för att spela upp sequencern
def play_sequencer():
    active_notes = {}
    for step in range(steps):
        # Spela Note-on för varje not i detta steg
        for note_data in sequencer[step]['notes']:
            note = note_data['note']
            velocity = note_data['velocity']
            length = note_data['length']
            if note not in active_notes:
                #output_port.send(mido.Message('note_on', note=note, velocity=velocity))
                fs.noteon(0, note, velocity)
                active_notes[note] = step + length  # Beräkna Note-off steg

        # Hantera Note-off
        notes_to_remove = []
        for note, off_step in active_notes.items():
            if step == off_step:
                #output_port.send(mido.Message('note_off', note=note, velocity=0))
                fs.noteoff(0, note)
                notes_to_remove.append(note)

        # Ta bort slutförda noter
        for note in notes_to_remove:
            del active_notes[note]

        # Vänta tills nästa steg
        time.sleep(step_duration)

# Spela sequencern i en loop
try:
    print("Startar uppspelning...")
    while True:
        play_sequencer()

except KeyboardInterrupt:
    print("Uppspelning stoppad.")

# Stäng MIDI-porten
#output_port.close()
