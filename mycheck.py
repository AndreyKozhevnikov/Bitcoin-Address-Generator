import AddressesGenerator
import time

print('start load file')
tic = time.perf_counter()
#filePath='c:\\tempbt\\balancesShort.csv'
filePath='c:\\tempbt\\balances-0-814085.csv'
file = open(filePath,'r')
existingAddresses={}
k=0
while True:
    content=file.readline()
    if not content:
        break
    values = content.split(';')
    existAddress=values[0]
    existingAddresses[existAddress]=1
    k=k+1
    if(k%10000==0):
        print(f'{k:_}', end ='\r')

    #print(existAddress)
    #values = content.split(';')
file.close()
print()
toc = time.perf_counter()
print(f"finish load file. loaded: {str(len(existAddress))} in {toc - tic:0.4f} seconds")

for i in range(500000,1000000000):
    adrSet=AddressesGenerator.generateSetAddresses(i)
    for adr in adrSet.adrs:
        if existingAddresses.get(adr) is not None:
            print(f"!!!!!!!!!!!!!!Key '{adr}' exists.")
            print(f"priv - '{adrSet.priv}' wif - '{adrSet.wif}'")
            f = open(f"demofile{i}.txt", "a")
            f.write(adr+'\n')
            f.write(adrSet.wif+'\n')
            f.close()    
    if i%10000==0:
        #print(i)
        toc = time.perf_counter()
        print(f"progress: {i} in {toc - tic:0.4f} seconds", end ='\r')
        tic = time.perf_counter()
    