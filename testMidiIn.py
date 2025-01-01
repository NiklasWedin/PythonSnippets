import mido

# Lista MIDI-ingångar
print("Tillgängliga MIDI-ingångar:")
print(mido.get_input_names())
print()

# Öppna Launchkey som ingång (anpassa namnet)
midi_in = mido.open_input("Launchkey MK2 25 Launchkey MIDI")  # Byt till rätt namn

# Läs inkommande MIDI-meddelanden
print("Lyssnar på inkommande MIDI-data...")
for msg in midi_in:
    print(msg)
