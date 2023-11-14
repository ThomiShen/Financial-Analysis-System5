import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

class StockPriceTransformer(nn.Module):
    def __init__(self, d_model=64, nhead=4, num_layers=2, dropout=0.1):
        super(StockPriceTransformer, self).__init__()
        self.input_linear = nn.Linear(1, d_model)
        self.transformer = nn.Transformer(d_model, nhead, num_layers, dropout=dropout)
        self.output_linear = nn.Linear(d_model, 1)

    def forward(self, src, tgt):
        src = self.input_linear(src)
        tgt = self.input_linear(tgt)
        output = self.transformer(src, tgt)
        output = self.output_linear(output)
        return output

def train_stock_price_model(stock_prices, input_seq_len=10, output_seq_len=5, epochs=30, lr=0.001, batch_size=16):
    num_days = len(stock_prices)
    num_samples = num_days - input_seq_len - output_seq_len + 1

    # 数据预处理
    src_data = torch.tensor([stock_prices[i:i+input_seq_len] for i in range(num_samples)]).unsqueeze(-1).float()
    tgt_data = torch.tensor([stock_prices[i+input_seq_len:i+input_seq_len+output_seq_len] for i in range(num_samples)]).unsqueeze(-1).float()

    # 创建模型实例
    model = StockPriceTransformer()

    # 损失函数和优化器
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    # 训练循环
    for epoch in range(epochs):
        for i in range(0, len(src_data), batch_size):
            src_batch = src_data[i:i + batch_size].transpose(0, 1)
            tgt_batch = tgt_data[i:i + batch_size].transpose(0, 1)

            optimizer.zero_grad()
            output = model(src_batch, tgt_batch[:-1])
            loss = criterion(output, tgt_batch[1:])
            loss.backward()
            optimizer.step()

        print(f"Epoch {epoch + 1}/{epochs}, Loss: {loss.item()}")

    return model

def predict_future_stock_prices(stock_prices, trained_model, input_seq_len=10, num_days_to_predict=5):
    # 预测未来股票价格
    src = torch.tensor(stock_prices[-input_seq_len:]).unsqueeze(-1).unsqueeze(1).float()
    tgt = torch.zeros(num_days_to_predict, 1, 1)

    with torch.no_grad():
        for i in range(num_days_to_predict):
            prediction = trained_model(src, tgt[:i+1])
            tgt[i] = prediction[-1]

    output = tgt.squeeze().tolist()
    output=[round(i,2) for i in output]

    return output

# 输入股票价格数据
# num_days = 200
# stock_prices = [20.53, 20.4, 20.56, 20.12, 19.8, 19.96, 19.8, 20.93, 20.6, 22.66, 22.89, 22.27, 22.61, 22.78, 22.77, 22.57, 22.14, 22.01, 22.13, 21.87, 21.56, 20.94, 21.1, 19.79, 19.56, 20.07, 20.22, 20.61, 20.4, 20.03]

# # 训练模型
# trained_model = train_stock_price_model(stock_prices)
#
# # 预测未来 5 天的股票价格
# future_predictions = predict_future_stock_prices(stock_prices, trained_model, input_seq_len=10, num_days_to_predict=5)
# print(f"Next 5 days of stock prices:", future_predictions)