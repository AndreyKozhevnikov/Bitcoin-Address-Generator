import AddressesGenerator
import time

print('start load file')
tic = time.perf_counter()
#filePath='c:\\tempbt\\balancesShort.csv'
# filePath='c:\\tempbt\\balances-0-814085.csv'
# file = open(filePath,'r')
# existingAddresses={}
# k=0
# while True:
#     content=file.readline()
#     if not content:
#         break
#     values = content.split(';')
#     existAddress=values[0]
#     existingAddresses[existAddress]=1
#     k=k+1
#     if(k%10000==0):
#         print(f'{k:_}', end ='\r')

#     #print(existAddress)
#     #values = content.split(';')
# file.close()
# print()
# toc = time.perf_counter()
# print(f"finish load file. loaded: {str(len(existAddress))} in {toc - tic:0.4f} seconds")
f = open("demofile3.txt", "a")
#f.write("Now the file has more content!")

for i in range(1,1000):
    adrSet=AddressesGenerator.generateSetAddresses(i)
    f.write(adrSet.wif+'\n')
    f.write(f"p2wpkh:{adrSet.wif}\n")
    f.write(f"p2wpkh-p2sh:{adrSet.wif}\n")
f.close()    
print('finish')
    

    