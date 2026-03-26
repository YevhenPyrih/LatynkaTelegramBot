def to_latin(text, translation):
    new_text = ""

    for char in text:
        try:
            if(char != char.lower()):
                new_text += translation[char.lower()].capitalize()
            else:
                new_text += translation[char.lower()]
        except:
            new_text += char
        
    return new_text