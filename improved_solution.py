#!/bin/python3

import os
from collections import deque

def profitOfBestTrade(trades):
    """
    Calculate the maximum profit from a series of trades using FIFO matching.
    
    Args:
        trades: List of strings in format "quantity price"
               Positive quantity = buy, Negative quantity = sell
    
    Returns:
        Maximum profit achieved from any single complete trade sequence
    """
    position_queue = deque()  # Queue of [quantity, price] for open positions
    current_profit = 0
    max_profit = 0
    
    for trade in trades:
        quantity, price = map(int, trade.split())
        
        # If queue is empty or same direction trade, add to queue
        if not position_queue or (position_queue[0][0] * quantity > 0):
            position_queue.append([quantity, price])
            continue
        
        # Opposite direction trade - close positions
        remaining_quantity = abs(quantity)
        direction = 1 if quantity > 0 else -1
        
        while remaining_quantity > 0 and position_queue:
            position_quantity = abs(position_queue[0][0])
            position_price = position_queue[0][1]
            
            # Calculate profit based on how much we're closing
            close_quantity = min(remaining_quantity, position_quantity)
            current_profit += -direction * (price - position_price) * close_quantity
            
            # Update remaining quantities
            remaining_quantity -= close_quantity
            
            if close_quantity >= position_quantity:
                # Fully closed this position
                max_profit = max(max_profit, current_profit)
                current_profit = 0
                position_queue.popleft()
            else:
                # Partially closed this position
                position_queue[0][0] += direction * close_quantity
        
        # If there's still remaining quantity, open new position
        if remaining_quantity > 0:
            position_queue.append([direction * remaining_quantity, price])
    
    # Consider any remaining unrealized profit
    max_profit = max(max_profit, current_profit)
    return max_profit


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')
    
    trades_count = int(input().strip())
    trades = [input() for _ in range(trades_count)]
    
    result = profitOfBestTrade(trades)
    
    fptr.write(str(result) + '\n')
    fptr.close()
