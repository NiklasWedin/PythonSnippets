import mido

midi_in = mido.open_input("Launchkey MK2 25 Launchkey MIDI")  # Byt till rätt namn
midi_out = mido.open_output('Launchkey MK2 25 Launchkey InCo')

pads = [40, 41, 42, 43, 48, 49, 50, 51, 36, 37, 38, 39, 44, 45, 46, 47]  # Notnummer för varje pad

def main():

    # Stäng av alla LEDs
    for pad in pads:
      midi_out.send(mido.Message('note_on', channel=15, note=pad, velocity=0))

    # Slå på en för debug
    midi_out.send(mido.Message('note_on', channel=15, note=50, velocity=54))

    active_pads = set()

    while True:
        print("Programmet körs. Tryck på trumplattorna för att tända/släcka dem.")

        for msg in midi_in:
            if msg.type == 'note_off' and msg.channel == 9 and msg.note in pads:  # Kanal 10 i MIDI är 9 i nollindexering
                note = msg.note
                if note in active_pads:
                  print(f"note: {note} channel {msg.channel}")
                  # Släck LED
                  midi_out.send(mido.Message('note_on', channel=15, note=note, velocity=64))
                  active_pads.remove(note)
                else:
                  # Avaktivera tidigare aktiv pad (Grön färg)
                  while active_pads:
                    active_pad = active_pads.pop()
                    midi_out.send(mido.Message('note_on', channel=15, note=active_pad, velocity=64))
                  # Tänd (Blinka) LED i rött
                  midi_out.send(mido.Message('note_on', channel=1, note=note, velocity=72))
                  active_pads.add(note)
                  print("Aktiv Pad: ", pads.index(note))

if __name__ == "__main__":
    main()

