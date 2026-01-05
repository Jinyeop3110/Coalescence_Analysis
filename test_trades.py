def profitOfBestTrade_original(trades):
    queue=[]
    current_profit = 0
    max_profit=0
    
    for trade in trades:
        a,b=trade.split()
        quantity=int(a)
        price=int(b)
        
        if not queue:
            queue.append([quantity,price])
        elif (queue[0][0]>0 and quantity>0) or (queue[0][0]<0 and quantity<0):
            queue.append([quantity,price])
        else:
            remaining_quantity=abs(quantity)
            if quantity>0:
                direction=1
            else:
                direction=-1
            while remaining_quantity>0 and queue:
                if remaining_quantity>abs(queue[0][0]):
                    #full liquidating
                    current_profit+=-direction*(price-queue[0][1])*abs(queue[0][0])
                    remaining_quantity+=direction*abs(queue[0][0])
                    max_profit=max(max_profit,current_profit)
                    current_profit=0
                    queue.pop(0)
                elif remaining_quantity<abs(queue[0][0]):
                    current_profit+=-direction*(price-queue[0][1])*abs(remaining_quantity)
                    queue[0][0]+=remaining_quantity*direction
                    remaining_quantity=0
                else : 
                    current_profit+=-direction*(price-queue[0][1])*abs(queue[0][0])
                    max_profit=max(max_profit,current_profit)
                    remaining_quantity=0
                    current_profit=0
                    queue.pop(0)
            if remaining_quantity>0:
                queue.append([direction*remaining_quantity, price])
                
    max_profit=max(max_profit,current_profit)     
    return int(max_profit)

# Test cases
test_cases = [
    # Case 1: Simple buy-sell
    (['100 100', '-100 110'], 1000),
    
    # Case 2: Multiple buys, single sell
    (['100 100', '100 105', '-200 110'], 1500),
    
    # Case 3: Partial close - BUG HERE
    (['100 100', '-50 110'], 500),
    
    # Case 4: Multiple trades with accumulation
    (['100 100', '-50 110', '-50 105'], 750),
]

print("Testing original implementation:\n")
for i, (trades, expected) in enumerate(test_cases, 1):
    result = profitOfBestTrade_original(trades[:])
    status = "✓" if result == expected else "✗"
    print(f"Test {i}: {status}")
    print(f"  Trades: {trades}")
    print(f"  Expected: {expected}, Got: {result}")
    print()
