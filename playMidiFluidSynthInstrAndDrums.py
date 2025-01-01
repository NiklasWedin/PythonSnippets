import fluidsynth
import time

fs = fluidsynth.Synth(gain=1.0)
fs.start(driver="alsa", midi_driver="alsa_raw")

midiChannel = 0
midiBank = 0

drumChannel = 9
drumBank = 128
drumInstrument = 0

#Drumsounds
bassDrum = 36
snareDrum = 38
hihatClosed = 42
hihatOpen = 46

sfid=fs.sfload("/usr/share/sounds/sf2/General_MIDI_64_1.6.sf2")

#Set drum sound
fs.program_select(drumChannel, sfid, drumBank, drumInstrument)

time.sleep(0.5)

for midiInstrument in range(127):

  #Play drumes
  drumInstrumet = bassDrum + midiInstrument
  fs.noteon(drumChannel, drumInstrumet, 100)

  print(f"Drum: {drumInstrumet} Instrument: {midiInstrument}")
 
  time.sleep(0.5)

#Set  instrument 
  fs.program_select(midiChannel, sfid, midiBank, midiInstrument)

  fs.noteon(0, 60, 70)
  fs.noteon(0, 67, 70)
  fs.noteon(0, 76, 70)

  input("Press Enter to play next instrument and next drum...")

  fs.noteoff(0, 60)
  fs.noteoff(0, 67)
  fs.noteoff(0, 76)

fs.play_midi_stop()
fs.delete()
