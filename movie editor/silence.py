import auditok
import numpy as np

record_start = np.zeros(100)
record_end = np.zeros(100)
duration = np.zeros(100)
speech = np.zeros(100)
num = 0

# split returns a generator of AudioRegion objects
audio_regions = auditok.split(
    "media\\testb1.wav",
    min_dur=0.2,        # minimum duration of a valid audio event in seconds
    max_dur=100,        # maximum duration of an event
    max_silence=2,      # maximum duration of tolerated continuous silence within an event
    energy_threshold=40  # threshold of detection
)

for i, r in enumerate(audio_regions):
    record_start[i] = r.meta.start
    record_end[i] = r.meta.end
    speech[i] = record_end[i] - record_start[i]
    print("Speech  {i}: {r.meta.start:.3f}s -- {r.meta.end:.3f}s".format(i=i,
          r=r), "Duration : ", speech[i])
    num = num+1

for j in range(num-1):
    #evaluate silence section length
    duration[j] = record_start[j+1] - record_end[j]

    print("Silence ", j, " :", round(record_end[j], 3), 's', 'to', round(
        record_start[j+1], 3), 's, Duration : ', duration[j])

    #if there are two continuous silence sections >2.5 
    if duration[j-1] > 2.5 and duration[j] > 2.5 and speech[j] < 5.0:
        print("instruction : ", round(
            record_start[j], 3), 's', 'to', round(record_end[j], 3), 's')

# for i, r in enumerate(audio_regions):

    # Regions returned by `split` have 'start' and 'end' metadata fields

    #print("Region  {i}: {r.meta.start:.3f}s -- {r.meta.end:.3f}s".format(i=i, r=r))

    # play detection
    # r.play(progress_bar=True)

    # region's metadata can also be used with the `save` method
    # (no need to explicitly specify region's object and `format` arguments)
    #filename = r.save("media/region_{meta.start:.3f}-{meta.end:.3f}.wav")
    #print("region saved as: {}".format(filename))
