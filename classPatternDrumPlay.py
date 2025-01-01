import fluidsynth
import time

fs = fluidsynth.Synth(gain=1.0)
fs.start(driver="alsa", midi_driver="alsa_raw")

#midiChannel = 0
midiBank = 0
midiInstrument = 0

drumChannel = 9
drumBank = 128
drumInstrument = 0

#Drumsounds
baseDrum = 36
snareDrum = 38
hihatClosed = 42
hihatOpen = 46

sfid=fs.sfload("/usr/share/sounds/sf2/General_MIDI_64_1.6.sf2")

fs.program_select(0, sfid, midiBank, midiInstrument)

#Set drum sound
fs.program_select(drumChannel, sfid, drumBank, drumInstrument)

time.sleep(0.5)

TEMPO = 120
stepTime = 60 / TEMPO / 4

drumPatternLength = 16


class Pattern:
  def __init__(self, midiChannel, noteNumber):
    self.midiChannel = midiChannel
    self.noteNumber = noteNumber
    self.bar_index = 0
    self.step_index = 0
    self.pattern = [1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0]

  def play(self):
    if self.pattern[self.step_index]:
      fs.noteon(self.midiChannel, self.noteNumber, 80)
    else:
      fs.noteoff(self.midiChannel, self.noteNumber)
    self.step_index = (self.step_index + 1) % drumPatternLength


pattern_basedrum = Pattern(drumChannel, baseDrum)
pattern_basedrum.pattern = [1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0]

pattern_snaredrum = Pattern(drumChannel, snareDrum)
pattern_snaredrum.pattern = [0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0]

pattern_hihatclosed = Pattern(drumChannel, hihatClosed)
pattern_hihatclosed.pattern = [1,0,1,0,1,0,1,0,1,0,1,0,1,1,0,0]

patterns = []
patterns.append(pattern_basedrum)
patterns.append(pattern_snaredrum)
patterns.append(pattern_hihatclosed)

while True: 

  for pattern in patterns:
    pattern.play()
  time.sleep(stepTime)

fs.play_midi_stop()
fs.delete()
