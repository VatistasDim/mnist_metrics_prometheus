from fastapi import FastAPI
from app.model.covnet import ConvNet
from torch import optim
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor

import torch
import psutil

app = FastAPI(
    title="MNIST Classifier",
)

train_data = datasets.MNIST(root='./data/mnist_data',
                            train=True,
                            transform=ToTensor(),
                            download=True)
test_data = datasets.MNIST(root='./data/mnist_data',
                            train=False,
                            transform=ToTensor(),
                            download=True)
loaders = {
    'train': DataLoader(train_data,
                        batch_size=10,
                        shuffle=True,
                        num_workers=4),
    'test': DataLoader(test_data,
                        batch_size=10,
                        shuffle=True,
                        )
    }
        
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/train")
async def train():
    model = ConvNet()
    optimizer = optim.Adam(model.parameters(), lr=0.01)
    criterion = nn.CrossEntropyLoss()
    model.compile(criterion=criterion, optimizer=optimizer)
    epochs, accuracy, loss = model.fit(loaders['train'], epochs=10)
    return {"train_accuracy": accuracy, "train_loss": loss, "epochs": epochs}

@app.get("/test")
async def test():

    model = ConvNet()
    model.load_state_dict(torch.load("app/data/mnist_model.pt"))
    model.eval()
    total_predicted, accuracy = model.test(loaders['test'])
    return {"test_accuracy": accuracy}

