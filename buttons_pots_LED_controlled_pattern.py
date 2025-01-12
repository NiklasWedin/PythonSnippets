import mido
import time
import fluidsynth

midi_out = mido.open_output('Launchkey MK2 25 Launchkey InCo')
midi_out.send(mido.Message('note_on', channel=15, note=50, velocity=54))

midi_notes = []

rec_midi_notes_on = []
rec_midi_notes_off = []

busy_processing = False

class Controller:
  def __init__(self):
    self.pads = [40, 41, 42, 43, 48, 49, 50, 51, 36, 37, 38, 39, 44, 45, 46, 47]  # Notnummer för varje pad
    self.pad_state = [0, 0, 0, 0, 0, 0, 0, 64, 0, 0, 0, 0, 0, 0, 0, 0]
    self.pad_channel = [2, 3, 4, 5, 6, 7, 8, 9]
    self.pots = [21, 22, 23, 24, 25, 26, 27, 28]
    self.pot_value = [0, 1, 2, 3, 4, 5, 6, 7]

    self.tempo = 120

    self.slider = 7
    self.slider_value = self.tempo

    self.prev_track_button = 103
    self.next_track_button = 102

    self.upper_row_button = 104
    self.lower_row_button = 105

    self.prev_button = 112
    self.next_button = 113
    self.play_button = 114
    self.stop_button = 115
    self.metronome_button = 116
    self.recording_button = 117

    self.recordingChannel = 9
    self.recording = False
    self.playing = False
    self.active_pads = set()
    self.metronome_on = True
    
    for pad_number in range(len(self.pad_state)):
      midi_out.send(mido.Message('note_on', channel=15, note=self.pads[pad_number], velocity=self.pad_state[pad_number]))

  def setValue(self, control_number, value):
    #Chack pots and set values
    if control_number in self.pots:
      self.pot_value[control_number-self.pots[0]] = value
      print("Pots:", self.pot_value)

    #Check slider value and use for tempo
    if control_number == self.slider:
      self.slider_value = value
      print("Slider: ", self.slider_value)
      self.tempo = value + 64
      print("Tempo: ", self.tempo)

    #Detect button pres, reacts on button relese
    if control_number == self.prev_track_button and value == 0:
      print("Previous Track")
    if control_number == self.next_track_button and value == 0:
      print("Next Track")
    if control_number == self.upper_row_button and value == 0:
      print("Upper row button")
    if control_number == self.lower_row_button and value == 0:
      print("Lower row button")
    if control_number == self.prev_button and value == 0:
      print("Previous?")
    if control_number == self.next_button and value == 0:
      print("Next?")
    if control_number == self.recording_button and value == 0:
      self.recording = True
      print("Starting recording!");
    if control_number == self.play_button and value == 0:
      self.playing = True
      print("Start playing!")
    if control_number == self.stop_button and value == 0:
      self.recording = False
      self.playing = False
      print("Stopping!")
    if control_number == self.metronome_button and value == 0:
      if self.metronome_on == False:
        self.metronome_on = True
        print("Metronome On!")
      else:
        self.metronome_on = False
        print("Metronome Off!")

  def togglePad(self, pad_number):
    if pad_number in self.pads:
      selected_pad = self.pads.index(pad_number)
      if self.pad_state[selected_pad]==0:
        self.pad_state[selected_pad]=64 
      else:
        self.pad_state[selected_pad]=0
      midi_out.send(mido.Message('note_on', channel=15, note=pad_number, velocity=self.pad_state[selected_pad]))
      print(self.pad_state)

songController = Controller()

def midiGet(data, evnt):
  global rec_midi_notes_on, rec_midi_notes_off, busy_processing
  inputChannel = 0
  selectedChannel = 2
  #global midi_time, pattern_timer, recording
  #midi_time = time.time() - start_time
#  print("Hej!")

  channel = fs.midi_event_get_channel(evnt)
  type = fs. midi_event_get_type(evnt)
#  print("Key: ", fs.midi_event_get_key(evnt), channel)
  key = fs.midi_event_get_key(evnt)
  velocity = fs.midi_event_get_velocity(evnt)
  if True:
    print(f"Channel: {channel} Type: {type} Key: {key} Velocity: {velocity}")

  while busy_processing:
    ...
  if channel == inputChannel and key < 100:
    if type == 144 and velocity > 0:
      rec_midi_notes_on.append({'note': key, 'velocity':velocity})
      fs.noteon(selectedChannel, key, velocity)
    if type == 128 or (type == 144 and velocity == 0):
      rec_midi_notes_off.append({'note': key})
      fs.noteoff(selectedChannel, key)   
    if True:
      print("Midi on: ", rec_midi_notes_on)
      print("Midi off: ", rec_midi_notes_off)

  #Detect controle, such as pots
  if channel == 0 and type == 176:
    songController.setValue(key, velocity)

  #Detect drum pads
  if channel == 9:
    if type == 128 or (type == 144 and velocity == 0):
      songController.togglePad(key) 
 
#  if control == 117 and channel == 0:  #Record button
#    recording = True
#    print("Recrording active")
#  if control == 114 and channel == 0:  #Stop button
#    recording = False
#    print("recording stopped")

#  fs.noteon(channel, key, velocity)

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
fs.program_select(2, sfid, 0, 32)
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
        #print(self.midiChannel, note, velocity)
        self.active_notes[note] = self.step_index + length  # Beräkna Note-off steg
#    print(self.active_notes)
    notes_to_remove = []
    if False:
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
        #print(self.midiChannel, note,velocity)
        self.active_notes[note] = self.step_index + length  # Beräkna Note-off steg
    notes_to_remove = []
    if False:
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
    if False:
      print("Rec_active_notes", self.rec_active_notes)
    rec_midi_notes_on = []
    if False:
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
    #if(self.step_index) == 0:
    #  print(list(self.pattern))

#Beat patterns

#songController = Controller()

chords = Pattern(midiChannel = 0)
chords.pattern = chord_pattern
metronome = Pattern(midiChannel = 9)
metronome.pattern = metronome_pattern
record = Pattern(midiChannel = 0)

#metronome_on = True

fs.noteon(9, 78, 100)
time.sleep(0.5)
fs.noteoff(9, 78)

# Spela sequencern i en loop
try:
  print("Startar uppspelning...")
  while True:
    step_duration = 60 / songController.tempo / 4  # Längd för en sextondel
    if songController.metronome_on:
      metronome.play()
    #chords.play()
    record.rec()
    # Vänta tills nästa steg
    time.sleep(step_duration)


except KeyboardInterrupt:
  print("Uppspelning stoppad.")

# Stäng MIDI-porten
#output_port.close()
