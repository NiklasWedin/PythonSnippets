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

#Set Instrument sound
fs.program_select(0, sfid, midiBank, midiInstrument)

#Set drum sound
fs.program_select(drumChannel, sfid, drumBank, drumInstrument)

time.sleep(0.5)

TEMPO = 120
stepTime = 60 / TEMPO / 4
sixtyfourthTime = 60 / TEMPO / 16

drumPatternLength = 16

def metronomeHandler(timeHandler):
  tick = 76
  tock = 77

  if timeHandler.newBar():
    fs.noteon(drumChannel, tick, 100)
    print("Tick!")
  elif timeHandler.newBeat():
    fs.noteon(drumChannel, tock, 80)
    print("Tock!")


class SongTimer:
  def __init__(self, tempo):
    self.tempo = tempo
    self.bar_counter = 0
    self.beat_counter = 0
    self.step_counter = 0
    self.step_time = 60 / tempo / 4
    self.start_time = 0
    self.song_time = 0
    self.new_beat = False
    self.new_bar = False

  def start(self):
    self.start_time = time.time()
    self.new_beat = True
    self.new_bar = True


  def update(self):
    current_time = time.time()-self.start_time

    if current_time - self.song_time > self.step_time:
      self.step_counter += 1
      if self.step_counter >=4:
        self.step_counter = 0
        self.beat_counter += 1
        self.new_beat = True
        if self.beat_counter >= 4:
          self.beat_counter = 0
          self.bar_counter += 1
          self.new_bar = True
      self.song_time = current_time

  def newBeat(self):
    if self.new_beat:
      self.new_beat = False
      return True
    else:
      return False

  def newBar(self):
    if self.new_bar:
      self.new_bar = False
      self.new_beat = False
      return True
    else:
      return False

  def info(self):
    print(f"Bar: {self.bar_counter} beat: {self.beat_counter} step: {self.step_counter} song time: {self.song_time}")

#  def nearestStepTime(self):


time_keeper = SongTimer(TEMPO)
time_keeper.start()

while True: 

  time_keeper.update()
  time_keeper.info()

  metronomeHandler(time_keeper)

  time.sleep(stepTime)
  #time.sleep(0.01)

fs.play_midi_stop()
fs.delete()
