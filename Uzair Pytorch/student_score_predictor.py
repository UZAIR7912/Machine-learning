import torch
import pandas as pd
from torch import nn
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
df = pd.read_csv("student_score_predictor.csv")
st_hr = torch.from_numpy(df["study_hours"].values).unsqueeze(1)
slp_hr = torch.from_numpy(df["sleep_hours"].values).unsqueeze(1)
pr_tst = torch.from_numpy(df["practice_tests"].values).unsqueeze(1)
X = torch.hstack((st_hr, slp_hr, pr_tst)).type(torch.float32)
y = torch.from_numpy(df["exam_score"].values).unsqueeze(1).type(torch.float32)
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3)
class RegressionModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer1 = nn.Linear(3,99)
        self.layer2 = nn.Linear(99,1)
    def forward(self,x:torch.Tensor) -> torch.Tensor:
        return(self.layer2(self.layer1(x)))
model = RegressionModel()
loss_fn = nn.L1Loss()
optimizer = torch.optim.Adam(model.parameters(),lr=0.01)
for epoch in range(1000):
    model.train()
    y_preds = model(X_train)
    loss = loss_fn(y_preds,y_train)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    if epoch % 100 == 0:
        print(f"loss: {loss.item()}")
while True:
    val1 = float(input("Enter Study hours: "))
    val2 = float(input("Enter sleep hours: "))
    val3 = float(input("Enter Practice tests: "))
    response_tensor = torch.tensor([val1,val2,val3], dtype=torch.float32)
    model.eval()
    with torch.inference_mode():
        response = model(response_tensor)
        print(f"You will get about {response.item()}% in the upcoming exam!")