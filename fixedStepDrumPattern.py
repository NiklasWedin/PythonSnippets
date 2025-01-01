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
baseDrum = 36
snareDrum = 38
hihatClosed = 42
hihatOpen = 46

sfid=fs.sfload("/usr/share/sounds/sf2/General_MIDI_64_1.6.sf2")

#Set drum sound
fs.program_select(drumChannel, sfid, drumBank, drumInstrument)

time.sleep(0.5)

TEMPO = 120
stepTime = 60 / TEMPO / 4

drumPatternLength = 16

baseDrumPattern =    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0 ,1, 0, 0, 0, 0, 0]
snareDrumPattern =   [0, 0, 0, 0, 1, 0, 0, 0, 0, 0 ,0, 0, 1, 0, 0, 0]
hihatClosedPattern = [0, 0, 1, 0, 0, 0, 1, 0, 1, 0 ,1, 0, 0, 1, 1, 0]
hihatOpenPattern =   [1, 0, 0, 0, 1, 0, 0, 0, 1, 0 ,0, 0, 1, 0, 0, 0]

while True: 

  for step in range(drumPatternLength):
    if baseDrumPattern[step]:
      fs.noteon(drumChannel, baseDrum, 100)
    if snareDrumPattern[step]:
      fs.noteon(drumChannel, snareDrum, 100)
    if hihatClosedPattern[step]:
      fs.noteon(drumChannel, hihatClosed, 100)
    if hihatOpenPattern[step]:
      fs.noteon(drumChannel, hihatOpen, 100)

    time.sleep(stepTime)

fs.play_midi_stop()
fs.delete()
