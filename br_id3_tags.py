from mutagen.mp3 import MP3
from mutagen.id3 import ID3, COMM, Encoding

# Open the MP3 file
audio = MP3('APL_456_001_CRIME WAVE_Michael McGuill.mp3', ID3=ID3)

comments = audio.tags.getall('COMM')

comment = comments[0]

comment.append("LC 5183")

audio.tags.setall('COMM::eng', [comment] + comments[1:])

audio.save()

print(audio.tags.getall('COMM'))

# # Create a new comment
# new_comment = 'LC 5183'
#
# # Add the new comment to the list of existing comments
# comments.append(COMM(encoding=Encoding.UTF16, lang='eng', desc='', text=new_comment))
#
# # Update the ID3 tag with the new comments
# audio.tags.setall('COMM::eng', comments)
#
# # Save the changes to the MP3 file
# audio.save()

