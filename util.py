import string
import easyocr

# Initialize the OCR reader
reader = easyocr.Reader(['en'], gpu=False)


# Mapping dictionaries for character conversion
characters=[i for i in string.ascii_letters]
digits=[i for i in string.digits]

def format_license(text):
  license_plate_=''
  for j in text:
    if j in characters:
      license_plate_+=j
    elif j in digits:
      license_plate_+=j

  return license_plate_


def license_complies_format(text):
  
  if len(text)!=7:
    return False
  
  if text[0] in characters and\
     text[1] in characters and\
     text[2] in characters and\
     text[3] in characters and\
     text[4] in characters and\
     text[5] in characters and\
     text[6] in characters:
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


def save_result(result):

  df_final=pd.DataFrame()
  for frame_no in result.keys():

    
    for car_id in result[frame_no].keys():
      
      df1=pd.DataFrame({'bbox':[result[frame_no][car_id]['car']['bbox']]})
      df2=pd.DataFrame({'license_plate':[result[frame_no][car_id]['license_plate']['bbox']],
                    'text':result[frame_no][car_id]['license_plate']['text'],
                    'bbox_score':result[frame_no][car_id]['license_plate']['bbox_score'],
                    'text_score':result[frame_no][car_id]['license_plate']['text_score']})
      df=pd.concat([df1,df2],axis=1)
      df.insert(0, 'frame', frame_no)
      df.insert(1, 'car_id', car_id)

      df_final=pd.concat([df_final,df],axis=0)
  return df_final.to_csv('result.csv',index=False)



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