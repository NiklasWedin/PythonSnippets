import mido
import time

# Lista MIDI-utgångar
print("Tillgängliga MIDI-utgångar:")
for names in mido.get_output_names():
  print("   ", names)
print()

#midi_out = mido.open_output('Launchkey MK2 25 Launchkey MIDI')
midi_out = mido.open_output('Launchkey MK2 25 Launchkey InCo')

#Basic Example 
#midi_out.send(mido.Message('note_on', channel=15,  note=36, velocity=7))

input("Press Enter to send out note_on to all channels, all keays and at all velocities...")

for midiChannel in range(16):
  for midiVelocity in range(128):
    for midiKey in range(128):
      midi_out.send(mido.Message('note_on', channel=midiChannel, note=midiKey, velocity=midiVelocity))
      print(f"Playing Midi Channel: {midiChannel} Key: {midiKey} Velicity: {midiVelocity}")
    time.sleep(0.01)
    
#   midi_out.send(mido.Message('note_off', channel=

#  input("Press Enter to play next midiChannel...")

