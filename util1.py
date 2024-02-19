import string
import easyocr

# Initialize the OCR reader
reader = easyocr.Reader(['en'], gpu=False)


# Mapping dictionaries for character conversion
dict_char_to_int = {'O': '0',
                    'I': '1',
                    'J': '3',
                    'A': '4',
                    'G': '6',
                    'S': '5'}

dict_int_to_char = {'0': 'O',
                    '1': 'I',
                    '3': 'J',
                    '4': 'A',
                    '6': 'G',
                    '5': 'S'}

def format_license(text):

  license_plate_=''
  mapping={0:dict_int_to_char,
           1:dict_int_to_char,
           2:dict_int_to_char,
           3:dict_int_to_char,
           4:dict_int_to_char,
           5:dict_int_to_char}

  for j in [0,1,2,3,4,5,6]:
    if text[j] in mapping.keys():
      license_plate_+=mapping[j][text[j]]
    else:
      license_plate_+=text[j]
  
  return license_plate_


def license_complies_format(text):

  if len(text)!=7:
    return False  
  
  if (text[0] in string.ascii_uppercase or text[0] in dict_char_to_int.keys()) and\
     (text[1] in string.ascii_uppercase or text[1] in dict_char_to_int.keys()) and\
     (text[2] in string.digits or text[2] in dict_char_to_int.keys()) and\
     (text[3] in string.digits or text[3] in dict_char_to_int.keys()) and\
     (text[4] in string.ascii_uppercase or text[4] in dict_char_to_int.keys()) and\
     (text[5] in string.ascii_uppercase or text[5] in dict_char_to_int.keys()) and\
     (text[6] in string.ascii_uppercase or text[6] in dict_char_to_int.keys()):
     return True
  
  else:
    return False


def read_license_plate(license_plate_crop_gray):

  detections = reader.readtext(license_plate_crop_gray)
  for detection in detections:
    box,text,score=detection
    text=text.upper().replace(' ','')
    if license_complies_format(text):
      return format_license(text),score
  
  return None,None




def get_car(license_plate,vehicle_track_ids):

  x1, y1, x2, y2, score, class_id = license_plate

  foundIt = False
  for j in range(len(vehicle_track_ids)):
    xcar1,ycar1,xcar2,ycar2,car_id=vehicle_track_ids[j]
    if x1>xcar1 and y1>ycar1 and x2<xcar2 and y2<ycar2:
      car_idx=j
      foundIt=True
      break
  
  if foundIt:
    return vehicle_track_ids[car_idx]
  
  return -1,-1,-1,-1,-1