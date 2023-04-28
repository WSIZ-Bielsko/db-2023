
w = [1,2,3,4,5,6,7,8,9,10]


BUCKET_SIZE = 3
for i in range((len(w)+BUCKET_SIZE-1)//BUCKET_SIZE):
    print(w[i*BUCKET_SIZE: (i+1)*BUCKET_SIZE])
