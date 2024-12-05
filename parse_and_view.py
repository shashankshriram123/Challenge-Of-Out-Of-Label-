import json
import pprint



with open('/Users/shashankshriram/Downloads/mi3Lab/contents_annotations.txt', 'r') as file:
    content = file.read()
data = eval(content)
#pprint.pprint(data, indent=2)

#with open("formated_annotations_data.txt", 'w') as output_file:
#    json.dump(data, output_file, indent=2)


#print(f"\nFormatted data has been written to:formated_annotations_data.txt")
