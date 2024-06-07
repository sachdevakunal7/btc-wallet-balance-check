import sys
import re
from time import sleep

try:    
    # Python 3
    from urllib.request import urlopen
except: 
    # Python 2
    from urllib2 import urlopen

def check_balance(address):
    # Set whether to play a bell sound when a balance is found
    SONG_BELL = True

    # Set a wait time for warnings (not currently used in the script)
    WARN_WAIT_TIME = 0

    # Define the information we want to extract from the blockchain
    blockchain_tags_json = ['total_received', 'final_balance']

    # Define the number of satoshis in a Bitcoin
    SATOSHIS_PER_BTC = 1e+8

    # Parse the address to remove any unnecessary characters
    check_address = address
    parse_address_structure = re.match(r' *([a-zA-Z1-9]{1,34})', check_address)
    if parse_address_structure is not None:
        check_address = parse_address_structure.group(1)
    else:
        print("\nThis Bitcoin Address is invalid" + check_address)
        exit(1)

    # Read information from the blockchain about the address
    reading_state = 1
    while reading_state:
        try:
            htmlfile = urlopen("https://blockchain.info/address/%s?format=json" % check_address, timeout=10)
            htmltext = htmlfile.read().decode('utf-8')
            reading_state = 0
        except:
            reading_state += 1
            print("Checking... " + str(reading_state))
            sleep(60 * reading_state)

    print("\nBitcoin Address = " + check_address)

    # Extract information from the HTML response
    blockchain_info_array = []
    for tag in blockchain_tags_json:
        try:
            blockchain_info_array.append(float(re.search(r'%s":(\d+),' % tag, htmltext).group(1)))
        except:
            print("Error '%s'." % tag)
            exit(1)

    # Display the balance for each type of information extracted
    for i, btc_tokens in enumerate(blockchain_info_array):
        sys.stdout.write("%s \t= " % blockchain_tags_json[i])
        if btc_tokens > 0.0:
            print("%.8f Bitcoin" % (btc_tokens / SATOSHIS_PER_BTC))
        else:
            print("0 Bitcoin")

        # If enabled, play a bell sound when a non-zero balance is found
        if SONG_BELL and blockchain_tags_json[i] == 'final_balance' and btc_tokens > 0.0:
            sys.stdout.write('\a\a\a')  # Ring the bell
            sys.stdout.flush()

            # Write the address and balance to a file
            arq1 = open('addresses-with-balance.txt', 'a')
            arq1.write("Bitcoin Address: %s" % check_address)
            arq1.write("\t Balance: %.8f Bitcoin" % (btc_tokens / SATOSHIS_PER_BTC))
            arq1.write("\n")
            arq1.close()

            # Wait for a specified time if required
            if WARN_WAIT_TIME > 0:
                sleep(WARN_WAIT_TIME)

# Open a file containing a list of Bitcoin addresses
with open("list-addresses.txt") as file:
    for line in file:
        # Open the output file to append results
        arq1 = open('addresses-with-balance.txt', 'a')
        address = str.strip(line)
        print("__________________________________________________\n")
        check_balance(address)

# Write a closing message to the output file
arq1 = open('addresses-with-balance.txt', 'a')
arq1.write("\nsachdevakunal7")
arq1.close()
