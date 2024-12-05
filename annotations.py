import pickle

with open('/Users/shashankshriram/Downloads/mi3Lab/bounding_boxes_output.pkl', 'rb') as file:
    data = pickle.load(file)
print("Successfully loaded the .pkl file!")
print(data)


#with open('/Users/shashankshriram/Downloads/mi3Lab/contents_annotations.txt', 'w') as txt_file:
#    txt_file.write(str(data))


#print(f"Contents have been written to : '/home/sshriram2/mi3Testing/contents_annotations.txt'")

