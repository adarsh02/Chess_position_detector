from models.cnn_model import CNNModel
from ultralytics import YOLO
import numpy as np
import cv2
from utils.image_processing import process_image
from utils.extract_fen_from_probs import assign_pieces,fen_from_onehot
import torch

def fen_from_imag(image_path):
    yolo_model = YOLO('essentials/yolo_model.pt')
    results = yolo_model([image_path])
    boxes = results[0].boxes
    coords=np.array((boxes.data)[:,:4][0])
    image=cv2.imread(image_path)
    new_img = image[int(coords[1]):int(coords[3]), int(coords[0]):int(coords[2])]
    x=process_image(new_img)

    fin=torch.tensor(x, dtype=torch.float32)
    fin=fin.unsqueeze(dim=1)

    

    model = CNNModel()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    checkpoint = torch.load('essentials/model_weights.pth',map_location=device)
    model.load_state_dict(checkpoint)

    fin.to(device)
    out = model(fin)
    pred = assign_pieces(out.tolist())
    squ=np.array(pred).reshape(8,8)

    return fen_from_onehot(squ)





