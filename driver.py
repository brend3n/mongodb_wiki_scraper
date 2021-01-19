import wiki_scrape as ws

print("\nWelcome to brend3n's wikipedia bot!\n")
while True:
    mode = input("Enter a mode\n1. Collect Data\n2. Quit\n")
    if mode == '1':
        ws.batch_store()
    elif mode == '2':
        break
    else:
        print("Invalid input... try again\n")
        continue