import mido
import time
import fluidsynth

midi_notes = []

rec_midi_notes_on = []
rec_midi_notes_off = []

busy_processing = False

def midiGet(data, evnt):
  global rec_midi_notes_on, rec_midi_notes_off, busy_processing
  recordingChannel = 0
  #global midi_time, pattern_timer, recording
  #midi_time = time.time() - start_time
#  print("Hej!")

  channel = fs.midi_event_get_channel(evnt)
  type = fs. midi_event_get_type(evnt)
#  print("Key: ", fs.midi_event_get_key(evnt), channel)
  key = fs.midi_event_get_key(evnt)
  velocity = fs.midi_event_get_velocity(evnt)

  while busy_processing:
    ...
  if channel == recordingChannel:
    if type == 144:
      rec_midi_notes_on.append({'note': key, 'velocity':velocity})
    if type == 128:
      rec_midi_notes_off.append({'note': key})

  print("Midi on: ", rec_midi_notes_on)
  print("Midi off: ", rec_midi_notes_off)
 
#  if control == 117 and channel == 0:  #Record button
#    recording = True
#    print("Recrording active")
#  if control == 114 and channel == 0:  #Stop button
#    recording = False
#    print("recording stopped")
  fs.noteon(channel, key, velocity)
#  print(channel,key,velocity)
#  if recording:
#    midi_list.append(midi_event(midi_time,channel,type, control, value))
#    print(len(midi_list))
  #midi_list.append(midi_event(pattern_timer,channel,type, control, value))
  #midi_time = midi_time + 1
  return 0

fs = fluidsynth.Synth(gain=1.0)
fs.start(driver="alsa", midi_driver="alsa_raw", midi_router=midiGet)

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
    {'notes': [{'note': 76, 'velocity': 100, 'length': 1}]},
    {'notes': []},  # Inga noter
    {'notes': []},  # Inga noter
    {'notes': []},  # Inga noter
    {'notes': [{'note': 77, 'velocity': 80, 'length': 1}]},
    {'notes': []},  # Inga noter
    {'notes': []},  # Inga noter
    {'notes': []},  # Inga noter
    {'notes': [{'note': 77, 'velocity': 80, 'length': 1}]},
    {'notes': []},  # Inga noter
    {'notes': []},  # Inga noter
    {'notes': []},  # Inga noter
    {'notes': [{'note': 77, 'velocity': 80, 'length': 1}]},
    {'notes': []},  # Inga noter
    {'notes': []},  # Inga noter
    {'notes': []}   # Inga noter
]

chord_pattern = [
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


class Pattern:
  def __init__(self, midiChannel):
    self.midiChannel = midiChannel
    self.bar_index = 0
    self.step_index = 0
    self.steps = 16
    self.pattern = [
      {'notes': []},  # Inga noter
      {'notes': []},  # Inga noter
      {'notes': []},  # Inga noter
      {'notes': []},  # Inga noter
      {'notes': []},  # Inga noter
      {'notes': []},  # Inga noter
      {'notes': []},  # Inga noter
      {'notes': []},  # Inga noter
      {'notes': []},  # Inga noter
      {'notes': []},  # Inga noter
      {'notes': []},  # Inga noter
      {'notes': []},  # Inga noter
      {'notes': []},  # Inga noter
      {'notes': []},  # Inga noter
      {'notes': []},  # Inga noter
      {'notes': []}   # Inga noter
    ]
    self.active_notes = {}
    self.rec_active_notes = {}

  # Funktion för att spela upp aktuellt tidssteg i pattern
  def play(self):
    # Spela Note-on för varje not i detta steg
    for note_data in self.pattern[self.step_index]['notes']:
#      print(note_data)
      note = note_data['note']
      velocity = note_data['velocity']
      length = note_data['length']
      if note not in self.active_notes:
        #output_port.send(mido.Message('note_on', note=note, velocity=velocity))
        fs.noteon(self.midiChannel, note, velocity)
        print(self.midiChannel, note,velocity)
        self.active_notes[note] = self.step_index + length  # Beräkna Note-off steg
#    print(self.active_notes)
    notes_to_remove = []
    print(f"Step: {self.step_index} Notes: {self.active_notes}")
    # Hantera Note-off
    for note, off_step in self.active_notes.items():
      if self.step_index == off_step:
        fs.noteoff(0, note)
        notes_to_remove.append(note)
#    print(notes_to_remove)
    # Ta bort slutförda noter
    for note in notes_to_remove:
      del self.active_notes[note]

    self.step_index = (self.step_index + 1) % self.steps

  def rec(self):
    global rec_midi_notes_on, rec_midi_notes_off, busy_processing
    #Replay earlier recorded notes
    for note_data in self.pattern[self.step_index]['notes']:
      note = note_data['note']
      velocity = note_data['velocity']
      length = note_data['length']
      if note not in self.active_notes:
        fs.noteon(self.midiChannel, note, velocity)
        print(self.midiChannel, note,velocity)
        self.active_notes[note] = self.step_index + length  # Beräkna Note-off steg
    notes_to_remove = []
    print(f"Step: {self.step_index} Notes: {self.active_notes}")
    # Hantera Note-off
    for note, off_step in self.active_notes.items():
      if self.step_index == off_step:
        #output_port.send(mido.Message('note_off', note=note, velocity=0))
        fs.noteoff(0, note)
        notes_to_remove.append(note)
    # Ta bort slutförda noter
    for note in notes_to_remove:
      del self.active_notes[note]

    #Process recorded notes
    for rec_note_on_data in rec_midi_notes_on:
      rec_note = rec_note_on_data['note']
      rec_velocity = rec_note_on_data['velocity']
      if rec_note not in self.rec_active_notes:
        #fs.noteon(self.midiChannel, note, velocity)
        self.rec_active_notes[rec_note] = self.step_index  # Spara start index för att kunna beräkna längd
        #self.pattern[self.step_index]['notes'].append({['note, velocity, 1})
        self.pattern[self.step_index]['notes'].append({'note': rec_note, 'velocity': rec_velocity, 'length': 0})
    print("Rec_active_notes", self.rec_active_notes)
    rec_midi_notes_on = []
    print(f"Step: {self.step_index} Notes: {self.rec_active_notes}")
    # Hantera Note-off
    for rec_note_off_data in rec_midi_notes_off:
      rec_note = rec_note_off_data['note']
      length = self.step_index - self.rec_active_notes[rec_note]
      #print(f"{self.step_index} - {self.rec_active_notes[rec_note]} = Length: {length}")
      # Uppdatera längd på not
      for note_data in self.pattern[self.rec_active_notes[rec_note]]['notes']:
        note = note_data['note']
        if note == rec_note:
          if length > 0:
            note_data['length'] = length
          else:
            note_data['length'] = 1
      del self.rec_active_notes[rec_note] 
    rec_midi_notes_off = []
      
    self.step_index = (self.step_index + 1) % self.steps
    if(self.step_index) == 0:
      print(list(self.pattern))

#Beat patterns
chords = Pattern(midiChannel = 0)
chords.pattern = chord_pattern
metronome = Pattern(midiChannel = 9)
metronome.pattern = metronome_pattern
record = Pattern(midiChannel = 0)

metronome_on = True

fs.noteon(9, 78, 100)
time.sleep(0.5)
fs.noteoff(9, 78)

# Spela sequencern i en loop
try:
  print("Startar uppspelning...")
  while True:
    if metronome_on:
      metronome.play()
    #chords.play()
    record.rec()
    # Vänta tills nästa steg
    time.sleep(step_duration)


except KeyboardInterrupt:
  print("Uppspelning stoppad.")

# Stäng MIDI-porten
#output_port.close()
