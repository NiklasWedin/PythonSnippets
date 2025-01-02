import mido
import time
import fluidsynth


fs = fluidsynth.Synth(gain=1.0)
fs.start(driver="alsa")

sfid=fs.sfload("/usr/share/sounds/sf2/General_MIDI_64_1.6.sf2")

#Set  instrument and drums
fs.program_select(0, sfid, 0, 22)
fs.program_select(9, sfid, 128, 0)

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

metronome_pattern = [
    {'notes': [{'note': 77, 'velocity': 100, 'length': 1}]},
    {'notes': []},  # Inga noter
    {'notes': []},  # Inga noter
    {'notes': []},  # Inga noter
    {'notes': [{'note': 76, 'velocity': 80, 'length': 1}]},
    {'notes': []},  # Inga noter
    {'notes': []},  # Inga noter
    {'notes': []},  # Inga noter
    {'notes': [{'note': 76, 'velocity': 80, 'length': 1}]},
    {'notes': []},  # Inga noter
    {'notes': []},  # Inga noter
    {'notes': []},  # Inga noter
    {'notes': [{'note': 76, 'velocity': 80, 'length': 1}]},
    {'notes': []},  # Inga noter
    {'notes': []},  # Inga noter
    {'notes': []}   # Inga noter
]

class Pattern:
  def __init__(self, midiChannel):
    self.midiChannel = midiChannel
    self.bar_index = 0
    self.step_index = 0
    self.steps = 16
    self.pattern = [
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
    self.active_notes = {}

  # Funktion för att spela upp aktuellt tidssteg i pattern
  def play(self):
    # Spela Note-on för varje not i detta steg
    for note_data in self.pattern[self.step_index]['notes']:
      print(note_data)
      note = note_data['note']
      velocity = note_data['velocity']
      length = note_data['length']
      if note not in self.active_notes:
        #output_port.send(mido.Message('note_on', note=note, velocity=velocity))
        fs.noteon(self.midiChannel, note, velocity)
        self.active_notes[note] = self.step_index + length  # Beräkna Note-off steg

    print(self.active_notes)

    notes_to_remove = []

    # Hantera Note-off
    for note, off_step in self.active_notes.items():
      if self.step_index == off_step:
        #output_port.send(mido.Message('note_off', note=note, velocity=0))
        fs.noteoff(0, note)
        notes_to_remove.append(note)

    print(notes_to_remove)

    # Ta bort slutförda noter
    for note in notes_to_remove:
      del self.active_notes[note]

    self.step_index = (self.step_index + 1) % self.steps

#Beat patterns
chords = Pattern(0)
metronome = Pattern(9)
metronome.pattern = metronome_pattern

metronome_on = True

# Spela sequencern i en loop
try:
  print("Startar uppspelning...")
  while True:
    if metronome_on:
      metronome.play()
    chords.play()
    # Vänta tills nästa steg
    time.sleep(step_duration)


except KeyboardInterrupt:
  print("Uppspelning stoppad.")

# Stäng MIDI-porten
#output_port.close()
